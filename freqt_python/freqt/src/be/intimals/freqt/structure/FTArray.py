#!/usr/bin/env python3
import copy


class FTArray:
    """
    FTArray represent a subtree/pattern (using an array).
    ex:
         1
        / \
       2   3
      /   / \
     4   5   6
    FTArray = [1, 2, -4, -1, -1, 3, -5, -1, -6]
    """

    def __init__(self, init_memory, n_node, n_leaf):
        """
        :param init_memory: list(int), initializer for the memory
        """
        self.memory = init_memory
        self.n_node = n_node
        self.n_leaf = n_leaf

    @staticmethod
    def make_root_pattern(root):
        return FTArray([root], 1, 0)

    def copy(self):
        return FTArray(self.memory.copy(), self.n_node, self.n_leaf)

    def get(self, i):
        """
         Get the element of the FTArray at index i
        :param i: int
        :return: int
        """
        return self.memory[i]

    def get_last(self):
        """
         Get the last element store in self.memory
        :return: int, last element
        """
        return self.memory[-1]

    def extend(self, prefix, candidate):
        """
         Extend the pattern with some extension = (prefix, candidate)
        :param prefix: int, number of -1 to be push
        :param candidate: int, the label of the node we want to add
        """
        self.n_node += 1
        if candidate < -1:
            self.n_leaf += 1

        self.memory = self.memory + ([-1] * prefix)
        self.memory.append(candidate)

    def undo_extend(self, prefix):
        """
        Undo some extension
        :param prefix: int, number of -1 that as been pushed
        """
        self.n_node -= 1
        if self.get_last() < -1:
            self.n_leaf -= 1

        _ = self.memory.pop()
        for _ in range(prefix):
            _ = self.memory.pop()

    def sub_list(self, start, stop):
        """
         Compute the sublist of self.memory going from index "start" to "stop"
            this function should create a new FTArray
         :param start: int, index where we start to include element
         :param stop:  int, index where we stop to include element
         :return: FTArray, the sub_list
        """
        # TODO
        return FTArray(self.memory[start:stop], self.n_node, self.n_leaf)

    def __eq__(self, other):
        return self.memory == other.memory

    def __hash__(self):
        return hash(tuple(self.memory))

    def size(self):
        """
         Compute the current size of the memory
         :return: int
        """
        return len(self.memory)

    def contains(self, element):
        """
         Return True if element is contains in the FTArray
         :param element: int
         :return: int
        """
        return element in self.memory

    def index(self, element):
        """
         Return the position of the first occurrence of element in the FTArray
            if the FTArray doesn't contains element, return -1
         :param element: int
         :return: int, the first

         note: the implementation of index() in Python returns ValueError if element is not found
        """
        try:
            return self.memory.index(element)
        except ValueError:
            return -1
