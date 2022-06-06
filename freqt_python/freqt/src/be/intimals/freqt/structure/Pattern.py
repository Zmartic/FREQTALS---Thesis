#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.util.Variables import UNICHAR


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

    def covert(self, string):
        tmp_list = []  # a list of node labels
        try:
            length = len(string)
            size = 0
            buff = ""  # store a node label

            index = 0
            while index < length:
                if string[index] == '(' or string[index] == ')':
                    if len(buff) != 0:
                        if buff[0] == '*':
                            tmp_list.append(buff)
                        else:
                            label = buff.split("_")
                            tmp_list.append(label[0])
                        buff = ""
                        size += 1
                    if string[index] == ')':
                        tmp_list.append(")")
                else:
                    if string[index] == '\t' or string[index] == ' ':
                        buff += "_"
                    else:
                        # adding to find leaf node i.e. *X(120)
                        if string[index] == '*':
                            bracket = 0
                            while bracket >= 0:
                                if string[index] == '(':
                                    bracket += 1
                                elif string[index] == ')':
                                    bracket -= 1
                                if bracket == -1:
                                    break
                                else:
                                    buff += string[index]
                                    index += 1
                            index -= 1
                        else:
                            buff += string[index]
                index += 1
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
        result_list = []
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
        node = 0
        for i in range(0, pos + 1):
            if patListOfstr[i] == ")":
                result += patListOfstr[i]
                node -= 1
            else:
                node += 1
                result += "(" + patListOfstr[i]

        for i in range(0, node):
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
            if patListOfStr[i] == ")":
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
     * find all children of the node at the parentPos
     * @param patListOfStr, a list of String
     * @param parentPos, int
     * @return list of string
    """
    def findChildrenLabels(self, pat_list_of_str, parent_pos):
        top = -1
        children1 = []
        if parent_pos < len(pat_list_of_str) - 1:
            for i in range(parent_pos + 1, len(pat_list_of_str)):
                if pat_list_of_str[i] == ")":
                    top -= 1
                else:
                    top += 1
                if top == 0 and not pat_list_of_str[i] == ")":
                    children1.append(pat_list_of_str[i])
                if top == -2:
                    break
        return children1
