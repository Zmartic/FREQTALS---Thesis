#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.FTArray import *


def checkBlackLabels(patFTArray, candidateFTArray, listLabelsDict, labelInt):
    """
     * return true if candidate is in black labels
     * @param pat, a FTArray
     * @param candidate, a FTArray
     * @param ListLabels Dictionnary with Integer as Key and a list as value
     * @param label, an int
     * @return
    """
    if patFTArray.size() == 1:
        return labelInt in listLabelsDict[patFTArray.get(0)]
    else:
        patternTemp = patFTArray.copy()
        patternTemp.addAll(candidateFTArray)
        parentPos = findParentPosition(patternTemp, candidateFTArray)
        # find parent's position of potentialCandidate in patternTemp
        parentLabel_Int = patternTemp.get(parentPos)
        # find children of the parentLabel
        if parentLabel_Int in listLabelsDict:
            if labelInt in listLabelsDict[parentLabel_Int]:
                return True
    return False

def getPatternStr(patFTArray, labelIndexDict):
    """
     * convert pattern of Int into String
     * @param patFTArray, FTArray
     * @param labelIndex, dictionary with <T> as keys and values
     * @return
    """
    patStr = list()
    for i in range(0, patFTArray.size()):
        if patFTArray.get(i) == -1:
            patStr.append(")")
        else:
            patStr.append(labelIndexDict[patFTArray.get(i)])
    return patStr

def checkMissingLeaf(patFTArray):
    """
     * return true if the pattern misses real leaf
     * @param patFTArray, FTArray
     * @return
    """
    result = False
    for i in range(0, patFTArray.size() - 1):
        if patFTArray.get(i) != -1 and patFTArray.get(i + 1) == -1:
            if patFTArray.get(i) >= 0:
                result = True
                break
    return result

def countLeafNode(patFTArray):
    """
     * return number of leafs in the pattern
     * @param patFTArray, FTArray
     * @return
    """
    count = 0
    for i in range(0, patFTArray.size()):
        if patFTArray.get(i) < -1:
            count += 1
    return count

def countNode(patFTArray):
    """
     * return total number of nodes in the pattern
     * @param patFTArray, FTArray
     * @return
    """
    count = 0
    for i in range(0, patFTArray.size()):
        if patFTArray.get(i) != -1:
            count += 1
    return count

def findParentPosition(patFTArray, candidateFTArray):
    """
     * return parent's position of the candidate in the pattern
     * @param patFTArray, FTArray
     * @param candidateFTArray, FTArray
     * @return
    """
    parentPos = 0
    nodeLevel = 0
    candidateSize = 0
    try:
        for i in range(0, candidateFTArray.size()):
            if candidateFTArray.get(i) == -1:
                nodeLevel += 1
            candidateSize += 1

        size = patFTArray.size() - candidateSize
        if nodeLevel == 0:
            parentPos = size - 1
        else:
            for i in range(size - 1, 0, -1):
                if patFTArray.get(i) == -1:
                    nodeLevel += 1
                else:
                    nodeLevel -= 1
                if nodeLevel == -1:
                    parentPos = i
                    break
    except:
        print("find parent position error ")

    return parentPos

def findChildrenPosition(patFTArray, parentPosInt):
    """
     * return all children's positions of parentPos in the pat
     * @param patFTArray, FTArray
     * @param parentPosInt, Integer
     * @return
    """
    top = -1
    tmp = FTArray()
    if parentPosInt < patFTArray.size() - 1:
        count = parentPosInt
        for i in range(parentPosInt + 1, patFTArray.size()):
            if patFTArray.get(i) == -1:
                top -= 1
            else:
                top += 1
                count += 1
            if top == 0 and patFTArray.get(i) != -1:
                tmp.add(i)
            if top == -2:
                break
    return tmp