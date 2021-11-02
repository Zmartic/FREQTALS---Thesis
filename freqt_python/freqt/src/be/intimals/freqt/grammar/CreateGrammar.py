#!/usr/bin/env python3
"""
create grammar for ASTs
"""
from freqt.src.be.intimals.freqt.input.ReadXMLInt import *
from freqt.src.be.intimals.freqt.util.Variables import *

from xml.dom import minidom
from xml.dom import Node
import os
import collections


class CreateGrammar(ReadXMLInt):

    __whiteLabels_dict = dict()  # dictionary with String as keys and list of String as values

    """
     * constructor
     * @param: path, String
     * @param: white, String
     * @param: grammar_dict, dictionary with String as keys and list of String as grammar
    """
    def createGrammar(self, path, white, grammar_dict):
        self.__whiteLabels_dict = self.read_whiteLabel(white)
        self.createGrammar2(path, grammar_dict)

    """
     * create grammar from multiple files
     * @param: f, string
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def createGrammar2(self, f, grammar_dict):
        subdir = [fi for fi in os.listdir(f) if os.path.isfile(os.path.join(f, fi))]
        subdir.sort()
        for i in range(len(subdir)):
            subdir[i] = f + '/' + subdir[i]
        for fi in subdir:
            if os.path.isfile(fi):
                if fi.endswith(".xml"):
                    doc = minidom.parse(fi)
                    doc.documentElement.normalize()
                    # create grammar
                    self.readGrammarDepthFirst(doc.documentElement, grammar_dict)

        directories = [fi for fi in os.listdir(f) if os.path.isdir(os.path.join(f, fi))]
        for i in range(len(directories)):
            directories[i] = f + '/' + directories[i]
        for dir in directories:
            if os.path.isdir(dir):
                self.createGrammar2(dir, grammar_dict)


    """
     * recur reading an AST node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def readGrammarDepthFirst(self, node, grammar_dict):
        try:
            # make sure it's element is a node type.
            if node.nodeType == Node.ELEMENT_NODE:
                if node.nodeName in grammar_dict:
                    self.updateNode(node, grammar_dict)
                else:
                    self.addNewNode(node, grammar_dict)

                if node.hasChildNodes():
                    # get list of children
                    nodeList = node.childNodes
                    if node.nodeName in self.__whiteLabels_dict:
                        whiteChildren = self.__whiteLabels_dict[node.nodeName]
                        # loop for each child
                        for i in range(len(nodeList)):
                            if nodeList[i].nodeType == Node.ELEMENT_NODE:
                                if nodeList[i].nodeName in whiteChildren:
                                    self.readGrammarDepthFirst(nodeList[i], grammar_dict)
                    else:
                        # loop for each child
                        for i in range(len(nodeList)):
                            if nodeList[i].nodeType == Node.ELEMENT_NODE:
                                self.readGrammarDepthFirst(nodeList[i], grammar_dict)

        except:
            e = sys.exc_info()[0]
            print("Grammar error: " + str(e))
            trace = traceback.format_exc()
            print(trace)

    """
     * add a new node to grammar
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def addNewNode(self, node, grammar_dict):
        variables = Variables()
        nbChildren = self.count_children(node)
        childrenList = node.childNodes
        tmp_list = list()
        if nbChildren == 0:  # add leaf node
            if node.nodeType == Node.ELEMENT_NODE:
                tmp_list.append("ordered")
                tmp_list.append("1")
                # keep leaf node in grammar if necessary
                tmp_list.append("leaf-node" + variables.uniChar + "false")
        else: # add internal node
            # 1 - find children
            childrenTemp_dict = collections.OrderedDict()  # ordered dictionary with Strong as keys and values
            # find children of the current node
            repeatedChild = self.isRepeatedChild(node, childrenList, childrenTemp_dict)

            if repeatedChild:
                tmp_list.append("unordered")
                tmp_list.append("1..*")
                for key in childrenTemp_dict:
                    tmp_list.append(key + variables.uniChar + "false")
            else:
                tmp_list.append("ordered")
                tmp_list.append(str(len(childrenTemp_dict)))
                for key in childrenTemp_dict:
                    tmp_list.append(key + variables.uniChar + childrenTemp_dict[key])
        grammar_dict[node.nodeName] = tmp_list

    """
     * update a node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def updateNode(self, node, grammar_dict):
        nbChildren = self.count_children(node)
        if nbChildren == 0:  # leaf node
            self.updateLeafNode(node, grammar_dict)
        else:  # internal node
            self.updateInternalNode(node, grammar_dict)

    """
     * updating internal node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def updateInternalNode(self, node, grammar_dict):
        variables = Variables()
        # find grammar of this current node
        oldGrammar_list = grammar_dict[node.nodeName]
        oldDegree = oldGrammar_list[1]
        # find children of the current node in grammar
        oldChildren_dict = collections.OrderedDict()  # dictionary with String as keys and values
        for i in range(2, len(oldGrammar_list)):
            temp_list = oldGrammar_list[i].split(variables.uniChar)
            oldChildren_dict[temp_list[0]] = temp_list[1]
        # find children of the current node
        childrenList_list = node.childNodes  # list of Node
        newChildren_dict = collections.OrderedDict()  # dictionary with String as keys and values
        repeatedChild = self.isRepeatedChild(node, childrenList_list, newChildren_dict)

        tmp_list = list()  # list of String
        if repeatedChild:
            tmp_list.append("unordered")
            tmp_list.append("1..*")
            newChildren_dict.update(oldChildren_dict)
            for key in newChildren_dict:
                tmp_list.append(key + variables.uniChar + "false")
        else:
            if len(newChildren_dict) == 1 and oldDegree == "1":
                tmp_list.append("ordered")
                tmp_list.append("1")
                newChildren_dict.update(oldChildren_dict)
                if len(newChildren_dict) > 1:
                    for key in newChildren_dict:
                        tmp_list.append(key + variables.uniChar + "false")
                else:
                    for key in newChildren_dict:
                        tmp_list.append(key + variables.uniChar + "true")
            else:
                if oldDegree == "1..*":
                    tmp_list.append("unordered")
                    tmp_list.append("1..*")
                    newChildren_dict.update(oldChildren_dict)
                    for key in newChildren_dict:
                        tmp_list.append(key + variables.uniChar + "false")
                else:  # update grammar [unordered, N..M, list of children]
                    # calculate intersection of old and new children
                    inter = self.inter(oldChildren_dict, newChildren_dict)  # dictionary with String as keys and values
                    # calculate union of old and new children
                    newChildren_dict.update(oldChildren_dict)
                    tmp_list.append("ordered")
                    if len(inter) != len(newChildren_dict):
                        tmp_list.append(str(len(inter)) + ".." + str(len(newChildren_dict)))
                        # update children
                        for key in newChildren_dict:
                            if key in inter:
                                tmp_list.append(key + variables.uniChar + "true")
                            else:
                                tmp_list.append(key + variables.uniChar + "false")
                    else:
                        # update degree
                        tmp_list.append(str(len(inter)))
                        # update children
                        for key in newChildren_dict:
                            tmp_list.append(key + variables.uniChar + newChildren_dict[key])
        grammar_dict[node.nodeName] = tmp_list

    """
     * find children of a node
     * @param: node, Node
     * @param: childrenList_list, a list of Node
     * @param: childrenTemp_dict, dictionary with String as keys and values
    """
    def isRepeatedChild(self, node, childrenList_list, childrenTemp_dict):
        repeatedChild = False
        if node.nodeName in self.__whiteLabels_dict:
            tmpChild_list = self.__whiteLabels_dict[node.nodeName]
            for i in range(len(childrenList_list)):
                if childrenList_list[i].nodeType == Node.ELEMENT_NODE:
                    if childrenList_list[i].nodeName in tmpChild_list:
                        if childrenList_list[i].nodeName in childrenTemp_dict:
                            childrenTemp_dict[childrenList_list[i].nodeName] = "false"
                            repeatedChild = True
                        else:
                            childrenTemp_dict[childrenList_list[i].nodeName] = "true"

        else:
            for i in range(len(childrenList_list)):
                if childrenList_list[i].nodeType == Node.ELEMENT_NODE:
                    if childrenList_list[i].nodeName in childrenTemp_dict:
                        childrenTemp_dict[childrenList_list[i].nodeName] = "false"
                        repeatedChild = True
                    else:
                        childrenTemp_dict[childrenList_list[i].nodeName] = "true"
        return repeatedChild

    """
     * update node having only leafs
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    def updateLeafNode(self, node, grammar_dict):
        variables = Variables()
        tmp_list = list()  # list of String
        tmp_list.append("ordered")
        tmp_list.append("1")
        tmp_list.append("leaf-node" + variables.uniChar + "false")
        grammar_dict[node.nodeName] = tmp_list

    """
     * find intersection elements of two children lists
     * @param: oldChildren_dict, dictionary with String as keys and values
     * @param: newChildren_dict, dictionary with String as keys and values
    """
    def inter(self, oldChildren_dict, newChildren_dict):
        inter = collections.OrderedDict()
        for key in oldChildren_dict:
            if key in newChildren_dict and oldChildren_dict[key] == "true":
                inter[key] = oldChildren_dict[key]
        return inter
