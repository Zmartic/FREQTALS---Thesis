#!/usr/bin/env python3
import sys
import time
import traceback

from freqt.src.be.intimals.freqt.constraint import Constraint
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqTExtStrategy
from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class
from freqt.src.be.intimals.freqt.structure.Location import Location
from freqt.src.be.intimals.freqt.structure.Projected import Projected


class FreqT1ClassExt(FreqT1Class):

    def __init__(self, _config, root_ids_list, _grammar_dict, _grammarInt_dict, _xmlCharacters_dict, _labelIndex_dict,
                 _transaction_list):
        super().__init__(_config)

        self.root_ids_list = root_ids_list
        self.constraints = FreqTExtStrategy(_config, _grammarInt_dict)

        self._grammar_dict = _grammar_dict
        self._xmlCharacters_dict = _xmlCharacters_dict
        self._labelIndex_dict = _labelIndex_dict
        self._transaction_list = _transaction_list

        # FreqTExt timeout variable
        self.__interruptedRootIDs = None

    def run(self):
        """
         * @param: _rootIDs_dict, dictionary with Projected as keys and FTArray as values
         * @param: _report, a open file ready to be writting
        """
        # set running time for the second steps
        self.set_starting_time()
        timeout_step2 = self.time_start + self._config.getTimeout() * 60

        while len(self.root_ids_list) != 0:
            # note : each group of rootID has a running time budget "timePerGroup"
            #        if a group cannot finish search in the given time
            #        this group will be stored in the "interruptedRootID"
            #        after passing over all groups in rootIDs, if still having time budget
            #        the algorithm will continue exploring patterns from groups stored in interruptedRootID

            # calculate running time for each group in the current round
            remaining_time = timeout_step2 - time.time()
            if remaining_time <= 0:
                break
            time_per_group = remaining_time / len(self.root_ids_list)

            self.__interruptedRootIDs = list()

            for elem in self.root_ids_list:
                # start expanding a group of rootID
                self.set_timeout(time_per_group)
                root_pat, occ = elem
                proj = self.getProjected(occ)

                # keep current pattern and location if this group cannot finish
                interrupted_pattern = root_pat.sub_list(0, 1)
                # expand the current root occurrences to find maximal patterns
                # print(self._rootIDs_dict[keys].memory) #-------------
                self.expand_pattern(root_pat, proj)
                # print(self._rootIDs_dict[keys].memory) #-------------

                if not self.finished:
                    self.__interruptedRootIDs.append((interrupted_pattern, occ))

            # update lists of root occurrences for next round
            self.root_ids_list = self.__interruptedRootIDs

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
        if not self.finished:
            return
        # check running for the current group
        if self.is_timeout():
            self.finished = False
            self.__interruptedRootIDs_dict[self.__interrupted_projected] = self.__interrupted_pattern
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

    def getProjected(self, root_occ):
        # create location for the current pattern
        proj = Projected()
        proj.set_depth(0)
        for loc, root in root_occ:
            proj.add(Location(root, root, loc, 1))
        return proj

    # --- TIMEOUT --- #

    def set_starting_time(self):
        """
         * set time to begin a run
        """
        self.time_start = time.time()

    def set_timeout(self, budget_time):
        self.finished = True
        self.timeout = time.time() + budget_time
