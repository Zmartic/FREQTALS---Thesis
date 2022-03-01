#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.core.FreqT_subtree import *


def check_subtree(pat1, pat2):
    """
     * check if pat1 is a subtree of pat2 ?
     * return 1 : pat1 is subset of 2; 2 : pat2 is subset of pat1; otherwise return 0
     * @param pat1, FTArray
     * @param pat2, FTArray
     * @param config, Config
     * @return
    """

    fast_result = fast_check_subtree(pat1, pat2)
    if fast_result != -1:
        return fast_result

    fr = FreqT_subtree()
    pat1_size = pat1.size()
    pat2_size = pat2.size()
    fr.checkSubtrees(pat1, pat2) if pat1_size < pat2_size else fr.checkSubtrees(pat2, pat1)

    if len(fr.getOutputPattern()) == 0:
        return 0

    return 1 if pat1_size <= pat2_size else 2


def fast_check_subtree(pat1, pat2):
    """
     return 0 = no subtree, 1 = pat1 is a subtree of pat2, 2 = pat2 is a subtree of pat1
      * @param: pat1, FTArray
      * @param: pat2, FTArray
    """
    if pat1.size() == pat2.size():
        return 1 if pat1 == pat2 else 0
    try:
        if pat1.size() > pat2.size():
            return 2 if hasSubtree(pat1, pat2) else 0

        return 1 if hasSubtree(pat2, pat1) else 0

    except ValueError:
        return -1


def hasSubtree(big, small):
    """
    return true if a tree is a subtree of an other
     * @param big, FTArray
     * @param small, FTArray
    """
    root = small.get(0) # the root of small
    smallSize = small.size()
    bigSize = big.size()
    startIdx = 0

    bigPart = big
    while True: # loop over big, searching for the root
        rootIdx = bigPart.index(root)
        if rootIdx == -1:
            return False
        bigPartSize = bigPart.size()
        if rootIdx + smallSize > bigPartSize:
            return False
        if treeIncludes(bigPart.sub_list(rootIdx, bigPartSize), small):
            return True
        startIdx += rootIdx + 1
        bigPart = big.sub_list(startIdx, bigSize)  # continue with the rest of the array

"""
 * both big and small have the same root, inclusion check ignores sub-trees that are in big but not in small
 * @param: big, FTArray
 * @param: small, FTArray
"""
def treeIncludes(big, small):
    if big.size() == small.size():
        return big == small

    smallSize = small.size()
    bigSize = big.size()
    smallIndex = 1
    bigIndex = 1

    # loop until the end of the small tree
    while smallIndex < smallSize:
        if bigIndex >= bigSize:
            # there is more in small that is not in big
            return False
        bigNode = big.get(bigIndex)
        smallNode = small.get(smallIndex)

        while bigNode != smallNode:
            if bigNode < -1:
                bigIndex += 2   # skip over leaves in big but not in small
                if bigIndex >= bigSize:
                    # there is more in small that is not in big
                    return False
            # in a branch in big that has the same prefix but continues differently in small
            # we need to go back and skip over it -- complex case
            elif bigNode == -1:
                raise ValueError  # TODO NO!
                # in big we have a branch that is not in small, skip over it
            else:
                bigIndex = skipOver(big, bigIndex + 1)
                if bigIndex >= bigSize:
                    # there is more in small that is not in big
                    return False
            bigNode = big.get(bigIndex)
        bigIndex += 1
        smallIndex += 1
    return True


"""
 * in the tree at offset-1 there is the start of a subtree that we should skip over
   return the offset in the tree after that subtree
 * @param: tree, FTArray
 * @param: offset, int
"""
def skipOver(tree, offset):
    offset += 1
    treeSize = tree.size()
    recursion = 1  # how deep are we recursing in the subtree
    while recursion >= 0:
        if offset >= treeSize:
            return offset  # end of the big tree, break out
        node = tree.get(offset)
        if node == -1:
            recursion -= 1
        else:
            recursion += 1

        offset += 1
    return offset
