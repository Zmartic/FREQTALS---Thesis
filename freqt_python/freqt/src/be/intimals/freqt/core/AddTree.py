#!/usr/bin/env python3
from freqt.src.be.intimals.freqt.core.CheckSubtree import check_subtree

"""
 Set of function used to add pattern to some structure
 Usually used inside add_tree() function from FreqT's implementation
"""


def add_maximal_pattern(pat, proj, mfp, not_maximal_set):
    """
     Add a pattern to the set of maximal frequent pattern (only keep maximal pattern = super-tree)
        * if pat is a sub-tree of an other pattern -> don't add pat
        * if an other pattern is a sub-tree of pat -> remove this other pattern
    :param pat:  FTArray,   the pattern requested to be added to mfp
    :param proj: Projected, the projection of pat
    :param mfp:  Dict(FTArray, Projected), the set of maximal frequent pattern
    :param not_maximal_set: Dict(FTArray), set of pattern previously encounter that were not maximal
    """
    if len(mfp) != 0:
        if pat in not_maximal_set:
            return
        if pat in mfp:
            return

        # check maximal pattern
        for max_pat in mfp.keys():
            res = check_subtree(pat, max_pat)
            if res == 1:  # * pat is a subtree of max_pat
                not_maximal_set.add(pat)
                return
            elif res == 2:  # * max_pat is a subtree of pat
                not_maximal_set.add(max_pat)
                del mfp[max_pat]

    # add new maximal pattern to the list
    mfp[pat.copy()] = proj


def add_root_ids(pat, proj, root_ids_list):
    """
     Add a pattern to the set of root occurrences (only keep sub-set of occurrences)
        * if the set of occurrence of pat is a super-set of an other pattern
          -> don't add the occurrences of pat
        * if the set of occurrence of an other pattern is a super-set of pat
          -> remove the occurrences of this other pattern
    :param pat:  FTArray,   the pattern requested to be added to root_ids_list
    :param proj: Projected, the projection of pat
    :param root_ids_list: List(Int, Set()), the list of roots with their set of occurrences
                          Occurrence = Tuple(location_id, root_location)
    """
    # set of root occurrences of current pattern
    root_occ1 = {(loc.get_location_id(), loc.get_root()) for loc in proj.get_locations()}

    # check whether the current root occurrences existing in the rootID
    for elem in root_ids_list:
        root_occ2 = elem[1]
        if len(root_occ1) <= len(root_occ2):
            if root_occ1.issubset(root_occ2):
                del elem
        else:
            if root_occ1.issuperset(root_occ2):
                return

    # store root occurrences and root label
    root_ids_list.append((pat.get(0), root_occ1))


def add_high_score_pattern(pat, proj, score, hsp, num_pattern):
    """
     Add a pattern to the set of N-highest chi-square score patterns
    :param pat:  FTArray,   the pattern requested to be added to hsp
    :param proj: Projected, the projection of pat
    :param score: Float, the pattern chi-square score
    :param hsp: Dict(FTArray, Tuple), the set of high chi-square score patterns
                Tuple(Projected, Float) for each pattern we store its projection and its score
    :param num_pattern: int, define the maximum number of pattern that can be store in hsp
    """

    if pat not in hsp:
        if len(hsp) >= num_pattern:
            min_pat = get_min_score_pattern(hsp, pat, score)
            # remove minScore pattern
            del min_pat
            # add new pattern
            hsp[pat] = (proj, score)
        else:
            # add new pattern
            hsp[pat] = (proj, score)


def get_min_score_pattern(hsp, current_pat, current_score):
    """
     Get the pattern which has minimum chi-square score in the list of patterns (hsp + current_pattern)
    :param hsp: Dict(FTArray, Tuple), the set of high chi-square score patterns
                Tuple(Projected, Float) for each pattern we store its projection and its score
    :param current_pat: FTArray, pattern that is currently added to hsp
    :param current_score: score of the pattern that is currently added to hsp
    :return: the minimum score pattern
    """
    min_score = current_score
    min_score_pattern = current_pat

    for key in hsp:
        score = hsp[key][1]
        if min_score > score:
            min_score = score
            min_score_pattern = key

    return min_score_pattern
