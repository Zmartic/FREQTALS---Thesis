#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.util.Variables import *


class Pattern:

    """
    subtree representation
    input subtree
         a
        /\
       b  c
      /    \
     *1     *2

    format 1 = a,b,*1,),),c,*2
    format 2 = (a(b(*1))(c(*2)))
    """

    def covert(self, str):
        tmp_list = list()  # a list of node labels
        try:
            length = len(str)
            size = 0
            buff = ""  # store a node label

            ii = 0
            while ii < length:
                if str[ii] == '(' or str[ii] == ')':
                    if len(buff) != 0:
                        if buff[0] == '*':
                            tmp_list.append(buff)
                        else:
                            label = buff.split("_")
                            tmp_list.append(label[0])
                        buff = ""
                        size += 1
                    if str[ii] == ')':
                        tmp_list.append(")")
                else:
                    if str[ii] == '\t' or str[ii] == ' ':
                        buff += "_"
                    else:
                        # adding to find leaf node i.e. *X(120)
                        if str[ii] == '*':
                            bracket = 0
                            while bracket >= 0:
                                if str[ii] == '(':
                                    bracket += 1
                                elif str[ii] == ')':
                                    bracket -= 1
                                if bracket == -1:
                                    break
                                else:
                                    buff += str[ii]
                                    ii += 1
                            ii -= 1
                        else:
                            buff += str[ii]
                ii += 1
            for i in range(len(tmp_list) - 1, -1, -1):
                if tmp_list[i] == ")":
                    tmp_list.pop(i)
                else:
                    break
        except:
            print("Pattern convert ")
        tmp_list_str = ", ".join(tmp_list)
        return tmp_list_str



    """
     * filter: remove the parts missed real leafs
     * @param pat_list, a list of String
     * @return
    """
    def removeMissingLeaf(self, pat_list):
        result_list = list()
        # find the last leaf
        pos = 0
        for i in range(0, len(pat_list)):
            if pat_list[i][0] == "*":
                pos = i
        # output patterns
        for i in range(0, pos + 1):
            result_list.append(pat_list[i])

        for i in range(pos, len(pat_list)):
            if pat_list[i] == ")":
                result_list.append(")")
            else:
                break
        return result_list

    """
     * transform format 1 into format 2
     * filter : remove the parts missed real leafs
     * @param pat
     * @return
    """
    # remove part of pattern missing leaf
    def getPatternString1(self, patListOfstr):
        result = ""
        # find the last leaf
        pos = 0
        for i in range(0, len(patListOfstr)):
            if patListOfstr[i][0] == '*':
                pos = i
        n = 0
        for i in range(0, pos +1):
            if patListOfstr[i] == ")":
                result += patListOfstr[i]
                n -= 1
            else:
                n += 1
                result += "(" + patListOfstr[i]

        for i in range(0, n):
            result += ")"

        return result

    """
     * transform pattern format 1 into format 2
     * @param pat
     * @return
    """
    def getPatternString(self, patListOfStr):
        result = ""
        n = 0
        for i in range(0, len(patListOfStr)):
            if patListOfStr[i].equals(")"):
                result += patListOfStr[i]
                n += 1
            else:
                n += 1
                result += "(" + patListOfStr[i]
        for i in range(0, n):
            result += ")"
        return result

    """
     * calculate size (total nodes) of a pattern
     * @param pat
     * @return
    """
    def getPatternSize(self, patListOfStr):
        size = 0
        for i in range(len(patListOfStr)):
            if not patListOfStr[i] == ")":
                size += 1
        return size

    """
     * find parent's position of a given candidate in a pattern
     * @param pat
     * @param candidate
     * @return
    """
    def findParentPosition(self, patListOfStr, candidateStr):
        parentPos = 0
        nodeLevel = 0
        candidateSize = 0
        try:
            p = candidateStr.split(Variables.uniChar)
            for i in range(0, len(p)):
                if p[i].equals(")"):
                    nodeLevel += 1
                if len(p[i]) != 0:
                    candidateSize += 1

            size = len(patListOfStr) - candidateSize
            if nodeLevel == 0:
                parentPos = size - 1
            else:
                for i in range(size - 1, 0, -1):
                    if patListOfStr[i].equals(")"):
                        nodeLevel += 1
                    else:
                        nodeLevel -= 1
                    if nodeLevel == -1:
                        parentPos = i
                        break
        except:
            print("find parent position error ")
        return parentPos

    """
     * find all children of the node at the parentPos
     * @param patListOfStr, a list of String
     * @param parentPos, int
     * @return list of string
    """
    def findChildrenLabels(self, patListOfStr, parentPos):
        top = -1
        children1 = list()
        if parentPos < len(patListOfStr) - 1:
            for i in range(parentPos + 1, len(patListOfStr)):
                if patListOfStr[i] == ")":
                    top -= 1
                else:
                    top += 1
                if top == 0 and not patListOfStr[i] == ")":
                    children1.append(patListOfStr[i])
                if top == -2:
                    break
        return children1