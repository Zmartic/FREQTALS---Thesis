#!/usr/bin/env python3
import copy


class FTArray:
    """
    We store data in memory.
    TODO
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
        if i < 0 or i >= len(self.memory):
            raise Exception("Out of bounds access in FTArray.get(i). i is " + str(i) + ", size is "
                            + str(len(self.memory)))
        return self.memory[i]

    def get_last(self):
        """
         get the last element store in self.memory
         :return: int
        """
        return self.memory[-1]

    def add(self, element):
        """
         Append one element to self.memory
         :param element: int
        """
        self.memory.append(element)

    def add_all(self, other):
        """
         Append the data of other to self.memory
         :param other: FTArray
        """
        self.memory = self.memory + other.memory

    def sub_list(self, start, stop):
        """
         Compute the sublist of self.memory going from index "start" to "stop"
         :param start: int
         :param stop:  int
         :return:      FTArray
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
         Return the position of element in the FTArray
         :param element: int
         :return: int
        """
        return self.memory.index(element)
