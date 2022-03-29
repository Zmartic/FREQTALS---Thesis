#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square, get_2class_support
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt


class FreqT2ClassExt(FreqT1ClassExt):

    def __init__(self, _config, root_ids_list, _grammar_dict, _grammarInt_dict, _xmlCharacters_dict, label_decoder,
                 _transaction_list, size_class1, size_class2):
        super().__init__(_config, root_ids_list, _grammar_dict, _grammarInt_dict, _xmlCharacters_dict, label_decoder,
                         _transaction_list)
        self.size_class1 = size_class1
        self.size_class2 = size_class2

    def add_tree_requested(self, pat, proj):
        if not self.constraints.satisfy_post_expansion_constraint(pat):
            return False
        # check chi-square score
        score = chi_square(proj, self.size_class1, self.size_class2, self._config.getWeighted())
        if satisfy_chi_square(score, self._config.getDSScore()):
            self.add_tree(pat, proj)
            return True
        return False

    def get_support_string(self, pat, proj):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        # note: the pattern score is recomputed once and the support twice here,
        #       but they were already computed inside add_tree_requested()
        score = chi_square(proj, self.size_class1, self.size_class2, self._config.getWeighted())
        ac = get_2class_support(proj, self._config.getWeighted())
        return str(ac[0]) + "-" + str(ac[1]) + "," + str(score) + "," + str(pat.n_node)
