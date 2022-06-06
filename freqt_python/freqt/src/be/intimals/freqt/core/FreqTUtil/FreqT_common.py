#!/usr/bin/env python3
import collections
from xml.dom import minidom
from xml.dom import Node
import sys
import traceback

import freqt.src.be.intimals.freqt.structure.Projected as proj

from freqt.src.be.intimals.freqt.constraint.Constraint import prune
from freqt.src.be.intimals.freqt.input.ReadFile import ReadFile
from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR



class FreqT_common:
    """
        find a common pattern in each cluster
    """

    def __init__(self):
        self.__config = None
        self.__grammar_dict = {}  # dictionary with String as keys and list of String as values
        self.__xml_characters_dict = {}  # dictionary with String as keys and String as values

        self.__common_output_patterns_dict = collections.OrderedDict  # ordered dictionary with String as keys and String as values
        self.__maximal_pattern_list = []  # list of String
        self.__new_transaction_list = []  # list of list of String
        self.__minsup = -1
        self.__found = False

    def FreqT_common(self, _config, _grammar_dict, _xml_characters_dict):
        """
         * @param: _config, Config
         * @param: _grammar_dict, dictionary with String as keys and list of String as values
         * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
        """
        self.__config = _config
        self.__grammar_dict = _grammar_dict
        self.__xml_characters_dict = _xml_characters_dict

    def project(self, projected):
        """
         * expand a subtree
         * @param: projected, Projected
        """
        if self.__found:
            return
        # find all candidates of the current subtree
        depth = projected.get_depth()
        candidate_dict = collections.OrderedDict()  # ordered dictionary with String as keys and Projected as values
        for i in range(projected.size()):
            loc_id = projected.get_location(i).get_location_id()
            pos = projected.get_location(i).get_position()
            prefix = ""
            for cur_d in range(-1, depth):
                if pos != -1:
                    if cur_d == -1:
                        start = self.__new_transaction_list[loc_id][pos].getNodeChild()
                    else:
                        start = self.__new_transaction_list[loc_id][pos].getNodeSibling()
                    newdepth = depth - cur_d
                    l_node = start
                    while l_node != -1:
                        item = prefix + UNICHAR + self.__new_transaction_list[loc_id][l_node].getNodeLabel()
                        if item in candidate_dict:
                            candidate_dict[item].set_location(loc_id, l_node)  # store right most positions
                        else:
                            tmp = proj.Projected()
                            tmp.set_depth(newdepth)
                            tmp.set_location(loc_id, l_node)  # store right most positions
                            candidate_dict[item] = tmp

                        l_node = self.__new_transaction_list[loc_id][l_node].getNodeSibling()

                    if cur_d != -1:
                        pos = self.__new_transaction_list[loc_id][pos].getNodeParent()
                    prefix += UNICHAR + ")"
        prune(candidate_dict, self.__minsup, False)

        if len(candidate_dict) == 0:
            self.add_common_pattern(self.__maximal_pattern_list, projected)
            self.__found = True
        else:
            # expand the current pattern with each candidate
            for keys, candidate in candidate_dict.items():
                old_size = len(self.__maximal_pattern_list)
                # add new candidate to current pattern
                m_pat = keys.split(UNICHAR)
                for i in range(len(m_pat)):
                    if len(m_pat[i]) != 0:
                        self.__maximal_pattern_list.append(m_pat[i])
                self.project(candidate)
                if old_size <= len(self.__maximal_pattern_list):
                    self.__maximal_pattern_list = self.__maximal_pattern_list[:old_size]
                else:
                    while len(self.__maximal_pattern_list) < old_size:
                        self.__maximal_pattern_list.append(None)

    def run(self, in_patterns, in_clusters, out_common_file):
        """
         1. for each cluster find a set of patterns
         2. create a tree data
         3. find the common pattern
         4. write cluster-common pattern to file
         * @param: inPatterns, String
         * @param: inClusters, String
         * @param: outCommonFile, String
        """
        self.__common_output_patterns_dict = collections.OrderedDict()  # ordered dictionary with String as keys and String as values
        clusters_list = self.read_clusters(in_clusters)  # list of list of Integer
        patterns_list = self.read_patterns(in_patterns)  # list of String
        pattern = Pattern()

        for cluster in clusters_list:
            if len(cluster) < 2:
                ttt = "1,1,1,1\t" + pattern.covert(patterns_list[cluster[0] - 1])
                self.__common_output_patterns_dict[patterns_list[cluster[0] - 1]] = ttt

            else:
                temp_database = {}  # dictionary with String as keys and values
                for j in range(len(cluster)):
                    temp_database[patterns_list[cluster[j] - 1]] = "nothing"
                self.__found = False
                self.__new_transaction_list = []
                self.init_database(temp_database)
                self.__minsup = len(temp_database)
                fp1_dict = self.build_fp1_set(self.__new_transaction_list)  # dictionary with String as keys and Projected as values
                prune(fp1_dict, self.__minsup, False)
                self.__maximal_pattern_list = []  # list of String
                for keys in fp1_dict:
                    if keys is not None and keys[0] != '*':
                        fp1_dict[keys].set_depth(0)
                        self.__maximal_pattern_list.append(keys)
                        self.project(fp1_dict[keys])
                        self.__maximal_pattern_list.pop(len(self.__maximal_pattern_list) - 1)
        # output common pattern in each cluster
        self.output_mfp(self.__common_output_patterns_dict, out_common_file)

    @staticmethod
    def build_fp1_set(trans_list):
        """
         * Return all frequent subtrees of size 1
         * @param: trans_list, list of list of String
         * @return a dictionary with String as keys and Projected as values
        """
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

    def add_common_pattern(self, pat_list, projected):
        """
         * @param: pat_list, list of String
         * @param: projected, Projected
        """

        pattern = Pattern()
        support = projected.get_support()
        wsupport = projected.get_root_support()  # => root location
        size = pattern.getPatternSize(pat_list)

        # replace "," in the leafs by uniChar
        pat_string = pat_list[0]
        for i in range(1, len(pat_list)):
            pat_string = pat_string + "," + pat_list[i]
        pattern_support = "rootOccurrences" + "," + str(support) + "," + str(wsupport) + "," + str(size) + "\t" + str(pat_string)  # keeping for XML output
        self.__common_output_patterns_dict[str(pat_list)] = pattern_support

    def output_mfp(self, maximal_patterns_dict, out_file):
        """
         * filter and print maximal patterns
         * @param: maximalPatterns_dict, dictionary with String as keys and values
         * @param: outFile, String
        """
        try:
            with open(out_file + ".txt", "w+", encoding='utf-8') as output_common_patterns:
                # output maximal patterns
                output_maximal_patterns = XMLOutput(out_file, self.__config, self.__grammar_dict, self.__xml_characters_dict)
                for keys in maximal_patterns_dict:
                    output_maximal_patterns.printPattern(maximal_patterns_dict[keys])
                    output_common_patterns.write(keys + "\n")
                output_maximal_patterns.close()
                output_common_patterns.flush()
        except:
            print("error print maximal patterns " + str(sys.exc_info()[0]) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def init_database(self, patterns_dict):
        """
         * create transaction from list of patterns
         * @param: patterns_dict, dictionary with String as keys and values
        """
        read_file = ReadFile()
        read_file.createTransactionFromMap(patterns_dict, self.__new_transaction_list)

    @staticmethod
    def read_patterns(in_patterns):
        """
         * @param: inPatterns, String
         * @return a list of String
        """
        patterns_list = []  # list of String
        try:
            with open(in_patterns, 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    if len(line) != 0:
                        line = line.replace("\n", "")
                        patterns_list.append(line)
                    line = file.readline()
            file.close()
        except:
            print("Error: read_patterns function " + str(sys.exc_info()[0]))
            trace = traceback.format_exc()
            print(trace)
            raise
        return patterns_list

    @staticmethod
    def read_clusters(in_clusters):
        """
         * @param: inClusters, String
         * @return a list of list of String
        """
        temp_list = []  # list of list of Integer
        try:
            # read XML file
            doc = minidom.parse(in_clusters)
            doc.documentElement.normalize()

            # for each cluster ID, collect a list of pattern ID
            clusters_list = doc.documentElement.childNodes
            for i in range(len(clusters_list)):
                if clusters_list.item(i).nodeType == Node.ELEMENT_NODE:
                    patterns_list = clusters_list.item(i).childNodes
                    # for each patterns get the pattern ID
                    t_list = []  # list of Integer
                    for node in patterns_list:
                        if node.nodeType == Node.ELEMENT_NODE:
                            node_map = node.attributes
                            for k in range(len(node_map)):
                                if node_map.item(k).name == "ID":
                                    t_list.append(int(node_map.item(k).value))
                    temp_list.append(t_list)
        except:
            print("Error: read_clusters function " + str(sys.exc_info()[0]))
            trace = traceback.format_exc()
            print(trace)
            raise
        return temp_list
