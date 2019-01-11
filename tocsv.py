
# coding: utf-8

# In[10]:

import read_data
import pandas as pd

array = read_data.read_all_flat("/home/yl2404/alignmentStatFiles/")

df = pd.DataFrame(array)

df["experiment_date"]=df["experiment_date"].apply(pd.to_datetime)


machine_name = df[df["machine_name"].notnull()]
ip_address = df[df["machine_name"].isnull()]


names = machine_name["machine_name"].unique()
for name in names:
    tmpdf = machine_name[machine_name["machine_name"]==name]
    
    tmpdf.sort_values(by="experiment_date").to_csv(name+".csv")
    
names = ip_address["host_ip_address"].unique()

for name in names:
    if pd.isnull(name):
        tmpdf = ip_address[ip_address["host_ip_address"].isnull()]
        tmpdf.sort_values(by="experiment_date").to_csv("NAN.csv")
    else:
        tmpdf = ip_address[ip_address["host_ip_address"]==name]
        tmpdf.sort_values(by="experiment_date").to_csv(name +".csv")


# In[11]:

names = machine_name["machine_name"].unique()
for name in names:
    tmpdf = machine_name[machine_name["machine_name"]==name]
    tmpdf.sort_values(by="experiment_date").to_csv(name+".csv")


# In[12]:

names = ip_address["host_ip_address"].unique()
for name in names:
    if pd.isnull(name):
        tmpdf = ip_address[ip_address["host_ip_address"].isnull()]
        tmpdf.sort_values(by="experiment_date").to_csv("NAN.csv")
    else:
        tmpdf = ip_address[ip_address["host_ip_address"]==name]
        tmpdf.sort_values(by="experiment_date").to_csv(name +".csv")


# In[13]:

metadata = ["project_name","sample_name","machine_name","host_ip_address","experiment_date"]
EXPT_parameter = ["camera_length","specimen_distance","rotation_x","Vert.detector","phi","camera_theta","camera_psi","voxel_size","pixel_size_x"]
AF_parameter = ["AF.camera_length","AF.specimen_distance","AF.origin_offset_horizontal","AF.origin_offset_vertical","AF.detector_tilt_phi","AF.detector_tilt_theta","AF.detector_tilt_psi"]
Diff_parameter = ["Camera distance","Sample distance","Hor. detector","Vert.detector","Phi detector","Theta detector","Psi detector"]


# In[14]:

columns = metadata + EXPT_parameter + AF_parameter


# In[16]:

#df["experiment_date"]=df["experiment_date"].apply(pd.to_datetime)

df['Vert.detector']= 0
df['phi']= 0



selected_df = df[columns]

sorted_columns = metadata.copy()
for i in range(len(Diff_parameter)):
    name = "DIFF-"+ Diff_parameter[i]
    selected_df[name] = selected_df[EXPT_parameter[i]]-selected_df[AF_parameter[i]]
    sorted_columns.append(EXPT_parameter[i])
    sorted_columns.append(AF_parameter[i])
    sorted_columns.append(name)
    
    

selected_df["AF.vxsize"] = selected_df["pixel_size_x"] * selected_df["AF.specimen_distance" ]/ selected_df["AF.camera_length"]
selected_df["vxsize error"] =  1 - selected_df["AF.vxsize"] / selected_df["voxel_size"]
sorted_columns.append("voxel_size")
sorted_columns.append("AF.vxsize")
sorted_columns.append("vxsize error")

selected_df = selected_df[sorted_columns]

machine_name = selected_df[selected_df["machine_name"].notnull()]
ip_address = selected_df[selected_df["machine_name"].isnull()]

names = machine_name["machine_name"].unique()
for name in names:
    tmpdf = machine_name[machine_name["machine_name"]==name]
    
    tmpdf.sort_values(by="experiment_date").to_csv(name+".csv")
    
names = ip_address["host_ip_address"].unique()
for name in names:
    if pd.isnull(name):
        tmpdf = ip_address[ip_address["host_ip_address"].isnull()]
        tmpdf.sort_values(by="experiment_date").to_csv("NAN.csv")
    else:
        tmpdf = ip_address[ip_address["host_ip_address"]==name]
        tmpdf.sort_values(by="experiment_date").to_csv(name +".csv")

