#!/usr/bin/env python3
import unittest
from freqt.src.be.intimals.freqt.structure.Location import *
from freqt.src.be.intimals.freqt.structure.Projected import *


class ProjectedTest(unittest.TestCase):
    def setUp(self):
        self.projection = Projected()

    def test_init(self):
        self.assertEqual(self.projection.get_depth(), -1)
        self.assertEqual(self.projection.get_support(), -1)
        self.assertEqual(self.projection.get_root_support(), -1)
        self.assertEqual(self.projection.size(), 0)

    def test_get_set(self):
        self.projection.set_depth(5)
        self.assertEqual(self.projection.get_depth(), 5)
        self.projection.set_support(9)
        self.assertEqual(self.projection.get_support(), 9)
        self.projection.set_root_support(42)
        self.assertEqual(self.projection.get_root_support(), 42)
        # ajoute 3 location
        self.projection.set_location(1, 2)
        self.projection.set_location(42, 25)
        self.projection.set_location(69, 46)
        self.assertEqual(self.projection.size(), 3)
        lo = self.projection.get_location(1)
        self.assertEqual(lo.getLocationId(), 42)
        self.projection.delete_location(1)
        self.assertEqual(self.projection.size(), 2)
        # test 2-class method
        projection2 = Projected()
        projection2.set_depth(5)
        self.assertEqual(projection2.get_depth(), 5)
        projection2.set_support(9)
        self.assertEqual(projection2.get_support(), 9)
        projection2.set_root_support(42)
        self.assertEqual(projection2.get_root_support(), 42)
        # ajoute 3 location 2-Class
        projection2.update_location(1, 1, 2)
        projection2.update_location(2, 42, 25)
        projection2.update_location(3, 69, 46)
        self.assertEqual(projection2.size(), 3)
        loca = projection2.get_location(1)
        self.assertEqual(loca.getLocationId(), 42)
        self.assertEqual(loca.getClassID(), 2)
        projection2.delete_location(1)
        self.assertEqual(projection2.size(), 2)
        loc = Location()
        self.assertEqual(loc.size(), 0)
        loc2 = Location()
        loc2.location2(loc, 2, 42, 3)
        projection2.add_location(2, 42, 25, loc2)
        self.assertEqual(projection2.size(), 3)
        projection2.add_location(2, 42, 25, loc2)
        self.assertEqual(projection2.size(), 3)


if __name__ == '__main__':
    unittest.main()
