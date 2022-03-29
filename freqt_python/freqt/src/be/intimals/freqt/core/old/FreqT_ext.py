#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square
from freqt.src.be.intimals.freqt.core.old.FreqT import FreqT
from freqt.src.be.intimals.freqt.structure.FTArray import FTArray
from freqt.src.be.intimals.freqt.structure.Projected import *

from freqt.src.be.intimals.freqt.constraint import Constraint

import time


"""
    extended FREQT + without using max size constraints
"""


class FreqT_ext(FreqT):

    __interruptedRootIDs_dict = dict()  # dictionary with Projected as keys and FTArray as value

    __timeStart2nd = -1
    __timeSpent = -1
    __timePerGroup = -1
    __timeStartGroup = -1

    __finishedGroup = False
    __interrupted_pattern = None
    __interrupted_projected = Projected()

    """
     * @param: _config, Config
     * @param: _grammar_dict, dictionary with String as keys and list of String as values
     * @param: _grammarInt_dict, dictionary with Integer as keys and list of String as values
     * @param: _blackLabelsInt_dict, dictionary with Integer as keys and list of Integer as values
     * @param: _whiteLabelsInt_dict, dictionary with Integer as keys and list of Integer as values
     * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
     * @param: _labelIndex_dict, dictionary with Integer as keys and String as values
     * @param: _transaction_list, list of list of NodeFreqT
     * @parm: _sizeClass1, Integer
     * @param: _sizeClass2, Integer
    """
    def __init__(self, _config, _grammar_dict, _grammarInt_dict, _blackLabelsInt_dict, _whiteLabelsInt_dict,
                  _xmlCharacters_dict, _labelIndex_dict, _transaction_list, _sizeClass1, _sizeClass2):
        super().__init__(_config)
        self._grammar_dict = _grammar_dict
        self._grammarInt_dict = _grammarInt_dict
        self._blackLabelsInt_dict = _blackLabelsInt_dict
        self._whiteLabelsInt_dict = _whiteLabelsInt_dict
        self._xmlCharacters_dict = _xmlCharacters_dict
        self._labelIndex_dict = _labelIndex_dict
        self._transaction_list = _transaction_list
        self.sizeClass1 = _sizeClass1
        self.sizeClass2 = _sizeClass2

    """
     * @param: _rootIDs_dict, dictionary with Projected as keys and FTArray as values
     * @param: _report, a open file ready to be writting
    """
    def run_ext(self, _rootIDs_dict, _report):
        try:
            # set running time for the second steps
            self.setRunningTime()
            # set the number of round
            roundCount = 1
            while len(_rootIDs_dict) != 0 and self.finished:
                # each group of rootID has a running time budget "timePerGroup"
                # if a group cannot finish search in the given time
                # this group will be stored in the "interruptedRootID"
                # after passing over all groups in rootIDs, if still having time budget
                # the algorithm will continue exploring patterns from groups stored in interruptedRootID
                self.__interruptedRootIDs_dict = dict()  # dictionary with Projected as keys and FTArray as value
                # calculate running time for each group in the current round
                self.__timePerGroup = (self.timeout - self.__timeSpent) / len(_rootIDs_dict)
                for keys in _rootIDs_dict:
                    root, occ = keys
                    root_pat = FTArray.make_root_pattern(root)
                    # start expanding a group of rootID
                    self.__timeStartGroup = time.time()
                    self.__finishedGroup = True

                    projected = self.getProjected(occ)

                    # keep current pattern and location if this group cannot finish
                    self.__interrupted_pattern = root_pat.copy()
                    self.__interrupted_projected = projected
                    # expand the current root occurrences to find maximal patterns
                    self.expand_pattern(root_pat.copy(), projected)

                # update running time
                self.__timeSpent = time.time() - self.__timeStart2nd
                # update lists of root occurrences for next round
                _rootIDs_dict = self.__interruptedRootIDs_dict.copy()
                # increase number of round
                roundCount += 1

            # print the largest patterns
            if len(self.MFP_dict) != 0:
                self.outputPatterns(self.MFP_dict, self._config, self._grammar_dict, self._labelIndex_dict, self._xmlCharacters_dict)

            # report result
            self.reportResult(_report)

        except:
            e = sys.exc_info()[0]
            print("expand maximal pattern error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    """
     * expand pattern to find maximal patterns
     * @param: largestPattern, FTArray
     * @param: projected, Projected
    """
    def expand_pattern(self, pattern, projected):
        try:
            if not self.__finishedGroup or not self.finished:
                return
            # check running time of the 2nd step
            if self.is2ndStepTimeout():
                self.finished = False
                return
            # check running for the current group
            if self.isGroupTimeout():
                self.__interruptedRootIDs_dict[self.__interrupted_projected] = self.__interrupted_pattern
                self.__finishedGroup = False
                return
            # find candidates for the current pattern
            candidates_dict = self.generate_candidates(projected, self._transaction_list)  # dictionary with FTArray as keys and Projected as values
            # prune on minimum support
            Constraint.prune(candidates_dict, self._config.getMinSupport(), self._config.getWeighted())
            # if there is no candidate then report pattern --> stop
            if len(candidates_dict) == 0:
                if self.leafPattern is not None:
                    # store pattern
                    self.add_tree(self.leafPattern, self.leafProjected)
                return

            oldSize = pattern.size()
            # expand the current pattern with each candidate
            for ext, new_proj in candidates_dict.items():
                prefix, candidate = ext
                pattern.extend(prefix, candidate)
                if pattern.get_last() < -1:
                    self.keep_leaf_pattern(pattern, new_proj)
                oldLeafPattern = self.leafPattern
                oldLeafProjected = self.leafProjected
                # check section and paragraphs in COBOL
                '''tmp = [-1] * prefix
                tmp.append(candidate)
                keys = FTArray(init_memory=tmp)'''
                #Constraint.check_cobol_constraints(largestPattern, candidates_dict, keys, self._labelIndex_dict, self._transaction_list)
                # check constraints
                if self.authorized_pattern(pattern, prefix):
                    if Constraint.is_not_full_leaf(pattern):
                        if self.satisfy_post_expansion_constraint(self.leafPattern):
                            # store the pattern
                            self.add_tree(self.leafPattern, self.leafProjected)
                    else:
                        # continue expanding pattern
                        self.expand_pattern(pattern, new_proj)

                self.restore_leaf_pattern(oldLeafPattern, oldLeafProjected)
                pattern = pattern.sub_list(0, oldSize)
        except:
            e = sys.exc_info()[0]
            print("Error: Freqt_ext projected " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    """
     * add pattern to maximal pattern list
     * @param: pat, FTArray
     * @param: projected, Projected
    """
    def add_tree(self, pat, projected):
        # check output constraints and right mandatory children before storing pattern
        if self._config.get2Class():
            # check chi-square score
            score = chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            if satisfy_chi_square(score, self._config.getDSScore()):
                self.add_maximal_pattern(pat, projected, self.MFP_dict)
        else:
            self.add_maximal_pattern(pat, projected, self.MFP_dict)

    """
     * get initial locations of a projected
     * @param: projected, Projected
    """

    def getProjected(self, root_occ):
        # create location for the current pattern
        proj = Projected()
        proj.set_depth(0)
        for loc, root in root_occ:
            proj.add(Location(root, root, loc, 1))
        return proj

    def reportResult(self, _report):
        if self.finished:
            self.log(_report, "\t + search finished")
        else:
            self.log(_report, "\t + timeout in the second step")

        self.log(_report, "\t + maximal patterns: " + str(len(self.MFP_dict)))
        currentTimeSpent = time.time() - self.__timeStart2nd
        self.log(_report, "\t + running time: ..." + str(currentTimeSpent) + "s")
        _report.flush()
        _report.close()

    def setRunningTime(self):
        self.finished = True
        self.__timeStart2nd = time.time()
        self.timeout = self._config.getTimeout()*60
        self.__timeSpent = 0

    def is2ndStepTimeout(self):
        return time.time() - self.__timeStart2nd > self.timeout

    def isGroupTimeout(self):
        return time.time() - self.__timeStartGroup > self.__timePerGroup