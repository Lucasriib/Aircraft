from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
from scipy.optimize import differential_evolution
from scipy.optimize import NonlinearConstraint, Bounds
import numpy as np
import os 
import subprocess 
import linecache  
import Geometria as geo 
import Takeoff
import AVL_exe as avl 
import Avl_run as run 
import random
from deap import creator, base, tools, algorithms

def resultados(x):

    pista_total = 50.00
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
    [AR,Sw,cma_w,Bw,C_1,C_2,C_3,Xref,lht,Sht,cht,bht,Svt,cvt,bvt,k,Xac,Xcg,lt,Constraint,Vht] = geo.Geoaircraft(x)

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

    fid.write('\r{:0.1f} {:0.5f} {:0.5f} {:0.2f} {:0.5f}'
            ' {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'
            ' {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'
            ' {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'
            ' {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.4f} {:0.3f} {:0.3f} {:0.5f} '.format(AR,Sw,cma_w,Bw,C_1,
                                C_2,C_3,Xref,lht,Sht,cht,
                                bht,Svt,cvt,bvt,k,
                                Xac,Xcg,lt, CL, CD, 
                                Cm0, CLa, Clb, Cma, Cnb, Xnp,SM,Weight_payload,MTOW/g,Constraint))
    
    fid.close()


    fid= open("Empenagem.txt","a+")

    fid.write('\r{:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'
              ' {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'.format(lht,Vht,Sht,cht,bht,Svt,cvt,bvt,SM,Cm0, CLa, Clb, Cma, Cnb, Xnp))
    
    fid.close()

    fid= open("Asa.txt","a+")

    fid.write('\r{:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f} {:0.5f}'
              ' {:0.5f} {:0.5f}'.format(Bw,AR,Sw,C_1,C_2,C_3,cma_w,CL,CD,Cm0))
    
    fid.close()


    return Weight_payload, SM, lt, Bw, AR   


def objfun(x):

    Weight_payload, SM, lt, Bw , AR = resultados(x)

    return Weight_payload

def constr_f(x):

    Weight_payload, SM, lt, Bw , AR = resultados(x)

    return SM

### OPTIMIZATION

# Create list of constraints
def constr_f2(x):

    Weight_payload, SM, lt, Bw , AR = resultados(x)

    return AR
# Create list of constraints
def constr_f3(x):

    Weight_payload, SM, lt, Bw , AR = resultados(x)
    soma = lt + Bw 
    return soma


# the sum of x[0] and x[1] must be less than 1.9
nlc1 = NonlinearConstraint(constr_f, 0.05, 0.25)
nlc2 = NonlinearConstraint(constr_f2, 5.0, 12.0)
nlc3 = NonlinearConstraint(constr_f3, np.PZERO, 3.5)
# N variable 
n_vars = 9 
#  Create list of bounds 
#           C1          C2         C3        b          Xac           Xcg        Vht       Cht        Bht
bnds1 = [[0.5,0.7], [0.3,0.5],[0.05,0.2],[1.6,3.0],[0.285,0.418],[0.24,0.28],[0.35,0.5],[0.4,0.15],[0.6,1.0]]
bounds = bnds1


# Run optimizer
# Solve the optimization problem
result_de = differential_evolution(objfun, bounds,constraints=(nlc1,nlc2,nlc3), disp= bool, seed=1, maxiter=5000, polish= False)
