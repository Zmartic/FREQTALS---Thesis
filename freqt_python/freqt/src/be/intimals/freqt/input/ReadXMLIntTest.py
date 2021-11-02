import unittest

from freqt.src.be.intimals.freqt.input.ReadXMLInt import *
from freqt.src.be.intimals.freqt.structure.NodeFreqT import *

from xml.dom import minidom
from xml.dom import Node


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.RXML = ReadXMLInt()
        self.RXML.lineNrs = []
        self.RXML._id = 0
        self.RXML._top = 0
        self.RXML._sr = []
        self.RXML._sibling = []
        self.RXML._labels = []
        self.RXML.countSection = -1
        self.RXML._abstractLeafs = False

    def test_getlineNrs(self):
        self.assertEqual(self.RXML.getlineNrs(), [])

    def test_countNBNode(self):
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        self.assertEqual(self.RXML.countNBNodes(doc.documentElement) + 1, 17)

    def test_countNBChildren(self):
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        self.assertEqual(self.RXML.count_children(doc.documentElement), 3)
        children = doc.documentElement.childNodes
        i = 0
        correct_output_child = [3, 1, 2]
        for child in children:
            if child.nodeType != Node.TEXT_NODE and child.nodeType == Node.ELEMENT_NODE:
                self.assertEqual(self.RXML.count_children(child), correct_output_child[i])
                i += 1

    def test_readWhiteLabel(self):
        correct_output = dict()
        children = set()
        children.add("B")
        children.add("D")
        correct_output["A"] = children
        self.assertEqual(self.RXML.read_whiteLabel("../../../../../test/Basic/listWhiteLabel.txt"), correct_output)

    def test_updateLabelIndex(self):
        # cas 1
        nodeLabel = "A"
        trans = [NodeFreqT(), NodeFreqT(), NodeFreqT]
        labelIndex = {}
        output_labelIndex = dict()
        output_labelIndex[0] = "A"
        self.RXML.updateLabelIndex(nodeLabel, trans, labelIndex)
        self.assertEqual(trans[0].getNode_label_int(), 0)
        self.assertEqual(labelIndex, output_labelIndex)
        # cas 2
        nodeLabel = "B"
        output_labelIndex = dict()
        output_labelIndex[0] = "A"
        output_labelIndex[1] = "B"
        self.RXML.updateLabelIndex(nodeLabel, trans, labelIndex)
        self.assertEqual(trans[0].getNode_label_int(), 1)
        self.assertEqual(labelIndex, output_labelIndex)
        # cas 3
        nodeLabel = "A"
        output_labelIndex = dict()
        output_labelIndex[0] = "A"
        output_labelIndex[1] = "B"
        self.RXML.updateLabelIndex(nodeLabel, trans, labelIndex)
        self.assertEqual(trans[0].getNode_label_int(), 0)
        self.assertEqual(labelIndex, output_labelIndex)

    def test_findLineNr(self):
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        children = doc.documentElement.childNodes
        i = 0
        correct_output = ["2", "6", "7"]
        for child in children:
            if child.nodeType != Node.TEXT_NODE and child.nodeType == Node.ELEMENT_NODE:
                self.assertEqual(self.RXML.find_LineNr(child), correct_output[i])
                i += 1

    def test_countSectionStatementBlock(self):
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        self.RXML.countSectionStatementBlock(doc.documentElement, "0")
        self.assertEqual(self.RXML.countSection, -1)
        self.RXML.countSection = 2
        self.RXML.countSectionStatementBlock(doc.documentElement, "1")
        self.assertEqual(self.RXML.countSection, 3)
        self.assertEqual(self.RXML.lineNrs, [1])

    def test_populateFileListNew(self):
        directory2 = '../../../../../resources/input-artificial-data/abstract-data'
        directory = '../../../../../test/Harder/version1'
        file_list = []
        file2_list = []
        correct_output_file_list = ['../../../../../test/Harder/version1/builder/Builder.xml',
                                    '../../../../../test/Harder/version1/builder/GridBagLayout_Builder.xml',
                                    '../../../../../test/Harder/version1/builder/GridLayout_Builder.xml',
                                    '../../../../../test/Harder/version1/builder/JTable_Builder.xml',
                                    '../../../../../test/Harder/version1/builder/TableBuilderDemo.xml',
                                    '../../../../../test/Harder/version1/builder/TableDirector.xml',
                                    '../../../../../test/Harder/version1/visitor/Book.xml',
                                    '../../../../../test/Harder/version1/visitor/Fruit.xml',
                                    '../../../../../test/Harder/version1/visitor/ItemElement.xml',
                                    '../../../../../test/Harder/version1/visitor/ShoppingCartClient.xml',
                                    '../../../../../test/Harder/version1/visitor/ShoppingCartVisitor.xml',
                                    '../../../../../test/Harder/version1/visitor/ShoppingCartVisitorImpl.xml']
        self.RXML.populate_file_list(directory2, file2_list)
        print(file2_list)
        self.RXML.populate_file_list(directory, file_list)
        self.assertEqual(file_list, correct_output_file_list)

    def test_calculatePositions(self):
        trans = []
        self.RXML._sr = [0, 1, 2, 3, 4, 5, 6]
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        size = self.RXML.countNBNodes(doc.documentElement) + 1
        correct_output_parent = [-1, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        correct_output_child = [-1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        correct_output_sibling = [-1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        for i in range(size):
            nodeTemp = NodeFreqT()
            nodeTemp.nodeFreqtInit(-1, -1, -1, "0", True)
            trans.append(nodeTemp)
            self.RXML._sibling.append(-1)
        self.RXML.calculatePositions(trans)
        for i in range(len(trans)):
            self.assertEqual(trans[i].getNodeParent(), correct_output_parent[i])
            self.assertEqual(trans[i].getNodeChild(), correct_output_child[i])
            self.assertEqual(self.RXML._sibling[i], correct_output_sibling[i])

    def test_readTreeDepthFirst(self):
        doc = minidom.parse("../../../../../test/Basic/ast1.xml")
        doc.documentElement.normalize()
        size = self.RXML.countNBNodes(doc.documentElement) + 1
        node = doc.documentElement
        trans = []
        correct_output_parent = [-1, 0, 1, 2, 1, 4, 1, 6, 0, 8, 9, 8, 11, -1, -1, -1, -1]
        correct_output_label = ['A', 'B', 'F', '*f1', 'F', '*f2', 'F', '*f3', 'D', 'D1', '*d1', 'D2', '*d2', '', '', '', '']
        correct_output_child = [1, 2, 3, -1, 5, -1, 7, -1, 9, 10, -1, 12, -1, -1, -1, -1, -1]
        correct_output_sibling = [-1, 8, 4, -1, 6, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1]
        for i in range(size):
            nodeTemp = NodeFreqT()
            nodeTemp.nodeFreqtInit(-1, -1, -1, "0", True)
            trans.append(nodeTemp)
            self.RXML._sibling.append(-1)
        labelIndex = {}
        whiteLabel = self.RXML.read_whiteLabel("../../../../../test/Basic/listWhiteLabel.txt")
        self.RXML.readTreeDepthFirst(node, trans, labelIndex, whiteLabel)
        for i in range(len(trans)):
            self.assertEqual(trans[i].getNodeLabel(), correct_output_label[i])
            self.assertEqual(trans[i].getNodeParent(), correct_output_parent[i])
            self.assertEqual(trans[i].getNodeChild(), correct_output_child[i])
            self.assertEqual(trans[i].getNodeSibling(), correct_output_sibling[i])


if __name__ == '__main__':
    unittest.main()
