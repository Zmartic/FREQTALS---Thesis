#!/usr/bin/env python3

"""
 * A location is an FTArray plus an identifier of this location
 * first element of FTArray is root location
"""
from freqt.src.be.intimals.freqt.structure.Location import Location


class LocationC(Location):

    def __init__(self, root_pos, right_most_pos, loc_id, class_id):
        """
        :class_id: int, class id of the transaction
        """
        super().__init__(root_pos, right_most_pos, loc_id, class_id)
        self.class_id = class_id

    def get_class_id(self):
        return self.class_id
