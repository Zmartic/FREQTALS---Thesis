#!/usr/bin/env python3
class NodeFreqT:

    def __init__(self):
        self.__node_label = ""  # String
        self.__node_label_int = -1  # Integer
        self.__line_nr = ""  # String
        self.__parent = -1  # Integer
        self.__child = -1  # Integer
        self.__sibling = -1  # Integer
        self.__degree = -1  # Integer
        self.__ordered = False # boolean
        # additional information in new singleTree
        self.__level = -1  # Integer
        self.__parent_ext = -1  # Integer
        self.__child_ext = -1  # Integer
        self.__sibling_ext = -1  # Integer

    def nodeFreqtInit(self, _parent, _child, _sibling, _degree, _ordered):
        self.__node_label = ""
        self.__node_label_int = -1
        self.__line_nr = ""
        self.__parent = _parent
        self.__child = _child
        self.__sibling = _sibling
        self.__degree = _degree
        self.__ordered = _ordered
        # additional information in new singleTree
        self.__level = -1
        self.__parent_ext = -1
        self.__child_ext = -1
        self.__sibling_ext = -1

    def setNode_label_int(self, node_label_int):
        self.__node_label_int = node_label_int

    def getNode_label_int(self):
        return self.__node_label_int

    # additional information for building single large tree
    def setNodeLevel(self, level):
        self.__level = level

    def setNodeSiblingExt(self, sibling_ext):
        self.__sibling_ext = sibling_ext

    def setNodeChildExt(self, child_ext):
        self.__child_ext = child_ext

    def setNodeParentExt(self, parent_ext):
        self.__parent_ext = parent_ext

    def getNodeLevel(self):
        return self.__level

    def getNodeSiblingExt(self):
        return self.__sibling_ext

    def getNodeChildExt(self):
        return self.__child_ext

    def getNodeParentExt(self):
        return self.__parent_ext

    def setNodeLabel(self, node_label):
        self.__node_label = node_label

    def setLineNr(self, line_nr):
        self.__line_nr = line_nr

    def setNodeSibling(self, sibling):
        self.__sibling = sibling

    def setNodeChild(self, child):
        self.__child = child

    def setNodeParent(self, parent):
        self.__parent = parent

    def setNodeDegree(self, degree):
        self.__degree = degree

    def setNodeOrdered(self, ordered):
        self.__ordered = ordered

    def getNodeLabel(self):
        return self.__node_label

    def getLineNr(self):
        return self.__line_nr

    def getNodeSibling(self):
        return self.__sibling

    def getNodeChild(self):
        return self.__child

    def getNodeParent(self):
        return self.__parent

    def getNodeDegree(self):
        return self.__degree

    def getNodeOrdered(self):
        return self.__ordered
