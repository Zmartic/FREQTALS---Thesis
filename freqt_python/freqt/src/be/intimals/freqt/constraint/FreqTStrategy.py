#!/usr/bin/env python3
from abc import ABC, abstractmethod

from freqt.src.be.intimals.freqt.constraint import Constraint


class FreqTStrategy(ABC):
    """ Abstract classes """
    @abstractmethod
    def __init__(self, config, grammar):
        """
        :param config: Config
        :param grammar: Dict(Int,String), decode integer into their corresponding label
        """

    @abstractmethod
    def allowed_label_as_root(self, label):
        """
         * Used during the creating of the initial set of root patterns
        :param label: Int, a label
        :return: whether label is allowed to occur as root
        """

    @abstractmethod
    def prune(self, proj):
        """ not yet implemented """
    @abstractmethod
    def is_pruned_pattern(self, pat, candidate_prefix):
        """
         * Used during the expansion of patterns
        :param pat: FTArray, extended pattern
        :param candidate_prefix: Int, number of "up" move (-1) in the extension added
        :return: whether this pattern can be pruned
        """

    @abstractmethod
    def stop_expand_pattern(self, pat):
        """
         * Used to stop the expansion of pattern
        :param pat: FTArray, a pattern
        :return: whether pat cannot be extended anymore
        """

    @abstractmethod
    def satisfy_post_expansion_constraint(self, pat):
        """
         * Used when the algorithm requests the addition of pat to the output
        :param pat: FTArray, a pattern
        :return: whether pat satisfy every constraint
        """


class FreqT1Strategy(FreqTStrategy):
    """ Implementation of Default FreqTStrategy """

    def __init__(self, config, grammar, root_labels_set=None):
        """
        :param config: Config
        :param grammar: Dict(Int,String), decode integer into their corresponding label
        :param root_labels_set:  Dict(Int), dictionary of allowed root labels
        """
        self.min_supp = config.get_min_support()
        self.min_node = config.get_min_node()
        self.max_leaf = config.get_max_leaf()
        self.min_leaf = config.get_min_leaf()

        self.grammar = grammar

        # read root labels (AST Nodes)
        self.root_labels_set = {} if root_labels_set is None else root_labels_set

    def allowed_label_as_root(self, label):
        """
         * If provided, self.root_labels_set defines the allowed label to occur as root
        :param label: Int, a label
        :return: whether label is allowed to occur as root
        """
        if label in self.root_labels_set or len(self.root_labels_set) == 0:
            return label != "" and label[0] != '*' and label[0].isupper()
        return False

    def prune(self, proj):
        """ not yet implemented """

    def is_pruned_pattern(self, pat, candidate_prefix):
        """
         * check left obligatory children constraint
        :param pat: FTArray, extended pattern
        :param candidate_prefix: Int, number of "up" move (-1) in the extension added
        :return: whether this pattern can be pruned
        """
        return Constraint.missing_left_obligatory_child(pat, candidate_prefix, self.grammar)

    def stop_expand_pattern(self, pat):
        """
         * check maximum leaf constraint
         * check real leaf constraint
        :param pat: FTArray, a pattern
        :return: whether pat cannot be extended anymore
        """
        return Constraint.satisfy_max_leaf(pat, self.max_leaf) or Constraint.is_not_full_leaf(pat)

    def satisfy_post_expansion_constraint(self, pat):
        """
         * check minimum size constraints
         * check right obligatory children
        :param pat: FTArray, a pattern
        :return: whether pat satisfy every constraint
        """
        return Constraint.satisfy_min_leaf(pat, self.min_leaf) and \
            Constraint.satisfy_min_node(pat, self.min_node) and \
            not Constraint.missing_right_obligatory_child(pat, self.grammar)


class FreqT1ExtStrategy(FreqTStrategy):
    """
        Implementation of FreqTStrategy for the 2nd step of the algorithm
        which drop the maximum size constraint
    """

    # Constraint.check_cobol_constraints(largestPattern, candidates_dict,
    #                                    keys, self._labelIndex_dict, self._transaction_list)

    def __init__(self, config, grammar):
        """
        :param config: Config
        :param grammar: Dict(Int,String), decode integer into their corresponding label
        """
        self.min_supp = config.get_min_support()
        self.min_node = config.get_min_node()
        # max leaf constraint dropped
        self.min_leaf = config.get_min_leaf()

        self.grammar = grammar

    def allowed_label_as_root(self, label):
        """ not used """

    def prune(self, proj):
        """ not yet implemented """

    def is_pruned_pattern(self, pat, candidate_prefix):
        """
         * check left obligatory children constraint
        :param pat: FTArray, extended pattern
        :param candidate_prefix: Int, number of "up" move (-1) in the extension added
        :return: whether this pattern can be pruned
        """
        return Constraint.missing_left_obligatory_child(pat, candidate_prefix, self.grammar)

    def stop_expand_pattern(self, pat):
        """
         * check real leaf constraint
        :param pat: FTArray, a pattern
        :return: whether pat cannot be extended anymore
        """
        return Constraint.is_not_full_leaf(pat)  # Max leaf constraint dropped

    def satisfy_post_expansion_constraint(self, pat):
        """
         * check minimum size constraints
         * check right obligatory children
        :param pat: FTArray, a pattern
        :return: whether pat satisfy every constraint
        """
        return Constraint.satisfy_min_leaf(pat, self.min_leaf) and \
            Constraint.satisfy_min_node(pat, self.min_node) and \
            not Constraint.missing_right_obligatory_child(pat, self.grammar)
