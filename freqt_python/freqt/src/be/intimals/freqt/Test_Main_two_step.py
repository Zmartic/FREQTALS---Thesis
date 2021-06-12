#!/usr/bin/env python3

import sys
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *


class MyTestCase(unittest.TestCase):

    def test_main_two_step(self):
        args_main_two_step = ["../../../../test/TestMain/config/design-patterns/visitor/config.properties", "2", "visitor"]
        # verify the correctness of two-step execution
        args_comparator_pattern_two_step = ["comparator",
                                   "../../../../test/TestMain/Correct_output/design-patterns/visitor/visitor_2_patterns.xml",
                                   "../../../../test/TestMain/Current_output/design-patterns/visitor_2_patterns.xml"]
        main(args_main_two_step)
        sys.stdout.flush()
        time.sleep(0.01)
        value2 = comparator(args_comparator_pattern_two_step)
        self.assertEqual(value2, "The files are identical")


if __name__ == '__main__':
    unittest.main()
