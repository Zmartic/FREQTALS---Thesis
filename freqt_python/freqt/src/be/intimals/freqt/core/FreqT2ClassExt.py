#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square, get_2class_support
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt


class FreqT2ClassExt(FreqT1ClassExt):
    """
     Implementation of the 2nd step of the FREQTALS algorithm on 1 class data
    """

    def __init__(self, _config, root_ids_list, _grammar_dict, _grammar_int_dict,
                 _xml_characters_dict, label_decoder, _transaction_list,
                 size_class1, size_class2):
        """
         :param config: Config
        """
        self._transaction_list = None
        self._transaction_class_id_list = None
        self.label_decoder = None
        self._grammar_dict = None
        self._xml_characters_dict = None
        self.constraints = None

        super().__init__(_config, root_ids_list, _grammar_dict, _grammar_int_dict,
                         _xml_characters_dict, label_decoder, _transaction_list)

        self.size_class1 = size_class1
        self.size_class2 = size_class2

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
        score = chi_square(proj, self.size_class1, self.size_class2, self._config.get_weighted())
        sup_c1, sup_c2 = get_2class_support(proj, self._config.get_weighted())
        return str(sup_c1) + "-" + str(sup_c2) + "," + str(score) + "," + str(pat.n_node)
