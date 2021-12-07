#!/usr/bin/env python3

from freqt.src.be.intimals.freqt.core.CheckSubtree import *


class Util:

    """
     * filter maximal patterns from list of frequent patterns
     * @param: _FP_dict, a dictionary with FTArray as key and String as value
     * @param: _config, Config
    """
    def filterFP(self, _FP_dict, _config):
        _MFP_dict = dict()
        try:
            #for each pattern
            for fp_keys in _FP_dict:
                found = False

                if len(_MFP_dict) == 0:
                    _MFP_dict[fp_keys] = _FP_dict[fp_keys]
                else:
                    #check the pattern existing in MFP list ?
                    for mfp_keys in _MFP_dict:
                        # check the labels of two subtrees before check maximal subtree
                        subtree = CheckSubtree().checkSubTree(fp_keys, mfp_keys, _config)
                        if subtree == 1:
                            found = True
                        elif subtree == 2:
                            _MFP_dict.pop(mfp_keys, -1)
                    if not found:
                        _MFP_dict[fp_keys] = _FP_dict[fp_keys]
        except:
            e = sys.exc_info()[0]
            print("Error: Filter maximal pattern: " + str(e))
            raise
        return _MFP_dict

    """
     * print input trees
     * @param: trans_list, a list of list of NodeFreqT
    """
    def printTransaction(self, trans_list):
        for elem in trans_list:
            for el in elem:
                print(str(el.getNodeLabel()) + "-" + str(el.getNode_label_int()) + " , ", end='')
            print("\n")

    """
     * print list of candidates: need for debugging
     * fp_dict, a dictionary with FTArray with keys and Projected as value
     * label_Index_dict, a dictionary with Integer as keys and String as value
    """
    def printCandidates(self, fp_dict, labelIndex_dict):
        for keys in fp_dict:
            projected = fp_dict[keys]

            print("candidate: ")
            for i in range(keys.size()):
                label = labelIndex_dict[keys.get(i)]
                if label is not None:
                    print(str(keys.get(i)) + " ")
                else:
                    print(label)
            print("\ndepth:" + str(projected.getProjectedDepth()) + "\n")
            print("locations: \n")
            self.printProjected(fp_dict[keys])

    """
     * print a pattern in FTArray format
     * @param: ft, FTArray
    """
    def printFTArray(self, ft):
        for i in range(ft.size()):
            print(str(ft.get(i)) + ",", end='')
        print()

    """
     * print a pattern in FTArray format
     * @param: ft, FTArray
     * @param: labelIndex_dict, a dictionary with Integer as keys and String as value
    """
    def printFTArray2(self, ft, labelIndex):
        for i in range(ft.size()):
            if ft.get(i) == -1:
                print("),")
            else:
                print(str(labelIndex[ft.get(i)]) + ",", end ='')
        print()

    """
     * print details of a projected
     * @param: projected, Projected
    """
    def printProjected(self, projected):
        for i in range(projected.getProjectLocationSize()):
            classID = projected.getProjectLocation(i).getClassID()
            locationID = projected.getProjectLocation(i).getLocationId()
            rootID = projected.getProjectLocation(i).getRoot()
            locationPos = projected.getProjectLocation(i).getLocationPos()
            print(str(classID) + "-" + str(locationID) + "-" + str(rootID) + "-" + str(locationPos), end='')
            if i < projected.getProjectLocationSize():
                print(";")

    """
     * get root occurrences of a pattern
     * @param: projected, Projected
    """
    def getStringRootOccurrence(self, projected):
        rootOccurrences = ""
        for i in range(projected.size()):
            rootOccurrences = rootOccurrences + str(projected.get_location(i).getClassID()) +\
                              "-" + str(projected.get_location(i).getLocationId()) + "-" + \
                              str(projected.get_location(i).getRoot())
            if i < projected.size() - 1:
                rootOccurrences = rootOccurrences + ";"
        return rootOccurrences

    """
     * return True if all element of the list 2 is contains in the list 1
     * @param: list1, a list
     * @param: list2, a list
    """
    def containsAll(self, list1, list2):
        for elem in list2:
            if elem not in list1:
                return False
        return True
