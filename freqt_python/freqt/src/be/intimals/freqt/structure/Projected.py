#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.Location import *


class Projected:

    def __init__(self):
        self.__depth = -1
        self.__support = -1
        self.__rootSupport = -1
        self.__locations = list()

    def set_depth(self, d):
        self.__depth = d

    def get_depth(self):
        return self.__depth

    def set_support(self, s):
        self.__support = s

    def get_support(self):
        return self.__support

    def set_root_support(self, s):
        self.__rootSupport = s

    def get_root_support(self):
        return self.__rootSupport

    def set_location(self, i, j):
        loc = Location()
        loc.setLocationId(i)
        loc.addLocationPos(j)
        self.__locations.append(loc)

    def get_location(self, i):
        return self.__locations[i]

    def get_locations(self):
        return self.__locations

    def delete_location(self, i):
        self.__locations.pop(i)

    def size(self):
        return len(self.__locations)

    # new procedure for 2 - class data
    def add_location(self, class_id, loc_id, pos, occurrences):
        # check if this location doesn't exist in the locations
        loc = Location()
        loc.location2(occurrences, class_id, loc_id, pos)
        found = False
        for location in self.__locations:
            if loc.getLocationId() == location.getLocationId() and loc.getRoot() == location.getRoot() and loc.getLocationPos() == location.getLocationPos():
                found = True
        if not found:
            self.__locations.append(loc)

    def update_location(self, class_id, loc_id, pos):
        loc = Location()
        loc.setClassID(class_id)
        loc.setLocationId(loc_id)
        loc.addLocationPos(pos)
        self.__locations.append(loc)

    def __str__(self):
        for i in range(len(self.__locations)):
            print("depth: " + str(self.__depth))
            print("sup: " + str(self.__support))
            print("root_sup: " + str(self.__rootSupport))
            print("locID: " + str(self.__locations[i].getLocationId()))
            print("rootId: " + str(self.__locations[i].getRoot()))
            print("LastId: " + str(self.__locations[i].getLast()))
            print("\n")
