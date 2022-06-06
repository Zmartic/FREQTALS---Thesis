#!/usr/bin/env python3
"""
create grammar for ASTs
"""
import sys
import traceback
from xml.dom import Node, minidom
import os
import collections

from freqt.src.be.intimals.freqt.util.Variables import UNICHAR


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
    for file in subdir:
        if os.path.isfile(file):
            if file.endswith(".xml"):
                doc = minidom.parse(file)
                doc.documentElement.normalize()
                # create grammar
                readGrammarDepthFirst(doc.documentElement, grammar_dict, white_labels)

    directories = [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]
    for i in range(len(directories)):
        directories[i] = path + '/' + directories[i]
    for directory in directories:
        if os.path.isdir(directory):
            createGrammar(directory, grammar_dict, white_labels)


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
                node_list = node.childNodes
                if node.nodeName in white_labels:
                    white_children = white_labels[node.nodeName]
                    # loop for each child
                    for child in node_list:
                        if child.nodeType == Node.ELEMENT_NODE:
                            if child.nodeName in white_children:
                                readGrammarDepthFirst(child, grammar_dict, white_labels)
                else:
                    # loop for each child
                    for child in node_list:
                        if child.nodeType == Node.ELEMENT_NODE:
                            readGrammarDepthFirst(child, grammar_dict, white_labels)

    except:
        print("Grammar error: " + str(sys.exc_info()[0]))
        trace = traceback.format_exc()
        print(trace)


def addNewNode(node, grammar_dict, white_labels):
    """
     * add a new node to grammar
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    tmp_list = []
    if count_children(node) == 0:  # add leaf node
        if node.nodeType == Node.ELEMENT_NODE:
            tmp_list.append("ordered")
            tmp_list.append("1")
            # keep leaf node in grammar if necessary
            tmp_list.append("leaf-node" + UNICHAR + "false")
    else:  # add internal node
        # 1 - find children
        children_temp_dict = collections.OrderedDict()  # ordered dictionary with Strong as keys and values
        # find children of the current node
        repeated_child = isRepeatedChild(node, node.childNodes, children_temp_dict, white_labels)

        if repeated_child:
            tmp_list.append("unordered")
            tmp_list.append("1..*")
            for key in children_temp_dict:
                tmp_list.append(key + UNICHAR + "false")
        else:
            tmp_list.append("ordered")
            tmp_list.append(str(len(children_temp_dict)))
            for key in children_temp_dict:
                tmp_list.append(key + UNICHAR + children_temp_dict[key])
    grammar_dict[node.nodeName] = tmp_list


def updateNode(node, grammar_dict, white_labels):
    """
     * update a node
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    if count_children(node) == 0:  # leaf node
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
    old_grammar_list = grammar_dict[node.nodeName]
    old_degree = old_grammar_list[1]
    # find children of the current node in grammar
    old_children_dict = collections.OrderedDict()  # dictionary with String as keys and values
    for i in range(2, len(old_grammar_list)):
        temp_list = old_grammar_list[i].split(UNICHAR)
        old_children_dict[temp_list[0]] = temp_list[1]
    # find children of the current node
    children_list = node.childNodes  # list of Node
    new_children_dict = collections.OrderedDict()  # dictionary with String as keys and values
    repeated_child = isRepeatedChild(node, children_list, new_children_dict, white_labels)

    tmp_list = []  # list of String
    if repeated_child:
        tmp_list.append("unordered")
        tmp_list.append("1..*")
        new_children_dict.update(old_children_dict)
        for key in new_children_dict:
            tmp_list.append(key + UNICHAR + "false")
    else:
        if len(new_children_dict) == 1 and old_degree == "1":
            tmp_list.append("ordered")
            tmp_list.append("1")
            new_children_dict.update(old_children_dict)
            if len(new_children_dict) > 1:
                for key in new_children_dict:
                    tmp_list.append(key + UNICHAR + "false")
            else:
                for key in new_children_dict:
                    tmp_list.append(key + UNICHAR + "true")
        else:
            if old_degree == "1..*":
                tmp_list.append("unordered")
                tmp_list.append("1..*")
                new_children_dict.update(old_children_dict)
                for key in new_children_dict:
                    tmp_list.append(key + UNICHAR + "false")
            else:  # update grammar [unordered, N..M, list of children]
                # calculate intersection of old and new children
                inter = _inter(old_children_dict, new_children_dict)  # dictionary with String as keys and values
                # calculate union of old and new children
                new_children_dict.update(old_children_dict)
                tmp_list.append("ordered")
                if len(inter) != len(new_children_dict):
                    tmp_list.append(str(len(inter)) + ".." + str(len(new_children_dict)))
                    # update children
                    for key in new_children_dict:
                        if key in inter:
                            tmp_list.append(key + UNICHAR + "true")
                        else:
                            tmp_list.append(key + UNICHAR + "false")
                else:
                    # update degree
                    tmp_list.append(str(len(inter)))
                    # update children
                    for key in new_children_dict:
                        tmp_list.append(key + UNICHAR + new_children_dict[key])
    grammar_dict[node.nodeName] = tmp_list


def isRepeatedChild(node, children_list, children_temp_dict, white_labels):
    """
     * find children of a node
     * @param: node, Node
     * @param: childrenList_list, a list of Node
     * @param: childrenTemp_dict, dictionary with String as keys and values
    """
    repeated_child = False
    if node.nodeName in white_labels:
        tmp_child_list = white_labels[node.nodeName]
        for child in children_list:
            if child.nodeType == Node.ELEMENT_NODE:
                if child.nodeName in tmp_child_list:
                    if child.nodeName in children_temp_dict:
                        children_temp_dict[child.nodeName] = "false"
                        repeated_child = True
                    else:
                        children_temp_dict[child.nodeName] = "true"

    else:
        for child in children_list:
            if child.nodeType == Node.ELEMENT_NODE:
                if child.nodeName in children_temp_dict:
                    children_temp_dict[child.nodeName] = "false"
                    repeated_child = True
                else:
                    children_temp_dict[child.nodeName] = "true"
    return repeated_child


def updateLeafNode(node, grammar_dict):
    """
     * update node having only leafs
     * @param: node, Node
     * @param: grammar_dict, dictionary with String as keys and list of string as values
    """
    tmp_list = []  # list of String
    tmp_list.append("ordered")
    tmp_list.append("1")
    tmp_list.append("leaf-node" + UNICHAR + "false")
    grammar_dict[node.nodeName] = tmp_list


def _inter(old_children_dict, new_children_dict):
    """
     * find intersection elements of two children lists
     * @param: old_children_dict, dictionary with String as keys and values
     * @param: new_children_dict, dictionary with String as keys and values
    """
    inter = collections.OrderedDict()
    for key in old_children_dict:
        if key in new_children_dict and old_children_dict[key] == "true":
            inter[key] = old_children_dict[key]
    return inter


### TMP to delete

def count_children(node):
    """
     * count number children of a node
     * @param node, a node
     * return the number of children of a given node
    """
    nb_children = 0
    for child in node.childNodes:
        if child.nodeType != Node.TEXT_NODE and child.nodeType == Node.ELEMENT_NODE:
            nb_children += 1
    return nb_children
