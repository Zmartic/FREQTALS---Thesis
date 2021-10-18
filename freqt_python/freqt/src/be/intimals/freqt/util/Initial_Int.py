#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.grammar.CreateGrammar import *
from freqt.src.be.intimals.freqt.grammar.ReadGrammar import *
from freqt.src.be.intimals.freqt.util.Variables import *

import sys

## UNUSED
def initGrammar_Int(path, gram_dict, labelIndex_dict):
    """
     * build grammar from a set of ASTs
     * @param: path, String
     * @param: gram_dict, a dictionary with Integer as keys and list of String as values
     * @param: labelIndex_dict, a dictionary with Integer as Integer and String as values
    """
    try:
        gramTemp_dict = dict() #dictionary with String as keys and list of String as values
        createGrammar = CreateGrammar()
        createGrammar.createGrammar2(path, gramTemp_dict)
        variables = Variables()
        for key in gramTemp_dict:
            index = find_index(key, labelIndex_dict)
            for i in range(2, len(gramTemp_dict[key])):
                temp = gramTemp_dict[key][i].split(variables.uniChar)
                if temp[0] != "leaf-node":
                    childIndex = find_index(temp[0], labelIndex_dict)
                    newChild = str(childIndex) + variables.uniChar + str(temp[1])
                    gramTemp_dict[key][i] = newChild
                else:
                    newChild = str(0) + variables.uniChar + str(temp[1])
                    gramTemp_dict[key][i] = newChild
            gram_dict[index] = gramTemp_dict[key]
    except:
        e = sys.exc_info()[0]
        print("Error: reading grammar " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)

def initGrammar_Int2(gramInt_dict, gramStr_dict, labelIndex_dict):
    """
     * convert grammar in form of String to Int
     * @param: gramInt_dict, a dictionary with Integer as keys and list of String as values
     * @param: gramStr_dict, a dictionary with String as keys and list of String as values
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
    """
    try:
        variables = Variables()
        for key in gramStr_dict:
            nodeChildren_list = gramStr_dict[key]  # list of string
            # find index of the current label
            index = find_index(key, labelIndex_dict)
            # new int children
            newChildren_list = list()  # list of string
            newChildren_list.append(nodeChildren_list[0])
            newChildren_list.append(nodeChildren_list[1])
            # find new int children
            for i in range(2, len(nodeChildren_list)):
                temp = nodeChildren_list[i].split(variables.uniChar)
                if temp[0] != "leaf-node":
                    childIndex = find_index(temp[0], labelIndex_dict)
                    newChild = str(childIndex) + variables.uniChar + str(temp[1])
                    newChildren_list.append(newChild)
                else:
                    newChild = str(0) + variables.uniChar + str(temp[1])
                    newChildren_list.append(newChild)
            #add current int label and int children into gramInt
            gramInt_dict[index] = newChildren_list
    except:
        e = sys.exc_info()[0]
        print("Error: reading grammar " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)

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
## UNUSED
def readWhiteLabel(path, _grammar_dict, _whiteLabels_dict, _blackLabels_dict, labelIndex_dict):
    """
     * read whitelist and create blacklist
     * @param: path, String
     * @param: _grammar_dict, a dictionary with Integer as keys and list of String as values
     * @param: _whiteLabels_dict, a dictionary with Integer as keys and list of Integer as values
     * @param: _blackLabels_dict, a dictionary with Integer as keys and list of Integer as values
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
    """
    #all black list labels are removed
    try:
        variables = Variables()
        try:
            with open(path) as f:
                line = f.readline()
                while line:
                    if len(line) != 0 and line[0] != '#':
                        str_tmp = line.split(" ")
                        ASTNode = str_tmp[0]
                        label_int = find_index(ASTNode, labelIndex_dict)
                        if label_int != -1:
                            whiteChildren_int_list = list() #list of Integer
                            whiteChildren_str_list = list() #list of str
                            for i in range(1, len(str_tmp)):
                                whiteChildren_str_list.append(str_tmp[i])
                                t = find_index(str_tmp[i], labelIndex_dict)
                                whiteChildren_int_list.append(t)
                            _whiteLabels_dict[label_int] = whiteChildren_int_list
                            #create blacklist
                            if label_int in _grammar_dict.keys():
                                #get all children of label_int in grammar
                                blackChildren_list = list() #list of String
                                sub_list = _grammar_dict[label_int][2:]
                                for elem in sub_list:
                                    blackChildren_list.append(elem)
                                #transform string to int
                                blackChildren_int_list = list() #list of Integer
                                for i in range(len(blackChildren_list)):
                                    blackChildren_list[i] = blackChildren_list[i].split(variables.uniChar)[0]
                                    index = int(blackChildren_list[i].split(variables.uniChar)[0])
                                    blackChildren_int_list.append(index)
                                for i in range(len(whiteChildren_int_list)):
                                    blackChildren_int_list.pop(whiteChildren_int_list[i])
                                _blackLabels_dict[label_int] = blackChildren_int_list
        except:
            e = sys.exc_info()[0]
            print("read white labels list error " + str(e) + "\n")
    except:
        e = sys.exc_info()[0]
        print("reading white list " + str(e) + "\n")
