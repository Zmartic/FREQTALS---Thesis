#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square, get_2class_support
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT1Strategy
from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.input.Initial_Int import convert_grammar_label2int, \
    read_XML_character, init_grammar, read_white_label


class FreqT2Class(FreqT1Class):

    def __init__(self, config):
        super().__init__(config)
        self.label_str2int = dict()
        self.sizeClass1 = -1
        self.sizeClass2 = -1

        # dictionary of maximal frequent patterns
        self.mfp = dict()
        # set of pattern that are not maximal
        self.not_maximal_set = set()

    def init_data(self):
        """
         * read input data
        """
        white_label = read_white_label(self._config.getWhiteLabelFile())

        # remove black labels when reading ASTs
        self._transaction_list = list()
        self._transactionClassID_list = list()
        self.label_decoder = dict()
        readXML = ReadXMLInt()
        readXML.readDatabase(self._transaction_list, 1, self._config.getInputFiles1(), self.label_decoder,
                             self._transactionClassID_list, white_label)
        readXML.readDatabase(self._transaction_list, 0, self._config.getInputFiles2(), self.label_decoder,
                             self._transactionClassID_list, white_label)
        self.sizeClass1 = sum(self._transactionClassID_list)
        self.sizeClass2 = len(self._transactionClassID_list) - self.sizeClass1

        # init grammar
        self._grammar_dict = dict()
        init_grammar(self._config.getInputFiles1(), white_label, self._grammar_dict, self._config.buildGrammar())
        init_grammar(self._config.getInputFiles2(), white_label, self._grammar_dict, self._config.buildGrammar())

        # read list of special XML characters
        self._xmlCharacters_dict = dict()
        self._xmlCharacters_dict = read_XML_character(self._config.getXmlCharacterFile())

        grammar_int = convert_grammar_label2int(self._grammar_dict, self.label_decoder)
        self.constraints = FreqT1Strategy(self._config, grammar_int)

    def add_tree_requested(self, pat, projected):
        # check chi-square score
        if self.constraints.satisfy_post_expansion_constraint(pat) and \
                satisfy_chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                                   self._config.getWeighted()):
            self.add_tree(pat, projected)
            return True
        return False

    def get_support_string(self, pat, proj):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        # note: the pattern score is recomputed once and the 2class_support twice here,
        #       but they were already computed inside add_tree_requested() -> satisfy_chi_square()
        score = chi_square(proj, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
        ac = get_2class_support(proj, self._config.getWeighted())
        return str(ac[0]) + "-" + str(ac[1]) + "," + str(score) + "," + str(pat.n_node)

