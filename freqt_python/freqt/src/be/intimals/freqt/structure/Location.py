#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.FTArray import *

"""
 * A location is an FTArray plus an identifier of this location
 * first element of FTArray is root location
"""


class Location(FTArray):
    #new variable for 2-class data
    classID = 0
    locationId = 0

    def __init__(self):
        super().__init__()
        self.classID = 0
        self.locationId = 0

    def getLocationId(self):
        return self.locationId

    def setLocationId(self, a):
        self.locationId = a

    def addLocationPos(self, x):
        self.add(x)

    def getLocationPos(self):
        return self.get_last()

    def getRoot(self):
        return self.get(0)

    def getIdPos(self):
        return str(self.locationId) + "-" + str(self.get_last()) + ";"

    def location(self, other, id, pos):
        self.ftarray(other)
        self.locationId = id
        self.add(pos)

    # new procedure for 2-class data
    def location2(self, other, classId, id, pos):
        self.ftarray(other)
        self.classID = classId
        self.locationId = id
        self.add(pos)

    def location3(self, classId, id, pos):
        self.classID = classId
        self.locationId = id
        self.add(pos)

    def getClassID(self):
        return self.classID

    def setClassID(self, a):
        self.classID = a

