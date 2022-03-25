#!/usr/bin/env python3

import time
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *

import cProfile


class MyTestCase(unittest.TestCase):

    def test_main_one_step(self):
        do_profile = False
        args_main_one_step = ["../../../../test/TestMain/config/design-patterns/builder/config.properties", "2", "builder"]
        # verify the correctness of one-step execution
        args_comparator_pattern_one_step = ["comparator",
                                            "../../../../test/TestMain/Correct_output/design-patterns/builder/builder_2_patterns.xml",
                                            "../../../../test/TestMain/Current_output/design-patterns/builder_2_patterns.xml"]
        if do_profile:
            pr = cProfile.Profile()
            pr.enable()
            main(args_main_one_step)
            pr.disable()
            pr.print_stats()
        else:
            main(args_main_one_step)

        sys.stdout.flush()
        time.sleep(0.01)
        value1 = comparator(args_comparator_pattern_one_step)
        self.assertEqual(value1, "The files are identical")


if __name__ == '__main__':
    unittest.main()
