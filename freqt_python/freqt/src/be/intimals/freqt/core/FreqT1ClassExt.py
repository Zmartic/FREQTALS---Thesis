#!/usr/bin/env python3
import sys
import time
import traceback

from freqt.src.be.intimals.freqt.constraint import Constraint
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqTExtStrategy
from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class
from freqt.src.be.intimals.freqt.structure.Projected import Projected


class FreqT1ClassExt(FreqT1Class):

    def __init__(self, _config, _rootIDs_dict, _grammar_dict, _grammarInt_dict, _xmlCharacters_dict, _labelIndex_dict,
                 _transaction_list):
        super().__init__(_config)

        self._rootIDs_dict = _rootIDs_dict
        self.constraints = FreqTExtStrategy(_config, _grammarInt_dict)

        self._grammar_dict = _grammar_dict
        self._xmlCharacters_dict = _xmlCharacters_dict
        self._labelIndex_dict = _labelIndex_dict
        self._transaction_list = _transaction_list

        # tmp
        self.__finishedGroup = True
        self.__interruptedRootIDs_dict = None
        self.__interrupted_pattern = None
        self.__interrupted_projected = None
        self.__timeStartGroup = -1
        self.__timePerGroup = -1

    def run_ext(self):
        """
         * @param: _rootIDs_dict, dictionary with Projected as keys and FTArray as values
         * @param: _report, a open file ready to be writting
        """
        # set running time for the second steps
        self.set_starting_time()

        while len(self._rootIDs_dict) != 0 and self.finished:
            # each group of rootID has a running time budget "timePerGroup"
            # if a group cannot finish search in the given time
            # this group will be stored in the "interruptedRootID"
            # after passing over all groups in rootIDs, if still having time budget
            # the algorithm will continue exploring patterns from groups stored in interruptedRootID
            self.__interruptedRootIDs_dict = dict()  # dictionary with Projected as keys and FTArray as value
            # calculate running time for each group in the current round
            self.__timePerGroup = (self.timeout - self.get_running_time()) / len(self._rootIDs_dict)
            for keys in self._rootIDs_dict:
                # start expanding a group of rootID
                self.__timeStartGroup = time.time()
                self.__finishedGroup = True

                projected = self.getProjected(keys)

                # keep current pattern and location if this group cannot finish
                self.__interrupted_pattern = self._rootIDs_dict[keys].sub_list(0, 1)
                self.__interrupted_projected = keys
                # expand the current root occurrences to find maximal patterns
                self.expand_pattern(self._rootIDs_dict[keys], projected)

            # update lists of root occurrences for next round
            self._rootIDs_dict = self.__interruptedRootIDs_dict

        # print the largest patterns
        if len(self.mfp) != 0:
            self.output_patterns(self.mfp, self._config, self._grammar_dict, self._labelIndex_dict,
                                 self._xmlCharacters_dict)

    def expand_pattern(self, pattern, projected):
        """
         * expand pattern
         * @param: pattern, FTArray
         * @param: projected, Projected
        """
        if not self.__finishedGroup or not self.finished:
            return
        # check running time of the 2nd step
        if self.is_timeout():
            self.finished = False
            return
        # check running for the current group
        if self.isGroupTimeout():
            self.__interruptedRootIDs_dict[self.__interrupted_projected] = self.__interrupted_pattern
            self.__finishedGroup = False
            return

        # --- find candidates of the current pattern ---
        candidates = FreqT1ClassExt.generate_candidates(projected, self._transaction_list)
        # prune candidate based on minSup
        Constraint.prune(candidates, self._config.getMinSupport(), self._config.getWeighted())
        # if there is no candidate then report the pattern and then stop
        if len(candidates) == 0:
            if self.leafPattern is not None:
                self.add_tree(self.leafPattern, self.leafProjected)
            return

        # --- expand each candidate pattern ---
        old_size = pattern.size()

        for extension, new_proj in candidates.items():
            candidate_prefix, candidate_label = extension
            # built the candidate pattern using the extension
            pattern.extend(candidate_prefix, candidate_label)

            # if the right most node of the pattern is a leaf then keep track this pattern
            if candidate_label < -1:
                self.keep_leaf_pattern(pattern, new_proj)
            # store leaf pattern
            old_leaf_pattern = self.leafPattern
            old_leaf_projected = self.leafProjected

            #Constraint.check_cobol_constraints(pattern, candidates, new_proj, self._labelIndex_dict,self._transaction_list)
            # check obligatory children constraint
            if self.constraints.authorized_pattern(pattern, candidate_prefix):
                # check constraints on maximal number of leaves and real leaf
                if self.constraints.stop_expand_pattern(pattern):
                    if self.constraints.satisfy_post_expansion_constraint(self.leafPattern):
                        # store the pattern
                        self.add_tree(self.leafPattern, self.leafProjected)
                else:
                    # continue expanding pattern
                    self.expand_pattern(pattern, new_proj)

            # restore the original pattern
            self.restore_leaf_pattern(old_leaf_pattern, old_leaf_projected)
            pattern = pattern.sub_list(0, old_size)

    """
         * get initial locations of a projected
         * @param: projected, Projected
        """

    def getProjected(self, projected):
        # create location for the current pattern
        ouputProjected = Projected()
        ouputProjected.set_depth(0)
        for i in range(projected.size()):
            classID = projected.get_location(i).get_class_id()
            locationID = projected.get_location(i).get_location_id()
            rootID = projected.get_location(i).get_root()
            ouputProjected.add_location(classID, locationID, rootID, None)
        return ouputProjected

    def isGroupTimeout(self):
        return time.time() - self.__timeStartGroup > self.__timePerGroup
