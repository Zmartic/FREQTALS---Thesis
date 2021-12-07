import unittest
from freqt.src.be.intimals.freqt.core.CheckSubtree import *
from freqt.src.be.intimals.freqt.structure.FTArray import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.checkSubtree = CheckSubtree()
        self.big = FTArray()
        self.small = FTArray()

    def test_SubtreePresent(self):
        big = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 4, 7, 8, -152]
        small = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertTrue(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SubtreeAbsent1(self):
        big = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 4, 7, 8, -152]
        small = [51, 52, 201, 69, 39, 4, 7, 8, -26, -1, -1, -1, -1, -1, -1, 101, 102, 4, 7, 8, -132, -1, -1, -1, -1, 103, 65, 4, 7, 8, -93]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SubtreeAbsent2(self):
        big = [51, 52, 201, 69, 39, 4, 7, 8, -26, -1, -1, -1, -1, -1, -1, 101, 102, 4, 7, 8, -132, -1, -1, -1, -1, 103, 65, 4, 7, 8, -93]
        small = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 4, 7, 8, -152]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SubtreeAbsent3(self):
        big = [51, 52, 201, 69, 39, 4, 7, 8, -26, -1, -1, -1, -1, -1, -1, 101, 102, 4, 7, 8, -132, -1, -1, -1, -1, 103, 65, 4, 7, 8, -93]
        small = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 4, 7, 8, -152]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SubtreeAbsent4(self):
        big = [51, 52, 64, 54, 65, 4, 7, 8, -89, -1, -1, -1, -1, -1, -1, -1, 238, 239, 78, 69, 39, 4, 7, 8, -171, -1, -1, -1, -1, -1, -1, 79, -11]
        small = [51, 52, 238, 239, 78, 69, 39, 4, 7, 8, -171, -1, -1, -1, -1, -1, -1, 79, -11, -1, -1, 4, 7, 8, -240]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SkipoverBreak(self):
        big = [51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 55, 56, 65, 54, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 4, 7, 8, -152]
        small = [51, 52, 201, 69, 39, 4, 7, 8, -26, -1, -1, -1, -1, -1, -1, 101, 102, 4, 7, 8, -132, -1, -1, -1, -1, 103, 65, 4, 7, 8, -93]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_SkipoverEnds(self):
        big = [51, 52, 64, 54, 65, 4, 7, 8, -192, -1, -1, -1, -1, -1, -1, -1, 64, 54, 65, 4, 7, 8, -283, -1, -1, -1, -1, 67, 65, 54, 7, 8, -284, -1, -1, -1, -1, 4, 7, 8, -205]
        small = [51, 52, 201, 69, 39, 4, 7, 8, -26, -1, -1, -1, -1, -1, -1, 101, 102, 4, 7, 8, -132, -1, -1, -1, -1, 103, 65, 4, 7, 8, -93]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertFalse(self.checkSubtree.hasSubtree(self.big, self.small))

    def test_Skip2Subtrees(self):
        big = [51, 52, 53, 54, 55, 56, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, 58, -59, -1, -1, 60, 61, -62, -1, -1, -1, -1, -1, 63, 51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 87, 51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 124, 125, -11]
        small = [51, 52, 53, 54, 55, 56, 65, 4, 7, 8, -93, -1, -1, -1, -1, -1, -1, -1, -1, 63, 51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 87, 51, 52, 64, 54, 65, 4, 7, 8, -96, -1, -1, -1, -1, 67, 124, 125, -11]

        self.big.FTArray_Test(big)
        self.small.FTArray_Test(small)

        self.assertTrue(self.checkSubtree.hasSubtree(self.big, self.small))


if __name__ == '__main__':
    unittest.main()
