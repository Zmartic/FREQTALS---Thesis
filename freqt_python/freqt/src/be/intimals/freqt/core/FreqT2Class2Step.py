#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import satisfy_chi_square, chi_square
from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT1Strategy
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.input.Initial_Int import convert_grammar_label2int, \
    read_XML_character, init_grammar, read_white_label


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
        white_label = read_white_label(self._config.getWhiteLabelFile())

        # remove black labels when reading ASTs
        self._transaction_list = list()
        self._transactionClassID_list = list()
        self.label_decoder = dict()
        readXML = ReadXMLInt()
        readXML.readDatabase(self._transaction_list, 1, self._config.getInputFiles1(), self.label_decoder,
                             self._transactionClassID_list, white_label)
        readXML.readDatabase(self._transaction_list, 0, self._config.getInputFiles2(), self.label_decoder,
                             self._transactionClassID_list, white_label)
        self.sizeClass1 = sum(self._transactionClassID_list)
        self.sizeClass2 = len(self._transactionClassID_list) - self.sizeClass1

        # init grammar
        self._grammar_dict = dict()
        init_grammar(self._config.getInputFiles1(), white_label, self._grammar_dict, self._config.buildGrammar())
        init_grammar(self._config.getInputFiles2(), white_label, self._grammar_dict, self._config.buildGrammar())

        # read list of special XML characters
        self._xmlCharacters_dict = dict()
        self._xmlCharacters_dict = read_XML_character(self._config.getXmlCharacterFile())

        grammar_int = convert_grammar_label2int(self._grammar_dict, self.label_decoder)
        self.constraints = FreqT1Strategy(self._config, grammar_int)

    def add_tree_requested(self, pat, proj):
        """
         * add the tree to the root IDs or the MFP
         * @param: pat FTArray
         * @param: projected, Projected
        """
        # check chi-square score
        if self.constraints.satisfy_post_expansion_constraint(pat) and \
                satisfy_chi_square(proj, self.sizeClass1, self.sizeClass2, self._config.getDSScore(),
                                   self._config.getWeighted()):
            self.add_tree(pat, proj)
            return True
        return False

    def add_tree(self, pat, proj):
        self.addHighScorePattern(pat, proj, self.hsp)

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
        root_ids_list = list()
        for proj in _HSP_dict:
            self.add_root_ids(proj, _HSP_dict[proj], root_ids_list)
        return root_ids_list

    def add_root_ids(self, pat, proj, root_ids_list):
        """
         * store root occurrences of pattern
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as values
        """
        # set of root occurrences of current pattern
        root_occ1 = {(loc.get_location_id(), loc.get_root()) for loc in proj.get_locations()}

        # check whether the current root occurrences existing in the rootID
        for elem in root_ids_list:
            root_occ2 = elem[1]
            if len(root_occ1) <= len(root_occ2):
                if root_occ1.issubset(root_occ2):
                    return
            else:
                if root_occ1.issuperset(root_occ2):
                    del elem

        # store root occurrences and root label
        root_ids_list.append((pat.get(0), root_occ1))

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
            from freqt.src.be.intimals.freqt.core.old.FreqT_ext import FreqT_ext
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
