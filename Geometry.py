from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
import numpy as np
import os 
import subprocess 
import linecache  
import Avlgeo
import random as rd
from random import uniform as random


def Geoaircraft(x):
    
    # Geo 

    #Variable design 
    C_1   	 = x[0]                 
    C_2   	 = x[1]                
    C_3   	 = x[2]                
    Bw       = x[3]               
    Xac      = x[4]                
    Xcg      = x[5]   
    Vht      = x[6] 
    cht      = x[7]
    bht      = x[8]

    #Airfoil
    perfil_section_1='TAU17.dat'
    perfil_section_2='TAU17.dat'
    perfil_section_3='NACA6412.dat'
    perfil_section_4='PSU94097.dat'

    # Aircraft variables 
    Alpha_w_takeoof = 0

    #Wing
    # 1 section - Ret
    B_w_1           = 0.55*Bw
    S_w_1           =B_w_1*( ( C_1 + C_2) / 2 )
    Afilamento_1    = C_2/C_1
    offset_1        =0
    cma_w_1 = 2/3 * (C_1)*( (1+Afilamento_1+Afilamento_1**2) / (1 + Afilamento_1) ) 

    # 2 section - 
    B_w_2           =0.45*Bw;                         
    S_w_2           =B_w_2*( ( C_2 + C_3) / 2 )
    Afilamento_2    =C_3/C_2
    offset_2        =0.0
    cma_w_2 = 2/3 * (C_2)*( (1+Afilamento_2+Afilamento_2**2) / (1 + Afilamento_2) ) 

    #ASA
    B_w             =  B_w_1 + B_w_2
    Sw              =  S_w_1 + S_w_2
    AR              =  B_w **2 / Sw
    cma_w           =  (cma_w_1 + cma_w_2)/2

    #################################################################
	## Variables 
    ## Input variables 
    name='Aerotau_2021'
    k = 3.5                                                         # [m] - 
    offset_wing=0
    perfil_wing='TAU17.dat'
    alpha_w = 0
    Xref=Xcg*C_1
    Yref= 0
    Zref= 0
    CDp = 0.10

    ## HT
    Sht = bht * cht                                                                                                
    lht = ( Vht*cma_w*Sw ) / Sht                                # 
    offset_ht=0

    ## VT
    ARvt = 1.5                                                          
    Svt = 0.10*Sw                                                       # 
    bvt = np.sqrt(ARvt*Svt)                                             # [m] -
    cvt = Svt/bvt                                                       # [m] -
    lvt = lht                                                           # 
    offset_vt=0

    ## Lt (Size constraint)
    lt =  Xac + 0.75*cht + lht 
    Constraint = Bw + lt # Bw + lt  3.7


    ## Data generate run
    Avlgeo.Avl_geo(name,Sw,cma_w,Bw,C_1,C_2,C_3,B_w_1,B_w_2,Xref,Yref,Zref,CDp,perfil_wing,lht,cht,bht,cvt,bvt)

    return AR,Sw,cma_w,Bw,C_1,C_2,C_3,Xref,lht,Sht,cht,bht,Svt,cvt,bvt,k,Xac,Xcg,lt,Constraint,Vht