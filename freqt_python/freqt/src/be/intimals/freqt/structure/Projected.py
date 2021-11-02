#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.Location import *


class Projected:

    def __init__(self):
        self.__depth = -1
        self.__support = -1
        self.__rootSupport = -1
        self.__locations = list()

    def setProjectedDepth(self, d):
        self.__depth = d

    def getProjectedDepth(self):
        return self.__depth

    def setProjectedSupport(self, s):
        self.__support = s

    def getProjectedSupport(self):
        return self.__support

    def setProjectedRootSupport(self, s):
        self.__rootSupport = s

    def getProjectedRootSupport(self):
        return self.__rootSupport

    def setProjectLocation(self, i, j):
        loc = Location()
        loc.setLocationId(i)
        loc.addLocationPos(j)
        self.__locations.append(loc)

    def getProjectLocation(self, i):
        return self.__locations[i]

    def getProjectLocations(self):
        return self.__locations

    def getProjectedLocationList(self):
        for i in range(len(self.__locations)):
            print("depth: " + str(self.__depth))
            print("sup: " + str(self.__support))
            print("root_sup: " + str(self.__rootSupport))
            print("locID: " + str(self.__locations[i].getLocationId()))
            print("rootId: " + str(self.__locations[i].getRoot()))
            print("LastId: " + str(self.__locations[i].getLast()))
            print("\n")

    def deleteProjectLocation(self, i):
        self.__locations.pop(i)

    def getProjectLocationSize(self):
        return len(self.__locations)

    # new procedure for 2 - class data
    def addProjectLocation(self, classID, id, pos, occurrences):
        # check if this location doesn't exist in the locations
        loc = Location()
        loc.location2(occurrences, classID, id, pos)
        found = False
        for location in self.__locations:
            if loc.getLocationId() == location.getLocationId() and loc.getRoot() == location.getRoot() and loc.getLocationPos() == location.getLocationPos():
                found = True
        if not found:
            self.__locations.append(loc)

    def setProjectLocation2(self, classID, i, j):
        loc = Location()
        loc.setClassID(classID)
        loc.setLocationId(i)
        loc.addLocationPos(j)
        self.__locations.append(loc)
