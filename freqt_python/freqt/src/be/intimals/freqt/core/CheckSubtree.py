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
            return 2 if has_subtree(pat1, pat2) else 0

        return 1 if has_subtree(pat2, pat1) else 0

    except ValueError:
        return -1


def complex_check_subtree(pat1, pat2):

    fr = FreqT_subtree()
    pat1_size = pat1.size()
    pat2_size = pat2.size()
    fr.checkSubtrees(pat1, pat2) if pat1_size < pat2_size else fr.checkSubtrees(pat2, pat1)

    return len(fr.getOutputPattern()) != 0


def has_subtree(big, small):
    """
    return true if a tree is a subtree of an other
     * @param big, FTArray
     * @param small, FTArray
    """
    root = small.get(0)  # the root of small
    small_size = small.size()
    big_size = big.size()
    start_idx = 0

    big_part = big
    while True:  # loop over big, searching for the root
        root_idx = big_part.index(root)

        if root_idx == -1:
            return False

        big_part_size = big_part.size()
        if root_idx + small_size > big_part_size:
            return False
        if treeIncludes(big_part.sub_list(root_idx, big_part_size), small):
            return True

        start_idx += root_idx + 1
        big_part = big.sub_list(start_idx, big_size)  # continue with the rest of the array


def treeIncludes(big, small):
    """
     * both big and small have the same root, inclusion check ignores sub-trees that are in big but not in small
     * @param: big, FTArray
     * @param: small, FTArray
    """
    small_size = small.size()
    big_size = big.size()
    if big_size == small_size:
        return big == small

    small_index = 1
    big_index = 1

    # loop until the end of the small tree
    while small_index < small_size:
        if big_index >= big_size:
            # there is more in small that is not in big
            return False
        big_node = big.get(big_index)
        small_node = small.get(small_index)

        while big_node != small_node:
            if big_node < -1:
                big_index += 2   # skip over leaves in big but not in small
                if big_index >= big_size:
                    # there is more in small that is not in big
                    return False
            # in a branch in big that has the same prefix but continues differently in small
            # we need to go back and skip over it -- complex case
            elif big_node == -1:
                raise ValueError
                # in big we have a branch that is not in small, skip over it
            else:
                big_index = skip_over(big, big_index + 1)
                if big_index >= big_size:
                    # there is more in small that is not in big
                    return False
            big_node = big.get(big_index)
        big_index += 1
        small_index += 1
    return True


def skip_over(tree, offset):
    """
     * in the tree at offset-1 there is the start of a subtree that we should skip over
       return the offset in the tree after that subtree
     * @param: tree, FTArray
     * @param: offset, int
    """
    offset += 1
    tree_size = tree.size()
    recursion = 1  # how deep are we recursing in the subtree
    while recursion >= 0:
        if offset >= tree_size:
            return offset  # end of the big tree, break out
        node = tree.get(offset)
        if node == -1:
            recursion -= 1
        else:
            recursion += 1

        offset += 1
    return offset
