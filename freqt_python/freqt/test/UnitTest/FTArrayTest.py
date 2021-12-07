import unittest
from freqt.src.be.intimals.freqt.structure.FTArray import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.fta = FTArray()
        self.other = FTArray()
        self.other.add(6)
        self.other.add(7)
        self.other.add(8)
        self.other.add(9)
        self.other.add(10)
        self.other.add(11)
        self.fta1 = FTArray()
        self.fta1.add(1)
        self.fta1.add(2)
        self.fta1.add(3)
        self.fta1.add(4)
        self.fta1.add(5)

    def test_initialisation(self):
        self.assertEqual(self.fta.getChunkSize(), 512)
        self.assertEqual(self.fta.size(), 0)
        self.assertEqual(self.fta.getMemory(),  [None] * self.fta.getChunkSize())
        self.assertEqual(self.fta.getIntMemory(), None)

    def test_get_and_set(self):
        # add 5 elements
        self.fta.add(1)
        self.fta.add(2)
        self.fta.add(3)
        self.fta.add(4)
        self.fta.add(5)
        self.assertEqual(self.fta.getLast(), 5)
        self.assertEqual(self.fta.get(3), 4)
        self.fta.set(10, 8)
        self.assertEqual(self.fta.get(10), 8)
        self.assertEqual(self.fta.contains(1), True)
        self.assertEqual(self.fta.contains(10), False)
        self.assertEqual(self.fta.indexOf(1), 0)
        self.fta.addAll(self.other)
        self.assertEqual(self.fta.get(11), 6)
        self.assertEqual(self.fta.get(16), 11)
        self.other.add(40000)
        self.other.setIntMemory(15, 88)
        self.assertEqual(self.other.get(15), 88)

    def test_shrink(self):
        # add 5 elements
        self.fta.add(1)
        self.fta.add(2)
        self.fta.add(3)
        self.fta.add(4)
        self.fta.add(5)
        self.assertEqual(self.fta.size(), 5)
        self.fta.shrink(3)
        self.assertEqual(self.fta.size(), 3)

    def test_hash(self):
        # add 5 elements
        self.fta.add(1)
        self.fta.add(2)
        self.fta.add(3)
        self.fta.add(4)
        self.fta.add(5)
        self.assertEqual(self.fta.hashCode(), hash(str(self.fta.getMemory())))

    def test_equal(self):
        l1 = [1, 2, 3]
        l2 = [1, 2]
        l3 = [1, 2, 3]
        l4 = [1, 2, 5]
        self.assertEqual(self.fta.equal(l1, l2), False)
        self.assertEqual(self.fta.equal(l1, l3), True)
        self.assertEqual(self.fta.equal(l1, l4), False)

    def test_equals(self):
        # add 5 elements
        self.fta.add(1)
        self.fta.add(2)
        self.fta.add(3)
        self.fta.add(4)
        self.fta.add(5)
        self.assertEqual(self.fta == self.fta1, True)
        self.assertEqual(self.fta == self.other, False)

    def test_migrate(self):
        copy = self.other.getMemory()
        self.other.migrateMemory()
        self.assertEqual(self.other.getMemory(), None)
        self.assertEqual(self.other.getIntMemory(), copy)

    def test_ftarray(self):
        self.fta.ftarray(self.other)
        self.assertEqual(self.fta.size(), self.other.size())
        self.assertEqual(self.fta.getMemory(), self.other.getMemory())
        self.assertEqual(self.fta.getIntMemory(), self.other.getIntMemory())
        self.other.add(40000)
        self.other.setIntMemory(15, 88)
        self.fta.ftarray(self.other)
        self.assertEqual(self.fta.size(), self.other.size())
        self.assertEqual(self.fta.getMemory(), self.other.getMemory())
        self.assertEqual(self.fta.getIntMemory(), self.other.getIntMemory())

    def test_arraycopy(self):
        l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        l2 = [1, 2, 1]
        l3 = [0] * len(l1)
        self.fta.arrayCopy(l1, 2, l2, 1, 5)
        self.assertEqual(l2, [1, 3, 4, 5, 6, 7])
        self.fta.arrayCopy(l1, 2, l3, 1, 5)
        self.assertEqual(l3, [0, 3, 4, 5, 6, 7, 0, 0, 0, 0])

    def test_copy(self):
        l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.fta.copy(15, l1)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None, None, None, None, None])

    def test_ensure(self):
        # add 5 elements
        self.fta.add(1)
        self.fta.add(2)
        self.fta.add(3)
        self.fta.add(4)
        self.fta.add(5)
        self.fta.ensureSpaceShort(12)
        self.assertEqual(len(self.fta.getMemory()), 512)
        self.fta.ensureSpaceShort(800)
        self.assertEqual(len(self.fta.getMemory()), 1024)
        self.fta.ensureSpaceShort(2000)
        self.assertEqual(len(self.fta.getMemory()), 2001)
        self.other.add(40000)
        self.other.ensureSpaceInt(12)
        self.assertEqual(len(self.other.getIntMemory()), 512)
        self.other.ensureSpaceInt(800)
        self.assertEqual(len(self.other.getIntMemory()), 1024)
        self.other.ensureSpaceInt(2000)
        self.assertEqual(len(self.other.getIntMemory()), 2001)


if __name__ == '__main__':
    unittest.main()
