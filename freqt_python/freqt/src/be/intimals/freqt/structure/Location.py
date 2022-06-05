#!/usr/bin/env python3

"""
 * A location is an FTArray plus an identifier of this location
 * first element of FTArray is root location
"""


class Location:

    def __init__(self, root_pos, right_most_pos, loc_id, class_id):
        """
        :root_pos: int, position on the root node
        :right_most_pos: int, position of the right most node
        :loc_id: int, the transaction tha contain the Location
        :class_id: int, class id of the transaction
        """
        self.root_pos = root_pos
        self.right_most_pos = right_most_pos
        self.location_id = loc_id
        self.class_id = class_id

    def get_location_id(self):
        return self.location_id

    def get_position(self):
        return self.right_most_pos

    def get_root(self):
        return self.root_pos

    def get_class_id(self):
        return self.class_id

    def __eq__(self, other):
        if self.location_id != other.location_id:
            return False
        if self.root_pos != other.root_pos:
            return False
        if self.right_most_pos != other.right_most_pos:
            return False
        return True
