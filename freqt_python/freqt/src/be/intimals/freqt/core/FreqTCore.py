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

    def __init__(self, _config):

        self._config = _config
        self.constraints = None

        self._transaction_list = list()  # list of list of NodeFreqT
        self._grammar_dict = dict()  # dictionary with String as keys and List of String as value
        self._xmlCharacters_dict = dict()  # dictionary with String as keys and String as value

        # new variables for Integer
        # self._blackLabelsInt_dict = dict()  # dictionary with Integer as keys and List of Integer as value
        # self._whiteLabelsInt_dict = dict()  # dictionary with Integer as keys and List of Integer as value

        # store transaction ids and their correspond class ids
        self._transactionClassID_list = list()  # list of Integer

        self.time_start = -1
        self.timeout = -1
        self.finished = False

    # ////////////////////////////////////////////////////////////

    # --- ABSTRACT ---

    def init_data(self):
        """
         * Called before run
        """
        pass

    def add_tree(self, pat, projected):
        """
         * Is called every time a frequent pattern (satisfying the constraints) is found
         * @param: pat FTArray
         * @param: projected, Projected
        """
        if self.constraints.satisfy_post_expansion_constraint(pat):
            return True
        return False

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

        FP1: OrderedDict[FTArray, Projected] = self.build_FP1()

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
         * build subtrees of size 1 based on root labels
           -> return a dictionary with FTArray as keys and Projected as value
         * @param: trans_list, a list of list of NodeFreqT
         * @param: _rootLabels_set, a list of String
         * @param: _transactionClassID_list, a list of Integer
        """
        FP1: OrderedDict[FTArray, Projected] = collections.OrderedDict()
        trans = self._transaction_list

        for trans_id in range(len(trans)):
            # get transaction label
            class_id = self._transactionClassID_list[trans_id]

            for loc in range(len(trans[trans_id])):
                node = trans[trans_id][loc]
                node_label = node.getNodeLabel()

                if self.constraints.allowed_label_as_root(node_label):
                    new_location = Location(loc, loc, trans_id, class_id)
                    FreqTCore.update_FP1(FP1, node.getNode_label_int(), new_location)

        return FP1

    @staticmethod
    def update_FP1(FP1, root_label, new_location):
        """
         * update FP1
        :param FP1: dict[FTArray, Projected]
        :param root_label: int, id of the label corresponding to the root node
        :param new_location: Location
        """
        new_tree = FTArray.make_root_pattern(root_label)

        if new_tree in FP1:
            FP1[new_tree].add(new_location)
        else:
            projected = Projected()
            projected.set_depth(0)
            projected.add(new_location)
            FP1[new_tree] = projected

    def expand_FP1(self, freq1):
        """
         * expand FP1 to find frequent subtrees based on input constraints
        :param freq1: dict[FTArray, Projected]
        """
        for pat in freq1:
            # expand pat to find maximal patterns
            self.expand_pattern(pat.copy(), freq1[pat])

    def expand_pattern(self, pattern, projected):
        """
         * expand pattern
         * @param: pattern, FTArray
         * @param: projected, Projected
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
        did_ever_stop_extend = False

        for extension, new_proj in candidates.items():
            candidate_prefix, candidate_label = extension

            # built the candidate pattern using the extension
            pattern.extend(candidate_prefix, candidate_label)

            if self.constraints.authorized_pattern(pattern, candidate_prefix):
                # check constraints on maximal number of leaves and real leaf
                if self.constraints.stop_expand_pattern(pattern):
                    if candidate_label < -1:
                        _ = self.add_tree(pattern.copy(), new_proj)
                    else:
                        did_ever_stop_extend = True

                else:
                    # continue expanding pattern
                    did_stop_extend = self.expand_pattern(pattern, new_proj)
                    if did_stop_extend:
                        if candidate_label < -1:
                            _ = self.add_tree(pattern.copy(), new_proj)
                        else:
                            did_ever_stop_extend = True

            # restore the pattern
            pattern.undo_extend(candidate_prefix)

        return did_ever_stop_extend

    @staticmethod
    def generate_candidates(projected, _transaction_list):
        """
         * generate candidates for a pattern, by extending occurrences of this pattern
        :param projected: Projected, occurrences of the pattern
        :param _transaction_list: list(list(NodeFreqT))
        :return: dict[Tuple, Projected], the set of candidates with their location

        note: the list of candidate are store in a OrderedDict to allow easy computation of the support
        which assume that (current.loc,current.root) <= (next.loc,next.root)
        """
        # use ordered dictionary to keep the order of the candidates
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
            # * try to add a child of the right most node
            candi_id = _transaction_list[loc_id][pos].getNodeChild()
            new_depth = depth + 1

            while candi_id != -1:
                node = _transaction_list[loc_id][candi_id]
                new_location = Location(root, candi_id, loc_id, class_id)
                FreqTCore.update_candidates(candidates_dict, node.getNode_label_int(), new_location, new_depth, 0)

                candi_id = node.getNodeSibling()

            # * try to add a sibling of a parent node
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
         * update candidate locations for two-class data
        :param freq1_dict: dict[Tuple, Projected]
        :param candidate_label: int
        :param new_location: Location
        :param depth: int
        :param prefix: int, number of time we push -1 to the pattern
        """
        extension = (prefix, candidate_label)

        if extension in freq1_dict:
            freq1_dict[extension].add(new_location)
        else:
            projected = Projected()
            projected.set_depth(depth)
            projected.add(new_location)
            freq1_dict[extension] = projected

    # --- UTIL --- #

    def init_report(self):
        """
         * create a report
         * @param: config, Config
         * @param: dataSize, Integer
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
        """
         * return input xmlCharacters
        """
        return self._xmlCharacters_dict

    def get_grammar(self):
        """
         * return input grammar
        """
        return self._grammar_dict

    @staticmethod
    def log(report, msg):
        """
         * write a string to report
         * @param: report, a file ready to be written
         * @param: msg, String
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
