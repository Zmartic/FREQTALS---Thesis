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

    def __init__(self, init_memory=None):
        """
        :param init_memory: list(int), initializer for the memory
        """
        if init_memory is None:
            init_memory = []

        self.memory = init_memory

    def copy(self):
        return FTArray(self.memory.copy())

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

    def add(self, element):
        """
         Append one element to the FTArray
        :param element: int
        """
        self.memory.append(element)

    def add_all(self, other):
        """
         Append the data of other to self
        :param other: FTArray
        """
        self.memory = self.memory + other.memory

    def extend(self, prefix, candidate):
        """
         Extend the pattern with some extension = (prefix, candidate)
        :param prefix: int, number of -1 to be push
        :param candidate: int, the label of the node we want to add
        """
        self.memory = self.memory + ([-1] * prefix)
        self.add(candidate)

    def sub_list(self, start, stop):
        """
         Compute the sublist of self.memory going from index "start" to "stop"
            this function should create a new FTArray
         :param start: int, index where we start to include element
         :param stop:  int, index where we stop to include element
         :return: FTArray, the sub_list
        """
        return FTArray(self.memory[start:stop])

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
