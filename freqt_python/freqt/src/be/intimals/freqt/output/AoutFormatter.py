#!/usr/bin/env python3


from abc import ABC, abstractmethod


class AOutputFormatter(ABC):  # abstract class

    @abstractmethod
    def __init__(self, filename, _config, _grammar_dict, _xml_characters_dict):
        """
         * create a AOutputFormatter element
         * @param: filename, String
         * @param: _config, Config
         * @param: _grammar_dict, a dictionary with String as keys and list of String as values
         * @param: _xml_characters_dict, dictionary with String as keys and String as values
        """
        self.nb_pattern = 0
        self.filename = filename
        self.out = None  # link to a file ready to be written
        self.config = _config  # Config structure
        self.grammar_dict = _grammar_dict  # a dictionary with String as keys and list of String as values
        self.xml_characters_dict = _xml_characters_dict  # ordered dictionary with String as keys and values
        self.openOutputFile()

    @abstractmethod
    def openOutputFile(self):
        self.out = open(self.filename, 'w+', encoding='utf-8')

    @property
    @abstractmethod
    def getNbPattern(self):
        return self.nb_pattern

    @abstractmethod
    def checkOutputConstraint(self, pat):
        """
         * check if a pattern satisfies output constraints
         * @param pat, a list of String
         * @return
        """
        """
        patternInt = PatternInt()
        if patternInt.checkMissingLeaf(pat) or patternInt.countLeafNode(pat) < self.config.getMinLeaf():
            return True
        else:
            return False
        """
        return True

    """
     * union two lists
     * @param list1, list
     * @param list2, list
     * @param <T>
     * @return a list
    """
    @abstractmethod
    def union(self, list1, list2):
        new_list = []
        for elem in list1:
            new_list.append(elem)
        for elem in list2:
            new_list.append(elem)
        return new_list

    @abstractmethod
    def printPattern(self, pat):
        """
         * print a given pattern
         * @param: pat, a string
        """

    @abstractmethod
    def close(self):
        """
         * close a file
        """
