# Avlrun generate 
from numpy import log as ln
from matplotlib import pyplot as plt
import numpy as np
import os 

#def generaterun(v,m,g):
def Avl_run(m,g,v,d,alpha,name,nameavl):
    Avlrun='Avl_run.run'
    file = name + ".avl"
    #####################################################################################################  
    #   Open file       
    fid= open(Avlrun,'w')
    #  Cabeçalho
    fid.write("LOAD {}\r".format(file))
    fid.write("oper\r")
    fid.write("c1\r")
    fid.write("m\r")
    fid.write("{:0.3f}\r".format(m))
    fid.write("g\r")
    fid.write("{:0.3f}\r".format(g))
    fid.write("v\r")
    fid.write("{:0.2f}\r".format(v))
    fid.write("d\r")
    fid.write("{:0.3f}\r".format(d))
    fid.write("\r")
    fid.write("a\r")
    fid.write("a\r")
    fid.write("{:0.1f}\r".format(alpha))
    fid.write("x\r")
    fid.write("st\r")
    fid.write("{}.st\r".format(name))
    fid.write("\r")
    fid.write("\r")
    fid.write("Quit\n")
    fid.close()
