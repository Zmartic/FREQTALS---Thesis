#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT2Strategy
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, readXMLCharacter, convert_grammar_keys2int
from freqt.src.be.intimals.freqt.util.Util import Util


class FreqT2Class2Step(FreqTCore):

    def __init__(self, config):
        super().__init__(config)
        self.label_str2int = dict()
        self.sizeClass1 = -1
        self.sizeClass2 = 1

        # Dict of high score pattern
        self.hsp = dict()

    def init_data(self):
        """
         * read input data
        """
        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles1(), self.label_str2int,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            readXML.readDatabase(self._transaction_list, 0,
                                 self._config.getInputFiles2(), self.label_str2int,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            self.sizeClass1 = sum(self._transactionClassID_list)
            self.sizeClass2 = len(self._transactionClassID_list) - self.sizeClass1
            initGrammar_Str(self._config.getInputFiles1(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())
            initGrammar_Str(self._config.getInputFiles2(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

            grammar_int = convert_grammar_keys2int(self._grammar_dict, self.label_str2int)
            self.constraints = FreqT2Strategy(self._config, grammar_int)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def add_tree(self, pat, projected):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check chi-square score
        if self.constraints.satisfy_post_expansion_constraint(pat) and \
                satisfy_chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                                   self._config.getWeighted()):
            self.addHighScorePattern(pat, projected, self.hsp)
            return True
        return False

    def post_mining_process(self, report):
        self.expandPatternFromRootIDs(self.groupRootOcc(self.hsp), report)

    def addHighScorePattern(self, pat, projected, _HSP_dict):
        """
         * add pattern to the list of 1000-highest chi-square score patterns
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _HSP_dict, dictionary with FTArray as keys and Projected as values
        """
        if pat not in _HSP_dict:
            score = chi_square(projected, self.sizeClass1, self.sizeClass2, self._config.getWeighted())
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
            scoreTmp = chi_square(_HSP_dict[key], self.sizeClass1, self.sizeClass2,
                                             self._config.getWeighted())
            if score > scoreTmp:
                score = scoreTmp
        return score

    def getMinScorePattern(self, _HSP_dict):
        """
         * get a pattern which has minimum chi-square score in the list of patterns
         * @param: _HSP_dict: dictionary with FTArray as key and Projected as values
        """
        min_score = 1000.0
        min_scorer_pattern = None
        for key in _HSP_dict:
            score = chi_square(_HSP_dict[key], self.sizeClass1, self.sizeClass2, self._config.getWeighted())
            if min_score > score:
                min_score = score
                min_scorer_pattern = key
        return min_scorer_pattern.copy()

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
                rootLabel_int = pat.sub_list(0, 1)
                _rootIDs_dict[projected] = rootLabel_int
        except:
            e = sys.exc_info()[0]
            print("Error: adding rootIDs " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

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

            # report the phase 1
            self.log(report, "- Step 1: Mining frequent patterns with max size constraints")
            self.log(report, "\t + running time = " + str(self.get_running_time()) + "s")
            self.log(report, "\t + root occurrences groups = " + str(len(_rootIDs_dict)))
            # phase 2: find maximal patterns from rootIDs
            self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

            # run the second step
            from freqt.src.be.intimals.freqt.core.FreqT_ext import FreqT_ext
            freqT_ext = FreqT_ext(self._config, self._grammar_dict, self.constraints.grammar,
                                  None,
                                  None, self._xmlCharacters_dict, self.label_str2int,
                                  self._transaction_list, self.sizeClass1, self.sizeClass2)
            freqT_ext.run_ext(_rootIDs_dict, report)

        except:
            e = sys.exc_info()[0]
            print("expand pattern from root IDs error " + str(e) + "\n")

    def is_timeout(self):
        """
         * check running time of the algorithm
        """
        return False
