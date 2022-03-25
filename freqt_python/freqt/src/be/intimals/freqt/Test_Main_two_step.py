#!/usr/bin/env python3

import time
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *

import cProfile


class MyTestCase(unittest.TestCase):

    def test_main_two_step(self):
        do_profile = False
        args_main_two_step = ["../../../../test/TestMain/config/design-patterns/visitor/config.properties", "2", "visitor"]
        # verify the correctness of two-step execution
        args_comparator_pattern_two_step = ["comparator",
                                   "../../../../test/TestMain/Correct_output/design-patterns/visitor/visitor_2_patterns.xml",
                                   "../../../../test/TestMain/Current_output/design-patterns/visitor_2_patterns.xml"]
        if do_profile:
            pr = cProfile.Profile()
            pr.enable()
            main(args_main_two_step)
            pr.disable()
            pr.print_stats()
        else:
            main(args_main_two_step)

        sys.stdout.flush()
        time.sleep(0.01)
        value2 = comparator(args_comparator_pattern_two_step)
        self.assertEqual(value2, "The files are identical")


if __name__ == '__main__':
    unittest.main()
