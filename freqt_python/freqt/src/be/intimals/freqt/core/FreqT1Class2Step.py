#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import DefaultStrategy
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, readXMLCharacter, convert_grammar_keys2int
from freqt.src.be.intimals.freqt.util.Util import Util


class FreqT1Class2Step(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        self.label_str2int = dict()  # label encoder
        # self.label_int2str = dict()  # label decoder

        self.root_ids_dict = dict()

    def init_data(self):
        """
         * read input data
        """
        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles(), self.label_str2int,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            # create grammar (labels are strings) which is used to print patterns
            initGrammar_Str(self._config.getInputFiles(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

            grammar_int = convert_grammar_keys2int(self._grammar_dict, self.label_str2int)
            self.constraints = DefaultStrategy(self._config, grammar_int)

        except:
            e = sys.exc_info()[0]
            print("read data set error " + str(e) + "\n")
            trace = traceback.format_exc()
            print(trace)

    def add_tree(self, pat, proj):
        """
         * add the tree to the root IDs
         * @param: pat FTArray
         * @param: projected, Projected
        """
        self.addRootIDs(pat, proj, self.root_ids_dict)

    def post_mining_process(self, report):
        self.expandPatternFromRootIDs(self.root_ids_dict, report)

    # --------------- #

    def addRootIDs(self, pat, projected, _rootIDs_dict):
        """
         * add root occurrences of pattern to rootIDs
         * @param: pat, FTArray
         * @param: projected, Projected
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as values
        """
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

    def expandPatternFromRootIDs(self, _rootIDs_dict, report):
        """
         * run the 2nd step to find maximal patterns from groups of root occurrences
         * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as value
         * @param: report, a open file ready to be writting
        """
        print("Mining maximal frequent subtrees ... \n")
        self.log(report, "")
        self.log(report, "OUTPUT")
        self.log(report, "===================")

        # report first phase
        self.log(report, "- Step 1: Mining frequent patterns with max size constraints")
        self.log(report, "\t + running time = " + str(self.get_running_time()) + "s")
        self.log(report, "\t + root occurrences groups = " + str(len(_rootIDs_dict)))
        # phase 2: find maximal patterns from rootIDs
        self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

        # run second step
        freqt_ext = FreqT1ClassExt(self._config, _rootIDs_dict, self._grammar_dict, self.constraints.grammar,
                                   self._xmlCharacters_dict, self.label_str2int, self._transaction_list)
        freqt_ext.run_ext()

        # report result
        if freqt_ext.finished:
            self.log(report, "\t + search finished")
        else:
            self.log(report, "\t + timeout in the second step")

        self.log(report, "\t + maximal patterns: " + str(len(freqt_ext.mfp)))
        self.log(report, "\t + running time: ..." + str(freqt_ext.get_running_time()) + "s")
        report.flush()
        report.close()

