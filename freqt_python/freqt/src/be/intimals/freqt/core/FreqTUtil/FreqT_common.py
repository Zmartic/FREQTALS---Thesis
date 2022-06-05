#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.config.Config import *
import freqt.src.be.intimals.freqt.structure.Projected as proj
from freqt.src.be.intimals.freqt.input.ReadFile import *
from freqt.src.be.intimals.freqt.output.XMLOutput import *

from freqt.src.be.intimals.freqt.constraint.Constraint import prune
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR


import collections
from xml.dom import minidom
from xml.dom import Node
import sys
import traceback

"""
    find a common pattern in each cluster
"""


class FreqT_common:

    def __init__(self):
        self.__config = None
        self.__grammar_dict = dict()  # dictionary with String as keys and list of String as values
        self.__xmlCharacters_dict = dict()  # dictionary with String as keys and String as values

        self.__commonOutputPatterns_dict = collections.OrderedDict  # ordered dictionary with String as keys and String as values
        self.__maximalPattern_list = list()  # list of String
        self.__newTransaction_list = list()  # list of list of String
        self.__minsup = -1
        self.__found = False

    """
     * @param: _config, Config
     * @param: _grammar_dict, dictionary with String as keys and list of String as values
     * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
    """
    def FreqT_common(self, _config, _grammar_dict, _xmlCharacters_dict):
        self.__config = _config
        self.__grammar_dict = _grammar_dict
        self.__xmlCharacters_dict = _xmlCharacters_dict

    """
     * expand a subtree
     * @param: projected, Projected
    """
    def project(self, projected):
        if self.__found:
            return
        # find all candidates of the current subtree
        depth = projected.get_depth()
        candidate_dict = collections.OrderedDict()  # ordered dictionary with String as keys and Projected as values
        for i in range(projected.size()):
            id = projected.get_location(i).get_location_id()
            pos = projected.get_location(i).get_position()
            prefix = ""
            for d in range(-1, depth):
                if pos != -1:
                    if d == -1:
                        start = self.__newTransaction_list[id][pos].getNodeChild()
                    else:
                        start = self.__newTransaction_list[id][pos].getNodeSibling()
                    newdepth = depth - d
                    l = start
                    while l != -1:
                        item = prefix + UNICHAR + self.__newTransaction_list[id][l].getNodeLabel()
                        if item in candidate_dict:
                            candidate_dict[item].set_location(id, l)  # store right most positions
                        else:
                            tmp = proj.Projected()
                            tmp.set_depth(newdepth)
                            tmp.set_location(id, l)  # store right most positions
                            candidate_dict[item] = tmp

                        l = self.__newTransaction_list[id][l].getNodeSibling()

                    if d != -1:
                        pos = self.__newTransaction_list[id][pos].getNodeParent()
                    prefix += UNICHAR + ")"
        prune(candidate_dict, self.__minsup, False)

        if len(candidate_dict) == 0:
            self.addCommonPattern(self.__maximalPattern_list, projected)
            self.__found = True
        else:
            # expand the current pattern with each candidate
            for keys in candidate_dict:
                oldSize = len(self.__maximalPattern_list)
                # add new candidate to current pattern
                p = keys.split(UNICHAR)
                for i in range(len(p)):
                    if len(p[i]) != 0:
                        self.__maximalPattern_list.append(p[i])
                self.project(candidate_dict[keys])
                if oldSize <= len(self.__maximalPattern_list):
                    self.__maximalPattern_list = self.__maximalPattern_list[:oldSize]
                else:
                    while len(self.__maximalPattern_list) < oldSize:
                        self.__maximalPattern_list.append(None)

    """
     1. for each cluster find a set of patterns
     2. create a tree data
     3. find the common pattern
     4. write cluster-common pattern to file
     * @param: inPatterns, String
     * @param: inClusters, String
     * @param: outCommonFile, String
    """
    def run(self, inPatterns, inClusters, outCommonFile):
        self.__commonOutputPatterns_dict = collections.OrderedDict()  # ordered dictionary with String as keys and String as values
        clusters_list = self.readClusters(inClusters)  # list of list of Integer
        patterns_list = self.readPatterns(inPatterns)  # list of String
        pattern = Pattern()

        for i in range(len(clusters_list)):
            if len(clusters_list[i]) < 2:
                ttt = "1,1,1,1\t" + pattern.covert(patterns_list[clusters_list[i][0] - 1])
                self.__commonOutputPatterns_dict[patterns_list[clusters_list[i][0] - 1]] = ttt

            else:
                tempDatabase = dict()  # dictionary with String as keys and values
                for j in range(len(clusters_list[i])):
                    tempDatabase[patterns_list[clusters_list[i][j] - 1]] = "nothing"
                self.__found = False
                self.__newTransaction_list = list()
                self.initDatabase(tempDatabase)
                self.__minsup = len(tempDatabase)
                FP1_dict = self.buildFP1Set(self.__newTransaction_list)  # dictionary with String as keys and Projected as values
                prune(FP1_dict, self.__minsup, False)
                self.__maximalPattern_list = list()  # list of String
                for keys in FP1_dict:
                    if keys is not None and keys[0] != '*':
                        FP1_dict[keys].set_depth(0)
                        self.__maximalPattern_list.append(keys)
                        self.project(FP1_dict[keys])
                        self.__maximalPattern_list.pop(len(self.__maximalPattern_list) - 1)
        # output common pattern in each cluster
        self.outputMFP(self.__commonOutputPatterns_dict, outCommonFile)


    """
     * Return all frequent subtrees of size 1
     * @param: trans_list, list of list of String
     * @return a dictionary with String as keys and Projected as values
    """
    def buildFP1Set(self, trans_list):
        freq1_dict = collections.OrderedDict()  # ordered dictionary with String as keys and Projected as values
        for i in range(len(trans_list)):
            for j in range(len(trans_list[i])):
                node_label = trans_list[i][j].getNodeLabel()

                if len(node_label) != 0:
                    # if node_label already exists
                    if node_label in freq1_dict:
                        freq1_dict[node_label].set_location(i, j)
                    else:
                        projected = proj.Projected()
                        projected.set_location(i, j)
                        freq1_dict[node_label] = projected
        return freq1_dict

    """
     * @param: pat_list, list of String
     * @param: projected, Projected
    """
    def addCommonPattern(self, pat_list, projected):

        pattern = Pattern()
        support = projected.get_support()
        wsupport = projected.get_root_support()  # => root location
        size = pattern.getPatternSize(pat_list)

        # replace "," in the leafs by uniChar
        patString = pat_list[0]
        for i in range(1, len(pat_list)):
            patString = patString + "," + pat_list[i]
        patternSupport = "rootOccurrences" + "," + str(support) + "," + str(wsupport) + "," + str(size) + "\t" + str(patString)  # keeping for XML output
        self.__commonOutputPatterns_dict[str(pat_list)] = patternSupport

    """
     * filter and print maximal patterns
     * @param: maximalPatterns_dict, dictionary with String as keys and values
     * @param: outFile, String
    """
    def outputMFP(self, maximalPatterns_dict, outFile):
        try:
            outputCommonPatterns = open(outFile + ".txt", "w+")
            # output maximal patterns
            outputMaximalPatterns = XMLOutput(outFile, self.__config, self.__grammar_dict, self.__xmlCharacters_dict)
            for keys in maximalPatterns_dict:
                outputMaximalPatterns.printPattern(maximalPatterns_dict[keys])
                outputCommonPatterns.write(keys + "\n")
            outputMaximalPatterns.close()
            outputCommonPatterns.flush()
            outputCommonPatterns.close()
        except:
            e = sys.exc_info()[0]
            print("error print maximal patterns " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    """
     * create transaction from list of patterns
     * @param: patterns_dict, dictionary with String as keys and values
    """
    def initDatabase(self, patterns_dict):
        readFile = ReadFile()
        readFile.createTransactionFromMap(patterns_dict, self.__newTransaction_list)



    """
     * @param: inPatterns, String
     * @return a list of String
    """
    def readPatterns(self, inPatterns):
        patterns_list = list()  # list of String
        try:
            f = open(inPatterns, 'r')
            line = f.readline()
            while line:
                if len(line) != 0:
                    line = line.replace("\n", "")
                    patterns_list.append(line)
                line = f.readline()
            f.close()
        except:
            e = sys.exc_info()[0]
            print("Error: readPatterns function " + str(e))
            trace = traceback.format_exc()
            print(trace)
            raise
        return patterns_list

    """
     * @param: inClusters, String
     * @return a list of list of String
    """
    def readClusters(self, inClusters):
        temp_list = list()  # list of list of Integer
        try:
            # read XML file
            doc = minidom.parse(inClusters)
            doc.documentElement.normalize()

            # for each cluster ID, collect a list of pattern ID
            clusters_list = doc.documentElement.childNodes
            for i in range(len(clusters_list)):
                if clusters_list.item(i).nodeType == Node.ELEMENT_NODE:
                    patterns_list = clusters_list.item(i).childNodes
                    # for each patterns get the pattern ID
                    t_list = list()  # list of Integer
                    for j in range(len(patterns_list)):
                        if patterns_list[j].nodeType == Node.ELEMENT_NODE:
                            nodeMap = patterns_list[j].attributes
                            for k in range(len(nodeMap)):
                                if nodeMap.item(k).name == "ID":
                                    ID = int(nodeMap.item(k).value)
                                    t_list.append(ID)
                    temp_list.append(t_list)
        except:
            e = sys.exc_info()[0]
            print("Error: readClusters function " + str(e))
            trace = traceback.format_exc()
            print(trace)
            raise
        return temp_list
