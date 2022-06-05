#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.util.Variables import UNICHAR


def satisfy_chi_square(score, chi_square_threshold):
    """
    :return: whether the score passes the threshold
    """
    return score >= chi_square_threshold


def chi_square(proj, size_class1, size_class2, weighted):
    """
    :param proj: Projected, projection of a pattern
    :param size_class1: number of class 1 trees
    :param size_class2: number of class 2 trees
    :param weighted: Boolean, whether weighted support is used
    :return: chi square value of the pattern
    """
    sup_c1, sup_c2 = get_2class_support(proj, weighted)

    # a: occurrences in the first class data
    # c: occurrences in the second class data

    yaminxb = size_class2 * sup_c1 - size_class1 * sup_c2
    one = yaminxb / ((sup_c1+sup_c2) * (size_class1 + size_class2 - sup_c1 - sup_c2))
    two = yaminxb / (size_class1 * size_class2)

    return one * two * (size_class1 + size_class2)


def get_2class_support(proj, weighted):
    """
    :param proj: Projected of a pattern
    :param weighted: Boolean, whether weighted support is used
    :return: Int, the supports of pattern in each class
    """
    if weighted:
        # count support by occurrences
        sup_c1 = get_root_support_class1(proj)
        sup_c2 = proj.get_root_support() - sup_c1
    else:
        # count support by files
        sup_c1 = get_support_class1(proj)
        sup_c2 = proj.get_support() - sup_c1

    return sup_c1, sup_c2


def get_support_class1(proj):
    """
    :param proj: Projected of a pattern
    :return: Int, support of pattern in the class 1
    """
    return len({loc.get_location_id()
                for loc in proj.get_locations() if loc.get_class_id() == 1})


def get_root_support_class1(proj):
    """
    :param proj: Projected of a pattern
    :return: Int, weighted support of pattern in the class 1
    """
    return len({(loc.get_location_id(), loc.get_root())
                for loc in proj.get_locations() if loc.get_class_id() == 1})


def prune(candidates, min_sup, weighted):
    """
     * prune candidates based on minimal support
    :param candidates: Dict(Any,Projected), candidate patterns with their projection
    :param min_sup: Int, minimum support threshold
    :param weighted: Boolean, whether weighted support is used
    """
    for elem in list(candidates.keys()):
        proj = candidates[elem]

        sup = proj.compute_support()
        w_sup = proj.compute_root_support()
        limit = w_sup if weighted else sup

        if limit < min_sup:
            del candidates[elem]


def prune_min_supp(proj, min_sup):
    """
    :param proj: Projected, projection of a pattern
    :param min_sup: Int, minimum support threshold
    :return: whether proj can be pruned
    """
    if min_sup < proj.compute_support():
        _ = proj.compute_root_support()
        return True
    return False


def prune_min_w_supp(proj, min_sup):
    """
    :param proj: Projected, projection of a pattern
    :param min_sup: Int, minimum weighted support threshold
    :return: whether proj can be pruned
    """
    if min_sup < proj.compute_root_support():
        _ = proj.compute_support()
        return True
    return False


def satisfy_min_node(pat, min_node):
    """
    :param pat: FTArray, pattern
    :param min_node: Int, minimum number of nodes
    :return: whether the number of nodes is larger or equal to min_node
    """
    return pat.n_node >= min_node


def satisfy_min_leaf(pat, min_leaf):
    """
    :param pat: FTArray, pattern
    :param min_leaf: Int, minimum number of leaf nodes
    :return: whether the number of leaves is larger or equal to min_leaf
    """
    return pat.n_leaf >= min_leaf


def satisfy_max_leaf(pat, max_leaf):
    """
    :param pat: FTArray, pattern
    :param max_leaf: Int, maximum number of leaf nodes
    :return: whether the number of leaves is smaller or equal to max_leaf
    """
    return pat.n_leaf >= max_leaf


def is_not_full_leaf(pat):
    """
    :param pat: FTArray, pattern
    :return: whether every leaf of pat are leaves in the data
    """
    for i in range(0, pat.size() - 1):
        if pat.get(i) != -1 and pat.get(i + 1) == -1:
            if pat.get(i) >= 0:
                return True
    return False


def missing_left_obligatory_child(pat, candidate_prefix, grammar):
    """
    :param pat: FTArray, pattern
    :param candidate_prefix: Int, number of -1 "up" move in the last extension added
    :param grammar: Dict(Int,List(String))
    :return: whether pattern misses obligatory child at the left side of the current node
    """
    # find parent's position of candidate in the patterns
    parent_pos = pat.find_parent_position(candidate_prefix)
    # find all children of patternLabel in grammar
    children_grammar = grammar[pat.get(parent_pos)]

    if children_grammar[0] == "ordered" and not children_grammar[1] == "1":
        # find all children of parentPos in pattern
        children_pos = pat.find_children_position(parent_pos)
        # compare children in pattern and children in grammar
        i = 0
        j = 2
        while i < len(children_pos) and j < len(children_grammar):
            child_grammar_temp = children_grammar[j].split(UNICHAR)
            label_int = int(child_grammar_temp[0])
            if pat.get(children_pos[i]) == label_int:
                i += 1
                j += 1
            else:
                # if this child is optional
                if child_grammar_temp[1] == "false":
                    j += 1
                elif child_grammar_temp[1] == "true":
                    return True

    return False


def missing_right_obligatory_child(pat, grammar):
    """
      1. find children of the current node in the pattern
      2. find children of the current node in the grammar
      3. compare two set of children to determine the pattern missing mandatory child or not
    :param pat: FTArray, pattern
    :param grammar: Dict(Int,List(String))
    :return: whether pattern misses obligatory child at the right side of the current node
    """
    for pos in range(pat.size()):
        current_label = pat.get(pos)
        if current_label >= 0:  # consider only internal label
            # find all children of patternLabel in grammar
            children_grammar = grammar[current_label]
            if children_grammar[0] == "ordered" and not children_grammar[1] == "1":
                # get all children of the current pos in pattern
                children_pos = pat.find_children_position(pos)
                if len(children_pos) > 0:
                    # -- check leaf children --
                    # compare two sets of children
                    # -> determine if this pattern misses mandatory child or not
                    i = 0
                    j = 2
                    while i < len(children_pos) and j < len(children_grammar):
                        child_grammar_temp = children_grammar[j].split(UNICHAR)
                        label_int = int(child_grammar_temp[0])

                        if pat.get(children_pos[i]) == label_int:
                            i += 1
                            j += 1
                        else:
                            if child_grammar_temp[1] == "false":
                                j += 1
                            elif child_grammar_temp[1] == "true":
                                return True

                    # check right children
                    if j < len(children_grammar):
                        while j < len(children_grammar):
                            child_grammar_temp = children_grammar[j].split(UNICHAR)
                            if child_grammar_temp[1] == "true":
                                return True
                            j += 1

    return False


# /////////// specific functions for COBOL source code //////////////////
def check_cobol_constraints(pattern, entry_dict, key, label_index, transaction_list):
    """
     * @param: pattern, FTArray
     * @param: entry_dict, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: labelIndex_dict, dictionary with Integer as keys and String as values
     * @param: transaction_list, list of list of NodeFreqT
    """
    # check continuous paragraphs
    # if potential candidate = SectionStatementBlock
    # then check if candidate belongs to black-section or not
    candidate_label = label_index[key.get(key.size() - 1)]
    if candidate_label == "SectionStatementBlock":
        check_black_section(entry_dict, key, transaction_list)

    # expand the pattern if all paragraphs are continuous
    if candidate_label == "ParagraphStatementBlock":
        check_continuous_paragraph(pattern, entry_dict, key, transaction_list)


def check_continuous_paragraph(pat, entry_dict, key, _transaction_list):
    """
     * @param: pat, FTArray
     * @param: entry_dict, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: _transaction_list, list of list of NodeFreqT
    """
    projected = entry_dict[key]
    # find parent's location of Paragraph
    parent_pos = pat.find_parent_position(key)
    # find Paragraph locations
    children_pos = pat.find_children_position(parent_pos)

    if len(children_pos) == 1:
        return
    # check continuous paragraphs
    # find the first position in pos --> compare to the last position

    i = 0
    while i < projected.getProjectLocationSize():
        pos = projected.getProjectLocation(i)
        pos_id = pos.getLocationId()

        first_pos = 0
        for j in range(pos.size() - 2, 0, -1):
            label = _transaction_list[pos_id][pos.get(j)].getNode_label_int()
            if label == pat.get(children_pos[len(children_pos) - 2]):
                first_pos = pos.get(j)
                break
        last_pos = pos.get(pos.size() - 1)
        if _transaction_list[pos_id][first_pos].getNodeSibling() != last_pos:
            # remove paragraph location
            projected.deleteProjectLocation(i)
            i -= 1
        else:
            i += 1
    # modify the entry value
    entry_dict[key] = projected


def check_black_section(entry_dict, key, _transaction_list):
    """
     * delete locations of a label that belongs to black-section?
     * @param: entry, dictionary with FTArray as keys and Projected as values
     * @param: key, FTArray, a key of entry_dict
     * @param: _transaction_list, list of list of NodeFreqT
    """
    black_section_list_set = set()
    black_section_list_set.add("*CCVS1")
    black_section_list_set.add("*CCVS-EXIT")

    projected = entry_dict[key]
    i = 0
    while i < projected.getProjectLocationSize():
        # get position of the current label
        proj_id = projected.getProjectLocation(i).getLocationId()
        # for each location check if it belongs to SectionStatementBlock or not
        current_pos = projected.getProjectLocation(i).getLocationPos()
        # check if label of section is in black-section or not
        while current_pos != -1:
            if _transaction_list[proj_id][current_pos].getNodeLabel() in black_section_list_set:
                projected.deleteProjectLocation(i)
                i -= 1
                break
            current_pos = _transaction_list[proj_id][current_pos].getNodeChild()
        i += 1
    # modify the values of the key
    entry_dict[key] = projected


def count_leaf_node(pat):
    """
    :param pat: FTArray, pattern
    :return: the number of leaf nodes in pat
    """
    count = 0
    for i in range(0, pat.size()):
        if pat.get(i) < -1:
            count += 1
    return count


def count_node(pat):
    """
    :param pat: FTArray, pattern
    :return: the number of nodes in pat
    """
    count = 0
    for i in range(0, pat.size()):
        if pat.get(i) != -1:
            count += 1
    return count
