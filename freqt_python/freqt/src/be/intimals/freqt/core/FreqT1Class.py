#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import prune
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.InitData import init_data_1class
from freqt.src.be.intimals.freqt.core.AddTree import add_maximal_pattern

from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern


class FreqT1Class(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        # dictionary of maximal frequent patterns
        self.mfp = dict()
        # set of pattern that are not maximal ( used for add_maximal_pattern() )
        self.not_maximal_set = set()

    def init_data(self):
        self._transaction_list, self._transactionClassID_list, self.label_decoder, self._grammar_dict, \
            self._xmlCharacters_dict, self.constraints = init_data_1class(self._config)

    def add_tree(self, pat, proj):
        add_maximal_pattern(pat, proj, self.mfp, self.not_maximal_set)

    def post_mining_process(self, report):
        """
         * print patterns found in the first step
        """
        self.log(report, "OUTPUT")
        self.log(report, "===================")
        if self.finished:
            self.log(report, "finished search")
        else:
            self.log(report, "timeout")
        # print pattern to xml file
        self.output_patterns(self.mfp, self._config, self._grammar_dict, self.label_decoder, self._xmlCharacters_dict)

        self.log(report, "+ Maximal patterns = " + str(len(self.mfp)))
        self.log(report, "+ Running times = " + str(self.get_running_time()) + " s")
        report.close()

    def output_patterns(self, output_patterns, config, grammar, label_decoder, xmlCharacters_dict):
        """
         * print maximal patterns to XML file
         * @param: MFP_dict, dictionary with FTArray as key and String as values
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as values
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys et String as values
        """
        try:
            out_file = config.get_output_file()
            # create output file to store patterns for mining common patterns
            output_common_patterns = open(out_file + ".txt", 'w+')
            # output maximal patterns
            output_maximal_patterns = XMLOutput(out_file, config, grammar, xmlCharacters_dict)
            pattern = Pattern()
            for pat in output_patterns:
                pat_str = pat.get_decoded_str(label_decoder)
                supports = self.get_support_string(pat, output_patterns[pat])
                output_maximal_patterns.report_Int(pat_str, supports)
                output_common_patterns.write(pattern.getPatternString1(pat_str) + "\n")

            output_maximal_patterns.close()
            output_common_patterns.flush()
            output_common_patterns.close()

        except:
            e = sys.exc_info()[0]
            print("Print maximal patterns error : " + str(e) + "\n")
            print(traceback.format_exc())

    def get_support_string(self, pat, proj):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        return str(proj.get_support()) + "," + str(proj.get_root_support()) + "," + str(pat.n_node)
