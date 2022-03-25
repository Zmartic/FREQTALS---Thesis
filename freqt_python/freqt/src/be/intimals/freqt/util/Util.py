#!/usr/bin/env python3

def read_whiteLabel(path):
    _whiteLabels = dict()
    try:
        f = open(path, 'r')
        line = f.readline()
        while line:
            if line != "" and line[0] != '#' and line != "\n":
                str_tmp = line.split()
                ASTNode = str_tmp[0]
                children_set = set()
                for i in range(1, len(str_tmp)):
                    children_set.add(str_tmp[i])
                _whiteLabels[ASTNode] = children_set
            line = f.readline()
        f.close()
    except:
        e = sys.exc_info()[0]
        print("Error: reading white list " + str(e))
        print(traceback.format_exc())

    return _whiteLabels