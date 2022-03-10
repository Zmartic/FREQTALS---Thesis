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
        self.__transactions_list = list()
        self.__input_pattern = small_pat.copy()

        self.init_database([small_pat, big_pat])

        root_label = self.__input_pattern.get(0)
        self.__maximal_pattern = FTArray(init_memory=[root_label])

    def check_subtree(self):
        """
         * check subtrees
        """
        # -- Init locations of initial pattern --
        root_label = self.__input_pattern.get(0)

        projected = Projected()
        projected.set_depth(0)
        for i in range(0, len(self.__transactions_list)):
            for j in range(0, len(self.__transactions_list[i])):
                node_label = self.__transactions_list[i][j].getNode_label_int()
                if node_label == root_label:
                    projected.set_location(i, j)

        # -- Extend initial pattern --
        return self.expand_pattern(projected)

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

    def expand_pattern(self, projected):
        """
         * expand a subtree
         * @param projected
        """
        candidates = self.generate_candidates(projected)  # output dict of with Tuple as key and Projected as value

        # Prune using candidate that doesn't appear in both pattern
        FreqT_subtree.prune_min2(candidates)

        if len(candidates) == 0:
            # check whether input_pattern is the maximal frequent pattern
            return self.__maximal_pattern == self.__input_pattern

        # expand the current pattern with the first candidate
        # note: we consider the first candidate because generate_candidate() start generating candidate from the small
        #       pattern. Which means that if we were to use and other candidate we would not be able
        #       to include this first candidate = portion of small pattern (due to left to right candidate generation)
        #       the maximal pattern thus cannot be the small pattern
        #       > ultimately generate_candidate() could be specialised to take this fact into account
        extension = next(iter(candidates))
        candidate_prefix, candidate_label = extension
        self.__maximal_pattern.extend(candidate_prefix, candidate_label)

        return self.expand_pattern(candidates[extension])

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

