#!/usr/bin/env python3
import sys

from freqt.src.be.intimals.freqt.constraint.Constraint import count_node
from freqt.src.be.intimals.freqt.structure.NodeFreqT import NodeFreqT


class ReadFileInt:
    """
     * create transaction from list of patterns
     * argument 1: a list of FTArray
     * argument 2: a list of list of NodeFreqtT
     * return
    """
    def createTransactionFromMap(self, in_patterns_list, trans_list_of_node_freqt):
        for elem in in_patterns_list:
            tran_tmp = []
            self.str2node(elem, tran_tmp)
            trans_list_of_node_freqt.append(tran_tmp)

    def str2node(self, pat, trans_node_freqt_list):
        """
         * transform a pattern into a node
         * argument 1: a FTArray pattern
         * arguemnt 2: a list of FreqNodeT
        """
        try:
            size_int = count_node(pat)
            # init a list of node
            sibling = [-1] * size_int
            for i in range(0, size_int):
                node_temp = NodeFreqT()
                node_temp.setNodeSibling(-1)
                node_temp.setNodeParent(-1)
                node_temp.setNodeChild(-1)
                trans_node_freqt_list.append(node_temp)
                sibling[i] = -1

            # create a tree
            sr_list = []
            loc_id = 0
            for i in range(0, pat.size()):
                if pat.get(i) == -1:
                    top = len(sr_list) - 1
                    if top < 1:
                        continue
                    child = sr_list[top]
                    parent = sr_list[top-1]
                    trans_node_freqt_list[child].setNodeParent(parent)
                    if trans_node_freqt_list[parent].getNodeChild() == -1:
                        trans_node_freqt_list[parent].setNodeChild(child)
                    if sibling[parent] != -1:
                        trans_node_freqt_list[sibling[parent]].setNodeSibling(child)
                    sibling[parent] = child
                    if top <= len(sr_list):
                        sr_list = sr_list[:top]
                    else:
                        while len(sr_list) < top:
                            sr_list.append(None)
                else:
                    trans_node_freqt_list[loc_id].setNode_label_int(pat.get(i))
                    sr_list.append(loc_id)
                    loc_id += 1
            top = len(sr_list)
            while top > 1:
                top = len(sr_list) - 1
                child = sr_list[top]
                parent = sr_list[top - 1]
                trans_node_freqt_list[child].setNodeParent(parent)
                if trans_node_freqt_list[parent].getNodeChild() == -1:
                    trans_node_freqt_list[parent].setNodeChild(child)
                if sibling[parent] != -1:
                    trans_node_freqt_list[sibling[parent]].setNodeSibling(child)
                sibling[parent] = child
                if top <= len(sr_list):
                    sr_list = sr_list[:top]
                else:
                    while len(sr_list) < top:
                        sr_list.append(None)

        except:
            print("Fatal: parse error << [" + str(sys.exc_info()[0]) + "]\n")
            raise
