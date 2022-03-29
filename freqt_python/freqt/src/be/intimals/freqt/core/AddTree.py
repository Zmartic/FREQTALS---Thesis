#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.core.CheckSubtree import check_subtree


def add_maximal_pattern(pat, proj, mfp, not_maximal_set):
    """
     * add maximal patterns
     * @param: pat, FTArray
     * @param: projected, Projected
     * @param: _MFP_dict, a dictionary with FTArray as keys and String as values
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
     * store root occurrences of pattern
     * @param: pat, FTArray
     * @param: projected, Projected
     * @param: _rootIDs_dict, a dictionary with Projected as keys and FTArray as values
    """
    # set of root occurrences of current pattern
    root_occ1 = {(loc.get_location_id(), loc.get_root()) for loc in proj.get_locations()}

    # check whether the current root occurrences existing in the rootID
    for elem in root_ids_list:
        root_occ2 = elem[1]
        if len(root_occ1) <= len(root_occ2):
            if root_occ1.issubset(root_occ2):
                return
        else:
            if root_occ1.issuperset(root_occ2):
                del elem

    # store root occurrences and root label
    root_ids_list.append((pat.get(0), root_occ1))


def add_high_score_pattern(pat, proj, score, hsp, num_pattern):
    """
     * add pattern to the list of N-highest chi-square score patterns
     * @param: pat, FTArray
     * @param: projected, Projected
     * @param: _HSP_dict, dictionary with FTArray as keys and Projected as values
    """
    if pat not in hsp:
        if len(hsp) >= num_pattern:
            min_pat = get_min_score_pattern(hsp, score)
            if min_pat is not None:
                # remove minScore pattern
                del min_pat
                # add new pattern
                hsp[pat] = (proj, score)
        else:
            # add new pattern
            hsp[pat] = (proj, score)


def get_min_score_pattern(hsp, current_score):
    """
     * get a pattern which has minimum chi-square score in the list of patterns
     * @param: _HSP_dict: dictionary with FTArray as key and Projected as values
    """
    min_score = current_score
    min_score_pattern = None

    for key in hsp:
        score = hsp[key][1]
        if min_score > score:
            min_score = score
            min_score_pattern = key

    return min_score_pattern
