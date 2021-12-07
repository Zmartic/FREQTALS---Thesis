#!/usr/bin/env python3
import unittest
from freqt.src.be.intimals.freqt.structure.Location import *
from freqt.src.be.intimals.freqt.structure.Projected import *


class ProjectedTest(unittest.TestCase):
    def setUp(self):
        self.projection = Projected()

    def test_init(self):
        self.assertEqual(self.projection.getProjectedDepth(), -1)
        self.assertEqual(self.projection.getProjectedSupport(), -1)
        self.assertEqual(self.projection.getProjectedRootSupport(), -1)
        self.assertEqual(self.projection.getProjectLocationSize(), 0)

    def test_get_set(self):
        self.projection.setProjectedDepth(5)
        self.assertEqual(self.projection.getProjectedDepth(), 5)
        self.projection.setProjectedSupport(9)
        self.assertEqual(self.projection.getProjectedSupport(), 9)
        self.projection.setProjectedRootSupport(42)
        self.assertEqual(self.projection.getProjectedRootSupport(), 42)
        # ajoute 3 location
        self.projection.setProjectLocation(1, 2)
        self.projection.setProjectLocation(42, 25)
        self.projection.setProjectLocation(69, 46)
        self.assertEqual(self.projection.getProjectLocationSize(), 3)
        lo = self.projection.getProjectLocation(1)
        self.assertEqual(lo.getLocationId(), 42)
        self.projection.deleteProjectLocation(1)
        self.assertEqual(self.projection.getProjectLocationSize(), 2)
        # test 2-class method
        projection2 = Projected()
        projection2.setProjectedDepth(5)
        self.assertEqual(projection2.getProjectedDepth(), 5)
        projection2.setProjectedSupport(9)
        self.assertEqual(projection2.getProjectedSupport(), 9)
        projection2.setProjectedRootSupport(42)
        self.assertEqual(projection2.getProjectedRootSupport(), 42)
        # ajoute 3 location 2-Class
        projection2.setProjectLocation2(1, 1, 2)
        projection2.setProjectLocation2(2, 42, 25)
        projection2.setProjectLocation2(3, 69, 46)
        self.assertEqual(projection2.getProjectLocationSize(), 3)
        loca = projection2.getProjectLocation(1)
        self.assertEqual(loca.getLocationId(), 42)
        self.assertEqual(loca.getClassID(), 2)
        projection2.deleteProjectLocation(1)
        self.assertEqual(projection2.getProjectLocationSize(), 2)
        loc = Location()
        self.assertEqual(loc.size(), 0)
        loc2 = Location()
        loc2.location2(loc, 2, 42, 3)
        projection2.addProjectLocation(2, 42, 25, loc2)
        self.assertEqual(projection2.getProjectLocationSize(), 3)
        projection2.addProjectLocation(2, 42, 25, loc2)
        self.assertEqual(projection2.getProjectLocationSize(), 3)


if __name__ == '__main__':
    unittest.main()
