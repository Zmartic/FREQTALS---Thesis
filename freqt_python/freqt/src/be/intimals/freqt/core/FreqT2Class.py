#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square, get_2class_support
from freqt.src.be.intimals.freqt.core.FreqT import FreqT
from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.structure.PatternInt import countNode
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, initGrammar_Int2, readRootLabel, \
    readXMLCharacter


class FreqT2Class(FreqT):

    def init_data(self):
        """
         * read input data
        """
        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles1(), self._labelIndex_dict,
                                 self.__transactionClassID_list, self._config.getWhiteLabelFile())
            readXML.readDatabase(self._transaction_list, 0,
                                 self._config.getInputFiles2(), self._labelIndex_dict,
                                 self.__transactionClassID_list, self._config.getWhiteLabelFile())
            self.sizeClass1 = sum(self.__transactionClassID_list)
            self.sizeClass2 = len(self.__transactionClassID_list) - self.sizeClass1
            initGrammar_Str(self._config.getInputFiles1(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())
            initGrammar_Str(self._config.getInputFiles2(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())
            initGrammar_Int2(self._grammarInt_dict, self._grammar_dict, self._labelIndex_dict)

            # read root labels (AST Nodes)
            readRootLabel(self._config.getRootLabelFile(), self.rootLabels_set)
            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def add_tree(self, pat, projected):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check chi-square score
        if satisfy_chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                              self._config.getWeighted()):
            self.add_maximal_pattern(pat, projected, self.MFP_dict)

    def get_support_string(self, pat, projected):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        score = chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
        ac = get_2class_support(projected, self._config.getWeighted())
        support = str(ac[0]) + "-" + str(ac[1])
        size = countNode(pat)

        return support + "," + str(score) + "," + str(size)
