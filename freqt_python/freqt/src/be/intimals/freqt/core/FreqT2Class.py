#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square, get_2class_support
from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class
from freqt.src.be.intimals.freqt.core.InitData import init_data_2class


class FreqT2Class(FreqT1Class):

    def __init__(self, config):
        super().__init__(config)
        self.sizeClass1 = -1
        self.sizeClass2 = -1

    def init_data(self):
        self._transaction_list, self._transactionClassID_list, self.label_decoder, self.sizeClass1, self.sizeClass2, \
            self._grammar_dict, self._xmlCharacters_dict, self.constraints = init_data_2class(self._config)

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
        # note: the pattern score is recomputed once and the support twice here,
        #       but they were already computed inside add_tree_requested() -> satisfy_chi_square()
        score = chi_square(proj, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
        ac = get_2class_support(proj, self._config.getWeighted())
        return str(ac[0]) + "-" + str(ac[1]) + "," + str(score) + "," + str(pat.n_node)

