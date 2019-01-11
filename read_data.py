"""
Yuchen Li
u6013787@anu.edu.au


"""
import os
import pandas

EXPT = "expt.in"  # name of expt file
ALIGNMENTPARMVALS = "AlignmentParmVals.dat" # name of AF file


def is_float(s):
    """
    :param input a string, if it can be return to float then return float, otherwise return itself:
    :return: float or string

    str -> float or str
    """
    try:
        float(s)
        return float(s)

    except ValueError:
        return s


def read_file(path):

    """
    :param path: the path of file AlignmentParmVals.dat and expt.in
    :return: dictionary of AF and Expt

    path -> (Alignment,Expt)
    """

    expt_file = os.path.join(path, EXPT)
    alignmentparmvals_file = os.path.join(path, ALIGNMENTPARMVALS)

    alignment = None

    # read AF
    if os.path.isfile(alignmentparmvals_file):  # if file exists
        alignment = {}
        with open(alignmentparmvals_file, "r") as f:
            for line in f:
                words = line.replace("\t", " ").split(": ")  # split the key and value

                name = words[0]
                value = is_float(words[1][:-1])
                alignment[name] = value

    # read Expt

    expt = None

    if os.path.isfile(expt_file):
        stack = []  # to record the bracket
        expt = {}
        stack.append(expt)

        with open(expt_file, "r", errors='replace') as f:
            multi_string = False
            name = None
            for line in f:
                if line == "\n":
                    continue
                if "BeginSection" in line:
                    name = line.split()[1]
                    new_dic = {}
                    stack[-1][name] = new_dic
                    stack.append(new_dic)
                    continue
                if "EndSection" in line:
                    stack.pop()
                    continue
                if "__start_multi_string__" in line:
                    multi_string = True
                    name = line.split()[0]
                    stack[-1][name] = ""
                    continue
                if "__end_multi_string__" in line:
                    multi_string = False
                    continue
                if multi_string:
                    stack[-1][name] += line
                    continue

                words = line.replace("\t", " ").split()

                if len(words) == 1:
                    name = words[0]
                    stack[-1][name] = None
                else:
                    name = words[0]
                    value = is_float(" ".join(words[1:]))
                    stack[-1][name] = value

    return alignment, expt


def read_file_flat(path):

    """
    :param path: the path of file AlignmentParmVals.dat and expt.in
    :return: dictionary of AF and Expt. Put them together

    path -> dict
    """

    expt_file = os.path.join(path, EXPT)
    alignmentparmvals_file = os.path.join(path, ALIGNMENTPARMVALS)

    df = {}

    # read AF
    if os.path.isfile(alignmentparmvals_file) and os.path.isfile(expt_file):  # if file exists
        with open(alignmentparmvals_file, "r") as f:
            for line in f:
                words = line.replace("\t", " ").split(": ")  # split the key and value
                name = "AF."+words[0]
                value = is_float(words[1][:-1])
                df[name] = value

        # read Expt

        with open(expt_file, "r", errors='replace') as f:
            multi_string = False
            name = None
            for line in f:
                if line == "\n":
                    continue
                if "BeginSection" in line:
                    continue
                if "EndSection" in line:
                    continue
                if "__start_multi_string__" in line:
                    multi_string = True
                    name = line.split()[0]
                    df[name] = ""
                    continue
                if "__end_multi_string__" in line:
                    multi_string = False
                    continue
                if multi_string:
                    df[name] += line
                    continue

                words = line.replace("\t", " ").split()

                if len(words) == 1:
                    continue
                name = words[0]
                value = is_float(" ".join(words[1:]))
                df[name] = value
    return df



def read_dir(dir):
    """
    :param dir:
    :return: array of instance of Alignment and Expt

    str -> [(alignment,expt)]
    """
    array = []
    for path in os.listdir(dir):
        array.append(read_file(os.path.join(dir, path)))
    return array


def read_dir_flat(dir):
    """
    :param dir:
    :return: array of instance of Alignment and Expt

    This funciton is used to produce .csv file
    str -> [dict]
    """
    array = []
    for path in os.listdir(dir):
        dic = read_file_flat(os.path.join(dir, path))
        if len(dic) > 0:
            array.append(dic)
    return array


def read_all(dir):
    for path in os.listdir(dir):
        yield read_dir(os.path.join(dir, path))


def read_all_flat(dir):
    """
    :param dir:
    :return: array of all data
    This funciton is used to produce .csv file
    """
    array = []
    for path in os.listdir(dir):
        array.extend(read_dir_flat(os.path.join(dir, path)))
    return array


if __name__ == "__main__":
    #item = read_file_flat("/home/yl2404/alignmentStatFiles/ANU3_Testing/5mm_Berea_Standard")
    #for i in item:
        #print(i,item[i])

    #print(len(item))
    item = read_all_flat("/home/yl2404/alignmentStatFiles/")
    #for i in item:
        #print(i)