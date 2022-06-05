#!/usr/bin/env python3

import sys
import traceback
from pyjavaproperties import Properties


class Config:

    def __init__(self, config_path):
        """ init """
        try:
            self.__prop = Properties()
            with open(config_path) as file:
                self.__prop.load(file)
            file.close()
        except:
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            raise

    def get_2class(self):
        """
        :return: whether data have 2 classes
        """
        return self.__prop.getProperty("2Class") is not None \
               and self.__prop.getProperty("2Class").lower() == "true"

    def get_ds_score(self):
        """
        :return: DSScore
        """
        try:
            return float(self.__prop.getProperty("minDSScore"))
        except:
            print(sys.exc_info()[0])
            raise

    def keep_highest_score(self):
        """ unused """
        return self.__prop.getProperty("keepHighestScore") is not None \
               and self.__prop.getProperty("keepHighestScore").lower() == "true"

    def get_num_patterns(self):
        """
        :return: the number of patterns
        """
        return int(self.__prop.getProperty("numPatterns"))

    def get_input_files1(self):
        """
        :return: class 1 input files
        """
        if self.__prop.getProperty("inputPath1") is None:
            return ""
        return self.__prop.getProperty("inputPath1")

    def get_input_files2(self):
        """
        :return: class 2 input files
        """
        if self.__prop.getProperty("inputPath2") is None:
            return ""
        return self.__prop.getProperty("inputPath2")

    def get_output_matches(self):
        """
        :return: output matches
        """
        if self.__prop.getProperty("outputMatches") is None:
            return ""
        return self.__prop.getProperty("outputMatches")

    def get_output_clusters(self):
        """
        :return: output clusters
        """
        if self.__prop.getProperty("outputClusters") is None:
            return ""
        return self.__prop.getProperty("outputClusters")

    def get_output_clusters_temp(self):
        """
        :return: output clusters temp
        """
        if self.__prop.getProperty("outputClustersTemp") is None:
            return ""
        return self.__prop.getProperty("outputClustersTemp")

    def get_output_common_patterns(self):
        """
        :return: output common patterns
        """
        if self.__prop.getProperty("outputCommonPatterns") is None:
            return ""
        return self.__prop.getProperty("outputCommonPatterns")

    def get_output_common_matches(self):
        """
        :return: output common matches
        """
        if self.__prop.getProperty("outputCommonMatches") is None:
            return ""
        return self.__prop.getProperty("outputCommonMatches")

    def get_output_common_clusters(self):
        """
        :return: output common clusters
        """
        if self.__prop.getProperty("outputCommonClusters") is None:
            return ""
        return self.__prop.getProperty("outputCommonClusters")

    def get_output_matches1(self):
        """
        :return: output matches class 1
        """
        if self.__prop.getProperty("outputMatches1") is None:
            return ""
        return self.__prop.getProperty("outputMatches1")

    def get_output_clusters1(self):
        """
        :return: output clusters class 1
        """
        if self.__prop.getProperty("outputClusters1") is None:
            return ""
        return self.__prop.getProperty("outputClusters1")

    def get_output_matches2(self):
        """
        :return: output matches class 2
        """
        if self.__prop.getProperty("outputMatches2") is None:
            return ""
        return self.__prop.getProperty("outputMatches2")

    def get_output_clusters2(self):
        """
        :return: output clusters class 2
        """
        if self.__prop.getProperty("outputClusters2") is None:
            return ""
        return self.__prop.getProperty("outputClusters2")

    def get_weighted(self):
        """
        :return: whether we prune using weighted support
        """
        return self.__prop.getProperty("weighted") is not None \
               and self.__prop.getProperty("weighted").lower() == "true"

    #######

    def get_two_step(self):
        """
        :return: whether we are using the 2 steps algorithm
        """
        return self.__prop.getProperty("twoStep") is not None \
               and self.__prop.getProperty("twoStep") == "true"

    def get_filter(self):
        """ unused """
        return self.__prop.getProperty("filter") is not None \
               and self.__prop.getProperty("filter") == "true"

    def get_abstract_leaves(self):
        """
        :return: abstract leaves configuration
        """
        return self.__prop.getProperty("abstractLeafs") is not None \
               and self.__prop.getProperty("abstractLeafs") == "true"

    def get_timeout(self):
        """
        :return: timeout
        """
        if self.__prop.getProperty("timeout") is None:
            return sys.maxsize
        return float(self.__prop.getProperty("timeout"))

    def get_prop(self):
        """
        :return: properties
        """
        return self.__prop

    def build_grammar(self):
        """
        :return: build grammar configuration
        """
        return self.__prop.getProperty("buildGrammar") is not None \
               and self.__prop.getProperty("buildGrammar") == "true"

    def get_grammar_file(self):
        """ unused """
        return self.__prop.getProperty("grammarFile")

    def get_root_label_file(self):
        """
        :return: root label file
        """
        return self.__prop.getProperty("rootLabelFile")

    def get_white_label_file(self):
        """
        :return: white label file
        """
        return self.__prop.getProperty("whiteLabelFile")

    def get_xml_character_file(self):
        """
        :return: xml character file
        """
        return self.__prop.getProperty("xmlCharacterFile")

    def get_input_files(self):
        """
        :return: input files
        """
        return self.__prop.getProperty("inputPath")

    def get_output_file(self):
        """
        :return: output file
        """
        if self.__prop.getProperty("outputPath") is None:
            return ""
        return self.__prop.getProperty("outputPath")

    def get_min_support(self):
        """
        :return: minimum support threshold
        """
        return int(self.__prop.getProperty("minSupport"))

    def get_min_node(self):
        """
        :return: minimum number of node
        """
        return int(self.__prop.getProperty("minNode"))

    def get_max_node(self):
        """ unused """
        return int(self.__prop.getProperty("maxNode"))

    def get_min_leaf(self):
        """
        :return: minimum number of leaf
        """
        return int(self.__prop.getProperty("minLeaf"))

    def get_max_leaf(self):
        """
        :return: maximum number of leaf
        """
        return int(self.__prop.getProperty("maxLeaf"))

    def post_process(self):
        """
        :return: post process configuration
        """
        return self.__prop.getProperty("pos") is not None \
               and self.__prop.getProperty("pos").lower() == "true"

    def get_min_support_list(self):
        """
         :return: a list of minimum-support values
         (only used when executing multiple Freq-T runs in parallel)
        """
        min_sup_list = self.__prop.getProperty("minSupportList")
        result = []
        for elem in min_sup_list.split(","):
            result.append(int(elem))
        return result

    def get_input_files_list(self):
        """
         :return: a list of input folders
         (only used when executing multiple Freq-T runs in parallel)
        """
        in_files_list = self.__prop.getProperty("inFilesList")
        return in_files_list.split(",")
