import unittest

from freqt.src.be.intimals.freqt.input.ReadFileInt import *
from freqt.src.be.intimals.freqt.structure.FTArray import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
             0
            /\
          10 11
          /   \
        20    21
        """
        self.fta = FTArray()
        self.fta.add(0)
        self.fta.add(10)
        self.fta.add(20)
        self.fta.add(-1)
        self.fta.add(-1)
        self.fta.add(11)
        self.fta.add(21)
        self.fta.add(-1)
        self.rdi = ReadFileInt()

    def test_str2node(self):
        correct_output_label = [0, 10, 20, 11, 21]
        correct_output_parent = [-1, 0, 1, 0, 3]
        correct_output_child = [1, 2, -1, 4, -1]
        correct_output_sibling = [-1, 3, -1, -1, -1]
        trans = []
        self.rdi.str2node(self.fta, trans)
        for i in range(len(trans)):
            self.assertEqual(trans[i].getNode_label_int(), correct_output_label[i])
            self.assertEqual(trans[i].getNodeChild(), correct_output_child[i])
            self.assertEqual(trans[i].getNodeParent(), correct_output_parent[i])
            self.assertEqual(trans[i].getNodeSibling(), correct_output_sibling[i])


if __name__ == '__main__':
    unittest.main()
