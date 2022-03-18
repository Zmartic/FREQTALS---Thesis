#!/usr/bin/env python3
from abc import ABC, abstractmethod

from freqt.src.be.intimals.freqt.constraint import Constraint
from freqt.src.be.intimals.freqt.util.Initial_Int import readRootLabel


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
    def authorized_pattern(self, pattern, candidate_prefix):
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


class DefaultStrategy(FreqTStrategy):

    def __init__(self, config, grammar, root_label_set=None):
        self.min_supp = config.getMinSupport()
        self.min_node = config.getMinNode()
        self.max_leaf = config.getMaxLeaf()
        self.min_leaf = config.getMinLeaf()

        self.grammar = grammar

        # read root labels (AST Nodes)
        #if root_label_set is not None:
        self.root_labels_set = set()
        readRootLabel(config.getRootLabelFile(), self.root_labels_set)
        '''if len(self.root_labels_set) == 0:
            self.is_root_allowed = lambda root: root != "" and root[0] != '*' and root[0].isupper()
        else:
            self.is_root_allowed = lambda root: root in self.root_labels_set'''

        if config.getWeighted():  # TODO maybe doesn't work
            self.prune_method = lambda proj: Constraint.prune_min_w_supp(proj, self.min_supp)
        else:
            self.prune_method = lambda proj: Constraint.prune_min_supp(proj, self.min_supp)

    def allowed_label_as_root(self, label):
        if label in self.root_labels_set or len(self.root_labels_set) == 0:
            return label != "" and label[0] != '*' and label[0].isupper()
        return False

    def prune(self, proj):  # maybe doesn't work
        return self.prune_method(proj)

    def authorized_pattern(self, pattern, candidate_prefix):
        # * check obligatory children constraint
        return not Constraint.missing_left_obligatory_child(pattern, candidate_prefix, self.grammar)

    def stop_expand_pattern(self, pattern):
        return Constraint.satisfy_max_leaf(pattern, self.max_leaf) or Constraint.is_not_full_leaf(pattern)

    def satisfy_post_expansion_constraint(self, pattern):
        if pattern is None:
            return False
        # * Minimum size constraints
        # * Right mandatory children
        return Constraint.satisfy_min_leaf(pattern, self.min_leaf) and \
            Constraint.satisfy_min_node(pattern, self.min_node) and \
            not Constraint.missing_right_obligatory_child(pattern, self.grammar)


class FreqTExtStrategy(DefaultStrategy):

    def stop_expand_pattern(self, pattern):
        return Constraint.is_not_full_leaf(pattern)
