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
        loc = Location(root_pos=j, right_most_pos=j, loc_id=i, class_id=0)
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
        if occurrences is None:
            loc = Location(pos, pos, loc_id, class_id)
        else:
            loc = Location(occurrences.get_root(), pos, loc_id, class_id)
        found = False
        for location in self.__locations:
            if loc == location:
                found = True
        if not found:
            self.__locations.append(loc)
        #elif len(self.__locations) == 0:
        #    print("this \"if not found\" is NOT always true")

    def add(self, new_loc):
        for location in self.__locations:
            if new_loc == location:
                return
        self.__locations.append(new_loc)

    def __str__(self):
        for i in range(len(self.__locations)):
            print("depth: " + str(self.__depth))
            print("sup: " + str(self.__support))
            print("root_sup: " + str(self.__rootSupport))
            print("locID: " + str(self.__locations[i].getLocationId()))
            print("rootId: " + str(self.__locations[i].getRoot()))
            print("LastId: " + str(self.__locations[i].getLast()))
            print("\n")
