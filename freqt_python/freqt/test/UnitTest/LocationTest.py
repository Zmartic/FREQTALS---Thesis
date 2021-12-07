import unittest
from freqt.src.be.intimals.freqt.structure.Location import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.loc = Location()

    def test_initialisation(self):
        self.assertEqual(self.loc.getLocationId(), 0)
        self.assertEqual(self.loc.getClassID(), 0)
        self.assertEqual(self.loc.size(), 0)
        self.assertEqual(self.loc.getIntMemory(), None)
        self.assertEqual(self.loc.getMemory(), [None] * self.loc.getChunkSize())

    def test_function(self):
        self.loc.setClassID(4)
        self.assertEqual(self.loc.getClassID(), 4)
        self.loc.setLocationId(44)
        self.assertEqual(self.loc.getLocationId(), 44)
        self.loc.addLocationPos(0)
        self.loc.addLocationPos(1)
        self.loc.addLocationPos(2)
        self.assertEqual(self.loc.getLocationPos(), 2)
        self.loc.addLocationPos(3)
        self.assertEqual(self.loc.getRoot(), 0)
        self.assertEqual(self.loc.getIdPos(), "44-3;")

    def test_location(self):
        loc2 = Location()
        loc2.addLocationPos(100)
        loc2.addLocationPos(400)
        loc2.addLocationPos(200)
        self.loc.location(loc2, 24, 6)
        self.assertEqual(self.loc.getLocationId(), 24)
        self.assertEqual(self.loc.getLast(), 6)
        self.assertEqual(self.loc.getRoot(), 100)

    def test_location2(self):
        loc2 = Location()
        loc2.addLocationPos(700)
        loc2.addLocationPos(500)
        loc2.addLocationPos(361)
        self.loc.location2(loc2, 10, 54, 8)
        self.assertEqual(self.loc.getClassID(), 10)
        self.assertEqual(self.loc.getLocationId(), 54)
        self.assertEqual(self.loc.getLast(), 8)
        self.assertEqual(self.loc.getRoot(), 700)

    def test_location3(self):
        self.loc.location3(88, 34, 16)
        self.assertEqual(self.loc.getClassID(), 88)
        self.assertEqual(self.loc.getLocationId(), 34)
        self.assertEqual(self.loc.getLast(), 16)
        self.loc.addLocationPos(88)
        self.assertEqual(self.loc.getRoot(), 16)
        self.assertEqual(self.loc.getLast(), 88)


if __name__ == '__main__':
    unittest.main()
