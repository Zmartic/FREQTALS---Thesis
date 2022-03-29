#!/usr/bin/env python3
import sys
import traceback

from freqt.src.be.intimals.freqt.constraint.Constraint import prune
from freqt.src.be.intimals.freqt.core.FreqTCore import FreqTCore
from freqt.src.be.intimals.freqt.core.InitData import init_data_1class
from freqt.src.be.intimals.freqt.core.AddTree import add_maximal_pattern

from freqt.src.be.intimals.freqt.output.XMLOutput import XMLOutput
from freqt.src.be.intimals.freqt.structure.Pattern import Pattern


class FreqT1Class(FreqTCore):

    def __init__(self, config):
        super().__init__(config)

        # dictionary of maximal frequent patterns
        self.mfp = dict()
        # set of pattern that are not maximal ( used for add_maximal_pattern() )
        self.not_maximal_set = set()

    def init_data(self):
        self._transaction_list, self._transactionClassID_list, self.label_decoder, self._grammar_dict, \
            self._xmlCharacters_dict, self.constraints = init_data_1class(self._config)

    '''def expand_pattern(self, pattern, projected):
        # if timeout then stop expand the pattern;
        if self.is_timeout():
            self.finished = False
            return False

        # --- find candidates of the current pattern ---
        candidates = FreqTCore.generate_candidates(projected, self._transaction_list)
        # prune candidate based on minSup
        prune(candidates, self._config.getMinSupport(), self._config.getWeighted())

        # --- expand each candidate pattern ---
        super_tree_added = False

        for extension, new_proj in candidates.items():
            candidate_prefix, candidate_label = extension

            # built the candidate pattern using the extension
            pattern.extend(candidate_prefix, candidate_label)

            if not self.constraints.is_pruned_pattern(pattern, candidate_prefix):
                # check constraints on maximal number of leaves and real leaf
                if self.constraints.stop_expand_pattern(pattern):
                    if candidate_label < -1:
                        if self.add_tree_requested(pattern, new_proj):
                            # pattern was added successfully
                            super_tree_added = True

                else:
                    # continue expanding pattern
                    did_add_tree = self.expand_pattern(pattern, new_proj)
                    if did_add_tree:
                        # Super-tree was found, no need to add a subtree
                        super_tree_added = True
                    elif candidate_label < -1:
                        if self.add_tree_requested(pattern, new_proj):
                            # pattern was added successfully
                            super_tree_added = True

            # restore the pattern
            pattern.undo_extend(candidate_prefix)

        return super_tree_added'''

    def add_tree(self, pat, proj):
        add_maximal_pattern(pat, proj, self.mfp, self.not_maximal_set)

    def post_mining_process(self, report):
        """
         * print patterns found in the first step
        """
        self.log(report, "OUTPUT")
        self.log(report, "===================")
        if self.finished:
            self.log(report, "finished search")
        else:
            self.log(report, "timeout")
        # print pattern to xml file
        self.output_patterns(self.mfp, self._config, self._grammar_dict, self.label_decoder, self._xmlCharacters_dict)

        self.log(report, "+ Maximal patterns = " + str(len(self.mfp)))
        self.log(report, "+ Running times = " + str(self.get_running_time()) + " s")
        report.close()

    def output_patterns(self, output_patterns, config, grammar, label_decoder, xmlCharacters_dict):
        """
         * print maximal patterns to XML file
         * @param: MFP_dict, dictionary with FTArray as key and String as values
         * @param: config, Config
         * @param: grammar_dict, dictionary with String as keys and list of String as values
         * @param: labelIndex_dict, dictionary with Integer as keys and String as values
         * @param: xmlCharacters_dict, dictionary with String as keys et String as values
        """
        try:
            out_file = config.getOutputFile()
            # create output file to store patterns for mining common patterns
            output_common_patterns = open(out_file + ".txt", 'w+')
            # output maximal patterns
            output_maximal_patterns = XMLOutput(out_file, config, grammar, xmlCharacters_dict)
            pattern = Pattern()
            for pat in output_patterns:
                pat_str = pat.get_decoded_str(label_decoder)
                supports = self.get_support_string(pat, output_patterns[pat])
                output_maximal_patterns.report_Int(pat_str, supports)
                output_common_patterns.write(pattern.getPatternString1(pat_str) + "\n")

            output_maximal_patterns.close()
            output_common_patterns.flush()
            output_common_patterns.close()

        except:
            e = sys.exc_info()[0]
            print("Print maximal patterns error : " + str(e) + "\n")
            print(traceback.format_exc())

    def get_support_string(self, pat, proj):
        """
         * get a string of support, score, size for a pattern
         * @param: pat, FTArray
         * @param: projected, Projected
        """
        return str(proj.get_support()) + "," + str(proj.get_root_support()) + "," + str(pat.n_node)
