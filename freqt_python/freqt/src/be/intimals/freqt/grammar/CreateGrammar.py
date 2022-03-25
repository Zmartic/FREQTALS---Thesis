#!/usr/bin/env python3
"""
create grammar for ASTs
"""
from freqt.src.be.intimals.freqt.input.ReadXMLInt import *
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR

from xml.dom import minidom
from xml.dom import Node
import os
import collections


def createGrammar(path, grammar_dict, white_labels):
    """
     * create grammar from multiple files
     * @param: f, string
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    subdir = [fi for fi in os.listdir(path) if os.path.isfile(os.path.join(path, fi))]
    subdir.sort()
    for i in range(len(subdir)):
        subdir[i] = path + '/' + subdir[i]
    for fi in subdir:
        if os.path.isfile(fi):
            if fi.endswith(".xml"):
                doc = minidom.parse(fi)
                doc.documentElement.normalize()
                # create grammar
                readGrammarDepthFirst(doc.documentElement, grammar_dict, white_labels)

    directories = [fi for fi in os.listdir(path) if os.path.isdir(os.path.join(path, fi))]
    for i in range(len(directories)):
        directories[i] = path + '/' + directories[i]
    for dir in directories:
        if os.path.isdir(dir):
            createGrammar(dir, grammar_dict, white_labels)


def readGrammarDepthFirst(node, grammar_dict, white_labels):
    """
     * recur reading an AST node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    try:
        # make sure it's element is a node type.
        if node.nodeType == Node.ELEMENT_NODE:
            if node.nodeName in grammar_dict:
                updateNode(node, grammar_dict, white_labels)
            else:
                addNewNode(node, grammar_dict, white_labels)

            if node.hasChildNodes():
                # get list of children
                nodeList = node.childNodes
                if node.nodeName in white_labels:
                    whiteChildren = white_labels[node.nodeName]
                    # loop for each child
                    for i in range(len(nodeList)):
                        if nodeList[i].nodeType == Node.ELEMENT_NODE:
                            if nodeList[i].nodeName in whiteChildren:
                                readGrammarDepthFirst(nodeList[i], grammar_dict, white_labels)
                else:
                    # loop for each child
                    for i in range(len(nodeList)):
                        if nodeList[i].nodeType == Node.ELEMENT_NODE:
                            readGrammarDepthFirst(nodeList[i], grammar_dict, white_labels)

    except:
        e = sys.exc_info()[0]
        print("Grammar error: " + str(e))
        trace = traceback.format_exc()
        print(trace)


def addNewNode(node, grammar_dict, white_labels):
    """
     * add a new node to grammar
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    nbChildren = count_children(node)
    childrenList = node.childNodes
    tmp_list = list()
    if nbChildren == 0:  # add leaf node
        if node.nodeType == Node.ELEMENT_NODE:
            tmp_list.append("ordered")
            tmp_list.append("1")
            # keep leaf node in grammar if necessary
            tmp_list.append("leaf-node" + UNICHAR + "false")
    else: # add internal node
        # 1 - find children
        childrenTemp_dict = collections.OrderedDict()  # ordered dictionary with Strong as keys and values
        # find children of the current node
        repeatedChild = isRepeatedChild(node, childrenList, childrenTemp_dict, white_labels)

        if repeatedChild:
            tmp_list.append("unordered")
            tmp_list.append("1..*")
            for key in childrenTemp_dict:
                tmp_list.append(key + UNICHAR + "false")
        else:
            tmp_list.append("ordered")
            tmp_list.append(str(len(childrenTemp_dict)))
            for key in childrenTemp_dict:
                tmp_list.append(key + UNICHAR + childrenTemp_dict[key])
    grammar_dict[node.nodeName] = tmp_list


def updateNode(node, grammar_dict, white_labels):
    """
     * update a node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    nbChildren = count_children(node)
    if nbChildren == 0:  # leaf node
        updateLeafNode(node, grammar_dict)
    else:  # internal node
        updateInternalNode(node, grammar_dict, white_labels)


def updateInternalNode(node, grammar_dict, white_labels):
    """
     * updating internal node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    # find grammar of this current node
    oldGrammar_list = grammar_dict[node.nodeName]
    oldDegree = oldGrammar_list[1]
    # find children of the current node in grammar
    oldChildren_dict = collections.OrderedDict()  # dictionary with String as keys and values
    for i in range(2, len(oldGrammar_list)):
        temp_list = oldGrammar_list[i].split(UNICHAR)
        oldChildren_dict[temp_list[0]] = temp_list[1]
    # find children of the current node
    childrenList_list = node.childNodes  # list of Node
    newChildren_dict = collections.OrderedDict()  # dictionary with String as keys and values
    repeatedChild = isRepeatedChild(node, childrenList_list, newChildren_dict, white_labels)

    tmp_list = list()  # list of String
    if repeatedChild:
        tmp_list.append("unordered")
        tmp_list.append("1..*")
        newChildren_dict.update(oldChildren_dict)
        for key in newChildren_dict:
            tmp_list.append(key + UNICHAR + "false")
    else:
        if len(newChildren_dict) == 1 and oldDegree == "1":
            tmp_list.append("ordered")
            tmp_list.append("1")
            newChildren_dict.update(oldChildren_dict)
            if len(newChildren_dict) > 1:
                for key in newChildren_dict:
                    tmp_list.append(key + UNICHAR + "false")
            else:
                for key in newChildren_dict:
                    tmp_list.append(key + UNICHAR + "true")
        else:
            if oldDegree == "1..*":
                tmp_list.append("unordered")
                tmp_list.append("1..*")
                newChildren_dict.update(oldChildren_dict)
                for key in newChildren_dict:
                    tmp_list.append(key + UNICHAR + "false")
            else:  # update grammar [unordered, N..M, list of children]
                # calculate intersection of old and new children
                inter = _inter(oldChildren_dict, newChildren_dict)  # dictionary with String as keys and values
                # calculate union of old and new children
                newChildren_dict.update(oldChildren_dict)
                tmp_list.append("ordered")
                if len(inter) != len(newChildren_dict):
                    tmp_list.append(str(len(inter)) + ".." + str(len(newChildren_dict)))
                    # update children
                    for key in newChildren_dict:
                        if key in inter:
                            tmp_list.append(key + UNICHAR + "true")
                        else:
                            tmp_list.append(key + UNICHAR + "false")
                else:
                    # update degree
                    tmp_list.append(str(len(inter)))
                    # update children
                    for key in newChildren_dict:
                        tmp_list.append(key + UNICHAR + newChildren_dict[key])
    grammar_dict[node.nodeName] = tmp_list


def isRepeatedChild(node, childrenList_list, childrenTemp_dict, white_labels):
    """
     * find children of a node
     * @param: node, Node
     * @param: childrenList_list, a list of Node
     * @param: childrenTemp_dict, dictionary with String as keys and values
    """
    repeatedChild = False
    if node.nodeName in white_labels:
        tmpChild_list = white_labels[node.nodeName]
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


def updateLeafNode(node, grammar_dict):
    """
     * update node having only leafs
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    tmp_list = list()  # list of String
    tmp_list.append("ordered")
    tmp_list.append("1")
    tmp_list.append("leaf-node" + UNICHAR + "false")
    grammar_dict[node.nodeName] = tmp_list


def _inter(oldChildren_dict, newChildren_dict):
    """
     * find intersection elements of two children lists
     * @param: oldChildren_dict, dictionary with String as keys and values
     * @param: newChildren_dict, dictionary with String as keys and values
    """
    inter = collections.OrderedDict()
    for key in oldChildren_dict:
        if key in newChildren_dict and oldChildren_dict[key] == "true":
            inter[key] = oldChildren_dict[key]
    return inter


### TMP to delete

def count_children(node):
    """
     * count number children of a node
     * @param node, a node
     * return the number of children of a given node
    """
    nb_children = 0
    for n in node.childNodes:
        if n.nodeType != Node.TEXT_NODE and n.nodeType == Node.ELEMENT_NODE:
            nb_children += 1
    return nb_children
