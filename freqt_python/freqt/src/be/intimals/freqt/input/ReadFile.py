#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.structure.NodeFreqT import NodeFreqT


class ReadFile:

    def createTransactionFromMap(self, in_patterns_dict, trans_list_of_list):
        """
         * create transaction from dictionary < pattern, supports>
         * argument 1: a dictionary <String, String>
         * argument 2: an list of list containing NodeFreqT elements
        """
        for elem in in_patterns_dict:
            tran_tmp_list = []  # list of NodeFreqT
            self.str2node(elem, tran_tmp_list)
            trans_list_of_list.append(tran_tmp_list)

    def str2node(self, string, trans):
        """
         * transform a string into node
         * argument 1: a string
         * argument 2: a list of node
        """
        length = len(string)
        size = 0
        buff = ""  # individual node
        tmp = []  # a list of node

        index = 0
        while index < length:
            if string[index] == '(' or string[index] == ')':
                if len(buff) != 0:
                    if buff[0] == '*':
                        tmp.append(buff)
                    else:
                        label = buff.split("_")
                        tmp.append(label[0])
                    buff = ""
                    size += 1
                if string[index] == ')':
                    tmp.append(')')
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
                            else:
                                if string[index] == ')':
                                    bracket -= 1
                            if bracket == -1:
                                break
                            buff += string[index]
                            index += 1
                        index -= 1
                    else:
                        buff += string[index]
            index += 1
        if len(buff) != 0:
            print("buff: " + buff)
            raise Exception("ArithmeticException")
        # init a list of node
        sibling = [-1] * size
        for _ in range(size):
            node_temp = NodeFreqT()
            node_temp.setNodeSibling(-1)
            node_temp.setNodeParent(-1)
            node_temp.setNodeChild(-1)
            trans.append(node_temp)
            sibling.append(-1)
        # create tree
        sr_list = []
        loc_id = 0
        for char in tmp:
            if char == ")":
                top = len(sr_list) - 1
                if top < 1:
                    continue
                child = sr_list[top]
                parent = sr_list[top-1]
                trans[child].setNodeParent(parent)
                if trans[parent].getNodeChild() == -1:
                    trans[parent].setNodeChild(child)
                if sibling[parent] != -1:
                    trans[sibling[parent]].setNodeSibling(child)
                sibling[parent] = child
                sr_list.pop(top)
            else:
                trans[loc_id].setNodeLabel(char)
                sr_list.append(loc_id)
                loc_id += 1
