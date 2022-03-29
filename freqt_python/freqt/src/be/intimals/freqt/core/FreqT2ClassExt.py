#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt


class FreqT2ClassExt(FreqT1ClassExt):

    def add_tree_requested(self, pat, proj):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check chi-square score
        if self.constraints.satisfy_post_expansion_constraint(pat) and \
                satisfy_chi_square(proj, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                                   self._config.getWeighted()):
            self.add_tree(pat, proj)
            return True
        return False