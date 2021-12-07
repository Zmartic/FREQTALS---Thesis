#!/usr/bin/env python3
import unittest
import freqt.src.be.intimals.freqt.structure.NodeFreqT as NodeFreqT


class NodeFreqTTest(unittest.TestCase):

    def setUp(self):
        self.node = NodeFreqT.NodeFreqT()
        self.node.nodeFreqtInit(1, 2, 3, 4, 5)

    def test_init(self):
        self.assertEqual(self.node.getNodeLabel(), "")
        self.assertEqual(self.node.getNode_label_int(), -1)
        self.assertEqual(self.node.getLineNr(), "")
        self.assertEqual(self.node.getNodeParent(), 1)
        self.assertEqual(self.node.getNodeChild(), 2)
        self.assertEqual(self.node.getNodeSibling(), 3)
        self.assertEqual(self.node.getNodeDegree(), 4)
        self.assertEqual(self.node.getNodeOrdered(), 5)
        self.assertEqual(self.node.getNodeLevel(), -1)
        self.assertEqual(self.node.getNodeParentExt(), -1)
        self.assertEqual(self.node.getNodeChildExt(), -1)
        self.assertEqual(self.node.getNodeSiblingExt(), -1)

    def test_get_set(self):
        self.node.setNodeLabel("Root")
        self.assertEqual(self.node.getNodeLabel(), "Root")
        self.node.setNode_label_int(534)
        self.assertEqual(self.node.getNode_label_int(), 534)
        self.node.setLineNr("Line 2")
        self.assertEqual(self.node.getLineNr(), "Line 2")
        self.node.setNodeParent(34)
        self.assertEqual(self.node.getNodeParent(), 34)
        self.node.setNodeChild(42)
        self.assertEqual(self.node.getNodeChild(), 42)
        self.node.setNodeSibling(84)
        self.assertEqual(self.node.getNodeSibling(), 84)
        self.node.setNodeDegree(105)
        self.assertEqual(self.node.getNodeDegree(), 105)
        self.node.setNodeOrdered(True)
        self.assertEqual(self.node.getNodeOrdered(), True)
        self.node.setNodeLevel(32)
        self.assertEqual(self.node.getNodeLevel(), 32)
        self.node.setNodeParentExt(81)
        self.assertEqual(self.node.getNodeParentExt(), 81)
        self.node.setNodeChildExt(56)
        self.assertEqual(self.node.getNodeChildExt(), 56)
        self.node.setNodeSiblingExt(69)
        self.assertEqual(self.node.getNodeSiblingExt(), 69)


if __name__ == '__main__':
    unittest.main()
