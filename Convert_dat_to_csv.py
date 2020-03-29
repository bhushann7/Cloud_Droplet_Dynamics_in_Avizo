import pandas as pd
import numpy as np
import glob
import os


file_path="/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Lagrangian/Raw_Data/"
f = [x for x in os.listdir(file_path)]

for i in f:
  path=os.path.join(file_path,i)
  x,y,z,r=[],[],[],[]
  g= open(path,"r") 
  print("file opened",i)
  for j in g.readlines():
    b=j.split()
    x.append(float(b[0])*10)
    y.append(float(b[1])*10)
    z.append(float(b[2])*10)
    r.append(float(b[3]))
  df = pd.DataFrame({'x': x, 'y': y, 'z': z,'r':r})
  new_name = i.split('.')[0] + i.split('.')[1]
  df.to_csv("./csv_data1/"+new_name+".csv")
  print("file done",i)
