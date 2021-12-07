#!/usr/bin/env python3
from collections import OrderedDict
from typing import Any

from freqt.src.be.intimals.freqt.output.XMLOutput import *
from freqt.src.be.intimals.freqt.util.Initial_Int import *
from freqt.src.be.intimals.freqt.util.Util import *
from freqt.src.be.intimals.freqt.structure.FTArray import *
from freqt.src.be.intimals.freqt.structure.Pattern import *

from freqt.src.be.intimals.freqt.structure.PatternInt import countNode, getPatternStr
from freqt.src.be.intimals.freqt.constraint import Constraint

import time
import collections


class FreqT:

    def __init__(self, _config):

        self._config = _config

        self._transaction_list = list()  # list of list of NodeFreqT
        self._grammar_dict = dict()  # dictionary with String as keys and List of String as value
        self._xmlCharacters_dict = dict()  # dictionary with String as keys and String as value

        # new variables for Integer
        self._labelIndex_dict = dict()  # dictionary with Integer as keys and String as value
        self._grammarInt_dict = dict()  # dictionary with Integer as keys and List of String as value
        self._blackLabelsInt_dict = dict()  # dictionary with Integer as keys and List of Integer as value
        self._whiteLabelsInt_dict = dict()  # dictionary with Integer as keys and List of Integer as value

        # store root labels
        self.rootLabels_set = set()  # set of string
        # store root occurrences of patterns
        self.rootIDs_dict = dict()  # dictionary with Projected as keys and FTArray as value
        # store file ids of patterns
        self.fileIDs_dict = dict()  # dictionary with String as keys and String as value
        # int nbInputFiles;
        self.lineNrs_list = list()  # list of Integer

        self.time_start = -1
        self.timeout = -1
        self.finished = False

        # store maximal patterns
        self.MFP_dict = dict()  # dictionary with FTArray as keys and String as value

        # store k-highest chi-square score patterns
        self.__HSP_dict = dict()  # dictionary with FTArray as keys and Projected as value

        # store transaction ids and their correspond class ids
        self.__transactionClassID_list = list()  # list of Integer
        self.sizeClass1 = -1
        self.sizeClass2 = 1

        self.leafPattern = FTArray()
        self.leafProjected = Projected()
        self.notF_set = set()  # set of FTArray

    # ////////////////////////////////////////////////////////////

    def run(self):
        try:
            # initialization
            self.init_data()
            self.set_starting_time()
            report = self.init_report()

            print("Mining frequent subtrees ...")

            FP1: OrderedDict[FTArray, Projected] = self.build_FP1()

            self.disconnect_not_whitelisted_node()

            # remove node SourceFile because it is not AST node ##
            not_ast_node = FTArray()
            not_ast_node.add(0)
            if not_ast_node in FP1:
                del FP1[not_ast_node]

            # prune FP1 on minimum support
            Constraint.prune(FP1, self._config.getMinSupport(), self._config.getWeighted())

            # expand FP1 to find maximal patterns
            self.expandFP1(FP1)

            if self._config.getTwoStep():
                self.notF_set = set()
                if self._config.get2Class():
                    # group root occurrences from 1000-highest chi-square score patterns
                    self.rootIDs_dict = self.groupRootOcc(self.__HSP_dict)
                # find pattern from root occurrences
                self.expandPatternFromRootIDs(self.rootIDs_dict, report)
            else:
                self.outputPatternInTheFirstStep(self.MFP_dict, self._config, self._grammar_dict, self._labelIndex_dict, self._xmlCharacters_dict, report)
        except:
            e = sys.exc_info()[0]
            print("Error: running Freqt_Int " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def init_data(self):
        """
         * read input data
        """
        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            if self._config.get2Class():
                readXML.readDatabase(self._transaction_list, 1,
                        self._config.getInputFiles1(), self._labelIndex_dict, self.__transactionClassID_list, self._config.getWhiteLabelFile())
                readXML.readDatabase(self._transaction_list, 0,
                        self._config.getInputFiles2(), self._labelIndex_dict, self.__transactionClassID_list, self._config.getWhiteLabelFile())
                self.sizeClass1 = sum(self.__transactionClassID_list)
                self.sizeClass2 = len(self.__transactionClassID_list) - self.sizeClass1
                initGrammar_Str(self._config.getInputFiles1(), self._config.getWhiteLabelFile(), self._grammar_dict, self._config.buildGrammar())
                initGrammar_Str(self._config.getInputFiles2(), self._config.getWhiteLabelFile(), self._grammar_dict, self._config.buildGrammar())
                initGrammar_Int2(self._grammarInt_dict, self._grammar_dict, self._labelIndex_dict)
            else:
                readXML.readDatabase(self._transaction_list, 1,
                        self._config.getInputFiles(), self._labelIndex_dict, self.__transactionClassID_list, self._config.getWhiteLabelFile())
                # create grammar (labels are strings) which is used to print patterns
                initGrammar_Str(self._config.getInputFiles(), self._config.getWhiteLabelFile(), self._grammar_dict, self._config.buildGrammar())
                # create grammar (labels are integers) which is used in the mining process
                initGrammar_Int2(self._grammarInt_dict, self._grammar_dict, self._labelIndex_dict)

            # read root labels (AST Nodes)
            readRootLabel(self._config.getRootLabelFile(), self.rootLabels_set)
            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def disconnect_not_whitelisted_node(self):
        white_labels = ReadXMLInt().read_whiteLabel(self._config.getWhiteLabelFile())
        for trans in self._transaction_list:
            for node in trans:
                label = node.getNodeLabel()
                if label in white_labels:
                    white = white_labels[label]

                    child_id = node.getNodeChild()
                    previous_child = None

                    while child_id != -1:
                        child = trans[child_id]
                        if child.getNodeLabel() in white:
                            if previous_child is None:
                                node.setNodeChild(child_id)
                            else:
                                previous_child.setNodeSibling(child_id)
                            previous_child = child
                        child_id = child.getNodeSibling()

                    if previous_child is None:
                        node.setNodeChild(-1)
        return

    def expandPatternFromRootIDs(self, _rootIDs_dict, report):
        """
         * run the 2nd step to find maximal patterns from groups of root occurrences
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as value
         * @param: report, a open file ready to be writting
        """
        try:
            print("Mining maximal frequent subtrees ... \n")
            self.log(report, "")
            self.log(report, "OUTPUT")
            self.log(report, "===================")

            diff1 = time.time() - self.time_start
            # report the phase 1
            self.log(report, "- Step 1: Mining frequent patterns with max size constraints")
            self.log(report, "\t + running time = " + str(diff1) + "s")
            self.log(report, "\t + root occurrences groups = " + str(len(_rootIDs_dict)))
            # phase 2: find maximal patterns from rootIDs
            self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

            # run the second step
            from freqt.src.be.intimals.freqt.core.FreqT_ext import FreqT_ext
            freqT_ext = FreqT_ext(self._config, self._grammar_dict, self._grammarInt_dict, self._blackLabelsInt_dict,
                                  self._whiteLabelsInt_dict, self._xmlCharacters_dict, self._labelIndex_dict,
                                  self._transaction_list, self.sizeClass1, self.sizeClass2)
            freqT_ext.run_ext(_rootIDs_dict, report)

        except:
            e = sys.exc_info()[0]
            print("expand pattern from root IDs error " + str(e) + "\n")

    def build_FP1(self):
        """
         * build subtrees of size 1 based on root labels
           -> return a dictionary with FTArray as keys and Projected as value
         * @param: trans_list, a list of list of NodeFreqT
         * @param: _rootLabels_set, a list of String
         * @param: _transactionClassID_list, a list of Integer
        """
        FP1: OrderedDict[FTArray, Projected] = collections.OrderedDict()
        trans = self._transaction_list
        try:
            for i in range(len(trans)):
                # get transaction label
                class_id = self.__transactionClassID_list[i]

                for j in range(len(trans[i])):
                    node_label = trans[i][j].getNodeLabel()
                    node_label_id = trans[i][j].getNode_label_int()

                    if node_label in self.rootLabels_set or len(self.rootLabels_set) == 0:
                        if node_label != "" and node_label[0] != '*' and node_label[0].isupper():
                            self.updateCandidates(FP1, node_label_id, class_id, i, j, 0, FTArray(), Location())
        except:
            e = sys.exc_info()[0]
            print("build FP1 error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

        return FP1

    def expandFP1(self, freq1):
        """
         * expand FP1 to find frequent subtrees based on input constraints
         * @param: freq1_dict, a dictionary with FTArray as keys and Projected as value
        """
        # for each label found in FP1, expand it to find maximal patterns
        for key in freq1:
            pattern = FTArray()
            pattern.addAll(key)
            # recursively expand pattern
            self.expandPattern(pattern, freq1[key])

    def expandPattern(self, pattern, projected):
        """
         * expand pattern
         * @param: pattern, FTArray
         * @param: projected, Projected
        """
        try:
            # if it is timeout then stop expand the pattern;
            if self.is_timeout():
                return
            # find candidates of the current pattern
            candidates_dict = self.generateCandidates(projected, self._transaction_list)  # dictionary with FTArray as keys and Projected as values
            # prune candidate based on minSup
            Constraint.prune(candidates_dict, self._config.getMinSupport(), self._config.getWeighted())
            # if there is no candidate then report the pattern and then stop
            if len(candidates_dict) == 0:
                if self.leafPattern.size() > 0:
                    self.addTree(self.leafPattern, self.leafProjected)
                return
            # expand each candidate to the current pattern
            for key in candidates_dict:
                oldSize = pattern.size()
                # add candidate into pattern
                pattern.addAll(key)
                # if the right most node of the pattern is a leaf then keep track this pattern
                if pattern.getLast() < -1:
                    self.keepLeafPattern(pattern, candidates_dict[key])
                # store leaf pattern
                oldLeafPattern = self.leafPattern
                oldLeafProjected = self.leafProjected
                # check obligatory children constraint
                if Constraint.missing_left_obligatory_child(pattern, key, self._grammarInt_dict):
                    # do nothing = don't store pattern
                    pass
                else:
                    # check constraints on maximal number of leafs and real leaf
                    if Constraint.satisfy_max_leaf(pattern, self._config.getMaxLeaf()) or Constraint.is_not_full_leaf(pattern):
                        # store the pattern
                        if self.leafPattern.size() > 0:
                            self.addTree(self.leafPattern, self.leafProjected)
                    else:
                        # continue expanding pattern
                        self.expandPattern(pattern, candidates_dict[key])
                pattern = pattern.subList(0, oldSize)
                self.keepLeafPattern(oldLeafPattern, oldLeafProjected)
        except:
            e = sys.exc_info()[0]
            print("Error: expandPattern " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)
            raise

    def generateCandidates(self, projected, _transaction_list):
        """
         * generate candidates for a pattern
          -> return a dictionary with FTArray as key and Projected as value
         * @param: projected, Projected
         * @param: _transaction_list, list of list of NodeFreqT
        """
        # use oredered dictionary to keep the order of the candidates
        candidates_dict: OrderedDict[FTArray, Projected] = collections.OrderedDict()
        try:
            # find candidates for each location
            depth = projected.getProjectedDepth()
            for occurrences in projected.get_locations():
                # store all locations of the labels in the pattern: this uses more memory but need for checking continuous paragraphs
                #occurrences = projected.getProjectLocation(i)

                classID = occurrences.getClassID()
                id = occurrences.getLocationId()
                pos = occurrences.getLocationPos()
                prefixInt = FTArray()
                # find candidates from left to right
                for d in range(-1, depth):
                    if pos != -1:
                        if d == -1:
                            start = _transaction_list[id][pos].getNodeChild()
                        else:
                            start = _transaction_list[id][pos].getNodeSibling()
                        newDepth = depth - d
                        l = start
                        while l != -1:
                            node_label_int = _transaction_list[id][l].getNode_label_int()
                            self.updateCandidates(candidates_dict, node_label_int, classID, id, l, newDepth, prefixInt, occurrences)
                            l = _transaction_list[id][l].getNodeSibling()
                        if d != -1:
                            pos = _transaction_list[id][pos].getNodeParent()
                        prefixInt.add(-1)
        except:
            e = sys.exc_info()[0]
            print("Error: generate candidates " + str(e) + "\n")
            raise
        return candidates_dict

    def updateCandidates(self, freq1_dict, candidate, classID, id, rightmostPos, depth, prefixInt, initLocations):
        """
         * update candidate locations for two-class data
         * @param: freq1_dict, a dictionary with FTArray as keys and Projected as values
         * @param: candidate, Integer
         * @param: classId, Integer
         * @param: id, Integer
         * @param: rightmostPos, Integer
         * @param: depth, Integer
         * @param: prefixInt, FTArray
         * @param: initLocations, Location
        """
        try:
            newTree = FTArray()
            newTree.addAll(prefixInt)
            newTree.add(candidate)

            # if candidate existed in the freq1 then add its location to projected
            if newTree in freq1_dict:
                freq1_dict[newTree].addProjectLocation(classID, id, rightmostPos, initLocations)
            else:
                # add new location
                projected = Projected()
                projected.set_depth(depth)
                projected.add_location(classID, id, rightmostPos, initLocations)
                freq1_dict[newTree] = projected

        except:
            e = sys.exc_info()[0]
            print("update projected location error " + str(e) + "\n")

    def keepLeafPattern(self, pat, projected):
        """
         * keep track the pattern which has the right-most node is a leaf
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        self.leafPattern = FTArray()
        self.leafPattern.ftarray(pat)
        self.leafProjected = projected

    def addTree(self, pat, projected):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check minsize constraints and right mandatory children
        if Constraint.check_output(pat, self._config.getMinLeaf(), self._config.getMinNode()) and not Constraint.missing_right_obligatory_child(pat, self._grammarInt_dict):
            if self._config.get2Class():
                # check chi-square score
                if Constraint.satisfy_chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getDSScore(), self._config.getWeighted()):
                    if self._config.getTwoStep():
                        # add pattern to the list of 1000-highest chi-square score patterns
                        self.addHighScorePattern(pat, projected, self.__HSP_dict)
                    else:
                        self.addMaximalPattern(pat, projected, self.MFP_dict)
            else:
                if self._config.getTwoStep():
                    # add root occurrences of the current pattern to rootIDs
                    self.addRootIDs(pat, projected, self.rootIDs_dict)
                else:
                    # add pattern to maximal pattern list
                    self.addMaximalPattern(pat, projected, self.MFP_dict)

    def addRootIDs(self, pat, projected, _rootIDs_dict):
        """
         * add root occurrences of pattern to rootIDs
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as values
        """
        try:
            # find root occurrences of current pattern
            util = Util()
            rootOccurrences = util.getStringRootOccurrence(projected)

            # check the current root occurrences existing in the rootID or not
            isAdded = True
            l1 = rootOccurrences.split(";")

            to_remove_list = list()
            for key in _rootIDs_dict:
                rootOccurrence1 = util.getStringRootOccurrence(key)
                l2 = rootOccurrence1.split(";")
                # if l1 is super set of l2 then we don't need to add l1 to rootIDs
                if util.containsAll(l1, l2):
                    isAdded = False
                    break
                else:
                    # if l2 is a super set of l1 then remove l2 from rootIDs
                    if util.containsAll(l2, l1):
                        to_remove_list.append(key)
            for elem in to_remove_list:
                _rootIDs_dict.pop(elem, -1)
            if isAdded:
                # store root occurrences and root label
                rootLabel_int = pat.subList(0, 1)
                _rootIDs_dict[projected] = rootLabel_int
        except:
            e = sys.exc_info()[0]
            print("Error: adding rootIDs " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def addMaximalPattern(self, pat, projected, _MFP_dict):
        """
         * add maximal patterns
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _MFP_dict, a dictionary with FTArray as keys and String as values
        """
        if len(_MFP_dict) != 0:
            for key in self.notF_set:
                if pat == key:
                    return
            for key in _MFP_dict:
                if pat == key:
                    return

            checkSubtree = CheckSubtree()
            to_remove_list = list()
            # check maximal pattern
            for key in _MFP_dict:
                if checkSubtree.checkSubTree(pat, key, self._config) == 1:
                    # pat is a subtree of entry.getKey
                    self.notF_set.add(pat)
                    return
                elif checkSubtree.checkSubTree(pat, key, self._config) == 2:
                    # entry.getKey is a subtree of pat
                    self.notF_set.add(key)
                    to_remove_list.append(key)

            for elem in to_remove_list:
                _MFP_dict.pop(elem, -1)

            # add new maximal pattern to the list
            patternSupport = self.getSupportString(pat, projected)
            _MFP_dict[pat] = patternSupport
        else:
            # add new maximal pattern to the list
            patternSupport = self.getSupportString(pat, projected)
            _MFP_dict[pat] = patternSupport

    def getSupportString(self, pat, projected):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        if self._config.get2Class():
            score = Constraint.chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            ac = Constraint.get2ClassSupport(projected, self._config.getWeighted())
            support = str(ac[0]) + "-" + str(ac[1])
            size = countNode(pat)
            result = support + "," + str(score) + "," + str(size)
        else:
            support = projected.getProjectedSupport()
            wsupport = projected.getProjectedRootSupport()
            size = countNode(pat)
            result = str(support) + "," + str(wsupport) + "," + str(size)
        return result

    def groupRootOcc(self, _HSP_dict):
        """
         * group root occurrences from 1000 patterns in HSP
          -> return a dictionary with Projected as keys and FTArray as values
         * @param: _HSP_dict, a dictionary with FTArray as keys and Projected as value
        """
        _rootIDs_dict = dict()
        for key in _HSP_dict:
            self.addRootIDs(key, _HSP_dict[key], _rootIDs_dict)
        return _rootIDs_dict

    def addHighScorePattern(self, pat, projected, _HSP_dict):
        """
         * add pattern to the list of 1000-highest chi-square score patterns
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _HSP_dict, dictionary with FTArray as keys and Projected as values
        """
        if pat not in _HSP_dict:
            score = Constraint.chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            if len(_HSP_dict) >= self._config.getNumPatterns():
                minScore = self.getMinScore(_HSP_dict)
                if score > minScore:
                    # get pattern which has minScore
                    minPattern = self.getMinScorePattern(_HSP_dict)
                    # remove minScore pattern
                    _HSP_dict.pop(minPattern, -1)
                    # add new pattern
                    _HSP_dict[pat] = projected
            else:
                # add new pattern
                _HSP_dict[pat] = projected

    def getMinScore(self, _HSP_dict):
        """
         * get minimum score of pattern in HSP_dict
         * @param: _HSP_dict: dictionary with FTArray as keys and Projected as values
        """
        score = 1000.0
        for key in _HSP_dict:
            scoreTmp = Constraint.chi_square(_HSP_dict[key], self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            if score > scoreTmp:
                score = scoreTmp
        return score

    def getMinScorePattern(self, _HSP_dict):
        """
         * get a pattern which has minimum chi-square score in the list of patterns
         * @param: _HSP_dict: dictionary with FTArray as key and Projected as values
        """
        score = 1000.0
        minScorerPattern = FTArray()
        for key in _HSP_dict:
            scoreTmp = Constraint.chi_square(_HSP_dict[key], self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            if score > scoreTmp:
                score = scoreTmp
                minScorerPattern.ftarray(key)
        return minScorerPattern

    def outputPatternInTheFirstStep(self, MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict, report):
        """
         * print patterns found in the first step
         * @param: MFP_dict, a dictionary with FTArray as keys and String as value
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as value
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys and Sting as values
         * @param: report, a link to a file ready to be written
        """
        self.log(report, "OUTPUT")
        self.log(report, "===================")
        if self.finished:
            self.log(report, "finished search")
        else:
            self.log(report, "timeout")
        # print pattern to xml file
        self.outputPatterns(MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict)

        end1 = time.time()
        diff1 = end1 - self.time_start
        self.log(report, "+ Maximal patterns = " + str(len(MFP_dict)))
        self.log(report, "+ Running times = " + str(diff1) + " s")
        report.close()

    def outputPatterns(self, MFP_dict, config, grammar_dict, labelIndex_dict, xmlCharacters_dict):
        """
         * print maximal patterns to XML file
         * @param: MFP_dict, dictionary with FTArray as key and String as values
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as values
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys et String as values
        """
        try:
            outFile = config.getOutputFile()
            # create output file to store patterns for mining common patterns
            outputCommonPatterns = open(outFile + ".txt", 'w+')
            # output maximal patterns
            outputMaximalPatterns = XMLOutput(outFile, config, grammar_dict, xmlCharacters_dict)
            pattern = Pattern()
            for key in MFP_dict:
                pat = getPatternStr(key, labelIndex_dict)
                supports = MFP_dict[key]
                outputMaximalPatterns.report_Int(pat, supports)
                outputCommonPatterns.write(pattern.getPatternString1(pat) + "\n")
            outputMaximalPatterns.close()
            outputCommonPatterns.flush()
            outputCommonPatterns.close()

        except:
            e = sys.exc_info()[0]
            print("Print maximal patterns error : " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def set_starting_time(self):
        """
         * set time to begin a run
        """
        self.time_start = time.time()
        self.timeout = self.time_start + self._config.getTimeout()*60 ### add start time to timeout ?
        self.finished = True

    def is_timeout(self):
        """
         * check running time of the algorithm
        """
        if not self._config.getTwoStep():
            if time.time() > self.timeout: ### add start time to timeout ?
                self.finished = False
                return True
        return False

    def init_report(self):
        """
         * create a report
         * @param: config, Config
         * @param: dataSize, Integer
        """
        data_size = len(self._transaction_list)
        report_file = self._config.getOutputFile().replace("\"", "") + "_report.txt"
        report = open(report_file, 'w+')

        self.log(report, "INPUT")
        self.log(report, "===================")
        self.log(report, "- data sources : " + self._config.getInputFiles())
        self.log(report, "- input files : " + str(data_size))
        self.log(report, "- minSupport : " + str(self._config.getMinSupport()))
        report.flush()

        return report

    def get_xml_characters(self):
        """
         * return input xmlCharacters
        """
        return self._xmlCharacters_dict

    def get_grammar(self):
        """
         * return input grammar
        """
        return self._grammar_dict

    def log(self, report, msg):
        """
         * write a string to report
         * @param: report, a file ready to be written
         * @param: msg, String
        """
        report.write(msg + "\n")
        report.flush()
