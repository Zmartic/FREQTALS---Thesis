#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.FreqTStrategy import FreqT1Strategy
from freqt.src.be.intimals.freqt.core.FreqT1ClassExt import FreqT1ClassExt
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore

from freqt.src.be.intimals.freqt.input.ReadXMLInt import ReadXMLInt
from freqt.src.be.intimals.freqt.util.Initial_Int import initGrammar_Str, readXMLCharacter, convert_grammar_keys2int


class FreqT1Class2Step(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        self.root_ids_list = list()

    def init_data(self):
        """
         * read input data
        """
        self._transaction_list = list()
        self._grammar_dict = dict()
        self._xmlCharacters_dict = dict()
        self._transactionClassID_list = list()

        self.label_encoder = dict()
        # self.label_decoder = dict()

        try:
            readXML = ReadXMLInt()
            # remove black labels when reading ASTs
            readXML.readDatabase(self._transaction_list, 1,
                                 self._config.getInputFiles(), self.label_encoder,
                                 self._transactionClassID_list, self._config.getWhiteLabelFile())
            # create grammar (labels are strings) which is used to print patterns
            initGrammar_Str(self._config.getInputFiles(), self._config.getWhiteLabelFile(), self._grammar_dict,
                            self._config.buildGrammar())

            # read list of special XML characters
            readXMLCharacter(self._config.getXmlCharacterFile(), self._xmlCharacters_dict)

            grammar_int = convert_grammar_keys2int(self._grammar_dict, self.label_encoder)
            self.constraints = FreqT1Strategy(self._config, grammar_int)

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
        self.addRootIDs(pat, proj, self.root_ids_list)

    def post_mining_process(self, report):
        self.expandPatternFromRootIDs(self.root_ids_list, report)

    # --------------- #

    def addRootIDs(self, pat, proj, root_ids_list):
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

    def expandPatternFromRootIDs(self, root_ids_list, report):
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
        self.log(report, "\t + root occurrences groups = " + str(len(root_ids_list)))
        # phase 2: find maximal patterns from rootIDs
        self.log(report, "- Step 2: Mining maximal patterns WITHOUT max size constraint:")

        # run second step
        freqt_ext = FreqT1ClassExt(self._config, root_ids_list, self._grammar_dict, self.constraints.grammar,
                                   self._xmlCharacters_dict, self.label_encoder, self._transaction_list)
        freqt_ext.run()

        # report result
        if freqt_ext.finished:
            self.log(report, "\t + search finished")
        else:
            self.log(report, "\t + timeout in the second step")

        self.log(report, "\t + maximal patterns: " + str(len(freqt_ext.mfp)))
        self.log(report, "\t + running time: ..." + str(freqt_ext.get_running_time()) + "s")
        report.flush()
        report.close()

    def is_timeout(self):
        """
         * check running time of the algorithm
        """
        return False
