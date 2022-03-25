#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT1Strategy
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.CheckSubtree import check_subtree

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, convert_grammar_label2int, \
    read_XML_character


class FreqT1Class(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        # dictionary of maximal frequent patterns
        self.mfp = dict()
        # set of pattern that are not maximal ( used for add_maximal_pattern() )
        self.not_maximal_set = set()

    def init_data(self):
        """
         * read input data
        """
        self._transaction_list = list()
        self._grammar_dict = dict()
        self._xmlCharacters_dict = dict()
        self._transactionClassID_list = list()

        #self.label_encoder = dict()
        self.label_decoder = dict()

        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles(), self.label_decoder,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            # create grammar (labels are strings) which is used to print patterns
            initGrammar_Str(self._config.getInputFiles(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            self._xmlCharacters_dict = read_XML_character(self._config.getXmlCharacterFile())

            grammar_int = convert_grammar_label2int(self._grammar_dict, self.label_decoder)
            self.constraints = FreqT1Strategy(self._config, grammar_int)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def add_tree(self, pat, proj):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        self.add_maximal_pattern(pat, proj, self.mfp)

    def post_mining_process(self, report):
        self.outputPatternInTheFirstStep(self.mfp, self._config, self._grammar_dict, self.label_decoder,
                                         self._xmlCharacters_dict, report)

    # --------------- #

    def add_maximal_pattern(self, pat, proj, mfp):
        """
         * add maximal patterns
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _MFP_dict, a dictionary with FTArray as keys and String as values
        """
        if len(mfp) != 0:
            if pat in self.not_maximal_set:
                return
            if pat in mfp:
                return

            # check maximal pattern
            for max_pat in mfp.keys():
                res = check_subtree(pat, max_pat)
                if res == 1:  # * pat is a subtree of max_pat
                    self.not_maximal_set.add(pat)
                    return
                elif res == 2:  # * max_pat is a subtree of pat
                    self.not_maximal_set.add(max_pat)
                    del mfp[max_pat]

        # add new maximal pattern to the list
        mfp[pat.copy()] = proj

    def outputPatternInTheFirstStep(self, mfp, config, grammar, label_decoder, xmlCharacters_dict, report):
        """
         * print patterns found in the first step
         * @param: MFP_dict, a dictionary with FTArray as keys and String as value
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as value
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys and Sting as values
         * @param: report, a link to a file ready to be written
        """
        self.log(report, "OUTPUT")
        self.log(report, "===================")
        if self.finished:
            self.log(report, "finished search")
        else:
            self.log(report, "timeout")
        # print pattern to xml file
        self.output_patterns(mfp, config, grammar, label_decoder, xmlCharacters_dict)

        self.log(report, "+ Maximal patterns = " + str(len(mfp)))
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
            out_file = config.getOutputFile()
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
