from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
import numpy as np
import os 
import subprocess 
import linecache  
import Geometria as geo 
import Takeoff
import AVL_exe as avl 
import Avl_run as run 

x = [1,1,1,1,1]    

pista_total = 50
mi = 0.03
delt = 0.01
rho = 1.15
g = 9.8065
m = 20
alpha = 0
d = 1.15
v = 12.5 
name = 'Aerotau_2021'
Wto_1 = m*g
Sto = 51 

nameavl = name + ".st"

#Calling function geo.
[AR,Sw,cma_w,Bw,Crw,Ctw,Xref,lht,Sht,cht,bht,Svt,cvt,bvt,k,Xac,Xcg,lt] = geo.Geoaircraft(x)

#Calling function avl
run.Avl_run(m,g,v,d,alpha,name,nameavl)

#Calling function avl
[CL, CD, Cm0, CLa, Clb, Cma, Cnb, Xnp] = avl.Avl_exe(nameavl)


#Calling function takeoff
[Sto, Wto] = Takeoff.takeoff_distance(CL,CD,Sw,pista_total,rho,mi,Wto_1,Sto,delt,g)

#Calling function weight.
[Pcp, Weight_payload,MTOW]= Takeoff.weight_aircraft(Wto, Sw, Sht,Svt,g)

# Save constraints 
fid= open("resultados.txt","a+")

SM = ( Xnp - Xref ) / cma_w 

print(Sto,SM,Weight_payload,MTOW/g)