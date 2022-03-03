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
    return fast_check_subtree(pat1, pat2)


def fast_check_subtree(pat1, pat2):
    """
     return 0 = no subtree, 1 = pat1 is a subtree of pat2, 2 = pat2 is a subtree of pat1
      * @param: pat1, FTArray
      * @param: pat2, FTArray
    """
    if pat1.size() == pat2.size():
        return 1 if pat1 == pat2 else 0

    if pat1.size() > pat2.size():
        return 2 if has_subtree(pat1, pat2) else 0

    return 1 if has_subtree(pat2, pat1) else 0


def complex_check_subtree(small, big):
    fr = FreqT_subtree()
    fr.checkSubtrees(small, big)

    return len(fr.getOutputPattern()) != 0


def has_subtree(big, small):
    """
    return true if a tree is a subtree of an other
     * @param big, FTArray
     * @param small, FTArray
    """
    root = small.get(0)  # the root of small
    start_idx = 0
    big_part = big

    while True:  # loop over big, searching for the root
        root_idx = big_part.index(root)
        if root_idx == -1:  # no root found
            return False

        # * Size consistency
        if root_idx + small.size() > big_part.size():
            return False

        # --- Verify if small is included in big_part ---
        big_part = big_part.sub_list(root_idx, big_part.size())

        if big_part.size() == small.size():
            return big_part == small

        small_index = 1
        big_part_index = 1
        is_included = True

        while small_index < small.size():  # loop until the end of the small tree
            if big_part_index >= big_part.size():
                is_included = False  # there is more in small that is not in big
                break

            # -- Look for small_node in big --
            big_node = big_part.get(big_part_index)
            small_node = small.get(small_index)

            while big_node != small_node:
                # - skip over leaves in big but not in small
                if big_node < -1:
                    big_part_index += 2
                # - in a branch in big that has the same prefix but continues differently in small
                # we need to go back and skip over it -- complex case
                elif big_node == -1:
                    return complex_check_subtree(small, big)
                # - in big we have a branch that is not in small, skip over it
                else:
                    big_part_index = skip_over(big_part, big_part_index + 1)

                if big_part_index >= big_part.size():
                    is_included = False  # there is more in small that is not in big
                    break

                big_node = big.get(big_part_index)
            # --                            --
            if not is_included:
                break
            big_part_index += 1
            small_index += 1

        if is_included:
            return True
        # ---                                         ---

        # * Continue looping with the rest of the array
        start_idx += root_idx + 1
        big_part = big.sub_list(start_idx, big.size())


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
