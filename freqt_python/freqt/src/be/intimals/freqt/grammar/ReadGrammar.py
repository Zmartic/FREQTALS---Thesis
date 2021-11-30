#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.input.ReadXMLInt import *
from freqt.src.be.intimals.freqt.util.Variables import *

from xml.dom import minidom
from xml.dom import Node
import collections


class ReadGrammar(ReadXMLInt):

    """
     * return a String
     * @param: child, Node
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def readAttribute1(self, child, grammar_dict):
        # add this child to grammar
        mandatory = "true"
        tmp_list = list()  # list of String without repetition
        nodeMapChild = child.attributes  # get attributes
        for l in range(len(nodeMapChild)):  # for each attribute
            n = nodeMapChild.item(l)
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

    """
     * @param: child, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def addAttribute(self, child, abstractNodes_dict, grammar_dict):
        nodeMap = child.attributes  # get attributes
        tmp_list = list()  # list of string without repetition
        for j in range(len(nodeMap)):  # for each attribute
            n = nodeMap.item(j)
            if n.name == "node":
                if "unordered" not in tmp_list:
                    tmp_list.append("unordered")
                if "1" not in tmp_list:
                    tmp_list.append("1")
                if n.value in abstractNodes_dict:
                    for i in range(len(abstractNodes_dict)):
                        if abstractNodes_dict[n.value][i] not in tmp_list:
                            tmp_list.append(abstractNodes_dict[n.value][i])
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
                if n.value in abstractNodes_dict:
                    for i in range(len(abstractNodes_dict[n.value])):
                        if abstractNodes_dict[n.value][i] not in tmp_list:
                            tmp_list.append(abstractNodes_dict[n.value][i])
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
                if n.value in abstractNodes_dict:
                    for i in range(len(abstractNodes_dict[n.value])):
                        if abstractNodes_dict[n.value][i] not in tmp_list:
                            tmp_list.append(abstractNodes_dict[n.value][i])
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

    """
     * @param: child, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def updateAttribute(self, child, abstractNodes_dict, grammar_dict):
        # check if old children == new children
        oldChildren_list = grammar_dict[child.nodeName].copy()  # list without repetition

        nodeMap = child.attributes  # get attributes
        newChildren_list = list()  # list without repetition

        for j in range(len(nodeMap)):  # for each attribute
            n = nodeMap.item(j)
            if n.value in abstractNodes_dict:
                for i in range(len(abstractNodes_dict[n.value])):
                    if abstractNodes_dict[n.value][i] not in newChildren_list:
                        newChildren_list.append(abstractNodes_dict[n.value][i])
            else:
                if n.name == "node" or n.name == "ordered-nodelist" or n.name == "unordered-nodelist":
                    if n.value + UNICHAR + "false" not in newChildren_list:
                        newChildren_list.append(n.value + UNICHAR + "false")
        for elem in newChildren_list:
            if elem not in oldChildren_list:
                oldChildren_list.append(newChildren_list)
        grammar_dict[child.nodeName] = oldChildren_list.copy()


    """"
     * add a child of AST or Synthetic node to grammar
     * @param: child, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def readAttribute(self, child, abstractNodes_dict, grammar_dict):
        if child.nodeName in grammar_dict:
            self.updateAttribute(child, abstractNodes_dict, grammar_dict)
        else:
            self.addAttribute(child, abstractNodes_dict, grammar_dict)

    """
     * @param: child, Node
    """
    def readMandatoryAttribute(self, child):
        mandatory = "true"
        nodeMap = child. attributes  # get attributes
        for j in range(len(nodeMap)):  # for each attribute
            n = nodeMap.item(j)
            if n.name == "mandatory":
                mandatory = str(n.value)
        return mandatory

    """
     * @param: node, String
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def findIndex(self, node, grammar_dict):
        index = 0
        keySet = grammar_dict.keys()  # list des keys can't contain repetition
        for s in keySet:
            ss = s.split(UNICHAR)
            if ss[0] == node:
                if len(ss) == 2:
                    index = int(ss[1]) + 1
        if index > 1:
            return index
        else:
            return 1

    """
     * find add abstract node in grammar
     * @param: root, Node
     * @return a dictionary with String as keys and list of String as values
    """
    def readAbstractNodes(self, root):
        abstractNodes_dict = collections.OrderedDict()  # dictionary with String as keys and list of String as values
        try:
            childrenNodes_list = root.childNodes
            for i in range(len(childrenNodes_list)):  # for each abstract node
                if childrenNodes_list[i].hasAttributes() and childrenNodes_list[i].hasChildNodes() and childrenNodes_list[i].nodeType == Node.ELEMENT_NODE:
                    nodeMap = childrenNodes_list[i].attributes
                    for j in range(len(nodeMap)):  # check if a node is abstract
                        node = nodeMap.item(j)
                        if node.name == "abstract" and str(node.value) == "true":
                            tmp1_list = list()  # list of String
                            childrenList_list = childrenNodes_list[i].childNodes
                            for k in range(len(childrenList_list)):  # for each child of Abstract
                                if childrenList_list[k].nodeType == Node.ELEMENT_NODE:
                                    if childrenNodes_list[i].nodeName not in abstractNodes_dict:
                                        tmp1_list.append(childrenList_list[k].nodeName + UNICHAR + "false")
                                        abstractNodes_dict[childrenNodes_list[i].nodeName] = tmp1_list
                                    else:
                                        abstractNodes_dict[childrenNodes_list[i].nodeName].append(childrenList_list[k].nodeName + UNICHAR + "false")
        except:
            e = sys.exc_info()[0]
            print("read abstract nodes error " + str(e))
        return abstractNodes_dict


    """
     * find all synthetic node in grammar
     * @param: root, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
     * @return a dictionary with String as keys and list of String as values
    """
    def readSyntheticNodes(self, root, abstractNodes_dict, grammar_dict):
        # find abstract/synthetic nodes
        syntheticNodes_dict = collections.OrderedDict()  # dictionary with String as keys and list of String as values
        childrenNodes_list = root.childNodes
        for i in range(len(childrenNodes_list)):  # for each node
            if childrenNodes_list[i].hasAttributes() and childrenNodes_list[i].nodeType == Node.ELEMENT_NODE:
                nodeMap = childrenNodes_list[i].attributes
                for j in range(len(nodeMap)):  # check if a node i is synthetic
                    node = nodeMap.item(j)
                    if node.name == "synthetic" and str(node.value) == "true":
                        # find all children of synthetic node i
                        syntheticChildren_set = set()  # list without repetition
                        childrenList_list = childrenNodes_list[i].childNodes
                        for k in range(len(childrenList_list)):  # for each child of Synthetic node
                            if childrenList_list[k].nodeType == Node.ELEMENT_NODE:
                                mandatory = self.readMandatoryAttribute(childrenList_list[k])
                                if childrenList_list[k].nodeName + UNICHAR + mandatory not in syntheticChildren_set:
                                    syntheticChildren_set.add(childrenList_list[k].nodeName + UNICHAR + mandatory)
                                self.readAttribute(childrenList_list[k], abstractNodes_dict, grammar_dict)

                        if childrenNodes_list[i].nodeName in syntheticNodes_dict:
                            # find the index of rule, # create new synthetic rule
                            index = self.findIndex(childrenNodes_list[i].nodeName, syntheticNodes_dict)
                            syntheticNodes_dict[childrenNodes_list[i].nodeName + UNICHAR + str(index)] = list(syntheticChildren_set.copy())
                        else:
                            syntheticNodes_dict[childrenNodes_list[i].nodeName] = list(syntheticChildren_set.copy())
        return syntheticNodes_dict

    """
     * @param: node, Node
    """
    def checkSyntheticNode(self, node):
        synthetic = False
        childrenNodes_list = node.childNodes
        for i in range(len(childrenNodes_list)):
            if childrenNodes_list[i].hasAttributes() and childrenNodes_list[i].nodeType == Node.ELEMENT_NODE:
                adhoc = childrenNodes_list[i].nodeName.split("_")
                if adhoc[0] == "Adhoc":
                    synthetic = True
        return synthetic

    """
     * @param: node, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def readSimpleNode(self, node, abstractNodes_dict, grammar_dict):
        childrenListTmp_list = list()  # list without repetition # find all its children
        childrenList_list = node.childNodes  # create grammar for each child

        for i in range(len(childrenList_list)):
            if childrenList_list[i].hasAttributes() and childrenList_list[i].nodeType == Node.ELEMENT_NODE:
                mandatory = self.readMandatoryAttribute(childrenList_list[i])
                currentChildLabel = childrenList_list[i].nodeName
                if currentChildLabel + UNICHAR + str(mandatory) not in childrenListTmp_list:
                    childrenListTmp_list.append(currentChildLabel + UNICHAR + str(mandatory))
                self.readAttribute(childrenList_list[i], abstractNodes_dict, grammar_dict)
        # add the current node to grammar
        if len(childrenListTmp_list) != 0:
            childrenListTmpVector_list = childrenListTmp_list.copy()
            childrenListTmpVector_list.insert(0, "unordered")
            childrenListTmpVector_list.insert(1, str(len(childrenListTmpVector_list) - 1))
            # if this node exists in grammar then increase index
            if node.nodeName in grammar_dict:
                index = self.findIndex(node.nodeName, grammar_dict)
                grammar_dict[node.nodeName + UNICHAR + str(index)] = childrenListTmpVector_list.copy()
            else:
                grammar_dict[node.nodeName] = childrenListTmpVector_list.copy()

    """
     * @param: label, String
     * @param: maps_dict, dictionary with String as keys and list of String as values
     * return a dictionary with String as keys and list of String as values
    """
    def getRules(self, label, maps_dict):
        rules = collections.OrderedDict()  # dictionary with String as keys and list of String as values
        keyList_list = maps_dict.keys()  # list of keys (a keys is unique)
        for s in keyList_list:
            ss = s.split(UNICHAR)
            if ss[0] == label:
                rules[s] = maps_dict[s].copy()

        return rules

    """
     * @param: node, Node
     * @param: syntheticNodes_dict, dictionary with String as keys and list of String as value
     * @param: grammar_dict, dictionary with String as keys and list of String as value
    """
    def readSpecialNode(self, node, syntheticNodes_dict, grammar_dict):
        # get the set of children
        childrenNodes_list = node.childNodes
        # find normal children
        # find set of rules of each synthetic node, example: WhiteStatement has 2 synthetic nodes
        normalChildren_list = list()  # list of String
        syntheticChildren_dict = collections.OrderedDict()  # dictionary with String as keys and a dictionary as values with String as keys and list of String as values
        for i in range(len(childrenNodes_list)):
            if childrenNodes_list[i].hasAttributes() and childrenNodes_list[i].nodeType == Node.ELEMENT_NODE:
                adhoc = childrenNodes_list[i].nodeName.split("_")
                if adhoc[0] == "Adhoc":  # synthetic child
                    syntheticLabel = ""
                    for j in range(1, len(adhoc) -1):
                        syntheticLabel = syntheticLabel + adhoc[j] + "_"
                    syntheticLabel = syntheticLabel + adhoc[adhoc.length - 1]

                    syntheticChildren_dict[childrenNodes_list[i].nodeName] = self.getRules(syntheticLabel, syntheticNodes_dict)
                else: # normal child
                    mandatory = self.readMandatoryAttribute(childrenNodes_list[i])
                    normalChildren_list.append(childrenNodes_list[i].nodeName + UNICHAR + mandatory)

        # create all cases of synthetic nodes,
        # i.e, node A has 3 synthetic child, and
        # synthetic child 1 has 2 cases
        # synthetic child 2 has 3 cases
        # synthetic child 3 has 4 cases
        # --> total how many combinations ? --> for each case create one rule
        # how to know mandatory of these children


        # combine allChildren = normalChild + each item in syntheticChild
        size = len(syntheticChildren_dict)
        index = 0
        if size == 1:  # node has only one synthetic child
            for key1 in syntheticChildren_dict:
                # for each rule of synthetic node create a rule in grammar
                for key2 in syntheticChildren_dict[key1]:
                    allChildren_list = normalChildren_list.copy() # list of String
                    for elem in syntheticChildren_dict[key1][key2]:
                        allChildren_list.append(elem)
                    # create one rule in grammar
                    allChildren_list.insert(0, "unordered")
                    allChildren_list.insert(1, str(len(allChildren_list) -1))
                    if index == 0:
                        grammar_dict[node.nodeName] = allChildren_list.copy()
                    else:
                        grammar_dict[node.nodeName + UNICHAR + str(index)] = allChildren_list.copy()
                    index += 1

    """
     * find all AST node in grammar
     * @param: root, Node
     * @param: abstractNodes_dict, dictionary with String as keys and list of String as values
     * @param: syntheticNodes_dict, dictionary with String as keys and list of String as values
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def readASTNodes(self, root, abstractNodes_dict, syntheticNodes_dict, grammar_dict):
        childrenNodes_list = root.childNodes
        for t in range(len(childrenNodes_list)):  # for each child (AST node)
            # if it is not abstract and not synthetic node and it has children
            if not childrenNodes_list[t].hasAttributes() and childrenNodes_list[t].hasChildNodes() and childrenNodes_list[t].nodeType == Node.ELEMENT_NODE:
                if self.checkSyntheticNode(childrenNodes_list[t]):
                    self.readSpecialNode(childrenNodes_list[t], syntheticNodes_dict, grammar_dict)
                else:
                    self.readSimpleNode(childrenNodes_list[t], abstractNodes_dict, grammar_dict)

    """
     * create grammar from file
     * @param: path, String
     * @param: grammar_dict, dictionary with String as keys and list of String as values
    """
    def readGrammar(self, path, grammar_dict):
        try:
            # for each file in folder create one tree
            doc = minidom.parse(path)
            doc.documentElement.normalize()

            root = doc.documentElement
            abstractNodes_dict = self.readAbstractNodes(root)  # dictionary with String as keys and list of String as values
            syntheticNodes_dict = self.readSyntheticNodes(root, abstractNodes_dict, grammar_dict)  # dictionary with String as keys and list of String as values
            self.readASTNodes(root, abstractNodes_dict, syntheticNodes_dict, grammar_dict)

        except:
            e = sys.exc_info()[0]
            print("read grammar file error " + str(e))
