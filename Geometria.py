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
    
    # Geometria 
    ## Desnormalizacao do vetor de entrada
    # Fronteira de cada var
    # Filename
    #     C1      C2      C3    AR    b     Xac   Xcg   gap
    # Lb = [ 0.5,   0.3,   0.05, 5.0 , 1.2, 0.285, 0.24   ]; # Lower bond
    # Ub = [ 0.7,   0.5,   0.2, 10.0 , 2.4, 0.418, 0.28  ]; # Upper bond

    #Del interfering files
    C_1   	 = x[0]    #*(Ub[0]-Lb[0]) )+ Lb[0]                 # [m] Envergadura da asa
    C_2   	 = x[1] #*(Ub[1]-Lb[1]) )+ Lb[1]                 # [adimen] Razão de afilamento da asa
    C_3   	 = x[2] #*(Ub[2]-Lb[2]) )+ Lb[2]                 # [m] Posicao do centro aerodinamico da asa em relacao a ponta do motor
    Bw       = x[3] #*(Ub[3]-Lb[3]) )+ Lb[3]                 # [m] Envergadura da asa
    Xac      = x[4] #*(Ub[4]-Lb[4]) )+ Lb[4]                 # [m] Posicao do centro aerodinamico da asa em relacao a ponta do motor
    Xcg      = x[5] #*(Ub[5]-Lb[5]) )+ Lb[5]  
    Vht      = x[6] #*(Ub[6]-Lb[6]) )+ Lb[6]
    cht      = x[7]
    bht      = x[8]

    filename= 'Wing_2020.avl'
    #Airfoil
    perfil_section_1='TAU17.dat'
    perfil_section_2='TAU17.dat'
    perfil_section_3='NACA6412.dat'
    perfil_section_4='PSU94097.dat'
    Alpha_w_takeoof = 0
    cl_w_takeoof = 0.8

    #Wing
    # 1 section - Ret
    B_w_1           = 0.55*Bw
    S_w_1           =B_w_1*( ( C_1 + C_2) / 2 )
    Afilamento_1    = C_2/C_1
    offset_1        =0
    cma_w_1 = 2/3 * (C_1)*( (1+Afilamento_1+Afilamento_1**2) / (1 + Afilamento_1) ) # [m] - Corda media da asa

    # 2 section - 
    B_w_2           =0.45*Bw;                         # C_3 < C_2 random(C_2- 0.05,C_2)
    S_w_2           =B_w_2*( ( C_2 + C_3) / 2 )
    Afilamento_2    =C_3/C_2
    offset_2        =0.0
    cma_w_2 = 2/3 * (C_2)*( (1+Afilamento_2+Afilamento_2**2) / (1 + Afilamento_2) ) # [m] - Corda media da asa

    #ASA
    B_w             =  B_w_1 + B_w_2
    Sw              =  S_w_1 + S_w_2
    AR              =  B_w **2 / Sw
    cma_w           =  (cma_w_1 + cma_w_2)/2

    #################################################################
	## Variaveis a serem otimizadas
    ## Calculos preliminares e variaveis definidas
    name='Aerotau_2021'
    k = 3.5                                                         # [m] - Requisito de projeto, o (comprimento total)+(largura total)<= 3.7                                                      # [adimen] - Coeficiente de atrito das rodas
    offset_wing=0
    perfil_wing='TAU17.dat'
    alpha_w = 0
    Xref=Xcg*C_1
    Yref= 0
    Zref= 0
    CDp = 0.10

    ## Dimensionamento HT  
    Sht = bht * cht                                                                                                
    lht = ( Vht*cma_w*Sw ) / Sht                                # Distancia do centro aerodinamico da emp. em relacao ao CG.
    offset_ht=0

    ## Dimensionamento VT
    ARvt = 1.5                                                          # [adimen] - (FLORES, 2017)
    Svt = 0.10*Sw                                                       # 15% da area da asa.
    bvt = np.sqrt(ARvt*Svt)                                             # [m] - Envergadura da empenagem
    cvt = Svt/bvt                                                       # [m] - Corda media da empenagem
    lvt = lht                                                           # Distancia do centro aerodinamico da emp. em relacao ao CG.
    offset_vt=0

    ## Lt (Size constraint)
    lt =  Xac + 0.75*cht + lht 
    Constraint = Bw + lt # Bw + lt  3.7

    #Biplano

    ## Data generate run
    Avlgeo.Avl_geo(name,Sw,cma_w,Bw,C_1,C_2,C_3,B_w_1,B_w_2,Xref,Yref,Zref,CDp,perfil_wing,lht,cht,bht,cvt,bvt)

    return AR,Sw,cma_w,Bw,C_1,C_2,C_3,Xref,lht,Sht,cht,bht,Svt,cvt,bvt,k,Xac,Xcg,lt,Constraint,Vht