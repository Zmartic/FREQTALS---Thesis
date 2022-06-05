"""
    Collection of function used to check whether a small pattern
    is a subtree of a big pattern
"""
# !/usr/bin/env python3

from freqt.src.be.intimals.freqt.core.FreqTUtil.FreqT_subtree import FreqT_subtree


def check_subtree(pat1, pat2):
    """
     Check if a on pattern is a subtree of an other pattern
    :param pat1: FTArray
    :param pat2: FTArray
    :return: int, 0 = no subtree
                  1 = pat1 is a subtree of pat2
                  2 = pat2 is a subtree of pat1
    """
    if pat1.size() == pat2.size():
        return 1 if pat1 == pat2 else 0

    if pat1.size() > pat2.size():
        return 2 if has_subtree(pat1, pat2) else 0

    return 1 if has_subtree(pat2, pat1) else 0


def has_subtree(big, small):
    """
     Return true if the tree "small" is a subtree of "big"
        * It's compute using a greedy algorithm which try to match each node of "small"
          with a node in "big" (from left to right)
        * If a complex case is encounter, fallback to a complete algorithm: FreqT_subtree
    :param big: FTArray, the big tree
    :param small: FTArray, the small tree
    :return: boolean, whether "small" is a subtree of "big"

    note: this function could be upgraded by avoiding to create sub_list of "big"
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
                # - skip over LEAF in big, which is not present in small
                if big_node < -1:
                    big_part_index += 2
                # - in a branch in big that has the same prefix but continues differently in small
                # we need to go back and skip over it -- complex case
                elif big_node == -1:
                    return FreqT_subtree(small, big).check_subtree()
                # - skip over BRANCH in big, which is not present in small
                else:
                    big_part_index = skip_over(big_part, big_part_index + 1)

                if big_part_index >= big_part.size():
                    is_included = False  # there is more in small that is not in big
                    break

                big_node = big_part.get(big_part_index)
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
        big_part = big.sub_list(start_idx, big.size())  # :: could be avoided


def skip_over(tree, offset):
    """
     In "tree" at offset-1 begins a branch that we would like to skip over.
     Return the new offset after skipping over this branch.
    :param tree: FTArray
    :param offset: int, the current offset
    :return: int, the new offset
    """
    offset += 1
    tree_size = tree.size()
    depth = 1  # depth of the branch

    while depth >= 0:  # stop when we have skipped the branch
        if offset >= tree_size:
            return offset  # end of the big tree, break out
        node = tree.get(offset)
        if node == -1:
            depth -= 1
        else:
            depth += 1

        offset += 1

    return offset
