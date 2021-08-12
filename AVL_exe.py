from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
import numpy as np
import os 
import subprocess 
import linecache  
import Avlgeo


def Avl_exe(nameavl):
  
    # Open file exe
    run_avl_command = "avl.exe <" + "Avl_run.run"
    p = subprocess.Popen(run_avl_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    try:
         p.wait(4)
    except subprocess.TimeoutExpired:
         p.kill()
        
            
    #  Open the st file to get the data.

    Save = []
    fid = open(nameavl,"r")
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
    Clb = float(Save_Clb.split(" ")[-1] )
    Cnb = float(Save_Cnb.split(" ")[-1] )
    Xnp = float(Save_Xnp.split(" ")[-1] )

    n=(-1)
    for token in Save_CLa.split(" "):
        try:
            # if this succeeds, you have your (first) float
            n = n+1
            CLa=float(Save_CLa.split(" ")[n])
            break
        except ValueError:
            pass 

    k=(-1)
    for token in Save_Cma.split(" "):
        try:
            # if this succeeds, you have your (first) float
            k = k+1
            Cma=float(Save_Cma.split(" ")[k])
            break
        except ValueError:
            pass 










    del Save 
    
    if os.path.exists(nameavl):
        os.remove(nameavl)

    return CL, CD, Cm0, CLa, Clb, Cma, Cnb, Xnp
