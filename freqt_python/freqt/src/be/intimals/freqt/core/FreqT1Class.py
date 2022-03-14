#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import DefaultStrategy
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.CheckSubtree import check_subtree

from freqt.src.be.intimals.freqt.structure.Pattern import Pattern
from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.PatternInt import countNode, getPatternStr
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, readXMLCharacter, convert_grammar_keys2int


class FreqT1Class(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        self.label_str2int = dict()  # label encoder
        # self.label_int2str = dict()  # label decoder

        # dictionary of maximal frequent patterns
        self.mfp = dict()
        # set of pattern that are not maximal
        self.not_maximal_set = set()

    def init_data(self):
        """
         * read input data
        """
        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles(), self.label_str2int,
                                 self.__transactionClassID_list, self._config.getWhiteLabelFile())
            # create grammar (labels are strings) which is used to print patterns
            initGrammar_Str(self._config.getInputFiles(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

            grammar_int = convert_grammar_keys2int(self._grammar_dict, self.label_str2int)
            self.constraints = DefaultStrategy(self._config, grammar_int)

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

    def post_mining_process(self):
        self.outputPatternInTheFirstStep(self.mfp, self._config, self._grammar_dict, self.label_str2int,
                                         self._xmlCharacters_dict, self.report)

    # --------------- #

    def add_maximal_pattern(self, pat, projected, _MFP_dict):
        """
         * add maximal patterns
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _MFP_dict, a dictionary with FTArray as keys and String as values
        """
        if len(_MFP_dict) != 0:
            if pat in self.not_maximal_set:
                return
            if pat in _MFP_dict:
                return

            to_remove_list = list()
            # check maximal pattern
            for max_pat in _MFP_dict.keys():
                res = check_subtree(pat, max_pat)
                if res == 1:  # * pat is a subtree of max_pat
                    self.not_maximal_set.add(pat)
                    return
                elif res == 2:  # * max_pat is a subtree of pat
                    self.not_maximal_set.add(max_pat)
                    to_remove_list.append(max_pat)

            for key in to_remove_list:
                del _MFP_dict[key]

        # add new maximal pattern to the list
        _MFP_dict[pat] = FreqT1Class.get_support_string(pat, projected)

    @staticmethod
    def get_support_string(pat, projected):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        support = projected.get_support()
        w_support = projected.get_root_support()
        size = countNode(pat)
        return str(support) + "," + str(w_support) + "," + str(size)

    def outputPatternInTheFirstStep(self, MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict, report):
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
        self.outputPatterns(MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict)

        self.log(report, "+ Maximal patterns = " + str(len(MFP_dict)))
        self.log(report, "+ Running times = " + str(self.get_running_time()) + " s")
        report.close()

    def outputPatterns(self, MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict):
        """
         * print maximal patterns to XML file
         * @param: MFP_dict, dictionary with FTArray as key and String as values
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as values
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys et String as values
        """
        try:
            outFile = config.getOutputFile()
            # create output file to store patterns for mining common patterns
            outputCommonPatterns = open(outFile + ".txt", 'w+')
            # output maximal patterns
            outputMaximalPatterns = XMLOutput(outFile, config, grammar_dict, xmlCharacters_dict)
            pattern = Pattern()
            for key in MFP_dict:
                pat = getPatternStr(key, labelIndex_dict)
                supports = MFP_dict[key]
                outputMaximalPatterns.report_Int(pat, supports)
                outputCommonPatterns.write(pattern.getPatternString1(pat) + "\n")
            outputMaximalPatterns.close()
            outputCommonPatterns.flush()
            outputCommonPatterns.close()

        except:
            e = sys.exc_info()[0]
            print("Print maximal patterns error : " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)