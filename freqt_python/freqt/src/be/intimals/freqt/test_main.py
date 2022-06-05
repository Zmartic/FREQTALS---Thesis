#!/usr/bin/env python3
import sys
import time
import unittest
import cProfile

from freqt.src.be.intimals.freqt.Comparator import comparator
from freqt.src.be.intimals.freqt.Main import main

TEST_DIR_CONFIG = "../../../../test/TestMain/config/"
TEST_DIR_CORRECT = "../../../../test/TestMain/Correct_output/"
TEST_DIR_OUT = "../../../../test/TestMain/Current_output/"


class MyTestCase(unittest.TestCase):
    """
        Unit tests for the FREQTALS algorithm
    """

    def test_main_one_step(self):
        """
         runs FreqT1Class
        """
        do_profile = False
        args_main = [TEST_DIR_CONFIG + "design-patterns/builder/config.properties", "2", "builder"]
        # verify the correctness of one-step execution
        args_comparator = ["comparator",
                           TEST_DIR_CORRECT + "design-patterns/builder/builder_2_patterns.xml",
                           TEST_DIR_OUT + "design-patterns/builder_2_patterns.xml"]
        if do_profile:
            profile = cProfile.Profile()
            profile.enable()
            main(args_main)
            profile.disable()
            profile.print_stats()
        else:
            main(args_main)

        sys.stdout.flush()
        time.sleep(0.01)
        value = comparator(args_comparator)
        self.assertEqual(value, "The files are identical")

    def test_main_two_step(self):
        """
         runs FreqT1Class2Step
        """
        do_profile = False
        args_main = [TEST_DIR_CONFIG + "design-patterns/visitor/config.properties", "2", "visitor"]
        # verify the correctness of two-step execution
        args_comparator = ["comparator",
                           TEST_DIR_CORRECT + "design-patterns/visitor/visitor_2_patterns.xml",
                           TEST_DIR_OUT + "design-patterns/visitor_2_patterns.xml"]
        if do_profile:
            profile = cProfile.Profile()
            profile.enable()
            main(args_main)
            profile.disable()
            profile.print_stats()
        else:
            main(args_main)

        sys.stdout.flush()
        time.sleep(0.01)
        value = comparator(args_comparator)
        self.assertEqual(value, "The files are identical")


if __name__ == '__main__':
    unittest.main()
