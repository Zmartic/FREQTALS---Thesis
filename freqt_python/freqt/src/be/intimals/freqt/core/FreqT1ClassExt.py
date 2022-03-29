#!/usr/bin/env python3
import time

from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT1ExtStrategy

from freqt.src.be.intimals.freqt.structure.FTArray import FTArray
from freqt.src.be.intimals.freqt.structure.Location import Location
from freqt.src.be.intimals.freqt.structure.Projected import Projected


class FreqT1ClassExt(FreqT1Class):

    def __init__(self, _config, root_ids_list, _grammar_dict, _grammarInt_dict, _xmlCharacters_dict, label_decoder,
                 _transaction_list):
        super().__init__(_config)

        self.root_ids_list = root_ids_list

        self.constraints = FreqT1ExtStrategy(_config, _grammarInt_dict)

        self._transaction_list = _transaction_list
        self._grammar_dict = _grammar_dict
        self._xmlCharacters_dict = _xmlCharacters_dict

        self.label_decoder = label_decoder

        # -- FreqTExt timeout variable --
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
                interrupted_pattern = root_pat
                # expand the current root occurrences to find maximal patterns
                # print(self._rootIDs_dict[keys].memory) #-------------
                self.expand_pattern(FTArray.make_root_pattern(root_pat), proj)
                # print(self._rootIDs_dict[keys].memory) #-------------

                if not self.finished:
                    self.__interruptedRootIDs.append((interrupted_pattern, occ))

            # update lists of root occurrences for next round
            self.root_ids_list = self.__interruptedRootIDs

        # print the largest patterns
        if len(self.mfp) != 0:
            self.output_patterns(self.mfp, self._config, self._grammar_dict, self.label_decoder,
                                 self._xmlCharacters_dict)

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
