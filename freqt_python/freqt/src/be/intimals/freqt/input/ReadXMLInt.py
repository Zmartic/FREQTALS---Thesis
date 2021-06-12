#!/usr/bin/env python3
import freqt.src.be.intimals.freqt.structure.NodeFreqT as NodeFreqT
from freqt.src.be.intimals.freqt.util.Variables import *

from xml.dom import minidom
from xml.dom import Node
import sys
import os
import traceback

"""
 *
 * create tree data from ASTs
 *
"""


class ReadXMLInt:

    _top = 0  #int
    _id = 0   #int
    _sr = list()   #list of int
    _sibling = list()    #list of int

    _labels = list()    #list of string
    lineNrs = list()   #list of int
    countSection = -1  #int
    _abstractLeafs = False #boolean

    _sep = "/"  # File.separator

    """
     * read 2-class ASTs, and remove black labels
     * @param database_list, a list of list of NodeFreqT
     * @param classId, an int
     * @param rootDirectory, a string    !!!!! File object in java
     * @param labelIndex, a dictionnary with Interger as Key and String as value
     * @param classIndex_list, a list of Interger
     * @param whiteLabelPath, a string
    """
    def readDatabase(self, database_list, classId, rootDirectory, labelIndex, classIndex_list, whiteLabelPath):
        files = list()
        self.populateFileListNew(rootDirectory, files)
        files.sort()
        # read white labels from file
        whiteLabels = self.readWhiteLabel(whiteLabelPath)  # dictionary with String as Key and set of String as value
        try:
            for fi in files:
                self.countSection = 0
                # store class label of transaction id
                classIndex_list.append(classId)

                # read XML file
                doc = minidom.parse(fi)
                doc.documentElement.normalize()
                # get total number of nodes
                size = self.countNBNodes(doc.documentElement) + 1
                # initial tree parameters
                self._id = 0
                self._top = 0
                self._sr = list()
                self._sibling = list()
                trans = list()
                for i in range(size):
                    nodeTemp = NodeFreqT.NodeFreqT()
                    nodeTemp.nodeFreqtInit(-1, -1, -1, "0", True)
                    trans.append(nodeTemp)
                    self._sibling.append(-1)
                # create tree
                self.readTreeDepthFirst(doc.documentElement, trans, labelIndex, whiteLabels)
                # add tree to database
                database_list.append(trans)

        except:
            print(" read AST error.")
            e = sys.exc_info()[0]
            print(e)
            raise

    """
     * collect full file names in a directory
     * @param directory, a file path
     * @param listFile, a list of String represented a file path
    """
    def populateFileListNew(self, directory, listFile):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for elem in files:
            if elem.endswith(".xml"):
                listFile.append(directory + '/' + elem)
        directories = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        for direc in directories:
            dir = directory + '/' + direc
            self.populateFileListNew(dir, listFile)

    """
     * ignore black labels when reading tree by breadth first traversal
     * @param node, a Node
     * @param trans, a list of NodeFreqT
     * labelIndex, a dictionary with Integer as key and String as value
     * whiteLabels, a dictionary with String as key and Set of String as value
    """
    def readTreeDepthFirst(self, node, trans, labelIndex, whiteLabels):
        try:
            variables = Variables()
            # if this is an internal node
            if node.nodeType == Node.ELEMENT_NODE:
                # add node label to trans
                trans[self._id].setNodeLabel(node.nodeName)
                # update index labels
                self.updateLabelIndex(node.nodeName, trans, labelIndex)
                # find line number of this node.
                lineNbTemp = self.findLineNr(node)
                # add line number to current node id
                trans[self._id].setLineNr(lineNbTemp)
                # count SectionStatementBlock: only using for Cobol
                self.countSectionStatementBlock(node, lineNbTemp)

                # increase id
                self._sr.append(self._id)
                self._id = self._id + 1
                # recursively read children
                nodeList = node.childNodes
                # only read children labels which are in the white list
                if node.nodeName in whiteLabels:
                    temp = whiteLabels[node.nodeName]
                    for i in range(len(nodeList)):
                        if nodeList[i].nodeName in temp:
                            self.readTreeDepthFirst(nodeList[i], trans, labelIndex, whiteLabels)
                else:
                    for i in range(len(nodeList)):
                        self.readTreeDepthFirst(nodeList.item(i), trans, labelIndex, whiteLabels)
                # calculate parent, child, sibling of internal node
                self.calculatePositions(trans)
            else:
                # this is a leaf
                if node.nodeType == Node.TEXT_NODE and len(node.data.strip()) != 0:
                    # if a has sibling it is not a unique leaf
                    a = node.nextSibling
                    b = node.previousSibling

                    if a is None and b is None:
                        if self._abstractLeafs:
                            leafLabel = "**"
                        else:
                            leafLabel = "*" + node.data.replace(",", variables.uniChar).strip()
                        # add leaf node label to trans
                        trans[self._id].setNodeLabel(leafLabel)
                        # update labelIndex for leaf labels
                        if leafLabel not in self._labels:
                            trans[self._id].setNode_label_int(len(labelIndex)*(-1))
                            labelIndex[len(labelIndex)*(-1)] = leafLabel
                            self._labels.append(leafLabel)
                        else:
                            trans[self._id].setNode_label_int(self._labels.index(leafLabel)*(-1))
                        # set line number of leaf node to -1
                        trans[self._id].setLineNr("-1")
                        # increase id
                        self._sr.append(self._id)
                        self._id = self._id + 1
                        # calculate parent, child, sibling of this leaf node
                        self.calculatePositions(trans)
        except:
            e = sys.exc_info()[0]
            print("Error in readTreeDepthFirst" + str(e))
            trace = traceback.format_exc()
            print(trace)
            raise

    """
     * @param trans, a list of NodeFreqT
    """
    def calculatePositions(self, trans):
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

    """
     * @param node, a node
     * @param lineNbTemp, a String
    """
    def countSectionStatementBlock(self, node, lineNbTemp):
        if node.tagName == "SectionStatementBlock" and self.countSection < 2:
            self.countSection += 1
        else:
            if self.countSection == 2:
                self.lineNrs.append(int(lineNbTemp))
                self.countSection += 1

    """
     * @param node, a node
    """
    def findLineNr(self, node):
        lineNbTemp = "0"
        nodeMap = node.attributes
        for i in range(len(nodeMap)):
            if nodeMap.item(i).name == "LineNr":
                lineNbTemp = nodeMap.item(i).value
        return lineNbTemp

    """
     * @param nodeLabel, a String
     * @param trans, a list of NodeFreqT
     * @param labelIndex, a dictionary with Interger as key and String as value
    """
    def updateLabelIndex(self, nodeLabel, trans, labelIndex):
        # update labelIndex for internal labels
        if len(labelIndex) == 0 and len(self._labels) == 0:
            trans[self._id].setNode_label_int(0)
            labelIndex[0] = nodeLabel
            self._labels.append(nodeLabel)
        else:
            if nodeLabel not in self._labels:
                trans[self._id].setNode_label_int(len(labelIndex))
                labelIndex[len(labelIndex)] = nodeLabel
                self._labels.append(nodeLabel)
            else:
                trans[self._id].setNode_label_int(self._labels.index(nodeLabel))

    """
     * read white labels from given file
     * @param path, a String
     * return a dictionary containing the whiteLabels with string as Key and a list of String as value.
    """
    def readWhiteLabel(self, path):
        _whiteLabels = dict()
        try:
            f = open(path, 'r')
            line = f.readline()
            while line:
                if line != "" and line[0] != '#' and line != "\n":
                    str_tmp = line.split()
                    ASTNode = str_tmp[0]
                    children_set = set()
                    for i in range(1, len(str_tmp)):
                        children_set.add(str_tmp[i])
                    _whiteLabels[ASTNode] = children_set
                line = f.readline()
            f.close()
        except:
            e = sys.exc_info()[0]
            print("Error: reading white list " + str(e))
            trace = traceback.format_exc()
            print(trace)
            raise
        return _whiteLabels

    """
     * count number children of a node
     * @param node, a node
     * return the number of children of a given node
    """
    def countNBChildren(self, node):
        nbChildren = 0
        list = node.childNodes
        for j in range(len(list)):
            if list[j].nodeType != Node.TEXT_NODE and list[j].nodeType == Node.ELEMENT_NODE:
                nbChildren += 1
        return nbChildren

    """
     * count total number of nodes of a Python XML
     * @param root, the root node of the xml tree
     * return the number of nodes of a Python XML
    """
    def countNBNodes(self, root):
        count = 0
        if root.nodeType == Node.ELEMENT_NODE:
            count += 1
            children = root.childNodes
            for child in children:
                count += self.countNBNodes(child)
        else:
            if root.nodeType == Node.TEXT_NODE and len(root.data.strip()) != 0:
                a = root.nextSibling
                b = root.previousSibling
                if a is None and b is None:
                    count += 1
        return count

    # return total number of reading files
    def getlineNrs(self):
        return self.lineNrs
