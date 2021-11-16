#!/usr/bin/env python3
import copy


class FTArray:

    """
    We store data in memory, until a storage of a datum outside the range of short happens.
    Then we migrate to intMemory, setting memory to null, and keep using intMemory forever.
    """
    __chunkSize = 512

    def __init__(self):
        self._firstFree = 0
        self._memory = [None] * self.__chunkSize
        self._intMemory = None

    def migrateMemory(self):
        self._intMemory = [None] * len(self._memory)
        for i in range(0, self._firstFree):
            self._intMemory[i] = self._memory[i]
        self._memory = None

    """
    Create an FTArray from an array of integers.!! THIS IS ONLY FOR TESTS !!
    * @ param testData
    """

    def FTArray_Test(self, testData):
        for datum in testData:
            self.add(datum)

    """
     * @param: source, FTArray
    """
    def ftarray(self, source):
        self._firstFree = source.size()
        if source.getMemory() is not None:
            self._memory = copy.deepcopy(source.getMemory())
        else:
            self._memory = None
            self._intMemory = copy.deepcopy(source.getIntMemory())

    def get(self, i):
        if i < 0 or i >= self._firstFree:
            raise Exception("Out of bounds access in FTArray.get(i). i is " + str(i) + ", size is " + str(self._firstFree))
        if self._memory is not None:
            return self._memory[i]
        return self._intMemory[i]

    def getLast(self):
        if self._memory is not None:
            return self._memory[self._firstFree - 1]
        return self._intMemory[self._firstFree - 1]

    def set(self, index, element):
        if self._memory is not None and (element > 32767 or element < -32768):
            self.migrateMemory()
        if self._memory is not None:
            self.ensureSpaceShort(index)
            self._memory[index] = element
        else:
            self.ensureSpaceInt(index)
            self._intMemory[index] = element
        if index >= self._firstFree:
            self._firstFree = index + 1

    def setIntMemory(self, index, element):
        self.ensureSpaceInt(index)
        self._intMemory[index] = element
        if index >= self._firstFree:
            self._firstFree = index + 1

    def arrayCopy(self, src, srcPos, dest, destPos, length):
        for i in range(length):
            if i + destPos < len(dest):
                dest[i + destPos] = src[i + srcPos]
            else:
                dest.append(src[i + srcPos])

    def add(self, element):
        self.set(self._firstFree, element)

    """
     * @param: other, FTArray
    """
    def addAll(self, other):
        if self._memory is not None and other.getMemory() is not None:
            newff = self._firstFree + other.size()
            self.ensureSpaceShort(newff)
            self.arrayCopy(other.getMemory(), 0, self._memory, self._firstFree, other.size())
            self._firstFree = newff
        else:
            if self._memory is not None:
                self.migrateMemory()
            if other.getMemory() is not None:
                for i in range(0, other.size()):
                    self.setIntMemory(self._firstFree, other.getMemory()[i])
            else:
                newff = self._firstFree + other.size()
                self.ensureSpaceInt(newff)
                self.arrayCopy(other.getIntMemory(), 0, self._intMemory, self._firstFree, other.size())
                self._firstFree = newff

    # this could be optimised to revert from intMemory to memory if all values fit
    # but unsure whether this is worthwhile - - next additions could need intMemory again
    def subList(self, start, stop):
        result = FTArray()
        result._firstFree = stop - start
        if self._memory is not None:
            result.ensureSpaceShort(result._firstFree)
            self.arrayCopy(self._memory, start, result._memory, 0, result._firstFree)
        else:
            result._memory = None
            result._intMemory = [None] * self.__chunkSize
            result.ensureSpaceInt(result._firstFree)
            self.arrayCopy(self._intMemory, start, result._intMemory, 0, result._firstFree)
        return result

    """
     * @param: newSize, Integer
    """
    def shrink(self, newSize):
        self._firstFree = newSize

    """
     * @param: list1, a list <T>
     * @param: list2, a list <T>
    """
    def equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        else:
            for i in range(len(list1)):
                if list1[i] != list2[i]:
                    return False
        return True

    def __eq__(self, other):
        if not isinstance(other, FTArray):
            return False
        if self._firstFree != other._firstFree:
            return False
        if self._memory is not None and other._memory is not None:
            return self.equal(self._memory, other._memory)
        if self._memory is None and other._memory is None:
            return self.equal(self._intMemory, other._intMemory)
        if self._memory is not None:
            for i in range(0, self._firstFree):
                if self._memory[i] != other._intMemory[i]:
                    return False
        else:
            for i in range(0, self._firstFree):
                if self._intMemory[i] != other._memory[i]:
                    return False
        return True

    def __hash__(self):     # cannot hash a list so transform it into a string before
        if self._memory is not None:
            return hash(str(self._memory))
        return hash(str(self._intMemory))

    def size(self):
        return self._firstFree

    """
     * @param: element, Integer
     return True if the element is contains in the FTArray
    """
    def contains(self, element):
        return self.indexOf(element) != -1

    """
     * @param: element, Integer
     return the position of the element
    """
    def indexOf(self, element):
        if self._memory is not None:
            for i in range(0, self._firstFree):
                if element == self._memory[i]:
                    return i
        else:
            for i in range(0, self._firstFree):
                if element == self._intMemory[i]:
                    return i
        return -1

    """
     * @param: lengthDst, Integer, the new length
     * @param: memorySrc, Integer, the place of the last element to copy
    """
    def copy(self, lengthDst, memorySrc):
        memoryDst = [None] * lengthDst
        for i in range(len(memorySrc)):
            memoryDst[i] = memorySrc[i]
        return memoryDst

    """
     * @param: index, Integer
    """
    def ensureSpaceShort(self, index):
        if index >= len(self._memory):
            speculativeLength = len(self._memory) + self.__chunkSize
            if index >= speculativeLength:
                newLength = index + 1
            else:
                newLength = speculativeLength
            memoryIntermediate = self.copy(newLength, self._memory)
            self._memory = copy.deepcopy(memoryIntermediate)

    """
     * @param: index, Integer
    """
    def ensureSpaceInt(self, index):
        if index >= len(self._intMemory):
            speculativeLength = len(self._intMemory) + self.__chunkSize
            if index >= speculativeLength:
                newLength = index + 1
            else:
                newLength = speculativeLength
            memoryIntermediate = self.copy(newLength, self._intMemory)
            self._intMemory = copy.deepcopy(memoryIntermediate)

    def getMemory(self):
        return self._memory

    def getIntMemory(self):
        return self._intMemory

    def getChunkSize(self):
        return self.__chunkSize

