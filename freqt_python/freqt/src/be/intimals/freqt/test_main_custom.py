#!/usr/bin/env python3

import time
import unittest

from freqt.src.be.intimals.freqt.Main import *
from freqt.src.be.intimals.freqt.Comparator import *

import cProfile

DO_PROFILE = True
WARM_UP = 0
VALIDATION = 1


class MyTestCase(unittest.TestCase):

    def test_main_one_step(self):
        args_main_one_step = ["../../../../test/TestMain/config/design-patterns/builder/config.properties", "2",
                              "builder"]
        args_antlr1 = ["../../../../test/CustomTest/antlr_meta/config.properties", "2", "grammar/v3"]
        args_antlr2 = ["../../../../test/CustomTest/antlr_meta/config.properties", "3", "grammar/v3"]
        args_antlr3 = ["../../../../test/CustomTest/antlr_meta/config2.properties", "3", "grammar/v3"]
        args_antlr4 = ["../../../../test/CustomTest/antlr_meta/config2.properties", "2", "grammar/v3"]
        single_run(args_antlr4)


def single_run(args_list):
    memory = ""  # args[4]
    debugFile = None  # args[5]
    finalConfig = None

    finalConfig = parse_config(args_list)
    if len(args_list) > 3:
        for i in range(3, len(args_list)):
            if args_list[i] == "--memory":
                memory = "-Xmx" + args_list[i + 1]
                i += 1
            if args_list[i] == "--debug-file":
                debugFile = args_list[i]

    config = Config(finalConfig)

    if config.get_2class():
        if config.get_two_step():
            print("doing 2classes 2steps")
            freqt = FreqT2Class2Step(config)
        else:
            print("doing 2classes 1step")
            freqt = FreqT2Class(config)
    else:
        if config.get_two_step():
            print("doing 1class 2steps")
            freqt = FreqT1Class2Step(config)
        else:
            print("doing 1class 1step")
            freqt = FreqT1Class(config)

    pr = cProfile.Profile()
    pr.enable()
    freqt.run()
    pr.disable()
    pr.print_stats()

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
