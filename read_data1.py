"""
Yuchen Li
u6013787@anu.edu.au

"""
import os
import json




EXPT = "expt.in"
ALIGNMENTPARMVALS = "AlignmentParmVals.dat"

def is_float(str):
    try:
        float(str)
        return str
    except ValueError:
        return "\""+str+"\""

def read_file(path):
    """
    :param path: the path of file AlignmentParmVals.dat and expt.in
    :return: instance of Alignment and Expt

    path -> (Alignment,Expt)
    """
    expt_file = os.path.join(path,EXPT)
    alignmentparmvals_file = os.path.join(path,ALIGNMENTPARMVALS)

    alignment = None

    # read alignment
    if os.path.isfile(alignmentparmvals_file):
        alignment = {}
        with open(alignmentparmvals_file,"r") as f:
            for line in f:
                words = line.replace("\t", " ").split(": ")
                name = words[0]

                value = is_float(words[1][:-1])
                alignment[name]= value

    # read expt

    expt = None

    if os.path.isfile(expt_file):
        stack = []
        expt = {}
        stack.append(expt)

        with open(expt_file,"r",errors='replace') as f:
            multi_string = False
            name = None
            print(path)
            for line in f:
                if line == "\n":
                    continue
                if "BeginSection" in line:
                    name = line.split()[1]
                    new_dic = {}
                    stack[-1][name]=new_dic
                    stack.append(new_dic)
                    continue
                if "EndSection" in line:
                    stack.pop()
                    continue
                if "__start_multi_string__" in line:
                    multi_string = True
                    name = line.split()[0]
                    stack[-1][name]=""
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
                    value = is_float(words[1])
                    stack[-1][name] = value


    return alignment,expt

def read_dir(dir):
    """
    :param dir:
    :return: array of instance of Alignment and Expt

    str -> [(alignment,expt)]
    """
    array = []
    for path in os.listdir(dir):
        array.append(read_file(os.path.join(dir,path)))
    return array
def read_all(dir):
    for path in os.listdir(dir):

        yield read_dir(os.path.join(dir,path))

if __name__ == "__main__" :
    ge = read_all("/home/yl2404/alignmentStatFiles/")
    for items in ge:
        for item in items:
            print(item)