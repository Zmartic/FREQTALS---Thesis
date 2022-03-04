#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.output.XMLOutput import *
from freqt.src.be.intimals.freqt.input.ReadFileInt import *
from freqt.src.be.intimals.freqt.structure.Projected import *

import collections


class FreqT_subtree:
    """
        check subtree relationship of 2 input patterns
    """

    def __init__(self, small_pat, big_pat):
        self.__found = False
        self.__transactions_list = list()
        self.__input_pattern = small_pat.copy()
        self.__is_subtree = False

        self.init_database([small_pat, big_pat])

        root_label = small_pat.get(0)
        self.__maximal_pattern = FTArray(init_memory=[root_label])

        # --- Check pattern subtree ---

        # init locations of pattern
        projected = Projected()
        projected.set_depth(0)
        for i in range(0, len(self.__transactions_list)):
            for j in range(0, len(self.__transactions_list[i])):
                node_label = self.__transactions_list[i][j].getNode_label_int()
                if node_label == root_label:
                    projected.set_location(i, j)

        self.expandPattern(projected)

    def check_subtree(self):
        """
         * check subtrees
        """
        return self.__is_subtree

    def generate_candidates(self, projected):
        """
         Generate candidates pattern and return a dictionary with FTArray as keys and Projected as value
         * @param projected, a projected object
        """
        depth = projected.get_depth()
        candidate_dict = collections.OrderedDict()
        for i in range(projected.size()):
            id = projected.get_location(i).get_location_id()
            pos = projected.get_location(i).get_position()
            prefix = 0
            for d in range(-1, depth):
                if pos != -1:
                    if d == -1:
                        start = self.__transactions_list[id][pos].getNodeChild()
                    else:
                        start = self.__transactions_list[id][pos].getNodeSibling()
                    newdepth = depth - d
                    l = start
                    while l != -1:
                        extension = (prefix, self.__transactions_list[id][l].getNode_label_int())
                        if extension in candidate_dict:
                            candidate_dict[extension].set_location(id, l)  # store right most positions
                        else:
                            tmp = Projected()
                            tmp.set_depth(newdepth)
                            tmp.set_location(id, l)  # store right most positions
                            candidate_dict[extension] = tmp
                        l = self.__transactions_list[id][l].getNodeSibling()
                    if d != -1:
                        pos = self.__transactions_list[id][pos].getNodeParent()
                    prefix += 1
        return candidate_dict

    def expandPattern(self, projected):
        """
         * expand a subtree
         * @param projected
        """
        if self.__found:
            return

        # find all candidates of the current subtree
        candidates = self.generate_candidates(projected)  # output dict of with Tuple as key and Projected as value

        FreqT_subtree.prune_min2(candidates)

        if len(candidates) == 0:
            self.__is_subtree = self.__maximal_pattern == self.__input_pattern
            # stop
            self.__found = True
            return

        # expand the current pattern with each candidate
        ### print("subtree: "+str(len(candidates)))
        # extension = next(iter(candidates))
        for extension, new_proj in candidates.items():
            print(extension)
            candidate_prefix, candidate_label = extension
            # add new candidate to current pattern
            self.__maximal_pattern.extend(candidate_prefix, candidate_label)
            self.expandPattern(new_proj)

    @staticmethod
    def prune_min2(candidates):
        """
         * Prune all the candidate that don't appear at least 2 times (one for each transaction)
         * @param: candidates, a dictionary with FTArray as key and Projected as value
         * @param: minSup, the minimal support value
        """
        for elem in list(candidates.keys()):
            if candidates[elem].compute_support() < 2:
                del candidates[elem]

    def init_database(self, patterns_list):
        """
         * create transaction from list of patterns
         * @param patterns, list of FTArray
        """
        read_file = ReadFileInt()
        read_file.createTransactionFromMap(patterns_list, self.__transactions_list)

