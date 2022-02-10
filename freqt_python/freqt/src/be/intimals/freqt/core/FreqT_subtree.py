#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.output.XMLOutput import *
from freqt.src.be.intimals.freqt.input.ReadFileInt import *
from freqt.src.be.intimals.freqt.structure.Projected import *
from freqt.src.be.intimals.freqt.constraint import Constraint

import collections
import traceback


class FreqT_subtree:
    """
        check subtree relationship of 2 input patterns
    """

    __maximalPattern = FTArray()
    __newTransaction_list = list()  # list of list of NodeFreqT

    __inputPattern = FTArray()
    __outputPattern = ""

    __found = False

    def getOutputPattern(self):
        return self.__outputPattern

    """
     Generate candidates pattern and return a dictionary with FTArray as keys and Projected as value
     * @param projected, a projected object
    """
    def generateCandidates(self, projected):
        depth = projected.get_depth()
        candidate_dict = collections.OrderedDict()
        for i in range(projected.size()):
            id = projected.get_location(i).getLocationId()
            pos = projected.get_location(i).getLocationPos()
            prefixInt = FTArray()
            for d in range(-1, depth):
                if pos != -1:
                    if d == -1:
                        start = self.__newTransaction_list[id][pos].getNodeChild()
                    else:
                        start = self.__newTransaction_list[id][pos].getNodeSibling()
                    newdepth = depth - d
                    l = start
                    while l != -1:
                        itemInt = FTArray()
                        itemInt.addAll(prefixInt)
                        itemInt.add(self.__newTransaction_list[id][l].getNode_label_int())
                        if itemInt in candidate_dict:
                            candidate_dict[itemInt].set_location(id, l)  # store right most positions
                        else:
                            tmp = Projected()
                            tmp.set_depth(newdepth)
                            tmp.set_location(id, l)  # store right most positions
                            candidate_dict[itemInt] = tmp
                        l = self.__newTransaction_list[id][l].getNodeSibling()
                    if d != -1:
                        pos = self.__newTransaction_list[id][pos].getNodeParent()
                    prefixInt.add(-1)
        return candidate_dict

    """
     * expand a subtree
     * @param projected
    """
    def expandPattern(self, projected):
        try:
            if self.__found:
                return

            # find all candidates of the current subtree
            candidate_dict = self.generateCandidates(projected)  # output dict of with FTArray as key and Projected as value

            Constraint.prune(candidate_dict, 2, False)  # pq 2 comme minsup?

            if len(candidate_dict) == 0:
                if self.__maximalPattern == self.__inputPattern:
                    self.__outputPattern = "found subtree"
                # not found and stop
                self.__found = True
                return

            else:
                # expand the current pattern with each candidate
                for keys in candidate_dict:
                    # add new candidate to current pattern
                    self.__maximalPattern.addAll(keys)
                    self.expandPattern(candidate_dict[keys])
        except:
            e = sys.exc_info()[0]
            print("ERROR: post-processing expanding" + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    """
     * Prune all the candidate that don't appear at least the value of the minSup
     * @param: candidates, a dictionary with FTArray as key and Projected as value
     * @param: minSup, the minimal support value
    """
    def prune(self, candidates_dict, minSup):
        to_remove_list = list()
        for keys in candidates_dict:
            sup = Constraint.get_support(candidates_dict[keys])
            wsup = Constraint.get_root_support(candidates_dict[keys])
            if sup < minSup:
                to_remove_list.append(keys)
            else:
                candidates_dict[keys].setProjectedSupport(sup)
                candidates_dict[keys].setProjectedRootSupport(wsup)
        for elem in to_remove_list:
            candidates_dict.pop(elem, -1)

    """
     * create transaction from list of patterns
     * @param patterns, list of FTArray
    """
    def initDatabase(self, patterns_list):
        readFile = ReadFileInt()
        readFile.createTransactionFromMap(patterns_list, self.__newTransaction_list)

    """
     * check subtrees
     * @param pat1, FTArray
     * @param pat2, FTArray
    """
    def checkSubtrees(self, pat1, pat2):
        try:
            # create input data
            self.__found = False
            self.__newTransaction_list = list()
            self.__inputPattern = pat1.copy()
            self.__outputPattern = ""

            inputPatterns = list()  # list of FTArray
            inputPatterns.append(pat1)
            inputPatterns.append(pat2)
            self.initDatabase(inputPatterns)

            self.__maximalPattern = FTArray()
            rootLabel_int = pat1.get(0)

            self.__maximalPattern.add(rootLabel_int)
            # init locations of pattern
            projected = Projected()
            projected.set_depth(0)
            for i in range(0, len(self.__newTransaction_list)):
                for j in range(0, len(self.__newTransaction_list[i])):
                    node_label = self.__newTransaction_list[i][j].getNode_label_int()
                    if node_label == rootLabel_int:
                        projected.set_location(i, j)
            # expand the pattern
            self.expandPattern(projected)

        except:
            e = sys.exc_info()[0]
            print("Error: check sub-trees: " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)
