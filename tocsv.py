"""
Yuchen Li
u6013787@anu.edu.au
"""
import read_data1
import pandas as pd

array = read_data1.read_all_flat("/home/yl2404/alignmentStatFiles/")

df = pd.DataFrame(array)

df["experiment_date"] = df["experiment_date"].apply(pd.to_datetime)

machine_name = df[df["machine_name"].notnull()]
ip_address = df[df["machine_name"].isnull()]

names = machine_name["machine_name"].unique()
for name in names:
    tmpdf = machine_name[machine_name["machine_name"] == name]

    tmpdf.sort_values(by="experiment_date").to_csv(name + ".csv")

names = ip_address["host_ip_address"].unique()
for name in names:
    if pd.isnull(name):
        tmpdf = ip_address[ip_address["host_ip_address"].isnull()]
        tmpdf.sort_values(by="experiment_date").to_csv("NAN.csv")
    else:
        tmpdf = ip_address[ip_address["host_ip_address"] == name]
        tmpdf.sort_values(by="experiment_date").to_csv(name + ".csv")