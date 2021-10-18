#!/usr/bin/env python3

"""
The following code is a translation of the Java implementation of the FREQTALS algorithm.
This algorithm was implemented by PHAM Hoang Son in May 2018.

python implementation: 12 June 2021
   by Quinet Loïc
"""

from freqt.src.be.intimals.freqt.config.Config import *
from freqt.src.be.intimals.freqt.core.FreqT import *
from freqt.src.be.intimals.freqt.core.FreqT_common import *

import sys
import os
import traceback
import time


def main(args):
    #agg = ["../../../../resources/conf-artifical-data/abstract-data/config.properties", "2", "abstract-data"]
    #agg = ["../../../../resources/conf-artifical-data/design-patterns/config.properties", "2", "visitor"]
    #args = agg

    if len(args) == 0:
        print("Single-run Freq-T usage:\n" +
                "CONFIG_FILE [MIN_SUPPORT] [INPUT_FOLDER] (--class) (--memory [VALUE]) (--debug-file) \n")
    else:
        if args[0] == "-multi":
            # ToDo
            print("not implemented yet")
        else:
            print("single run")
            singleRun(args)

def singleRun(args_list):
    try:
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

        # load final configuration;
        config = Config()
        config.config(finalConfig)

        freqt = FreqT()
        freqt.FreqTInit(config)
        freqt.run()

        # run forestmatcher to find matches of patterns in source code
        runForestMatcher(config, memory)

        if not config.get2Class():
            # find common patterns in each cluster
            findCommonPattern(config, freqt.getGrammar(), freqt.getXmlCharacters())
            # clean up files
            cleanUp(config)

        print("Finished ... \n")
    except:
        e = sys.exc_info()[0]
        print("!!! Error: main " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)
        print("\n")


def parseConfig(args_list):
    try:
        configBasic = Config()
        configBasic.config(args_list[0])
        inputMinSup = args_list[1]
        inputFold = args_list[2]

        sep = "/"
        # create final configuration as used by FreqT
        prop = configBasic.getProp()
        # input data
        inputPath = configBasic.getInputFiles().replace("\"", "") + sep + inputFold

        inputPath1 = inputPath + sep + configBasic.getInputFiles1()
        inputPath2 = inputPath + sep + configBasic.getInputFiles2()

        outputDir = configBasic.getOutputFile()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)

        outputPrefix = configBasic.getOutputFile().replace("\"", "") + sep + inputFold.replace(sep, "_") + "_" + str(inputMinSup)

        # output patterns
        outputPatterns = outputPrefix + "_patterns.xml"
        if os.path.exists(outputPatterns):
            os.remove(outputPatterns)

        # final configuration as used by FreqT
        finalConfig = outputPrefix + "_config.properties"
        if os.path.exists(finalConfig):
            os.remove(finalConfig)

        # create parameters for forest matcher
        outputMatches = outputPrefix + "_matches.xml"
        if os.path.exists(outputPrefix):
            os.remove(outputPrefix)

        outputClusters = outputPrefix + "_clusters.xml"
        if os.path.exists(outputClusters):
            os.remove(outputClusters)

        outputMatches1 = outputPrefix + "_matches_1.xml"
        if os.path.exists(outputPrefix):
            os.remove(outputPrefix)

        outputClusters1 = outputPrefix + "_clusters_1.xml"
        if os.path.exists(outputClusters):
            os.remove(outputClusters)

        outputMatches2 = outputPrefix + "_matches_2.xml"
        if os.path.exists(outputPrefix):
            os.remove(outputPrefix)

        outputClusters2 = outputPrefix + "_clusters_2.xml"
        if os.path.exists(outputClusters):
            os.remove(outputClusters)

        outputClustersTemp = outputPrefix + "_matches_clusters.xml"
        if os.path.exists(outputClustersTemp):
            os.remove(outputClustersTemp)

        outputCommonPatterns = outputPrefix + "_patterns_common.xml"
        if os.path.exists(outputCommonPatterns):
            os.remove(outputCommonPatterns)

        outputCommonMatches = outputPrefix + "_matches_common.xml"
        if os.path.exists(outputCommonMatches):
            os.remove(outputCommonMatches)

        outputCommonClusters = outputPrefix + "_common_clusters.xml"
        if os.path.exists(outputCommonClusters):
            os.remove(outputCommonClusters)

        outputCommonClustersMatches = outputPrefix + "_matches_common_clusters.xml"
        if os.path.exists(outputCommonClustersMatches):
            os.remove(outputCommonClustersMatches)

        # update properties
        prop.setProperty("minSupport", inputMinSup)

        prop.setProperty("outputMatches", outputMatches)
        prop.setProperty("outputClusters", outputClusters)

        prop.setProperty("inputPath", inputPath)
        prop.setProperty("inputPath1", inputPath1)
        prop.setProperty("inputPath2", inputPath2)
        prop.setProperty("outputPath", outputPatterns)
        prop.setProperty("minSupportList", "")
        prop.setProperty("inFilesList", "")

        prop.setProperty("outputMatches1", outputMatches1)
        prop.setProperty("outputClusters1", outputClusters1)

        prop.setProperty("outputMatches2", outputMatches2)
        prop.setProperty("outputClusters2", outputClusters2)

        prop.setProperty("outputClustersTemp", outputClustersTemp)
        prop.setProperty("outputCommonPatterns", outputCommonPatterns)
        prop.setProperty("outputCommonMatches", outputCommonMatches)
        prop.setProperty("outputCommonClusters", outputCommonClusters)

        prop.setProperty("outputClustersTemp", outputClustersTemp)
        prop.setProperty("outputCommonPatterns", outputCommonPatterns)
        prop.setProperty("outputCommonMatches", outputCommonMatches)
        prop.setProperty("outputCommonClusters", outputCommonClusters)
        whitefile = prop.getProperty("whiteLabelFile")
        prop.setProperty("whiteLabelFile", whitefile)
        rootLabelFile = prop.getProperty("rootLabelFile")
        prop.setProperty("rootLabelFile", rootLabelFile)
        xmlCharacfile = prop.getProperty("xmlCharacterFile")
        prop.setProperty("xmlCharacterFile", xmlCharacfile)

        # save new properties in the final configuration
        prop.store(open(finalConfig, 'w', encoding='utf-8'))

        return finalConfig

    except:
        e = sys.exc_info()[0]
        print("parse args error: " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)


"""
 * @param: config, Config
 * @param: memory, String
"""
def runForestMatcher(config, memory):
    # run forestmatcher to create matches.xml and clusters.xml
    try:
        print("Running forestmatcher ...")
        if config.get2Class():
            command1 = "java -jar ../../../../forestmatcher.jar " + str(config.getInputFiles1()) + " " + str(config.getOutputFile())\
                       + " " + str(config.getOutputMatches1()) + " " + str(config.getOutputClusters1())
            os.system(command1)

            command2 = "java -jar ../../../../forestmatcher.jar " + str(config.getInputFiles2()) + " " + str(config.getOutputFile())\
                       + " " + str(config.getOutputMatches2()) + " " + str(config.getOutputClusters2())
            os.system(command2)

        else:
            if len(memory) == 0:
                command = "java -jar " + memory + " ../../../../forestmatcher.jar" + " " + str(config.getInputFiles()) + " " + \
                          str(config.getOutputFile()) + " " + str(config.getOutputMatches()) + " " + str(config.getOutputClusters())
            else:
                command = "java -jar ../../../../forestmatcher.jar " + " " + \
                          str(config.getInputFiles()) + " " + str(config.getOutputFile()) + " " + str(config.getOutputMatches()) \
                          + " " + str(config.getOutputClusters())
            os.system(command)
    except:
        e = sys.exc_info()[0]
        print("forestmatcher error: " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)



"""
 * @param: config, Config
 * @param: grammar_dict, a dictionary with String as keys and list of String as values
 * @param: xmlCharacters_dict, dictionary with String as keys and String as values
"""


def findCommonPattern(config, grammar_dict, xmlCharacters_dict):
    pattern = config.getOutputClustersTemp()
    if os.path.exists(pattern):
        #find common patterns in each cluster
        print("Mining common patterns in clusters ... \n")
        outputPatternsTemp = config.getOutputFile() + ".txt"
        common = FreqT_common()
        common.FreqT_common(config, grammar_dict, xmlCharacters_dict)
        common.run(outputPatternsTemp, config.getOutputClustersTemp(), config.getOutputCommonPatterns())

        #find matches for common_patterns
        command = "java -jar ../../../../forestmatcher.jar " + str(config.getInputFiles()) + " " + \
                  str(config.getOutputCommonPatterns()) + " " + str(config.getOutputCommonMatches()) + " " + \
                  str(config.getOutputCommonClusters())
        value = os.system(command)

def cleanUp(config):
    print("Cleaning up ... \n")
    if os.path.exists(config.getOutputFile() + ".txt"):
        os.remove(config.getOutputFile() + ".txt")
    if os.path.exists(config.getOutputCommonPatterns() + ".txt"):
        os.remove(config.getOutputCommonPatterns()+".txt")


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
    sys.exit()



