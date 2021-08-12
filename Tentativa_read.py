from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
import numpy as np
import os 
import subprocess 
import linecache  
import Avlgeo
import random



Save = []
fid = open('Aerotau_2021.st',"r")
contents = fid.readlines()
for line in contents: 
    line.split(" ")
    Save.append(line)
fid.close()    

Save_CL  = Save[23] 
Save_CD  = Save[24]
Save_Cm0 = Save[20]
Save_CLa = Save[36]
Save_Clb = Save[38]
Save_Cma = Save[39]
Save_Cnb = Save[40]
Save_Xnp = Save[50]

CL  = float(Save_CL.split(" ")[-1])
CD  = float(Save_CD.split(" ")[-1]  )
Cm0 = float(Save_Cm0.split(" ")[-1] )
#CLa = float(Save_CLa.split(" ")[12] )
Clb = float(Save_Clb.split(" ")[-1] )
print((Save_CLa.split(" ")))

# n = (-1)
# for item in Save_CLa.split(" "):
#     n=n+1
#     print(item,n)
#     if item == float:
#         break
# else:
#     print(item)
n=(-1)
for token in Save_CLa.split(" "):
    try:
        # if this succeeds, you have your (first) float
        n = n+1
        print(float(token),n) 
        CLa=float(Save_CLa.split(" ")[n])
        print("CLa=",CLa)
        break
    except ValueError:
        pass 

k=(-1)
for token in Save_Cma.split(" "):
    try:
        # if this succeeds, you have your (first) float
        k = k+1
        print(float(token),k) 
        Cma=float(Save_Cma.split(" ")[k])
        print("Cma=",Cma)
        break
    except ValueError:
        pass 


# try:
#     Cma=float(Save_Cma.split(" ")[14])
# except (ValueError) as e:
#         Cma=float(Save_Cma.split(" ")[13])
# except (ValueError) as a:
#             Cma=float(Save_Cma.split(" ")[12])

#print(CLa)

Cnb = float(Save_Cnb.split(" ")[-1] )
Xnp = float(Save_Xnp.split(" ")[-1] )

# print(np.random.uniform(0.0,1.0,6))
