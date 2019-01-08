"""
Yuchen Li
u6013787@anu.edu.au

"""
import os
import json

class Alignment:
    def __str__(self):
        return str(vars(self))


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

    if os.path.isfile(alignmentparmvals_file):
        alignment = Alignment()
        with open(alignmentparmvals_file,"r") as f:
            print(alignmentparmvals_file)
            for line in f:
                words = line.replace("\t", " ").split(": ")
                print(words)
                name = words[0]

                value = is_float(words[1][:-1])
                exec("alignment."+name+"="+value)

    return alignment

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