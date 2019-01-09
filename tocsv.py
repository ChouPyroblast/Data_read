"""
Yuchen Li
u6013787@anu.edu.au
"""

import read_data1
import pandas as pd

array = read_data1.read_all_flat("/home/yl2404/alignmentStatFiles/")

df = pd.DataFrame(array)

df.iloc[1]


