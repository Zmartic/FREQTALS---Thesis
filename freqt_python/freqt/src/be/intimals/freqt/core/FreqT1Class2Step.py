#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.constraint.Constraint import prune
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt
from freqt.src.be.intimals.freqt.core.InitData import init_data_1class
from freqt.src.be.intimals.freqt.core.AddTree import add_root_ids


class FreqT1Class2Step(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        self.root_ids_list = list()

    def init_data(self):
        self._transaction_list, self._transactionClassID_list, self.label_decoder, self._grammar_dict, \
            self._xmlCharacters_dict, self.constraints = init_data_1class(self._config)

    '''def expand_pattern(self, pattern, projected):
        # if timeout then stop expand the pattern;
        if self.is_timeout():
            self.finished = False
            return False

        # --- find candidates of the current pattern ---
        candidates = FreqTCore.generate_candidates(projected, self._transaction_list)
        # prune candidate based on minSup
        prune(candidates, self._config.getMinSupport(), self._config.getWeighted())

        # --- expand each candidate pattern ---

        for extension, new_proj in candidates.items():
            candidate_prefix, candidate_label = extension

            # built the candidate pattern using the extension
            pattern.extend(candidate_prefix, candidate_label)

            if not self.constraints.is_pruned_pattern(pattern, candidate_prefix):
                if candidate_label < -1:
                    if not self.add_tree_requested(pattern, new_proj):
                        self.expand_pattern(pattern, new_proj)
                    # else:
                    #   don't expand
                    #   note: pattern was added successfully, super-tree of this pattern can only
                    #         have a smaller set of occurrences and is thus not interesting 
                # check constraints on maximal number of leaves and real leaf
                elif not self.constraints.stop_expand_pattern(pattern):
                    self.expand_pattern(pattern, new_proj)

            # restore the pattern
            pattern.undo_extend(candidate_prefix)

        return'''

    def add_tree(self, pat, proj):
        add_root_ids(pat, proj, self.root_ids_list)

    def post_mining_process(self, report):
        """
         * run the 2nd step to find maximal patterns from groups of root occurrences
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as value
         * @param: report, a open file ready to be writting
        """
        print("Mining maximal frequent subtrees ... \n")
        self.log(report, "")
        self.log(report, "OUTPUT")
        self.log(report, "===================")

        # report first phase
        self.log(report, "- Step 1: Mining frequent patterns with max size constraints")
        self.log(report, "\t + running time = " + str(self.get_running_time()) + "s")
        self.log(report, "\t + root occurrences groups = " + str(len(self.root_ids_list)))
        # phase 2: find maximal patterns from rootIDs
        self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

        # run second step
        freqt_ext = FreqT1ClassExt(self._config, self.root_ids_list, self._grammar_dict, self.constraints.grammar,
                                   self._xmlCharacters_dict, self.label_decoder, self._transaction_list)
        freqt_ext.run()

        # report result
        if freqt_ext.finished:
            self.log(report, "\t + search finished")
        else:
            self.log(report, "\t + timeout in the second step")

        self.log(report, "\t + maximal patterns: " + str(len(freqt_ext.mfp)))
        self.log(report, "\t + running time: ..." + str(freqt_ext.get_running_time()) + "s")
        report.flush()
        report.close()

    def is_timeout(self):
        """
         Timeout disable for the first step
        """
        return False
