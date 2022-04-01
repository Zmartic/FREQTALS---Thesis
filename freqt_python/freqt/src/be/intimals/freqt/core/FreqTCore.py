#!/usr/bin/env python3
import time

import collections
from collections import OrderedDict
from typing import Tuple

from freqt.src.be.intimals.freqt.structure.FTArray import FTArray
from freqt.src.be.intimals.freqt.structure.Location import Location
from freqt.src.be.intimals.freqt.structure.Projected import Projected

from freqt.src.be.intimals.freqt.constraint import Constraint

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt


class FreqTCore:
    """
     The core of FreqT algorithm (is a base for other implementation)
     * Implements the expansion of a pattern
    """

    def __init__(self, _config):

        self._config = _config
        self.constraints = None

        self._transaction_list = None  # List(List(NodeFreqT)), the set of ASTs
        self._grammar_dict = None  # Dict(String, String)
        self._xmlCharacters_dict = None  # Dict(String, String)

        # store transaction ids and their correspond class ids
        self._transactionClassID_list = None  # List(Int)

        # store the conversion of labels : str -> int
        self.label_decoder = None  # Dict(String, Int)

        self.time_start = -1
        self.timeout = -1
        self.finished = False

    # ////////////////////////////////////////////////////////////

    # --- ABSTRACT ---

    def init_data(self):
        """
         * Called before run
        """
        self.constraints = None

        self._transaction_list = list()
        self._grammar_dict = dict()
        self._xmlCharacters_dict = dict()
        self._transactionClassID_list = list()

        self.label_decoder = dict()
        pass

    def add_tree(self, pattern, projected):
        """
         * Is called every time a frequent pattern (satisfying the constraints) is found
             note: this function should copy pattern
        :param pattern: FTArray, a frequent pattern
        :param projected: Projected, projection of pattern
        """
        pass

    def post_mining_process(self, report):
        """
         * Called at the end of the main run
        """
        pass

    # --- CORE --- #

    def run(self):
        self.init_data()
        self.set_starting_time()
        report = self.init_report()

        print("Mining frequent subtrees ...")

        self.disconnect_not_whitelisted_node()

        FP1 = self.build_FP1()  # OrderedDict(Int, Projected), the root label and its occurrences

        # remove node SourceFile because it is not AST node ##
        not_ast_node = FTArray.make_root_pattern(0)
        if not_ast_node in FP1:
            del FP1[not_ast_node]

        Constraint.prune(FP1, self._config.getMinSupport(), self._config.getWeighted())

        self.expand_FP1(FP1)

        self.post_mining_process(report)

    def disconnect_not_whitelisted_node(self):
        white_labels = ReadXMLInt().read_whiteLabel(self._config.getWhiteLabelFile())
        for trans in self._transaction_list:
            for node in trans:
                label = node.getNodeLabel()
                if label in white_labels:
                    white = white_labels[label]

                    child_id = node.getNodeChild()
                    previous_child = None

                    while child_id != -1:
                        child = trans[child_id]
                        if child.getNodeLabel() in white:
                            if previous_child is None:
                                node.setNodeChild(child_id)
                            else:
                                previous_child.setNodeSibling(child_id)
                            previous_child = child
                        child_id = child.getNodeSibling()

                    if previous_child is None:
                        node.setNodeChild(-1)
        return

    def build_FP1(self):
        """
         * Build FP1 consisting of "root pattern" (pattern of size 1)
        :return: OrderedDict(Int, Projected)
        """
        FP1 = collections.OrderedDict()  # OrderedDict[Int, Projected]
        trans = self._transaction_list

        for trans_id in range(len(trans)):

            for loc in range(len(trans[trans_id])):
                node = trans[trans_id][loc]

                if self.constraints.allowed_label_as_root(node.getNodeLabel()):
                    class_id = self._transactionClassID_list[trans_id]
                    new_location = Location(loc, loc, trans_id, class_id)
                    FreqTCore.update_FP1(FP1, node.getNode_label_int(), new_location)

        return FP1

    @staticmethod
    def update_FP1(FP1, root_label, new_location):
        """
         * Add a new location for some "root pattern" in FP1
        :param FP1: OrderedDict(Int, Projected)
        :param root_label: Int, id of the label corresponding to the root node
        :param new_location: Location, occurrence of root_label in the data
        """
        if root_label in FP1:
            FP1[root_label].add(new_location)
        else:
            projected = Projected()
            projected.set_depth(0)
            projected.add(new_location)
            FP1[root_label] = projected

    def expand_FP1(self, freq1):
        """
         * Expand FP1 to find frequent subtrees based on input constraints
        :param freq1: dict(Int, Projected), root label and its occurrences
        """
        for root in freq1:
            # expand root patterns to find maximal patterns
            root_pat = FTArray.make_root_pattern(root)
            _ = self.expand_pattern(root_pat, freq1[root])

    def expand_pattern(self, pattern, projected):
        """
         Expand pattern
         * Pattern is expanded until stop_expand_pattern() is satisfied.
         * Pattern that has stop expanding sends "add tree request".
         * Those requests can be caught by other patterns.
         * If they satisfy all the constraints, they consume the request an are added to the output.
         note: If a pattern has a leaf which is not a "leaf node" in the data
               this pattern should not be add to the output.
        :param pattern: FTArray, the pattern we are expanding
        :param projected: Projected, the projection of pattern
        :return: Boolean, whether a "add tree request" have been sent
        """
        # if timeout then stop expand the pattern;
        if self.is_timeout():
            self.finished = False
            return False

        # --- find candidates of the current pattern ---
        candidates: OrderedDict[Tuple, Projected] = FreqTCore.generate_candidates(projected, self._transaction_list)
        # prune candidate based on minSup
        Constraint.prune(candidates, self._config.getMinSupport(), self._config.getWeighted())
        if len(candidates) == 0:
            return True

        # --- expand each candidate pattern ---
        current_request = False

        for extension, new_proj in candidates.items():
            candidate_prefix, candidate_label = extension

            # built the candidate pattern using the extension
            pattern.extend(candidate_prefix, candidate_label)

            if not self.constraints.is_pruned_pattern(pattern, candidate_prefix):
                if self.constraints.stop_expand_pattern(pattern):
                    # * Request generated
                    if candidate_label < -1:
                        # > Consume request
                        _ = self.add_tree_requested(pattern, new_proj)
                    else:
                        # > Passes request to parent
                        current_request = True

                else:
                    # Continue expanding pattern
                    add_tree_requested = self.expand_pattern(pattern, new_proj)
                    if add_tree_requested:
                        if candidate_label < -1:
                            # > Consume request
                            _ = self.add_tree_requested(pattern, new_proj)
                        else:
                            # > Passes request to parent
                            current_request = True

            # restore the pattern
            pattern.undo_extend(candidate_prefix)

        return current_request

    @staticmethod
    def generate_candidates(projected, _transaction_list):
        """
         Generate candidates for a pattern
         For each occurrences, we compute every possible extended version (= one additional node),
         all those new occurrences are compiled in candidates_dict
         * patterns are generated from "left to right"
           (which means that adding a node to some pattern which doesn't correspond to
           the right most node of the newly created pattern is not allowed)
        :param projected: Projected, occurrences of a pattern
        :param _transaction_list: List(List(NodeFreqT))
        :return: dict(Tuple, Projected), the set of candidates with their occurrences
                 Candidate = (prefix, label)
                             :prefix: Int, number of "up" move (-1)
                             :label: Int, label of the new added node

        note: the list of candidate are store in a OrderedDict to allow easy computation of the support
        which assume that (current.loc,current.root) <= (next.loc,next.root)
        for java implementation
        """
        candidates_dict: OrderedDict[Tuple, Projected] = collections.OrderedDict()
        depth = projected.get_depth()

        # --- find candidates for each location ---
        for occurrences in projected.get_locations():
            # store all locations of the labels in the pattern:
            # this uses more memory but need for checking continuous paragraphs

            class_id = occurrences.get_class_id()
            loc_id = occurrences.get_location_id()
            pos = occurrences.get_position()
            root = occurrences.get_root()

            # --- find candidates (from left to right) ---
            # * try to add a child to the right most node
            candi_id = _transaction_list[loc_id][pos].getNodeChild()
            new_depth = depth + 1

            while candi_id != -1:
                node = _transaction_list[loc_id][candi_id]
                new_location = Location(root, candi_id, loc_id, class_id)
                FreqTCore.update_candidates(candidates_dict, node.getNode_label_int(), new_location, new_depth, 0)

                candi_id = node.getNodeSibling()

            # * try to add a sibling to a parent node
            prefix = 1
            for d in range(depth):
                current_node = _transaction_list[loc_id][pos]

                candi_id = current_node.getNodeSibling()
                new_depth = depth - d

                while candi_id != -1:
                    node = _transaction_list[loc_id][candi_id]
                    new_location = Location(root, candi_id, loc_id, class_id)
                    FreqTCore.update_candidates(candidates_dict, node.getNode_label_int(), new_location,
                                                new_depth, prefix)

                    candi_id = node.getNodeSibling()

                pos = current_node.getNodeParent()
                if pos == -1:
                    break
                prefix += 1

        return candidates_dict

    @staticmethod
    def update_candidates(freq1_dict, candidate_label, new_location, depth, prefix):
        """
        * Add a new location for some extension (= prefix, label) in freq1_dict
        :param freq1_dict: Dict(Tuple, Projected), the set of candidates with their occurrences
                           Candidate = (prefix, candidate_label)
        :param candidate_label: Int, label of the added node
        :param new_location: Int, an occurrence of the candidate
        :param depth: Int
        :param prefix: Int, number of "up" move (-1) of the extension
        """

        extension = (prefix, candidate_label)

        if extension in freq1_dict:
            freq1_dict[extension].add(new_location)
        else:
            projected = Projected()
            projected.set_depth(depth)
            projected.add(new_location)
            freq1_dict[extension] = projected

    def add_tree_requested(self, pat, proj):
        """
         * Request addition of a pattern to the output
        :param pat: FTArray, the pattern
        :param proj: Projected, its projection
        :return: Boolean, whether pat was add to the output
        """
        if self.constraints.satisfy_post_expansion_constraint(pat):
            self.add_tree(pat, proj)
            return True
        return False

    # --- UTIL --- #

    def init_report(self):
        """
         * Create a report
        """
        data_size = len(self._transaction_list)
        report_file = self._config.getOutputFile().replace("\"", "") + "_report.txt"
        report = open(report_file, 'w+')

        self.log(report, "INPUT")
        self.log(report, "===================")
        self.log(report, "- data sources : " + self._config.getInputFiles())
        self.log(report, "- input files : " + str(data_size))
        self.log(report, "- minSupport : " + str(self._config.getMinSupport()))
        report.flush()

        return report

    def get_xml_characters(self):
        return self._xmlCharacters_dict

    def get_grammar(self):
        return self._grammar_dict

    @staticmethod
    def log(report, msg):
        """
         * Write a string to report
        :param report: a file ready to be written
        :param msg: String
        """
        report.write(msg + "\n")
        report.flush()

    # --- TIMEOUT --- #

    def set_starting_time(self):
        """
         * set time to begin a run
        """
        self.time_start = time.time()
        self.timeout = self.time_start + self._config.getTimeout() * 60
        self.finished = True

    def is_timeout(self):
        """
         * check running time of the algorithm
        """
        return time.time() > self.timeout

    def get_running_time(self):
        return time.time() - self.time_start
