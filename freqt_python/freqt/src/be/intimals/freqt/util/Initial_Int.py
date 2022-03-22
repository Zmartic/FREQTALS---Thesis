#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.grammar.CreateGrammar import *
from freqt.src.be.intimals.freqt.grammar.ReadGrammar import *
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR

import sys


def convert_grammar_label2int(gram_str, label_index):
    """
         * convert grammar in form of String to Int
         * @param: gramInt_dict, a dictionary with Integer as keys and list of String as values
         * @param: gramStr_dict, a dictionary with String as keys and list of String as values
         * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
        """
    gram_int = dict()

    for key in gram_str:
        nodeChildren_list = gram_str[key]  # list of string
        # find index of the current label
        index = find_index(key, label_index)
        # new int children
        newChildren_list = list()  # list of string
        newChildren_list.append(nodeChildren_list[0])
        newChildren_list.append(nodeChildren_list[1])
        # find new int children
        for i in range(2, len(nodeChildren_list)):
            temp = nodeChildren_list[i].split(UNICHAR)
            if temp[0] != "leaf-node":
                childIndex = find_index(temp[0], label_index)
                newChild = str(childIndex) + UNICHAR + str(temp[1])
                newChildren_list.append(newChild)
            else:
                newChild = str(0) + UNICHAR + str(temp[1])
                newChildren_list.append(newChild)
        # add current int label and int children into gramInt
        gram_int[index] = newChildren_list

    return gram_int


def initGrammar_Str(path, white, gram_dict, _buildGrammar):
    """
     * Load the grammar from a given file or build it from a set of ASTs
     * @param: path, String
     * @param: white, String
     * @param: gram_dict, a dictionary with String as keys and list of string as values
     * @gram: _buildGrammar, boolean
    """
    try:
        if _buildGrammar:
            createGrammar = CreateGrammar()
            createGrammar.createGrammar(path, white, gram_dict)
        else:
            read = ReadGrammar()
            read.readGrammar(path, gram_dict)
    except:
        e = sys.exc_info()[0]
        print("Error: reading grammar " + str(e) + "\n")


def readRootLabel(path, rootLabels_set):
    """
     * read list of root labels
     * @param: path, String
     * @param: rootLabels_set, a set of String
    """
    try:
        with open(path) as f:
            line = f.readline()
            while line:
                if len(line) != 0 and line[0] != '#' and line != "\n":
                    line = line.replace("\n", "")
                    str_tmp = line.split(" ")
                    rootLabels_set.add(str_tmp[0])
                line = f.readline()
    except:
        e = sys.exc_info()[0]
        print("Error: reading listRootLabel " + str(e) + "\n")


def readXMLCharacter(path, listCharacters_dict):
    """
     * read list of special XML characters
     * @param: path, String
     * @param: listCharacters_dict, dictionary with String as keys and String as values
    """
    try:
        with open(path) as f:
            line = f.readline()
            while line:
                if len(line) != 0 and line[0] != '#':
                    str_tmp = line.split("\t")
                    listCharacters_dict[str_tmp[0]] = str_tmp[1]
                line = f.readline()
    except:
        e = sys.exc_info()[0]
        print("Error: reading XMLCharater " + str(e) + "\n")


def find_index(label, labelIndex_dict):
    """
     * find the position of a label in a dictionary
     * @param: label, String
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
    """
    index = -1
    for key in labelIndex_dict:
        if labelIndex_dict[key] == label:
            index = key
    return index
