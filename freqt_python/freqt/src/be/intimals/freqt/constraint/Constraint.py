#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.structure.PatternInt import *
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR

import sys
import traceback


def satisfyChiSquare(projected, sizeClass1, sizeClass2, chiSquareThreshold, weighted):
    score = chiSquare(projected, sizeClass1, sizeClass2, weighted)
    if score >= chiSquareThreshold:
        return True
    else:
        return False


def chiSquare(projected, sizeClass1, sizeClass2, weighted):
    """
     * return chiSquare value of a pattern in two classes
    """
    ac = get2ClassSupport(projected, weighted)

    a = ac[0]  # occurrences in the first class data
    c = ac[1]  # occurrences in the second class data

    yaminxb = sizeClass2 * a - sizeClass1 * c
    one = yaminxb / ((a+c) * (sizeClass1 + sizeClass2 - a - c))
    two = yaminxb / (sizeClass1 * sizeClass2)

    return one * two * (sizeClass1 + sizeClass2)


def get2ClassSupport(projected, weighted):
    """
     * return number of occurrences of a pattern in two classes
    """
    a = 0
    c = 0
    if weighted:
        # count support by occurrences
        a = getRootSupportClass1(projected)
        c = getRootSupport(projected) - a
    else:
        # count support by files
        a = getSupportClass1(projected)
        c = getSupport(projected) - a
    return [a, c]


def getSupportClass1(projected):
    """
     * count support of pattern in the class 1
    """
    a = 0
    old = - 1
    for i in range(projected.getProjectLocationSize()):
        if projected.getProjectLocation(i).getClassID() == 1 and projected.getProjectLocation(i).getLocationId() != old:
            a += 1
            old = projected.getProjectLocation(i).getLocationId()
    return a


def getRootSupportClass1(projected):
    """
     * count root support of pattern in the class 1
    """
    rootSup = 0
    oldLocationID = - 1
    oldRootID = -1
    for i in range(projected.getProjectLocationSize()):
        classID1 = projected.getProjectLocation(i).getClassID()
        locationID1 = projected.getProjectLocation(i).getLocationId()
        rootID1 = projected.getProjectLocation(i).getRoot()
        if classID1 == 1:
            if locationID1 == oldLocationID and rootID1 != oldRootID or locationID1 != oldLocationID:
                rootSup += 1
            oldLocationID = locationID1
            oldRootID = rootID1
    return rootSup


def checkOutput(pat, minLeaf, minNode):
    """
     * check output constraints: minLeaf and minNode
     * @param pat
     * @return
    """
    if satisfyMinLeaf(pat, minLeaf) and satisfyMinNode(pat, minNode):
        return True
    return False


def getSupport(projected):
    """
     * calculate the support of a pattern = number of files
     * @param projected
     * @return
    """
    old = -1
    sup = 0
    for i in range(projected.getProjectLocationSize()):
        if projected.getProjectLocation(i).getLocationId() != old:
            sup += 1
        old = projected.getProjectLocation(i).getLocationId()
    return sup


def getRootSupport(projected):
    """
     * calculate the root support of a pattern = number of occurrences
     * @param projected
     * @return
    """
    rootSup = 0
    oldLocationID = -1
    oldRootID = -1
    for i in range(projected.getProjectLocationSize()):
        locationID1 = projected.getProjectLocation(i).getLocationId()
        rootID1 = projected.getProjectLocation(i).getRoot()
        if locationID1 == oldLocationID and rootID1 != oldRootID or locationID1 != oldLocationID:
            rootSup += 1
        oldLocationID = locationID1
        oldRootID = rootID1
    return rootSup


def prune(candidates, minSup, weighted):
    """
     * prune candidates based on minimal support
     * @param: candidates, dictionary with FTArray as key and Projected as value
     * @param: minSup, int
     * @param: weighted, boolean
    """
    to_remove_list = list()
    for elem in candidates:
        sup = getSupport(candidates[elem])
        wsup = getRootSupport(candidates[elem])
        if weighted:
            limit = wsup
        else:
            limit = sup
        if limit < minSup:
            to_remove_list.append(elem)
        else:
            candidates[elem].setProjectedSupport(sup)
            candidates[elem].setProjectedRootSupport(wsup)
    for elem in to_remove_list:
        candidates.pop(elem, -1)


def checkBlackListLabel(label_int, _blackLabels):
    """
     * return true if the label_int is in the set of black labels
     * @param: label_int, an integer
     * @param: _blackLabels, une liste de liste d'Integer
    """
    for labels in _blackLabels:
        if label_int in labels:
            return True
    return False

"""
 * return True if the candidates are in the black label list
 * @param: pat, a FTArray
 * @param: key, a FTArray
 * @param: _blackLabels_dict, a dictionary with Integer as Key and List of Integer as Value
"""
"""
def isBlacklisted(pat, key, _blackLabels_dict):
    pattern_Int = PatternInt()
    candidateLabel_int = key.get(key.size() - 1)
    return checkBlackListLabel(candidateLabel_int, _blackLabels_dict.values()) and pattern_Int.checkBlackLabels(pat, key, _blackLabels_dict, candidateLabel_int)
"""


def satisfyMinNode(pat, minNode):
    """
     * return true if the number of nodes is larger or equal to minNode
     * @param pat
     * @return
    """
    pattern_Int = PatternInt()
    return pattern_Int.countNode(pat) >= minNode


def satisfyMinLeaf(pat, minLeaf):
    """
     * return true if the number of leafs is larger or equal to minLeaf
     * @param pat
     * @return
    """
    pattern_Int = PatternInt()
    return pattern_Int.countLeafNode(pat) >= minLeaf


def satisfyMaxLeaf(pattern, maxLeaf):
    """
     * return true if the number of leafs of the pattern is larger than maxLeaf
     * @param pattern
     * @return
    """
    pattern_Int = PatternInt()
    return pattern_Int.countLeafNode(pattern) >= maxLeaf


def isNotFullLeaf(pattern):
    """
     * return true if the pattern misses leaf
     * @param pattern
     * @return
    """
    pattern_Int = PatternInt()
    return pattern_Int.checkMissingLeaf(pattern)


def missingLeftObligatoryChild(pat, candidate, _grammarInt):
    """
     * return true if pattern misses obligatory child at the left side of the current node
     * @param: pat, FTArray
     * @param: candidate, FTArray
     * @param: _grammarInt_dict, dictionary with Integer as keys and list of String as values
    """
    missMandatoryChild = False
    try:
        pattern_Int = PatternInt()
        # find parent's position of candidate in the patterns
        parentPos = pattern_Int.findParentPosition(pat, candidate)

        # find all children of patternLabel in grammar
        childrenG_list = _grammarInt[pat.get(parentPos)]

        if childrenG_list[0] == "ordered" and not childrenG_list[1] == "1":
            # find all children of parentPos in pattern
            childrenP = pattern_Int.findChildrenPosition(pat, parentPos)
            # compare children in pattern and children in grammar
            i = 0
            j = 2
            while i < childrenP.size() and j < len(childrenG_list) and not missMandatoryChild:
                childGrammarTemp = childrenG_list[j].split(UNICHAR)
                label_int = int(childGrammarTemp[0])
                if pat.get(childrenP.get(i)) == label_int:
                    i += 1
                    j += 1
                else:
                    # if this child is optional
                    if childGrammarTemp[1] == "false":
                        j += 1
                    elif childGrammarTemp[1] == "true":
                        missMandatoryChild = True

    except:
        e = sys.exc_info()[0]
        print("check left Obligatory Children error: " + str(e) + "\n")
        trace = traceback.format_exc()
        print(trace)

    return missMandatoryChild


def missingRightObligatoryChild(pat, _grammarInt_dict):
    """
     *  return true if the pattern misses the obligatory child at right side of the current node
        for each node in the pattern do
      1. find children of the current node in the pattern
      2. find children of the current node in the grammar
      3. compare two set of children to determine the pattern missing mandatory child or not
     * @param: pat, FTArray
     * @param: _grammerInt_dict, dictionary with Integer as keys and list of String as values
    """
    missMandatoryChild = False
    try:
        pattern_Int = PatternInt()
        for pos in range(pat.size()):
            currentLabel = pat.get(pos)
            if currentLabel >= 0: # consider only internal label
                # find all children of patternLabel in grammar
                childrenG_list = _grammarInt_dict[currentLabel]
                if childrenG_list[0] == "ordered" and not childrenG_list[1] == "1":
                    # get all children of the current pos in pattern
                    childrenP = pattern_Int.findChildrenPosition(pat, pos)
                    if childrenP.size() > 0:
                        # check leaf children
                        # compare two sets of children to determine this pattern misses mandatory child or not
                        i = 0
                        j = 2
                        while i < childrenP.size() and j < len(childrenG_list) and not missMandatoryChild:
                            childGrammarTemp = childrenG_list[j].split(UNICHAR)
                            label_int = int(childGrammarTemp[0])

                            if pat.get(childrenP.get(i)) == label_int:
                                i += 1
                                j += 1
                            else:
                                if childGrammarTemp[1] == "false":
                                    j += 1
                                elif childGrammarTemp[1] == "true":
                                    missMandatoryChild = True

                        # check right children
                        if j < len(childrenG_list):
                            while j < len(childrenG_list) and not missMandatoryChild:
                                childGrammarTemp = childrenG_list[j].split(UNICHAR)
                                if childGrammarTemp[1] == "true":
                                    missMandatoryChild = True
                                j += 1

    except:
        e = sys.exc_info()[0]
        print("check Right Obligatory Children error: " + str(e) + "\n")

    return missMandatoryChild


# /////////// specific functions for COBOL source code //////////////////
def checkCobolConstraints(pattern, entry_dict, key, labelIndex_dict, transaction_list):
    """
     * @param: pattern, FTArray
     * @param: entry_dict, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: labelIndex_dict, dictionary with Integer as keys and String as values
     * @param: transaction_list, list of list of NodeFreqT
    """
    # check continuous paragraphs
    # if potential candidate = SectionStatementBlock then check if candidate belongs to black-section or not
    candidateLabel = labelIndex_dict[key.get(key.size() - 1)]
    if candidateLabel == "SectionStatementBlock":
        checkBlackSection(entry_dict, key, transaction_list)

    # expand the pattern if all paragraphs are continuous
    if candidateLabel == "ParagraphStatementBlock":
        checkContinuousParagraph(pattern, entry_dict, key, transaction_list)


def checkContinuousParagraph(pat, entry_dict, key, _transaction_list):
    """
     * @param: pat, FTArray
     * @param: entry_dict, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: _transaction_list, list of list of NodeFreqT
    """
    try:
        pattern_Int = PatternInt()
        projected = entry_dict[key]
        # find parent's location of Paragraph
        parentPos = pattern_Int.findParentPosition(pat, key)
        # find Paragraph locations
        childrenPos = pattern_Int.findChildrenPosition(pat, parentPos)

        if childrenPos.size() == 1:
            return
        # check continuous paragraphs
        # find the first position in pos --> compare to the last position

        i = 0
        while i < projected.getProjectLocationSize():
            pos = projected.getProjectLocation(i)
            id = pos.getLocationId()

            firstPos = 0
            for j in range(pos.size() - 2 , 0, -1):
                if _transaction_list[id][pos.get(j)].getNode_label_int() == pat.get(childrenPos.get(childrenPos.size() - 2)):
                    firstPos = pos.get(j)
                    break
            lastPos = pos.get(pos.size() - 1)
            if _transaction_list[id][firstPos].getNodeSibling() != lastPos:
                # remove paragraph location
                projected.deleteProjectLocation(i)
                i -= 1
            else:
                i += 1
        # modify the entry value
        entry_dict[key] = projected

    except:
        e = sys.exc_info()[0]
        print("checkContinuousParagraph " + str(e) + "\n")


def checkBlackSection(entry_dict, key, _transaction_list):
    """
     * delete locations of a label that belongs to black-section?
     * @param: entry, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: _transaction_list, list of list of NodeFreqT
    """
    #TODO: read black-section from file
    blackSectionList_set = set()
    blackSectionList_set.add("*CCVS1")
    blackSectionList_set.add("*CCVS-EXIT")

    try:
        projected = entry_dict[key]
        i = 0
        while i < projected.getProjectLocationSize():
            # get position of the current label
            id = projected.getProjectLocation(i).getLocationId()
            # for each location check if it belongs to SectionStatementBlock or not
            currentPos = projected.getProjectLocation(i).getLocationPos()
            # check if label of section is in black-section or not
            while currentPos != -1:
                if _transaction_list[id][currentPos].getNodeLabel() in blackSectionList_set:
                    projected.deleteProjectLocation(i)
                    i -= 1
                    break
                else:
                    currentPos = _transaction_list[id][currentPos].getNodeChild()
            i += 1
        # modify the values of the key
        entry_dict[key] = projected

    except:
        e = sys.exc_info()[0]
        print("Error: Delete SectionStatementBlock " + str(e) + "\n")
