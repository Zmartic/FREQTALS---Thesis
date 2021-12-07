import unittest
from freqt.src.be.intimals.freqt.input.ReadFile import *


class MyTestCase(unittest.TestCase):
    def test_str2node(self):
        """
            subtree representation
            input subtree
                 a              #node0
                /\                /\
               b  c        #node1   #node3
              /    \        /          \
             *1     *2   #node2        #node4

            format = (a(b(*1))(c(*2)))
        """
        value_str = "(a(b(*1))(c(*2)))"
        correct_output_label = ['a', 'b', '*1', 'c', '*2']
        correct_output_parent = [-1, 0, 1, 0, 3]
        correct_output_child = [1, 2, -1, 4, -1]
        correct_output_sibling = [-1, 3, -1, -1, -1]
        trans = []
        rd = ReadFile()
        rd.str2node(value_str, trans)
        for i in range(len(trans)):
            self.assertEqual(trans[i].getNodeLabel(), correct_output_label[i])
            self.assertEqual(trans[i].getNodeParent(), correct_output_parent[i])
            self.assertEqual(trans[i].getNodeChild(), correct_output_child[i])
            self.assertEqual(trans[i].getNodeSibling(), correct_output_sibling[i])


if __name__ == '__main__':
    unittest.main()
