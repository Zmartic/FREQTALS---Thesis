#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT2Strategy
from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.input.Initial_Int import convert_grammar_label2int, \
    read_XML_character, init_grammar


class FreqT2Class(FreqT1Class):

    def __init__(self, config):
        super().__init__(config)
        self.label_str2int = dict()
        self.sizeClass1 = -1
        self.sizeClass2 = 1

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
                                 self._config.getInputFiles1(), self.label_str2int,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            readXML.readDatabase(self._transaction_list, 0,
                                 self._config.getInputFiles2(), self.label_str2int,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            self.sizeClass1 = sum(self._transactionClassID_list)
            self.sizeClass2 = len(self._transactionClassID_list) - self.sizeClass1
            init_grammar(self._config.getInputFiles1(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())
            init_grammar(self._config.getInputFiles2(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            self._xmlCharacters_dict = read_XML_character(self._config.getXmlCharacterFile())

            grammar_int = convert_grammar_label2int(self._grammar_dict, self.label_str2int)
            self.constraints = FreqT2Strategy(self._config, grammar_int)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def add_tree(self, pat, projected):
        """
         * add the tree to the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check chi-square score
        if self.constraints.satisfy_post_expansion_constraint(pat) and \
                satisfy_chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                                   self._config.getWeighted()):
            self.add_maximal_pattern(pat, projected, self.mfp)
            return True
        return False

    def post_mining_process(self, report):
        self.outputPatternInTheFirstStep(self.mfp, self._config, self._grammar_dict, self.label_str2int,
                                         self._xmlCharacters_dict, report)  #TODO
