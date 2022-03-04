#!/usr/bin/env python3

import sys
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *

import cProfile

from freqt.src.be.intimals.freqt.core import CheckSubtree

DO_PROFILE = True
WARM_UP = 5
VALIDATION = 10


class MyTestCase(unittest.TestCase):

    def test_main_one_step(self):
        args_main_one_step = ["../../../../test/TestMain/config/design-patterns/builder/config.properties", "2",
                              "builder"]
        test_main(args_main_one_step)


def test_main(args):

    # -- Warm up --
    for _ in range(WARM_UP):
        main(args)
        sys.stdout.flush()
        time.sleep(0.01)

    # -- Test --
    if DO_PROFILE:
        pr = cProfile.Profile()
        pr.enable()

        for _ in range(VALIDATION):
            main(args)
            sys.stdout.flush()
            time.sleep(0.01)

        pr.disable()
        pr.print_stats(sort='ncalls')
        time.sleep(0.01)

    else:
        for _ in range(WARM_UP):
            main(args)
            sys.stdout.flush()
            time.sleep(0.01)


if __name__ == '__main__':
    unittest.main()
