#!/usr/bin/env python3


from abc import ABC, abstractmethod
import collections


class AOutputFormatter(ABC):  # abstract class
    nbPattern = -1
    fileName = ""
    out = None  # link to a file ready to be written
    config = None  # Config structure
    grammar_dict = dict()  # a dictionary with String as keys and list of String as values
    xmlCharacters_dict = dict()  # dictionary with String as keys and String as values
    patSupMap_ord_dict = collections.OrderedDict()  # ordered dictionary with String as keys and values

    """
     * create a AOutputFormatter element
     * @param: _fileName, String
     * @param: _config, Config
     * @param: _grammar_dict, a dictionary with String as keys and list of String as values
     * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
    """
    @abstractmethod
    def __init__(self, _fileName, _config, _grammar_dict, _xmlCharacters_dict):
        self.nbPattern = 0
        self.fileName = _fileName
        self.config = _config
        self.grammar_dict = _grammar_dict
        self.xmlCharacters_dict = _xmlCharacters_dict
        self.openOutputFile()

    @abstractmethod
    def openOutputFile(self):
        self.out = open(self.fileName, 'w+')

    @property
    @abstractmethod
    def getNbPattern(self):
        return self.nbPattern

    """
     * check if a pattern satisfies output constraints
     * @param pat, a list of String
     * @return
    """
    @abstractmethod
    def checkOutputConstraint(self, pat):
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
        newList = list()
        for elem in list1:
            newList.append(elem)
        for elem in list2:
            newList.append(elem)
        return newList

    """
     * print a given pattern
     * @param: pat, a string
    """
    @abstractmethod
    def printPattern(self, pat):
        pass

    """
     * close a file
    """
    @abstractmethod
    def close(self):
        pass
