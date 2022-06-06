#!/usr/bin/env python3
import collections
import sys
from xml.dom import Node, minidom

from freqt.src.be.intimals.freqt.util.Variables import UNICHAR


def readAttribute1(child, grammar_dict):
    """
     * return a String
     * @param: child, Node
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    # add this child to grammar
    mandatory = "true"
    tmp_list = []  # list of String without repetition
    node_map_child = child.attributes  # get attributes
    for index in range(len(node_map_child)):  # for each attribute
        n = node_map_child.item(index)
        if n.name == "mandatory":
            mandatory = str(n.value)
        elif n.name == "node":  # a node has many values
            # if the previous degree is 1..* ?
            if child.nodeName in grammar_dict:
                if grammar_dict[child.nodeName][1] == "1..*":
                    if grammar_dict[child.nodeName][0] not in tmp_list:
                        tmp_list.append(grammar_dict[child.nodeName][0])
                    if grammar_dict[child.nodeName][1] not in tmp_list:
                        tmp_list.append(grammar_dict[child.nodeName][1])
                else:
                    if "unordered" not in tmp_list:
                        tmp_list.append("unordered")
                    if "1" not in tmp_list:
                        tmp_list.append("1")
            else:
                if "unordered" not in tmp_list:
                    tmp_list.append("unordered")
                if "1" not in tmp_list:
                    tmp_list.append("1")
            if child.nodeName in grammar_dict:
                for i in range(2, len(grammar_dict[child.nodeName])):
                    if grammar_dict[child.nodeName][i] not in tmp_list:
                        tmp_list.append(grammar_dict[child.nodeName][i])
            if n.value + UNICHAR + "false" not in tmp_list:
                tmp_list.append(n.value + UNICHAR + "false")
            grammar_dict[child.nodeName] = tmp_list
        elif n.name == "ordered-nodelist":
            if "ordered" not in tmp_list:
                tmp_list.append("ordered")
            if "1..*" not in tmp_list:
                tmp_list.append("1..*")
            if child.nodeName in grammar_dict:
                for i in range(2, len(grammar_dict[child.nodeName])):
                    if grammar_dict[child.nodeName][i] not in tmp_list:
                        tmp_list.append(grammar_dict[child.nodeName][i])
            if n.value + UNICHAR + "false" not in tmp_list:
                tmp_list.append(n.value + UNICHAR + "false")
            grammar_dict[child.nodeName] = tmp_list

        elif n.name == "unordered-nodelist":
            if "unordered" not in tmp_list:
                tmp_list.append("unordered")
            if "1..*" not in tmp_list:
                tmp_list.append("1..*")
            if child.nodeName in grammar_dict:
                for i in range(2, len(grammar_dict[child.nodeName])):
                    if grammar_dict[child.nodeName][i] not in tmp_list:
                        tmp_list.append(grammar_dict[child.nodeName][i])
            if n.value + UNICHAR + "false" not in tmp_list:
                tmp_list.append(n.value + UNICHAR + "false")
            grammar_dict[child.nodeName] = tmp_list

        elif n.name == "simplevalue":
            if "unordered" not in tmp_list:
                tmp_list.append("unordered")
            if "1" not in tmp_list:
                tmp_list.append("1")
            if n.value + UNICHAR + "false" not in tmp_list:
                tmp_list.append(n.value + UNICHAR + "false")
                grammar_dict[child.nodeName] = tmp_list
    return mandatory


def addAttribute(child, abstract_nodes_dict, grammar_dict):
    """
     * @param: child, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    node_map = child.attributes  # get attributes
    tmp_list = []  # list of string without repetition
    for j in range(len(node_map)):  # for each attribute
        n = node_map.item(j)
        if n.name == "node":
            if "unordered" not in tmp_list:
                tmp_list.append("unordered")
            if "1" not in tmp_list:
                tmp_list.append("1")
            if n.value in abstract_nodes_dict:
                for i in range(len(abstract_nodes_dict)):
                    if abstract_nodes_dict[n.value][i] not in tmp_list:
                        tmp_list.append(abstract_nodes_dict[n.value][i])
                grammar_dict[child.nodeName] = tmp_list.copy()
            else:
                if n.value + UNICHAR + "false" not in tmp_list:
                    tmp_list.append(n.value + UNICHAR + "false")
                grammar_dict[child.nodeName] = tmp_list.copy()

        if n.name == "ordered-nodelist":
            if "ordered" not in tmp_list:
                tmp_list.append("ordered")
            if "1..*" not in tmp_list:
                tmp_list.append("1..*")
            if n.value in abstract_nodes_dict:
                for i in range(len(abstract_nodes_dict[n.value])):
                    if abstract_nodes_dict[n.value][i] not in tmp_list:
                        tmp_list.append(abstract_nodes_dict[n.value][i])
                grammar_dict[child.nodeName] = tmp_list.copy()
            else:
                if n.value + UNICHAR + "false" not in tmp_list:
                    tmp_list.append(n.value + UNICHAR + "false")
                grammar_dict[child.nodeName] = tmp_list.copy()

        if n.name == "unordered-nodelist":
            if "unordered" not in tmp_list:
                tmp_list.append("unordered")
            if "1..*" not in tmp_list:
                tmp_list.append("1..*")
            if n.value in abstract_nodes_dict:
                for i in range(len(abstract_nodes_dict[n.value])):
                    if abstract_nodes_dict[n.value][i] not in tmp_list:
                        tmp_list.append(abstract_nodes_dict[n.value][i])
                grammar_dict[child.nodeName] = tmp_list.copy()
            else:
                if n.value + UNICHAR + "false" not in tmp_list:
                    tmp_list.append(n.value + UNICHAR + "false")
                grammar_dict[child.nodeName] = tmp_list.copy()

        if n.name == "simplevalue":
            if "unordered" not in tmp_list:
                tmp_list.append("unordered")
            if "1" not in tmp_list:
                tmp_list.append("1")
            if n.value not in tmp_list:
                tmp_list.append(n.value)
            grammar_dict[child.nodeName] = tmp_list.copy()


def updateAttribute(child, abstract_nodes_dict, grammar_dict):
    """
     * @param: child, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    # check if old children == new children
    old_children_list = grammar_dict[child.nodeName].copy()  # list without repetition

    node_map = child.attributes  # get attributes
    new_children_list = []  # list without repetition

    for j in range(len(node_map)):  # for each attribute
        n = node_map.item(j)
        if n.value in abstract_nodes_dict:
            for i in range(len(abstract_nodes_dict[n.value])):
                if abstract_nodes_dict[n.value][i] not in new_children_list:
                    new_children_list.append(abstract_nodes_dict[n.value][i])
        else:
            if n.name in ["node","ordered-nodelist","unordered-nodelist"]:
                if n.value + UNICHAR + "false" not in new_children_list:
                    new_children_list.append(n.value + UNICHAR + "false")
    for elem in new_children_list:
        if elem not in old_children_list:
            old_children_list.append(new_children_list)
    grammar_dict[child.nodeName] = old_children_list.copy()


def readAttribute(child, abstract_nodes_dict, grammar_dict):
    """
     * add a child of AST or Synthetic node to grammar
     * @param: child, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    if child.nodeName in grammar_dict:
        updateAttribute(child, abstract_nodes_dict, grammar_dict)
    else:
        addAttribute(child, abstract_nodes_dict, grammar_dict)


def readMandatoryAttribute(child):
    """
     * @param: child, Node
    """
    mandatory = "true"
    node_map = child.attributes  # get attributes
    for j in range(len(node_map)):  # for each attribute
        n = node_map.item(j)
        if n.name == "mandatory":
            mandatory = str(n.value)
    return mandatory


def findIndex(node, grammar_dict):
    """
     * @param: node, String
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    index = 0
    key_set = grammar_dict.keys()  # list des keys can't contain repetition
    for s in key_set:
        ss = s.split(UNICHAR)
        if ss[0] == node:
            if len(ss) == 2:
                index = int(ss[1]) + 1
    if index > 1:
        return index
    return 1


def readAbstractNodes(root):
    """
     * find add abstract node in grammar
     * @param: root, Node
     * @return a dictionary with String as keys and list of String as values
    """
    abstract_nodes_dict = collections.OrderedDict()  # dictionary with String as keys and list of String as values
    try:
        children_nodes_list = root.childNodes
        for child in children_nodes_list:  # for each abstract node
            if child.hasAttributes() and child.hasChildNodes() and child.nodeType == Node.ELEMENT_NODE:
                node_map = child.attributes
                for j in range(len(node_map)):  # check if a node is abstract
                    node = node_map.item(j)
                    if node.name == "abstract" and str(node.value) == "true":
                        tmp1_list = []  # list of String
                        children_list = child.childNodes
                        for k_child in children_list:  # for each child of Abstract
                            if k_child.nodeType == Node.ELEMENT_NODE:
                                if child.nodeName not in abstract_nodes_dict:
                                    tmp1_list.append(k_child.nodeName + UNICHAR + "false")
                                    abstract_nodes_dict[child.nodeName] = tmp1_list
                                else:
                                    abstract_nodes_dict[child.nodeName].append(k_child.nodeName + UNICHAR + "false")
    except:
        print("read abstract nodes error " + str(sys.exc_info()[0]))
    return abstract_nodes_dict


def readSyntheticNodes(root, abstract_nodes_dict, grammar_dict):
    """
     * find all synthetic node in grammar
     * @param: root, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
     * @return a dictionary with String as keys and list of String as values
    """
    # find abstract/synthetic nodes
    synthetic_nodes_dict = collections.OrderedDict()  # dictionary with String as keys and list of String as values
    children_nodes_list = root.childNodes
    for child in children_nodes_list:  # for each node
        if child.hasAttributes() and child.nodeType == Node.ELEMENT_NODE:
            node_map = child.attributes
            for node in node_map:  # check if a node i is synthetic
                if node.name == "synthetic" and str(node.value) == "true":
                    # find all children of synthetic node i
                    synthetic_children_set = set()  # list without repetition
                    children_list = child.childNodes
                    for k in range(len(children_list)):  # for each child of Synthetic node
                        if children_list[k].nodeType == Node.ELEMENT_NODE:
                            mandatory = readMandatoryAttribute(children_list[k])
                            if children_list[k].nodeName + UNICHAR + mandatory not in synthetic_children_set:
                                synthetic_children_set.add(children_list[k].nodeName + UNICHAR + mandatory)
                            readAttribute(children_list[k], abstract_nodes_dict, grammar_dict)

                    if child.nodeName in synthetic_nodes_dict:
                        # find the index of rule, # create new synthetic rule
                        index = findIndex(child.nodeName, synthetic_nodes_dict)
                        synthetic_nodes_dict[child.nodeName + UNICHAR + str(index)] = list(synthetic_children_set.copy())
                    else:
                        synthetic_nodes_dict[child.nodeName] = list(synthetic_children_set.copy())
    return synthetic_nodes_dict


def checkSyntheticNode(node):
    """
     * @param: node, Node
    """
    synthetic = False
    children_nodes_list = node.childNodes
    for child in children_nodes_list:
        if child.hasAttributes() and child.nodeType == Node.ELEMENT_NODE:
            adhoc = child.nodeName.split("_")
            if adhoc[0] == "Adhoc":
                synthetic = True
    return synthetic


def readSimpleNode(node, abstract_nodes_dict, grammar_dict):
    """
     * @param: node, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    children_tmp_list = []  # list without repetition # find all its children
    children_list = node.childNodes  # create grammar for each child

    for child in children_list:
        if child.hasAttributes() and child.nodeType == Node.ELEMENT_NODE:
            mandatory = readMandatoryAttribute(child)
            current_child_label = child.nodeName
            if current_child_label + UNICHAR + str(mandatory) not in children_tmp_list:
                children_tmp_list.append(current_child_label + UNICHAR + str(mandatory))
            readAttribute(child, abstract_nodes_dict, grammar_dict)
    # add the current node to grammar
    if len(children_tmp_list) != 0:
        children_tmp_vector_list = children_tmp_list.copy()
        children_tmp_vector_list.insert(0, "unordered")
        children_tmp_vector_list.insert(1, str(len(children_tmp_vector_list) - 1))
        # if this node exists in grammar then increase index
        if node.nodeName in grammar_dict:
            index = findIndex(node.nodeName, grammar_dict)
            grammar_dict[node.nodeName + UNICHAR + str(index)] = children_tmp_vector_list.copy()
        else:
            grammar_dict[node.nodeName] = children_tmp_vector_list.copy()


def getRules(label, maps_dict):
    """
     * @param: label, String
     * @param: maps_dict, dictionary with String as keys and list of String as values
     * return a dictionary with String as keys and list of String as values
    """
    rules = collections.OrderedDict()  # dictionary with String as keys and list of String as values
    key_list = maps_dict.keys()  # list of keys (a keys is unique)
    for s in key_list:
        ss = s.split(UNICHAR)
        if ss[0] == label:
            rules[s] = maps_dict[s].copy()

    return rules


def readSpecialNode(node, synthetic_nodes_dict, grammar_dict):
    """
     * @param: node, Node
     * @param: synthetic_nodes_dict, dictionary with String as keys and list of String as value
     * @param: grammar_dict, dictionary with String as keys and list of String as value
    """
    # get the set of children
    children_nodes_list = node.childNodes
    # find normal children
    # find set of rules of each synthetic node, example: WhiteStatement has 2 synthetic nodes
    normal_children_list = []  # list of String
    synthetic_children_dict = collections.OrderedDict()  # dictionary with String as keys and a dictionary as values with String as keys and list of String as values
    for child in children_nodes_list:
        if child.hasAttributes() and child.nodeType == Node.ELEMENT_NODE:
            adhoc = child.nodeName.split("_")
            if adhoc[0] == "Adhoc":  # synthetic child
                synthetic_label = ""
                for j in range(1, len(adhoc) - 1):
                    synthetic_label = synthetic_label + adhoc[j] + "_"
                synthetic_label = synthetic_label + adhoc[adhoc.length - 1]

                synthetic_children_dict[child.nodeName] = getRules(synthetic_label, synthetic_nodes_dict)
            else:  # normal child
                mandatory = readMandatoryAttribute(child)
                normal_children_list.append(child.nodeName + UNICHAR + mandatory)

    # create all cases of synthetic nodes,
    # i.e, node A has 3 synthetic child, and
    # synthetic child 1 has 2 cases
    # synthetic child 2 has 3 cases
    # synthetic child 3 has 4 cases
    # --> total how many combinations ? --> for each case create one rule
    # how to know mandatory of these children

    # combine allChildren = normalChild + each item in syntheticChild
    size = len(synthetic_children_dict)
    index = 0
    if size == 1:  # node has only one synthetic child
        for key1 in synthetic_children_dict:
            # for each rule of synthetic node create a rule in grammar
            for key2 in synthetic_children_dict[key1]:
                all_children_list = normal_children_list.copy()  # list of String
                for elem in synthetic_children_dict[key1][key2]:
                    all_children_list.append(elem)
                # create one rule in grammar
                all_children_list.insert(0, "unordered")
                all_children_list.insert(1, str(len(all_children_list) - 1))
                if index == 0:
                    grammar_dict[node.nodeName] = all_children_list.copy()
                else:
                    grammar_dict[node.nodeName + UNICHAR + str(index)] = all_children_list.copy()
                index += 1


def readASTNodes(root, abstract_nodes_dict, synthetic_nodes_dict, grammar_dict):
    """
     * find all AST node in grammar
     * @param: root, Node
     * @param: abstract_nodes_dict, dictionary with String as keys and list of String as values
     * @param: synthetic_nodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    children_nodes_list = root.childNodes
    for child in children_nodes_list:  # for each child (AST node)
        # if it is not abstract and not synthetic node and it has children
        if not child.hasAttributes() and child.hasChildNodes() and child.nodeType == Node.ELEMENT_NODE:
            if checkSyntheticNode(child):
                readSpecialNode(child, synthetic_nodes_dict, grammar_dict)
            else:
                readSimpleNode(child, abstract_nodes_dict, grammar_dict)


def readGrammar(path, grammar):
    """
     * create grammar from file
     * @param: path, String
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    try:
        # for each file in folder create one tree
        doc = minidom.parse(path)
        doc.documentElement.normalize()

        root = doc.documentElement
        abstract_nodes_dict = readAbstractNodes(root)  # dictionary with String as keys and list of String as values
        synthetic_nodes_dict = readSyntheticNodes(root, abstract_nodes_dict, grammar)  # dictionary with String as keys and list of String as values
        readASTNodes(root, abstract_nodes_dict, synthetic_nodes_dict, grammar)

    except:
        print("read grammar file error " + str(sys.exc_info()[0]))
