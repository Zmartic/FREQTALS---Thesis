#!/usr/bin/env python3

import time
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *

import cProfile

from freqt.src.be.intimals.freqt.core import CheckSubtree
from freqt.src.be.intimals.freqt.core.old.FreqT import FreqT

DO_PROFILE = True
WARM_UP = 5
VALIDATION = 10


class MyTestCase(unittest.TestCase):

    def test_main_one_step(self):
        args_main_one_step = ["../../../../test/TestMain/config/design-patterns/builder/config.properties", "2",
                              "builder"]
        args_custom = ["../../../../test/CustomTest/config.properties", "2", "grammar"]
        single_run(args_main_one_step)


def single_run(args_list):
    memory = ""  # args[4]
    debugFile = None  # args[5]
    finalConfig = None

    finalConfig = parseConfig(args_list)
    if len(args_list) > 3:
        for i in range(3, len(args_list)):
            if args_list[i] == "--memory":
                memory = "-Xmx" + args_list[i + 1]
                i += 1
            if args_list[i] == "--debug-file":
                debugFile = args_list[i]

    config = Config()
    config.config(finalConfig)

    #freqt = FreqT1Class(config)
    freqt = FreqT(config)

    #pr = cProfile.Profile()
    #pr.enable()
    freqt.run()
    #pr.disable()
    #pr.print_stats()

    sys.stdout.flush()
    time.sleep(0.01)

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
