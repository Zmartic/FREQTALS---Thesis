#!/usr/bin/env python3
import sys
from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square
from freqt.src.be.intimals.freqt.core.AddTree import add_high_score_pattern, add_root_ids
from freqt.src.be.intimals.freqt.core.FreqT1Class2Step import FreqT1Class2Step
from freqt.src.be.intimals.freqt.core.FreqT2ClassExt import FreqT2ClassExt
from freqt.src.be.intimals.freqt.core.InitData import init_data_2class


class FreqT2Class2Step(FreqT1Class2Step):
    """
     Implementation of the 1st step of the FREQTALS algorithm on 2 classes data
    """

    def __init__(self, config):
        """
         :param config: Config
        """
        self._transaction_list = None
        self._transaction_class_id_list = None
        self.label_decoder = None
        self._grammar_dict = None
        self._xml_characters_dict = None
        self.constraints = None

        super().__init__(config)

        self.size_class1 = -1
        self.size_class2 = -1

        # Dict of high score pattern
        self.hsp = {}

    def init_data(self):
        """
         * Initialize the database
         note: this function preprocess the database
        """
        self._transaction_list, \
        self._transaction_class_id_list, \
        self.label_decoder, \
        self.size_class1, self.size_class2, \
        self._grammar_dict, \
        self._xml_characters_dict, \
        self.constraints = init_data_2class(self._config)

    def add_tree_requested(self, pat, proj):
        """
         * Request addition of a pattern to the output
         > ensures that patterns satisfy the post expansion constraints
         + check chi-square scores threshold
        :param pat: FTArray, the pattern
        :param proj: Projected, its projection
        :return: Boolean, whether pat was add to the output
        """
        if not self.constraints.satisfy_post_expansion_constraint(pat):
            return False
        # check chi-square score
        score = chi_square(proj, self.size_class1, self.size_class2, self._config.get_weighted())
        if satisfy_chi_square(score, self._config.get_ds_score()):
            add_high_score_pattern(pat, proj, score, self.hsp, self._config.get_num_patterns())
            return True
        return False

    def post_mining_process(self, report):
        """
         * run the 2nd step to find maximal patterns from groups of root occurrences
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as value
         * @param: report, a open file ready to be writting
        """
        # -- Group root occurrence --
        root_ids_list = []
        for pat, tmp in self.hsp.items():
            proj = tmp[0]
            add_root_ids(pat, proj, root_ids_list)

        try:
            print("Mining maximal frequent subtrees ... \n")
            self.log(report, "")
            self.log(report, "OUTPUT")
            self.log(report, "===================")

            # report the phase 1
            self.log(report, "- Step 1: Mining frequent patterns with max size constraints")
            self.log(report, "\t + running time = " + str(self.get_running_time()) + "s")
            self.log(report, "\t + root occurrences groups = " + str(len(root_ids_list)))
            # phase 2: find maximal patterns from rootIDs
            self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

            # run second step
            freqt_ext = FreqT2ClassExt(self._config, self.root_ids_list, self._grammar_dict, self.constraints.grammar,
                                       self._xml_characters_dict, self.label_decoder, self._transaction_list,
                                       self.size_class1, self.size_class2)
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

        except:
            print("expand pattern from root IDs error " + str(sys.exc_info()[0]) + "\n")

    def is_timeout(self):
        """
         Timeout disable for the first step
        """
        return False
