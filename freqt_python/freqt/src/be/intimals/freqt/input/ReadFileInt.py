#!/usr/bin/env python3
import sys

from freqt.src.be.intimals.freqt.constraint.Constraint import countNode
from freqt.src.be.intimals.freqt.structure.NodeFreqT import *


class ReadFileInt:
    """
     * create transaction from list of patterns
     * argument 1: a list of FTArray
     * argument 2: a list of list of NodeFreqtT
     * return
    """
    def createTransactionFromMap(self, inPatternsFTArrayList, transListOfNodeFreqTList):
        for elem in inPatternsFTArrayList:
            tran_tmp = list()
            self.str2node(elem, tran_tmp)
            transListOfNodeFreqTList.append(tran_tmp)

    """
     * transform a pattern into a node
     * argument 1: a FTArray pattern
     * arguemnt 2: a list of FreqNodeT
    """
    def str2node(self, patFTArray, transFreqNodeTList):
        try:
            size_int = countNode(patFTArray)
            # init a list of node
            sibling = [-1] * size_int
            for i in range(0, size_int):
                nodeTemp = NodeFreqT()
                nodeTemp.setNodeSibling(-1)
                nodeTemp.setNodeParent(-1)
                nodeTemp.setNodeChild(-1)
                transFreqNodeTList.append(nodeTemp)
                sibling[i] = -1

            # create a tree
            sr = list()
            id = 0
            for i in range(0, patFTArray.size()):
                if patFTArray.get(i) == -1:
                    top = len(sr) - 1
                    if top < 1:
                        continue
                    child = sr[top]
                    parent = sr[top-1]
                    transFreqNodeTList[child].setNodeParent(parent)
                    if transFreqNodeTList[parent].getNodeChild() == -1:
                        transFreqNodeTList[parent].setNodeChild(child)
                    if sibling[parent] != -1:
                        transFreqNodeTList[sibling[parent]].setNodeSibling(child)
                    sibling[parent] = child
                    if top <= len(sr):
                        sr = sr[:top]
                    else:
                        while len(sr) < top:
                            sr.append(None)
                else:
                    transFreqNodeTList[id].setNode_label_int(patFTArray.get(i))
                    sr.append(id)
                    id += 1
            top = len(sr)
            while top > 1:
                top = len(sr) - 1
                child = sr[top]
                parent = sr[top - 1]
                transFreqNodeTList[child].setNodeParent(parent)
                if transFreqNodeTList[parent].getNodeChild() == -1:
                    transFreqNodeTList[parent].setNodeChild(child)
                if sibling[parent] != -1:
                    transFreqNodeTList[sibling[parent]].setNodeSibling(child)
                sibling[parent] = child
                if top <= len(sr):
                    sr = sr[:top]
                else:
                    while len(sr) < top:
                        sr.append(None)

        except:
            e = sys.exc_info()[0]
            print("Fatal: parse error << [" + str(e) + "]\n")
            raise
