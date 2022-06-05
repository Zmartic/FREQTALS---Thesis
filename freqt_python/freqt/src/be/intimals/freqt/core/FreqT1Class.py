#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.InitData import init_data_1class
from freqt.src.be.intimals.freqt.core.AddTree import add_maximal_pattern

from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern


class FreqT1Class(FreqTCore):
    """
        Implementation of the FREQTALS algorithm on 1 class data
        > naive approach (in 1 step)
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

        # dictionary of maximal frequent patterns
        self.mfp = {}
        # set of pattern that are not maximal ( used for add_maximal_pattern() )
        self.not_maximal_set = set()

    def init_data(self):
        """
         * Initialize the database
         note: this function preprocess the database
        """
        self._transaction_list, \
        self._transaction_class_id_list, \
        self.label_decoder, \
        self._grammar_dict, \
        self._xml_characters_dict, \
        self.constraints = init_data_1class(self._config)

    def add_tree(self, pat, proj):
        """ add pattern to self.mfp """
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
        self.output_patterns(self.mfp, self._config)

        self.log(report, "+ Maximal patterns = " + str(len(self.mfp)))
        self.log(report, "+ Running times = " + str(self.get_running_time()) + " s")
        report.close()

    def output_patterns(self, output_patterns, config):
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
            with open(out_file + ".txt", 'w+', encoding='utf-8') as output_common_patterns:
                output_maximal_patterns = XMLOutput(out_file, config, self._grammar_dict,
                                                    self._xml_characters_dict)
                pattern = Pattern()
                for pat in output_patterns:
                    pat_str = pat.get_decoded_str(self.label_decoder)
                    supports = self.get_support_string(pat, output_patterns[pat])
                    output_maximal_patterns.report_Int(pat_str, supports)
                    output_common_patterns.write(pattern.getPatternString1(pat_str) + "\n")

                output_maximal_patterns.close()
                output_common_patterns.flush()
                output_common_patterns.close()

        except:
            print("Print maximal patterns error : " + str(sys.exc_info()[0]) + "\n")
            print(traceback.format_exc())

    @staticmethod
    def get_support_string(pat, proj):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        return str(proj.get_support()) + "," + str(proj.get_root_support()) + "," + str(pat.n_node)
