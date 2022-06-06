#!/usr/bin/env python3
import traceback

from freqt.src.be.intimals.freqt.output.AoutFormatter import AOutputFormatter
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern
from freqt.src.be.intimals.freqt.structure.Projected import Projected

import sys


class XMLOutput(AOutputFormatter):
    __uniChar = u"\u00A5"

    """
     * @param: _file, String
     * @param: _config, Config
     * @param: _grammar_dict, dictionary with String as keys and a list of String as values
     * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
    """
    def __init__(self, _file, _config, _grammar_dict, _xml_characters_dict):
        super().__init__(_file, _config, _grammar_dict, _xml_characters_dict)
        self.pat_sup_map = None

    """
     * @param: _file, String
     * @param: _config, Config
     * @param: _grammar_dict, dictionary with String as keys and a list of String as values
     * @param: _xmlCharacters_dict, dictionary with String as keys and String as values
     * @param: _patSupMap_dict, dictionary with String as keys and String as values
    """
    def XMLOutput(self, _file, _config, _grammar_dict, _xml_characters_dict, _pat_sup_map):
        super().__init__(_file, _config, _grammar_dict, _xml_characters_dict)
        self.pat_sup_map = _pat_sup_map

    def openOutputFile(self):
        super().openOutputFile()
        self.out.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        self.out.write("<results>\n")

    def close(self):
        self.out.write("</results>\n")
        self.out.flush()
        self.out.close()

    def getNbPattern(self):
        super().getNbPattern()

    def checkOutputConstraint(self, pat):
        super().checkOutputConstraint(pat)

    def union(self, list1, list2):
        super().union(list1, list2)

    """
     * @param: _pat, String
    """
    def printPattern(self, _pat):
        pat_list = list()  # list of string
        try:
            patterns = Pattern()
            str_tmp = _pat.split("\t")
            supports = str_tmp[0].split(",")

            pattern = str_tmp[1].split(",")

            for i in range(len(pattern)):
                pat_list.append(pattern[i].strip())

            # remove right-path missed real leafs
            pat_list = patterns.removeMissingLeaf(pat_list)

            projected = Projected()
            projected.set_support(int(supports[1]))
            projected.set_root_support(int(supports[2]))

            self.report_Str(pat_list, projected)
        except:
            print("printPattern xml error : " + str(sys.exc_info()[0]) + "\n")
            print(traceback.format_exc())
            print(str(pat_list) + "\n")

    """
     * new report function to print pattern in the form of Integer
     * @param: pat_list, a list of String
     * @param: supports, a String
    """
    def report_Int(self, pat_list, supports):
        try:

            self.nb_pattern += 1
            pattern = Pattern()

            # keep meta-variables in pattern
            meta_variable_dict = {}  # dictionary with String as keys and Integer as values

            sup = supports.split(",")

            if self.config.get_2class():
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup[0]) +
                               "\" score=\"" + str(sup[1]) + "\" size=\"" + str(sup[2]) + "\">\n")
            else:
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup[0]) +
                               "\" wsupport=\"" + str(sup[1]) + "\" size=\"" + str(sup[2]) + "\">\n")

            # print pattern
            n = 0
            tmp_list = list()  # list of String
            # number of meta-variable ???
            for i in range(len(pat_list) - 1):
                # open a node
                if pat_list[i] != ")" and pat_list[i + 1] != ")":
                    node_order = self.grammar_dict[pat_list[i]][0]
                    node_degree = self.grammar_dict[pat_list[i]][1]
                    children_list = pattern.findChildrenLabels(pat_list, i)  # list of String

                    if node_order == "unordered":
                        if node_degree == "1":
                            if len(children_list) == 0:
                                meta_label = self.getMetaLabel(pat_list, meta_variable_dict, i)
                                self.out.write("<" + str(pat_list[i]) + ">\n")
                                self.out.write("<Dummy>\n")
                                self.out.write("<__directives>\n")
                                self.out.write("<optional />\n")
                                self.out.write("<meta-variable>\n")
                                self.out.write("<parameter key=\"name\" value=\"?" + str(meta_label) + "\"/>\n")
                                self.out.write("</meta-variable>\n")
                                self.out.write("</__directives>\n")
                                self.out.write("</Dummy>\n")
                            else:
                                self.out.write("<" + str(pat_list[i]) + ">\n")

                        elif node_degree == "1..*":
                            self.out.write("<" + str(pat_list[i]) + ">\n")
                            self.out.write("<__directives>")

                            # add new directive for nodes which have children directly follow each others
                            if pat_list[i] == "TheBlocks" and pat_list[i-1] == "SectionStatementBlock":
                                self.out.write("<match-succession/>")
                            else:
                                self.out.write("<match-sequence/>")

                            self.out.write("</__directives>\n")

                        else:
                            self.out.write("<" + str(pat_list[i]) + ">\n")
                    else:
                        if node_degree == "1":
                            if len(children_list) == 0:
                                meta_label = self.getMetaLabel(pat_list, meta_variable_dict, i)
                                self.out.write("<" + str(pat_list[i]) + ">\n")
                                self.out.write("<Dummy>\n")
                                self.out.write("<__directives>\n")
                                self.out.write("<optional />\n")
                                self.out.write("<meta-variable>\n")
                                self.out.write("<parameter key=\"name\" value=\"?" + str(meta_label) + "\"/>\n")
                                self.out.write("</meta-variable>\n")
                                self.out.write("</__directives>\n")
                                self.out.write("</Dummy>\n")

                            else:
                                self.out.write("<" + str(pat_list[i]) + ">\n")

                        else:  # N children: if this node has full children
                            self.out.write("<" + str(pat_list[i]) + ">\n")
                            self.out.write("<__directives>\n")
                            self.out.write("<match-sequence/>\n")
                            self.out.write("</__directives>\n")

                    tmp_list.append(pat_list[i])
                    n += 1
                else:
                    # print leaf node of subtree
                    if pat_list[i] != ")" and pat_list[i + 1] == ")":
                        # TODO: abstracting leafs of Cobol data
                        if pat_list[i][0] == '*':
                            self.outputLeaf(pat_list, i)
                        else:  # leaf of subtree is an internal node in the original tree
                            self.outputNode(pat_list, meta_variable_dict, i)
                    else:
                        # close a node
                        if pat_list[i] == ")" and pat_list[i + 1] == ")":
                            self.out.write("</" + str(tmp_list[n - 1]) + ">\n")
                            tmp_list.pop(n-1)
                            n -= 1

            # print the last node of pattern
            if pat_list[len(pat_list) - 1][0] == '*':
                self.outputLeaf(pat_list, len(pat_list) - 1)
            else:
                i = len(pat_list) - 1
                self.outputNode(pat_list, meta_variable_dict, i)

            # close nodes
            for i in range(n-1, -1, -1):
                self.out.write("</" + str(tmp_list[i]) + ">\n")

            self.out.write("</subtree>\n")

        except:
            print("report_Int xml error : " + str(sys.exc_info()[0]) + "\n")
            print(str(pat_list) + "\n")
            trace = traceback.format_exc()
            print(trace)

    """
     * print pattern
     * @param: pat_list, a list of String
     * @param: projected, Projected
    """
    def report_Str(self, pat_list, projected):
        try:
            self.nb_pattern += 1
            pattern = Pattern()

            # keep meta-variables in pattern
            meta_variable_dict = dict()  # dictionary with String as keys and Integer as values
            # print support, wsupport, size
            if self.config.post_process() and len(self.pat_sup_map) != 0:
                pat_temp = pattern.getPatternString(pat_list)
                sup = self.pat_sup_map[pat_temp].split(",")
                size = pattern.getPatternSize(pat_list)
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup[1]) +
                               "\" wsupport=\"" + str(sup[2]) + "\" size=\"" + str(size) + "\">\n")
            else:
                sup = projected.get_support()
                wsup = projected.get_root_support()
                size = pattern.getPatternSize(pat_list)
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup) +
                               "\" wsupport=\"" + str(wsup) + "\" size=\"" + str(size) + "\">\n")
            # print pattern
            n = 0
            tmp_list = list()  # list of String
            # number of meta-variable ???
            for i in range(len(pat_list) - 1):
                # open a node
                if pat_list[i] != ")" and pat_list[i + 1] != ")":

                    node_order = self.grammar_dict[pat_list[i]][0]
                    node_degree = self.grammar_dict[pat_list[i]][1]
                    children_list = pattern.findChildrenLabels(pat_list, i)  # list of String

                    if node_order == "unordered":
                        if node_degree == "1":
                            if len(children_list) == 0:
                                meta_label = self.getMetaLabel(pat_list, meta_variable_dict, i)
                                self.out.write("<" + str(pat_list[i]) + ">\n")
                                self.out.write("<Dummy>\n")
                                self.out.write("<__directives>\n")
                                self.out.write("<optional />\n")
                                self.out.write("<meta-variable>\n")
                                self.out.write("<parameter key=\"name\" value=\"?" + str(meta_label) + "\"/>\n")
                                self.out.write("</meta-variable>\n")
                                self.out.write("</__directives>\n")
                                self.out.write("</Dummy>\n")

                            else:
                                self.out.write("<" + str(pat_list[i]) + ">\n")

                        elif node_degree == "1..*":
                            self.out.write("<" + str(pat_list[i]) + ">\n")
                            self.out.write("<__directives>")

                            # add new directive for nodes which have children directly follow each others
                            if pat_list[i] == "TheBlocks" and pat_list[i-1] == "SectionStatementBlock":
                                self.out.write("<match-succession/>")
                            else:
                                self.out.write("<match-sequence/>")

                            self.out.write("</__directives>\n")

                        else:
                            self.out.write("<" + str(pat_list[i]) + ">\n")

                    else:
                        if node_degree == "1":
                            if len(children_list) == 0:
                                meta_label = self.getMetaLabel(pat_list, meta_variable_dict, i)
                                self.out.write("<" + str(pat_list[i]) + ">\n")
                                self.out.write("<Dummy>\n")
                                self.out.write("<__directives>\n")
                                self.out.write("<optional />\n")
                                self.out.write("<meta-variable>\n")
                                self.out.write("<parameter key=\"name\" value=\"?" + str(meta_label) + "\"/>\n")
                                self.out.write("</meta-variable>\n")
                                self.out.write("</__directives>\n")
                                self.out.write("</Dummy>\n")

                            else:
                                self.out.write("<" + str(pat_list[i]) + ">\n")

                        else:  # N children: if this node has full children
                            self.out.write("<" + str(pat_list[i]) + ">\n")
                            self.out.write("<__directives>\n")
                            self.out.write("<match-sequence/>\n")
                            self.out.write("</__directives>\n")

                    tmp_list.append(pat_list[i])
                    n += 1
                else:
                    # print leaf node of subtree
                    if pat_list[i] != ")" and pat_list[i + 1] == ")":
                        # TODO: abstracting leafs of Cobol data
                        if pat_list[i][0] == '*':
                            self.outputLeaf(pat_list, i)
                        else:  # leaf of subtree is an internal node in the original tree
                            self.outputNode(pat_list, meta_variable_dict, i)
                    else:
                        # close a node
                        if pat_list[i] == ")" and pat_list[i + 1] == ")":
                            self.out.write("</" + str(tmp_list[n - 1]) + ">\n")
                            tmp_list.pop(n-1)
                            n -= 1
            # print the last node of pattern
            if pat_list[len(pat_list) - 1][0] == '*':
                self.outputLeaf(pat_list, len(pat_list) - 1)
            else:
                i = len(pat_list) - 1
                self.outputNode(pat_list, meta_variable_dict, i)

            # close nodes
            for i in range(n-1, -1, -1):
                self.out.write("</" + str(tmp_list[i]) + ">\n")

            self.out.write("</subtree>\n")

        except:
            print("report_Str xml error : " + str(sys.exc_info()[0]) + "\n")
            print(traceback.format_exc())
            print(str(pat_list) + "\n")

    """
     * function use to print a leaf node
     * @param: pat_list, list of String
     * @param: i, Integer
    """
    def outputLeaf(self, pat_list, i):
        if self.config.get_abstract_leaves():
            self.out.write("<Dummy>\n")
            self.out.write("<__directives>\n")
            self.out.write("<optional />\n")
            self.out.write("<meta-variable>\n")
            self.out.write("<parameter key=\"name\" value=\"?" + str(pat_list[i-1]) + "\"/>\n")
            self.out.write("</meta-variable>\n")
            self.out.write("</__directives>\n")
            self.out.write("</Dummy>\n")
        else:
            for t in range(1, len(pat_list[i])):
                if str(pat_list[i][t]) in self.xml_characters_dict:
                    self.out.write(str(self.xml_characters_dict[str(pat_list[i][t])]))
                else:
                    self.out.write(str(pat_list[i][t]))
            self.out.write("\n")

    """
     * fuction use to print a node
     * @param: pat_list, a list of String
     * @param: meta_variable_dict, a dictionary with String as keys and Integer as values
     * @param: i, Integer
    """
    def outputNode(self, pat_list, meta_variable_dict, i):
        node_order = self.grammar_dict[pat_list[i]][0]
        node_degree = self.grammar_dict[pat_list[i]][1]
        if node_order == "unordered":
            if node_degree == "1":
                meta_label = self.getMetaLabel(pat_list, meta_variable_dict, i)

                self.out.write("<" + str(pat_list[i]) + ">\n")
                self.out.write("<Dummy>\n")
                self.out.write("<__directives>\n")
                self.out.write("<optional />\n")
                self.out.write("<meta-variable>\n")
                self.out.write("<parameter key=\"name\" value=\"?" + str(meta_label) + "\"/>\n")
                self.out.write("</meta-variable>\n")
                self.out.write("</__directives>\n")
                self.out.write("</Dummy>\n")
                self.out.write("</" + str(pat_list[i]) + ">\n")

            elif node_degree == "1..*":
                self.out.write("<" + str(pat_list[i]) + ">\n")
                self.out.write("<__directives>")

                if pat_list[i] == "TheBlocks" and pat_list[i-1] == "SectionStatementBlock":
                    self.out.write("<match-succession/>")
                else:
                    self.out.write("<match-sequence/>")

                self.out.write("</__directives>\n")
                self.out.write("</" + str(pat_list[i])+">\n")

            else:
                self.out.write("<" + str(pat_list[i]) + "/>\n")

        else:
            self.out.write("<" + str(pat_list[i]) + ">\n")
            self.out.write("<__directives>\n")
            self.out.write("<match-sequence/>\n")
            self.out.write("</__directives>\n")
            self.out.write("</" + str(pat_list[i]) + ">\n")
    """
     * return a String
     * @param: pat_list, list of String
     * @param: meta_variable_dict, dictionary with String as keys and Integer as values
     * @param: i, Integer
    """
    def getMetaLabel(self, pat_list, meta_variable_dict, i):
        if pat_list[i] in meta_variable_dict:
            meta_variable_dict[pat_list[i]] = meta_variable_dict[pat_list[i]] + 1
            meta_label = pat_list[i] + str(meta_variable_dict[pat_list[i]])
        else:
            meta_label = pat_list[i] + "1"
            meta_variable_dict[pat_list[i]] = 1
        return meta_label

    """
     * print Python pattern
     * @param: pat_list, list of string
     * @param; supports, String
    """
    def report_Py(self, pat_list, supports):
        try:
            # count number of output pattern
            self.nb_pattern += 1

            # print support
            sup = supports.split(",")
            if self.config.get_2class():
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup[0]) +
                               "\" score=\"" + str(sup[1]) + "\" size=\"" + str(sup[2]) + "\">\n")
            else:
                self.out.write("<subtree id=\"" + str(self.nb_pattern) + "\" support=\"" + str(sup[0]) +
                               "\" wsupport=\"" + str(sup[1]) + "\" size=\"" + str(sup[2]) + "\">\n")

            # print pattern
            n = 0
            tmp_list = list() # list of String
            for i in range(0, len(pat_list)):
                # open node
                if pat_list[i] != ")" and pat_list[i + 1] != ")":
                    self.out.write("<" + str(pat_list[i]) + ">\n")
                    tmp_list.append(pat_list[i])
                    n += 1
                else:
                    # print leaf node
                    if pat_list[i] != ")" and pat_list[i + 1] == ")":
                        self.out.write(pat_list[i][1:])
                    else:
                        # close node
                        if pat_list[i] == ")" and pat_list[i + 1] == ")":
                            self.out.write("</" + str(tmp_list[n - 1]) + ">\n")
                            tmp_list.pop(n-1)
                            n -= 1

            # print the last node of pattern
            self.out.write(pat_list[len(pat_list) - 1][1:])

            # close nodes
            for i in range(n-1, -1, -1):
                self.out.write("</" + str(tmp_list[i]) + ">\n")

            # close subtree
            self.out.write("</subtree>\n")
        except:
            print("report Python xml error : " + str(sys.exc_info()[0]) + "\n")
            print(str(pat_list) + "\n")
