#!/usr/bin/env python3

"""
The following code is a translation of the Java implementation of the FREQTALS algorithm.
This algorithm was implemented by PHAM Hoang Son in May 2018.

python implementation: June 2022
   by Quinet Loïc, Arnaud Spits
"""
import os
import sys
import traceback

from freqt.src.be.intimals.freqt.config.Config import Config

from freqt.src.be.intimals.freqt.core.FreqT1Class import FreqT1Class
from freqt.src.be.intimals.freqt.core.FreqT1Class2Step import FreqT1Class2Step
from freqt.src.be.intimals.freqt.core.FreqT2Class import FreqT2Class
from freqt.src.be.intimals.freqt.core.FreqT2Class2Step import FreqT2Class2Step
from freqt.src.be.intimals.freqt.core.FreqTUtil.FreqT_common import FreqT_common


def main(args_list):
    if len(args_list) == 0:
        print("Single-run Freq-T usage:\n" +
              "CONFIG_FILE [MIN_SUPPORT] [INPUT_FOLDER] " +
              "(--class) (--memory [VALUE]) (--debug-file) \n")
    else:
        if args_list[0] == "-multi":
            print("not implemented yet")
        else:
            print("single run")
            single_run(args_list)


def single_run(args_list):
    memory = ""  # args[4]
    debug_file = None  # args[5]
    final_config = None

    final_config = parse_config(args_list)
    if len(args_list) > 3:
        for i in range(3, len(args_list)):
            if args_list[i] == "--memory":
                memory = "-Xmx" + args_list[i + 1]
                i += 1
            if args_list[i] == "--debug-file":
                debug_file = args_list[i]

    # load final configuration;
    config = Config(final_config)

    if config.get_2class():
        if config.get_two_step():
            freqt = FreqT2Class2Step(config)
        else:
            freqt = FreqT2Class(config)
    else:
        if config.get_two_step():
            freqt = FreqT1Class2Step(config)
        else:
            freqt = FreqT1Class(config)

    freqt.run()

    # run forestmatcher to find matches of patterns in source code
    run_forest_matcher(config, memory)

    if not config.get_2class():
        # find common patterns in each cluster
        find_common_pattern(config, freqt.get_grammar(), freqt.get_xml_characters())
        # clean up files
        clean_up(config)

    print("Finished ... \n")


def parse_config(args_list):
    """
     * Initialise the configuration
    :param args_list: list(String), inputs
    :return: Config
    """
    try:
        # create final configuration as used by FreqT
        config_basic = Config(args_list[0])
        prop = config_basic.get_prop()

        input_min_sup = args_list[1]
        prop.setProperty("minSupport", input_min_sup)

        input_fold = args_list[2]
        sep = "/"

        # input data
        input_path = config_basic.get_input_files().replace("\"", "") + sep + input_fold
        prop.setProperty("inputPath", input_path)

        input_path1 = input_path + sep + config_basic.get_input_files1()
        prop.setProperty("inputPath1", input_path1)

        input_path2 = input_path + sep + config_basic.get_input_files2()
        prop.setProperty("inputPath2", input_path2)

        output_dir = config_basic.getOutputFile()
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_prefix = config_basic.getOutputFile().replace("\"", "") + sep \
                        + input_fold.replace(sep, "_") + "_" \
                        + str(input_min_sup)

        # output patterns
        output_patterns = output_prefix + "_patterns.xml"
        if os.path.exists(output_patterns):
            os.remove(output_patterns)
        prop.setProperty("outputPath", output_patterns)

        # create parameters for forest matcher
        output_matches = output_prefix + "_matches.xml"
        if os.path.exists(output_prefix):
            os.remove(output_prefix)
        prop.setProperty("outputMatches", output_matches)

        output_clusters = output_prefix + "_clusters.xml"
        if os.path.exists(output_clusters):
            os.remove(output_clusters)
        prop.setProperty("outputClusters", output_clusters)

        output_matches1 = output_prefix + "_matches_1.xml"
        if os.path.exists(output_prefix):
            os.remove(output_prefix)
        prop.setProperty("outputMatches1", output_matches1)

        output_clusters1 = output_prefix + "_clusters_1.xml"
        if os.path.exists(output_clusters):
            os.remove(output_clusters)
        prop.setProperty("outputClusters1", output_clusters1)

        output_matches2 = output_prefix + "_matches_2.xml"
        if os.path.exists(output_prefix):
            os.remove(output_prefix)
        prop.setProperty("outputMatches2", output_matches2)

        output_clusters2 = output_prefix + "_clusters_2.xml"
        if os.path.exists(output_clusters):
            os.remove(output_clusters)
        prop.setProperty("outputClusters2", output_clusters2)

        output_clusters_temp = output_prefix + "_matches_clusters.xml"
        if os.path.exists(output_clusters_temp):
            os.remove(output_clusters_temp)
        prop.setProperty("outputClustersTemp", output_clusters_temp)

        output_common_patterns = output_prefix + "_patterns_common.xml"
        if os.path.exists(output_common_patterns):
            os.remove(output_common_patterns)
        prop.setProperty("outputCommonPatterns", output_common_patterns)

        output_common_matches = output_prefix + "_matches_common.xml"
        if os.path.exists(output_common_matches):
            os.remove(output_common_matches)
        prop.setProperty("outputCommonMatches", output_common_matches)

        output_common_clusters = output_prefix + "_common_clusters.xml"
        if os.path.exists(output_common_clusters):
            os.remove(output_common_clusters)
        prop.setProperty("outputCommonClusters", output_common_clusters)

        output_common_clusters_matches = output_prefix + "_matches_common_clusters.xml"
        if os.path.exists(output_common_clusters_matches):
            os.remove(output_common_clusters_matches)

        prop.setProperty("minSupportList", "")
        prop.setProperty("inFilesList", "")

        white_file = prop.getProperty("whiteLabelFile")
        prop.setProperty("whiteLabelFile", white_file)
        root_label_file = prop.getProperty("rootLabelFile")
        prop.setProperty("rootLabelFile", root_label_file)
        xml_chara_file = prop.getProperty("xmlCharacterFile")
        prop.setProperty("xmlCharacterFile", xml_chara_file)

        # final configuration as used by FreqT
        final_config = output_prefix + "_config.properties"
        if os.path.exists(final_config):
            os.remove(final_config)
        # save new properties in the final configuration
        with open(final_config, 'w', encoding='utf-8') as f:
            prop.store(f)
        f.close()

        return final_config

    except:
        print("parse args error: " + str(sys.exc_info()[0]) + "\n")
        trace = traceback.format_exc()
        print(trace)


def run_forest_matcher(config, memory):
    """
     run forestmatcher to create matches.xml and clusters.xml
     * @param: config, Config
     * @param: memory, String
    """
    try:
        print("Running forestmatcher ...")
        if config.get_2class():
            command1 = "java -jar ../../../../forestmatcher.jar " \
                       + str(config.get_input_files1()) + " " \
                       + str(config.getOutputFile()) + " " \
                       + str(config.get_output_matches1()) + " " \
                       + str(config.get_output_clusters1())
            os.system(command1)

            command2 = "java -jar ../../../../forestmatcher.jar " \
                       + str(config.get_input_files2()) + " " \
                       + str(config.getOutputFile()) + " " \
                       + str(config.get_output_matches2()) + " " \
                       + str(config.get_output_clusters2())
            os.system(command2)

        else:
            if len(memory) == 0:
                command = "java -jar " + memory + " ../../../../forestmatcher.jar" + " " \
                          + str(config.get_input_files()) + " " \
                          + str(config.getOutputFile()) + " " \
                          + str(config.get_output_matches()) + " " \
                          + str(config.get_output_clusters())
            else:
                command = "java -jar ../../../../forestmatcher.jar " + " " \
                          + str(config.get_input_files()) + " " \
                          + str(config.getOutputFile()) + " " \
                          + str(config.get_output_matches()) + " " \
                          + str(config.get_output_clusters())
            os.system(command)
    except:
        print("forestmatcher error: " + str(sys.exc_info()[0]) + "\n")
        trace = traceback.format_exc()
        print(trace)


def find_common_pattern(config, grammar_dict, xml_characters_dict):
    """
     * @param: config, Config
     * @param: grammar_dict, a dictionary with String as keys and list of String as values
     * @param: xml_characters_dict, dictionary with String as keys and String as values
    """
    pattern = config.get_output_clusters_temp()

    if os.path.exists(pattern):
        # find common patterns in each cluster
        print("Mining common patterns in clusters ... \n")
        output_patterns_temp = config.getOutputFile() + ".txt"
        common = FreqT_common()
        common.FreqT_common(config, grammar_dict, xml_characters_dict)
        common.run(output_patterns_temp,
                   config.get_output_clusters_temp(),
                   config.get_output_common_patterns())

        # find matches for common_patterns
        command = "java -jar ../../../../forestmatcher.jar " \
                  + str(config.get_input_files()) + " " \
                  + str(config.get_output_common_patterns()) + " " \
                  + str(config.get_output_common_matches()) + " " \
                  + str(config.get_output_common_clusters())
        _ = os.system(command)


def clean_up(config):
    print("Cleaning up ... \n")
    if os.path.exists(config.getOutputFile() + ".txt"):
        os.remove(config.getOutputFile() + ".txt")
    if os.path.exists(config.get_output_common_patterns() + ".txt"):
        os.remove(config.get_output_common_patterns() + ".txt")


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
    sys.exit()
