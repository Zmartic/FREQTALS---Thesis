#!/usr/bin/env python3
from xml.dom import Node, minidom
import sys
import os
import traceback

import freqt.src.be.intimals.freqt.structure.NodeFreqT as NodeFreqT
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR

"""
 *
 * create tree data from ASTs
 *
"""


class ReadXMLInt:

    def __init__(self):
        self._top = 0
        self._id = 0
        self._sr = []        # list of int
        self._sibling = []   # list of int

        self._labels = []    # list of string
        self.line_nrs = []    # list of int
        self.count_section = -1
        self._abstract_leaves = False

    def readDatabase(self, database, class_id, root_directory, label_index, class_index_list, white_labels):
        """
         * read 2-class ASTs, and remove black labels
         * @param database_list, a list of list of NodeFreqT
         * @param classId, an int
         * @param rootDirectory, a string    !!!!! File object in java
         * @param label_index, a dictionnary with Interger as Key and String as value
         * @param classIndex_list, a list of Interger
         * @param whiteLabelPath, a string
        """
        files = []
        self.populate_file_list(root_directory, files)
        files.sort()

        try:
            for file in files:
                self.count_section = 0
                # store class label of transaction id
                class_index_list.append(class_id)

                # read XML file
                doc = minidom.parse(file)
                doc.documentElement.normalize()

                # get total number of nodes
                size = self.countNBNodes(doc.documentElement) + 1
                # initial tree parameters
                self._id = 0
                self._top = 0
                self._sr = []
                self._sibling = []
                trans = []
                for _ in range(size):
                    node_temp = NodeFreqT.NodeFreqT()
                    node_temp.nodeFreqtInit(-1, -1, -1, "0", True)
                    trans.append(node_temp)
                    self._sibling.append(-1)
                # create tree
                self.readTreeDepthFirst(doc.documentElement, trans, label_index, white_labels)
                # add tree to database
                database.append(trans)

        except:
            print(" read AST error.")
            print(sys.exc_info()[0])
            raise

    def populate_file_list(self, directory, file_list):
        """
         * collect full file names in a directory
         * @param directory, a file path
         * @param listFile, a list of String represented a file path
        """
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for elem in files:
            if elem.endswith(".xml"):
                file_list.append(directory + '/' + elem)
        directories = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        for direc in directories:
            self.populate_file_list(directory + '/' + direc, file_list)

    def readTreeDepthFirst(self, node, trans, label_index, white_labels):
        """
         * ignore black labels when reading tree by breadth first traversal
         * @param node, a Node
         * @param trans, a list of NodeFreqT
         * label_index, a dictionary with Integer as key and String as value
         * white_labels, a dictionary with String as key and Set of String as value
        """
        try:
            # if this is an internal node
            if node.nodeType == Node.ELEMENT_NODE:
                # add node label to trans
                trans[self._id].setNodeLabel(node.nodeName)
                # update index labels
                self.updateLabelIndex(node.nodeName, trans, label_index)
                # find line number of this node.
                line_nb_temp = self.find_LineNr(node)
                # add line number to current node id
                trans[self._id].setLineNr(line_nb_temp)
                # count SectionStatementBlock: only using for Cobol
                self.countSectionStatementBlock(node, line_nb_temp)

                # increase id
                self._sr.append(self._id)
                self._id = self._id + 1
                # recursively read children
                node_list = node.childNodes
                # only read children labels which are in the white list
                if node.nodeName in white_labels:
                    temp = white_labels[node.nodeName]
                    for node_i in node_list:
                        if node_i.nodeName in temp:
                            self.readTreeDepthFirst(node_i, trans, label_index, white_labels)
                else:
                    for node_i in node_list:
                        self.readTreeDepthFirst(node_i, trans, label_index, white_labels)
                # calculate parent, child, sibling of internal node
                self.calculatePositions(trans)
            else:
                # this is a leaf
                if node.nodeType == Node.TEXT_NODE and len(node.data.strip()) != 0:
                    # if a has sibling it is not a unique leaf

                    if node.nextSibling is None and node.previousSibling is None:
                        if self._abstract_leaves:
                            leaf_label = "**"
                        else:
                            leaf_label = "*" + node.data.replace(",", UNICHAR).strip()
                        # add leaf node label to trans
                        trans[self._id].setNodeLabel(leaf_label)
                        # update label_index for leaf labels
                        if leaf_label not in self._labels:
                            trans[self._id].setNode_label_int(len(label_index)*(-1))
                            label_index[len(label_index)*(-1)] = leaf_label
                            self._labels.append(leaf_label)
                        else:
                            trans[self._id].setNode_label_int(self._labels.index(leaf_label)*(-1))
                        # set line number of leaf node to -1
                        trans[self._id].setLineNr("-1")
                        # increase id
                        self._sr.append(self._id)
                        self._id = self._id + 1
                        # calculate parent, child, sibling of this leaf node
                        self.calculatePositions(trans)
        except:
            print("Error in readTreeDepthFirst" + str(sys.exc_info()[0]))
            trace = traceback.format_exc()
            print(trace)
            raise

    def calculatePositions(self, trans):
        """
         * @param trans, a list of NodeFreqT
        """
        self._top = len(self._sr) - 1
        if self._top < 1:
            return
        child = self._sr[self._top]
        parent = self._sr[self._top - 1]
        trans[child].setNodeParent(parent)
        if trans[parent].getNodeChild() == -1:
            trans[parent].setNodeChild(child)
        if self._sibling[parent] != -1:
            trans[self._sibling[parent]].setNodeSibling(child)
        self._sibling[parent] = child
        self._sr.pop(self._top)

    def countSectionStatementBlock(self, node, line_nb_temp):
        """
         * @param node, a node
         * @param line_nb_temp, a String
        """
        if node.tagName == "SectionStatementBlock" and self.count_section < 2:
            self.count_section += 1
        else:
            if self.count_section == 2:
                self.line_nrs.append(int(line_nb_temp))
                self.count_section += 1

    def find_LineNr(self, node):
        """
         * @param node, a node
        """
        node_map = node.attributes
        for i in range(len(node_map)):
            if node_map.item(i).name == "LineNr":
                return node_map.item(i).value
        return "0"

    def updateLabelIndex(self, node_label, trans, label_index):
        """
         * @param nodeLabel, a String
         * @param trans, a list of NodeFreqT
         * @param label_index, a dictionary with Interger as key and String as value
        """
        # update label_index for internal labels
        if len(label_index) == 0 and len(self._labels) == 0:
            trans[self._id].setNode_label_int(0)
            label_index[0] = node_label
            self._labels.append(node_label)
        else:
            if node_label not in self._labels:
                trans[self._id].setNode_label_int(len(label_index))
                label_index[len(label_index)] = node_label
                self._labels.append(node_label)
            else:
                trans[self._id].setNode_label_int(self._labels.index(node_label))

    def read_whiteLabel(self, path):
        """
         * read white labels from given file
         * @param path, a String
         * return a dictionary containing the white_labels with string as Key and a list of String as value.
        """
        _white_labels = {}
        try:
            with open(path, 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    if line != "" and line[0] != '#' and line != "\n":
                        str_tmp = line.split()
                        ast_node = str_tmp[0]
                        children_set = set()
                        for i in range(1, len(str_tmp)):
                            children_set.add(str_tmp[i])
                        _white_labels[ast_node] = children_set
                    line = file.readline()
        except:
            print("Error: reading white list " + str(sys.exc_info()[0]))
            trace = traceback.format_exc()
            print(trace)
            raise
        return _white_labels

    def count_children(self, node):
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

    def countNBNodes(self, root):
        """
         * count total number of nodes of a Python XML
         * @param root, the root node of the xml tree
         * return the number of nodes of a Python XML
        """
        count = 0
        if root.nodeType == Node.ELEMENT_NODE:
            count += 1
            children = root.childNodes
            for child in children:
                count += self.countNBNodes(child)
        else:
            if root.nodeType == Node.TEXT_NODE and len(root.data.strip()) != 0:
                if root.nextSibling is None and root.previousSibling is None:
                    count += 1
        return count

    # return total number of reading files
    def getlineNrs(self):
        return self.line_nrs
