#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.Location import *


class Projected:

    def __init__(self):
        """
        :depth: int, ...
        :support: int, total number of transaction represented in Projected
        :rootSupport: int, total number of location with distinct root represented in Projected
        """
        self.__depth = -1
        self.__support = -1
        self.__rootSupport = -1
        self.__locations = list()

    def set_depth(self, depth):
        self.__depth = depth

    def get_depth(self):
        return self.__depth

    def set_support(self, support):
        self.__support = support

    def get_support(self):
        return self.__support

    def set_root_support(self, rootSupport):
        self.__rootSupport = rootSupport

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

    def compute_support(self):
        self.__support = len({loc.get_location_id() for loc in self.__locations})
        return self.__support

    def compute_root_support(self):
        self.__rootSupport = len({(loc.get_location_id(), loc.get_root()) for loc in self.__locations})
        return self.__rootSupport

    # new procedure for 2 - class data
    def add_location(self, class_id, loc_id, pos, occurrences):
        # check if this location doesn't exist in the locations
        if occurrences is None:
            loc = Location(pos, pos, loc_id, class_id)
        else:
            loc = Location(occurrences.get_root(), pos, loc_id, class_id)

        if loc not in self.__locations:  # always true ?
            self.__locations.append(loc)

    def add(self, new_loc):
        if new_loc not in self.__locations:  # always true ?
            self.__locations.append(new_loc)

    def __str__(self):
        for i in range(len(self.__locations)):
            print("depth: " + str(self.__depth))
            print("sup: " + str(self.__support))
            print("root_sup: " + str(self.__rootSupport))
            print("locID: " + str(self.__locations[i].get_location_id()))
            print("rootId: " + str(self.__locations[i].get_root()))
            print("LastId: " + str(self.__locations[i].get_position()))
            print("\n")
        return ""
