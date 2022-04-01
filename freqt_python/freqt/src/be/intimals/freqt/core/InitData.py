#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import *
from freqt.src.be.intimals.freqt.grammar.CreateGrammar import createGrammar
from freqt.src.be.intimals.freqt.grammar.ReadGrammar import readGrammar
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR
from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt


def init_data_1class(config):
    """
     * read input data
    """
    white_label = read_white_label(config.getWhiteLabelFile())

    # remove black labels when reading ASTs
    transactions = list()
    trans_class_id = list()  # actually not useful
    label_decoder = dict()
    readXML = ReadXMLInt()
    readXML.readDatabase(transactions, 1, config.getInputFiles(), label_decoder, trans_class_id, white_label)

    # create grammar (labels are strings) which is used to print patterns
    grammar = dict()
    init_grammar(config.getInputFiles(), white_label, grammar, config.buildGrammar())

    # read list of special XML characters
    xml_char_dict = read_XML_character(config.getXmlCharacterFile())

    grammar_int = convert_grammar_label2int(grammar, label_decoder)
    root_label_set = read_root_label(config.getRootLabelFile())
    constraints = FreqT1Strategy(config, grammar_int, root_label_set)

    return transactions, trans_class_id, label_decoder, grammar, xml_char_dict, constraints


def init_data_2class(config):
    """
     * read input data
    """
    white_label = read_white_label(config.getWhiteLabelFile())

    # remove black labels when reading ASTs
    transactions = list()
    trans_class_id = list()
    label_decoder = dict()
    readXML = ReadXMLInt()
    readXML.readDatabase(transactions, 1, config.getInputFiles1(), label_decoder, trans_class_id, white_label)
    readXML.readDatabase(transactions, 0, config.getInputFiles2(), label_decoder, trans_class_id, white_label)
    size_class1 = sum(trans_class_id)
    size_class2 = len(trans_class_id) - size_class1

    # init grammar
    grammar = dict()
    init_grammar(config.getInputFiles1(), white_label, grammar, config.buildGrammar())
    init_grammar(config.getInputFiles2(), white_label, grammar, config.buildGrammar())

    # read list of special XML characters
    xml_char_dict = read_XML_character(config.getXmlCharacterFile())

    grammar_int = convert_grammar_label2int(grammar, label_decoder)
    root_label_set = read_root_label(config.getRootLabelFile())
    constraints = FreqT1Strategy(config, grammar_int, root_label_set)

    return transactions, trans_class_id, label_decoder, size_class1, size_class2, grammar, xml_char_dict, constraints


# --- INITIAL INT --- #

def init_grammar(path, white, gram_dict, _build_grammar):
    """
     * Load the grammar from a given file or build it from a set of ASTs
     * @param: path, String
     * @param: white, String
     * @param: gram_dict, a dictionary with String as keys and list of string as values
     * @gram: _buildGrammar, boolean
    """
    try:
        if _build_grammar:
            createGrammar(path, gram_dict, white)
        else:
            readGrammar(path, gram_dict)
    except:
        e = sys.exc_info()[0]
        print("init grammar error " + str(e) + "\n")
        print(traceback.format_exc())


def convert_grammar_label2int(gram_str, label_index):
    """
     * convert grammar in form of String to Int
     * @param: gramInt_dict, a dictionary with Integer as keys and list of String as values
     * @param: gramStr_dict, a dictionary with String as keys and list of String as values
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
    """
    gram_int = dict()

    for key in gram_str:
        node_children_list = gram_str[key]  # list of string
        # find index of the current label
        index = find_index(key, label_index)
        # new int children
        new_children_list = [node_children_list[0], node_children_list[1]]

        # find new int children
        for i in range(2, len(node_children_list)):
            temp = node_children_list[i].split(UNICHAR)
            if temp[0] != "leaf-node":
                child_index = find_index(temp[0], label_index)
                new_child = str(child_index) + UNICHAR + str(temp[1])
                new_children_list.append(new_child)
            else:
                new_child = str(0) + UNICHAR + str(temp[1])
                new_children_list.append(new_child)
        # add current int label and int children into gramInt
        gram_int[index] = new_children_list

    return gram_int


def find_index(label, label_index):
    """
     * find the position of a label in a dictionary
     * @param: label, String
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as values
    """
    for index in label_index:
        if label_index[index] == label:
            return index
    return -1


def read_white_label(path):
    _whiteLabels = dict()
    try:
        f = open(path, 'r')
        line = f.readline()
        while line:
            if line != "" and line[0] != '#' and line != "\n":
                str_tmp = line.split()
                ast_node = str_tmp[0]
                children_set = set()
                for i in range(1, len(str_tmp)):
                    children_set.add(str_tmp[i])
                _whiteLabels[ast_node] = children_set
            line = f.readline()
        f.close()
    except:
        e = sys.exc_info()[0]
        print("Error: reading white list " + str(e))
        print(traceback.format_exc())

    return _whiteLabels


def read_root_label(path):
    """
     * read list of root labels
     * @param: path, String
     * @param: rootLabels_set, a set of String
    """
    root_labels_set = set()
    try:
        with open(path) as f:
            line = f.readline()
            while line:
                if len(line) != 0 and line[0] != '#' and line != "\n":
                    line = line.replace("\n", "")
                    str_tmp = line.split(" ")
                    root_labels_set.add(str_tmp[0])
                line = f.readline()
    except:
        e = sys.exc_info()[0]
        print("Error: reading listRootLabel " + str(e) + "\n")

    return root_labels_set


def read_XML_character(path):
    """
     * read list of special XML characters
     * @param: path, String
     * @param: listCharacters_dict, dictionary with String as keys and String as values
    """
    xml_characters = dict()
    try:
        with open(path) as f:
            line = f.readline()
            while line:
                if len(line) != 0 and line[0] != '#':
                    str_tmp = line.split("\t")
                    xml_characters[str_tmp[0]] = str_tmp[1]
                line = f.readline()
    except:
        e = sys.exc_info()[0]
        print("Error: reading XMLCharacter " + str(e) + "\n")

    return xml_characters
