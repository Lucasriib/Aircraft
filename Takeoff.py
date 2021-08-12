from numpy import log as ln
from matplotlib import pyplot as plt
from scipy.optimize import minimize 
import numpy as np
import os 
import subprocess 
import linecache  
import math

def empuxo(V,rho):
    
    ## Dados das helices
    # D k c* CL* gamma n Test
    helice = [0.32385, 0.75, 0.022, 0.903, 0.0, 200.00, 42.60] # APC 12.75 x 3.75
    D = helice[0] # [m] - Diametro da helice
    k = helice[1] # [adimen] - 75# do raio da helice para analise
    c_ast = helice[2] # [m] - Corda caracteristica na regiao de 75# do raio da helice
    CL_ast = helice[3] # [adimen] - Coeficiente de sustentacao em 75# do raio da helice
    gamma = helice[4] # [adimen] - Caracteristica de 1/(L/D) proposta por vural, proximo de 0
    n = helice[5] # [rps] - Rotacoes por segundo da helice em maxima potencia do motor
    J =  V/(n*D) # [adimen] - Razao de avanco da helice
    T = (k**2)*(math.pi**2)*c_ast*0.5*rho*(n**2.0)*(D**3)*(CL_ast - 2.0*J/k)*math.sqrt(1.0+(J/(k*math.pi))**2.0)*(1-J*math.tan(gamma)/(k*math.pi))
    Test = helice[6] # Empuxo estatico
    Tdin = T # Empuxo dinamico avaliado para determinada velocidade
    ## Se o empuxo dinamico e superior ao empuxo estatico, assumir o estatico.

    if Tdin >= Test:
        Tdin = Test

    if Tdin < 0:
        Tdin = 0


    return Tdin

def takeoff_distance(CL,CD,Sw,pista_total,rho,mi,Wto_1,Sto,delt,g):
    Wto = Wto_1
    rho = rho
    pista_total = pista_total
    Sto = Sto

    while Sto > pista_total:
        L   = 0
        V   = 0
        Sto = 0
        CL=CL
        CD=CD
        while L <= Wto:

            T = empuxo(V,rho)


            if V == 0:
                a = (g/Wto)*(T - mi*Wto) # [m/s^2] - Aceleraï¿½ï¿½o da aeronave com velocidade 0
            else:
                a = (g/Wto)*(T - mi*Wto - (CD - mi*CL)*0.5*rho*V**(2)*Sw)
            
            Sto = Sto + V*delt + 0.5*a*delt**(2)
            V = V + a*delt
            L = rho*V**(2)*0.5*CL*Sw
             
            if Sto > pista_total:
                break 

        if L < Wto:
            Wto = Wto - 0.2*g
            L   = 0
            V   = 0
            T = 0
            a = 0 
            CL=CL
            CD=CD
        if L > Wto:
            break

    #print(Sto)        
    return Sto, Wto        


def weight_aircraft(Wto, Sw, Sht,Svt,g):
    ##Pontuação carga paga
    MTOW = Wto
    # Peso Motor
    Weight_engine = 0.730 #[Kg]

    # Peso Tail
    Weight_tail = 0.400 #[Kg]

    # Peso Empenagem Vertical
    Weight_ev = Svt*1.25 #[Kg]

    # Peso Empenagem Horizontal
    Weight_eh = Sht*1.02 #[Kg]

    # Peso Asa
    Weight_wing = Sw*0.84 #[Kg]

    # Peso Eletrica
    Weight_ele = 0.900#[Kg]

    # Peso Trem de pouso
    Weight_tp = 0.100 #[Kg]

    # Peso total da estrutura
    weight_struct = Weight_engine + Weight_tail + Weight_ev + Weight_eh + Weight_wing + Weight_ele + Weight_tp # value of struct total

    # Carga paga
    Weight_payload = ( MTOW/g ) - weight_struct # Payload =[KG]

    # Pontuação da carga paga
    Pcp = 12.5 * Weight_payload 

    return Pcp, Weight_payload,MTOW     

##MTOW 
