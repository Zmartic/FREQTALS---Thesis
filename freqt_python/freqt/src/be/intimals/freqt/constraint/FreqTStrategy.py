#!/usr/bin/env python3
from abc import ABC, abstractmethod

from freqt.src.be.intimals.freqt.constraint import Constraint


class FreqTStrategy(ABC):
    @abstractmethod
    def __init__(self, config, grammar):
        pass

    @abstractmethod
    def allowed_label_as_root(self, label):
        pass

    @abstractmethod
    def prune(self, proj):
        pass

    @abstractmethod
    def is_pruned_pattern(self, pattern, candidate_prefix):
        """

        :param pattern:
        :param candidate_prefix:
        :return:
        """
        pass

    @abstractmethod
    def stop_expand_pattern(self, pattern):
        """

        :param pattern:
        :return:
        """
        pass

    @abstractmethod
    def satisfy_post_expansion_constraint(self, pattern):
        """

        :param pattern:
        :return:
        """
        pass


class FreqT1Strategy(FreqTStrategy):

    def __init__(self, config, grammar, root_labels_set=None):
        self.min_supp = config.get_min_support()
        self.min_node = config.get_min_node()
        self.max_leaf = config.get_max_leaf()
        self.min_leaf = config.get_min_leaf()

        self.grammar = grammar

        # read root labels (AST Nodes)
        self.root_labels_set = dict() if root_labels_set is None else root_labels_set

    def allowed_label_as_root(self, label):
        if label in self.root_labels_set or len(self.root_labels_set) == 0:
            return label != "" and label[0] != '*' and label[0].isupper()
        return False

    def prune(self, proj):
        pass

    def is_pruned_pattern(self, pattern, candidate_prefix):
        # * check obligatory children constraint
        return Constraint.missing_left_obligatory_child(pattern, candidate_prefix, self.grammar)

    def stop_expand_pattern(self, pattern):
        return Constraint.satisfy_max_leaf(pattern, self.max_leaf) or Constraint.is_not_full_leaf(pattern)

    def satisfy_post_expansion_constraint(self, pattern):
        # * Minimum size constraints
        # * Right mandatory children
        return Constraint.satisfy_min_leaf(pattern, self.min_leaf) and \
            Constraint.satisfy_min_node(pattern, self.min_node) and \
            not Constraint.missing_right_obligatory_child(pattern, self.grammar)


class FreqT1ExtStrategy(FreqTStrategy):

    # Constraint.check_cobol_constraints(largestPattern, candidates_dict, keys, self._labelIndex_dict, self._transaction_list) TODO

    def __init__(self, config, grammar):
        self.min_supp = config.get_min_support()
        self.min_node = config.get_min_node()
        # max leaf constraint dropped
        self.min_leaf = config.get_min_leaf()

        self.grammar = grammar

    def allowed_label_as_root(self, label):
        pass

    def prune(self, proj):
        pass

    def is_pruned_pattern(self, pattern, candidate_prefix):
        # * check obligatory children constraint
        return Constraint.missing_left_obligatory_child(pattern, candidate_prefix, self.grammar)

    def stop_expand_pattern(self, pattern):
        return Constraint.is_not_full_leaf(pattern)  # Max leaf constraint dropped

    def satisfy_post_expansion_constraint(self, pattern):
        # * Minimum size constraints
        # * Right mandatory children
        return Constraint.satisfy_min_leaf(pattern, self.min_leaf) and \
            Constraint.satisfy_min_node(pattern, self.min_node) and \
            not Constraint.missing_right_obligatory_child(pattern, self.grammar)

