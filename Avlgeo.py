# Avlgeo generate 
from numpy import log as ln
from matplotlib import pyplot as plt
import numpy as np
import os 

#def generaterun(v,m,g):
#####################################################################################################   

def Avl_geo(name,Sw,cma_w,Bw,C_1,C_2,C_3,B_w_1,B_w_2,Xref,Yref,Zref,CDp,perfil_wing,lht,cht,bht,cvt,bvt):
    
    # Cleaning 

    if os.path.exists("{} .avl".format(name)):
        os.remove(name)

    Arquivo = name + ".avl"
    #   Open file       
    fid= open(Arquivo,'w')
    #  Cabeçalho
    fid.write("{}\r".format(name))
    fid.write("0.0\r")
    fid.write("0 0 0\r")
    fid.write("{:0.3f} {:0.3f} {:0.3f}\r".format(Sw, cma_w, Bw)) #Sref   Cref   Bref
    fid.write("{:0.3f} {:0.3f} {:0.3f}\r".format(Xref,Yref,Zref)) #Xref   Yref   Zref
    fid.write("{:0.3f}\r".format(CDp)) #CDp
    #  Surface 
    #  Asa 
    fid.write("SURFACE\r")
    fid.write("ASA\r")
    fid.write("20 1 35 1\r") #Discretização
    fid.write("YDUPLICATE\r")
    fid.write("0.0\r")
    fid.write("ANGLE\r")
    fid.write("0.0\r")
    fid.write("COMPONENT\r")
    fid.write("1\r")
    #  SECTION 1 
    fid.write("SECTION\r")
    fid.write("0 0 0 {:0.3f} 0\r".format(C_1))
    fid.write("AFILE\r")
    fid.write("{}\r".format(perfil_wing))
    fid.write("CLAF\r")
    fid.write("1.094\r")
    #  SECTION 2
    fid.write("SECTION\r")
    fid.write("0 {:0.3f} 0 {:0.3f} 0\r".format((B_w_1/2), C_2))
    fid.write("AFILE\r")
    fid.write("{}\r".format(perfil_wing))
    fid.write("CLAF\r")
    fid.write("1.094\r")
    #  SECTION 3
    fid.write("SECTION\r")
    fid.write("0 {:0.3f} 0 {:0.3f} 0\r".format((B_w_1 + B_w_2/2), C_3))
    fid.write("AFILE\r")
    fid.write("{}\r".format(perfil_wing))
    fid.write("CLAF\r")
    fid.write("1.094\r")
    #  Surface 
    #  HT 
    fid.write("SURFACE\r")
    fid.write("Horizontal tail\r")
    fid.write("5 1 10 1\r") #Discretização
    fid.write("YDUPLICATE\r")
    fid.write("0.0\r")
    fid.write("ANGLE\r")
    fid.write("0.0\r")
    fid.write("TRANSLATE\r")
    fid.write("{:0.3f} 0 0\r".format((lht + C_1*0.25 - cht*0.25)))
    fid.write("COMPONENT\r")
    fid.write("2\r")
    #  SECTION
    fid.write("SECTION\r")
    fid.write("0 0 0 {:0.3f} 0\r".format(cht))
    fid.write("NACA\r")
    fid.write("0012\r")
    fid.write("SECTION\r")
    fid.write("0 {:0.3f} 0 {:0.3f} 0\r".format((bht/2), cht))
    fid.write("NACA\r")
    fid.write("0012\r")
    #  Surface 
    #  VT 
    fid.write("SURFACE\r")
    fid.write("Vertical tail\r")
    fid.write("5 1 10 1\r") #Discretização
    fid.write("YDUPLICATE\r")
    fid.write("0.0\r")
    fid.write("ANGLE\r")
    fid.write("0.0\r")
    fid.write("TRANSLATE\r")
    fid.write("{:0.3f} 0 0\r".format((lht + C_1*0.25 - cht*0.25)))
    fid.write("COMPONENT\r")
    fid.write("3\r")
    #  SECTION
    fid.write("SECTION\r")
    fid.write("0 0 0 {:0.3f} 0\r".format(cvt))
    fid.write("NACA\r")
    fid.write("0012\r")
    fid.write("SECTION\r")
    fid.write("0 0 {:0.3f} {:0.3f} 0\r".format((bvt/2), cvt))
    fid.write("NACA\r")
    fid.write("0012\r")
    fid.close()

    return Arquivo