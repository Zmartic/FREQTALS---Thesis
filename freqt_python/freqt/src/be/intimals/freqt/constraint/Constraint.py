#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.structure.PatternInt import *
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR

import sys
import traceback


def satisfy_chi_square(projected, size_class1, size_class2, chi_square_threshold, weighted):
    score = chi_square(projected, size_class1, size_class2, weighted)
    return score >= chi_square_threshold


def chi_square(projected, size_class1, size_class2, weighted):
    """
     * return chiSquare value of a pattern in two classes
    """
    a, c = get_2class_support(projected, weighted)

    # a: occurrences in the first class data
    # c: occurrences in the second class data

    yaminxb = size_class2 * a - size_class1 * c
    one = yaminxb / ((a+c) * (size_class1 + size_class2 - a - c))
    two = yaminxb / (size_class1 * size_class2)

    return one * two * (size_class1 + size_class2)


def get_2class_support(projected, weighted):
    """
     * return number of occurrences of a pattern in two classes
    """
    if weighted:
        # count support by occurrences
        a = get_root_support_class1(projected)
        c = get_root_support(projected) - a
    else:
        # count support by files
        a = get_support_class1(projected)
        c = get_support(projected) - a

    return a, c


def get_support_class1(projected):
    """
     * count support of pattern in the class 1
    """
    sup = 0
    old_loc_id = -1

    for loc in projected.getProjectLocations():
        loc_id = loc.getLocationId()

        if loc.getClassID() == 1 and loc_id != old_loc_id:
            sup += 1
            old_loc_id = loc_id

    return sup


def get_root_support_class1(projected):
    """
     * count root support of pattern in the class 1
    """
    root_sup = 0
    old_loc_id = - 1
    old_root_id = -1

    for loc in projected.getProjectLocations():
        class_id = loc.getClassID()
        loc_id = loc.getLocationId()
        root_id = loc.getRoot()

        if class_id == 1:
            if loc_id != old_loc_id or (loc_id == old_loc_id and root_id != old_root_id):
                root_sup += 1
            old_loc_id = loc_id
            old_root_id = root_id

    return root_sup


def get_support(projected):
    """
     * calculate the support of a pattern = number of files
     * @param projected
     * @return
    """
    sup = 0
    old_loc_id = -1

    for loc in projected.getProjectLocations():
        loc_id = loc.getLocationId()

        if loc_id != old_loc_id:
            sup += 1
            old_loc_id = loc_id
    return sup


def get_root_support(projected):
    """
     * calculate the root support of a pattern = number of occurrences
     * @param projected
     * @return
    """
    root_sup = 0
    old_loc_id = -1
    old_root_id = -1
    for loc in projected.getProjectLocations():
        loc_id = loc.getLocationId()
        root_id = loc.getRoot()

        if loc_id != old_loc_id or (loc_id == old_loc_id and root_id != old_root_id):
            root_sup += 1
            old_loc_id = loc_id
            old_root_id = root_id
    return root_sup


def prune(candidates, min_sup, weighted):
    """
     * prune candidates based on minimal support
     * @param: candidates, dictionary with FTArray as key and Projected as value
     * @param: minSup, int
     * @param: weighted, boolean
    """
    keys = list(candidates.keys())
    for elem in keys:
        proj = candidates[elem]

        sup = get_support(proj)
        wsup = get_root_support(proj)
        limit = wsup if weighted else sup

        if limit < min_sup:
            del candidates[elem]
        else:
            proj.setProjectedSupport(sup)
            proj.setProjectedRootSupport(wsup)


def check_black_list_label(label, black_labels):  # UNUSED
    """
     * return true if the label_int is in the set of black labels
     * @param: label_int, an integer
     * @param: _blackLabels, une liste de liste d'Integer
    """
    for labels in black_labels:
        if label in labels:
            return True
    return False


def check_output(pat, min_leaf, min_node):
    """
     * check output constraints: minLeaf and minNode
     * @param pat
     * @return
    """
    return satisfy_min_leaf(pat, min_leaf) and satisfy_min_node(pat, min_node)


def satisfy_min_node(pat, min_node):
    """
     * return true if the number of nodes is larger or equal to minNode
     * @param pat
     * @return
    """
    return countNode(pat) >= min_node


def satisfy_min_leaf(pat, min_leaf):
    """
     * return true if the number of leafs is larger or equal to minLeaf
     * @param pat
     * @return
    """
    return countLeafNode(pat) >= min_leaf


def satisfyMaxLeaf(pattern, maxLeaf):
    """
     * return true if the number of leafs of the pattern is larger than maxLeaf
     * @param pattern
     * @return
    """
    return countLeafNode(pattern) >= maxLeaf


def isNotFullLeaf(pattern):
    """
     * return true if the pattern misses leaf
     * @param pattern
     * @return
    """
    return checkMissingLeaf(pattern)


def missingLeftObligatoryChild(pat, candidate, _grammarInt):
    """
     * return true if pattern misses obligatory child at the left side of the current node
     * @param: pat, FTArray
     * @param: candidate, FTArray
     * @param: _grammarInt_dict, dictionary with Integer as keys and list of String as values
    """
    missMandatoryChild = False
    try:
        # find parent's position of candidate in the patterns
        parentPos = findParentPosition(pat, candidate)

        # find all children of patternLabel in grammar
        childrenG_list = _grammarInt[pat.get(parentPos)]

        if childrenG_list[0] == "ordered" and not childrenG_list[1] == "1":
            # find all children of parentPos in pattern
            childrenP = findChildrenPosition(pat, parentPos)
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
        for pos in range(pat.size()):
            currentLabel = pat.get(pos)
            if currentLabel >= 0: # consider only internal label
                # find all children of patternLabel in grammar
                childrenG_list = _grammarInt_dict[currentLabel]
                if childrenG_list[0] == "ordered" and not childrenG_list[1] == "1":
                    # get all children of the current pos in pattern
                    childrenP = findChildrenPosition(pat, pos)
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
        projected = entry_dict[key]
        # find parent's location of Paragraph
        parentPos = findParentPosition(pat, key)
        # find Paragraph locations
        childrenPos = findChildrenPosition(pat, parentPos)

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
