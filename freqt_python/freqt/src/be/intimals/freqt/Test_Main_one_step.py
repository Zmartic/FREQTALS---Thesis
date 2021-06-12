#!/usr/bin/env python3

import sys
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *


class MyTestCase(unittest.TestCase):

    def test_main_one_step(self):
        args_main_one_step = ["../../../../test/TestMain/config/design-patterns/builder/config.properties", "2", "builder"]
        # verify the correctness of one-step execution
        args_comparator_pattern_one_step = ["comparator",
                                            "../../../../test/TestMain/Correct_output/design-patterns/builder/builder_2_patterns.xml",
                                            "../../../../test/TestMain/Current_output/design-patterns/builder_2_patterns.xml"]
        main(args_main_one_step)
        sys.stdout.flush()
        time.sleep(0.01)
        value1 = comparator(args_comparator_pattern_one_step)
        self.assertEqual(value1, "The files are identical")


if __name__ == '__main__':
    unittest.main()
