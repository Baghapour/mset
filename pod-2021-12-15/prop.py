from cmn import *
import sys
import numpy as np

#================
# Grashof number
#================

def calcFromGrashof(g=9.86,n=1,Gr=None,beta=None,dT=None,L=None,nu=None):
    #----------
    # Calc Gr
    #----------
    #if  isn(Gr) and notn(dT) and notn(L) and notn(nu) and notn(beta):
    if  isn(Gr) and allnotn([dT,L,nu,beta]):
        Data = 'Grashof'
        if alls([beta,dT,L,nu]):
            Grashof = arr([g*beta*dT*L**3/nu**2 for i in range(n)])
        else:
            try:
                Grashof = g*arr(beta)*arr(dT)*arr(L)**3/arr(nu)**2
                return Data,Grashof
            except:
                sys.exit("calcFromGrashof: Mismatching data dimensions for Grashof.")                   
    #----------
    # Calc beta
    #----------
    #elif  isn(beta) and notn(dT) and notn(L) and notn(nu):
    elif  isn(beta) and allnotn([dT,L,nu]):
        Data = 'beta'
        if alls([dT,L,nu,Gr]):
            beta = arr([Gr*nu**2/(g*dT*L**3) for i in range(n)])
        else:
            try:
                beta = arr(Gr)*arr(nu)**2/(g*arr(dT)*arr(L)**3)
                return Data,beta
            except:
                sys.exit("calcFromGrashof: Mismatching data dimensions for beta.")            
    #----------
    # Calc dT
    #----------
    #elif  isn(dT) and notn(beta) and notn(L) and notn(nu):
    elif  isn(dT) and allnotn([beta,L,nu]):
        Data = 'dT'
        if alls([beta,L,nu,Gr]):
            dT = arr([Gr*nu**2/(g*beta*L**3) for i in range(n)])  
        else:
            try:
                dT = arr(Gr)*arr(nu)**2/(g*arr(beta)*arr(L)**3)
                return Data,dT
            except:
                sys.exit("calcFromGrashof: Mismatching data dimensions for dT.") 
    #----------
    # Calc L
    #----------
    #elif  isn(L) and notn(beta) and notn(dT) and notn(nu):
    elif  isn(L) and allnotn([beta,dT,nu]):
        Data = 'L'
        if alls([beta,dT,nu,Gr]):
            L = arr([(Gr*nu**2/(g*beta*dT))**(1./3.) for i in range(n)])  
        else:
            try:
                L = (arr(Gr)*arr(nu)**2/(g*arr(beta)*arr(dT)))**(1./3.)
                return Data,L
            except:
                sys.exit("calcFromGrashof: Mismatching data dimensions for L.") 
    #----------
    # Calc nu
    #----------
    #elif  isn(nu) and notn(beta) and notn(dT) and notn(L):
    elif  isn(nu) and allnotn([beta,dT,L]):
        Data = 'nu'
        if alls([beta,L,nu,Gr]):
            nu = arr([(g*beta*dT*L**3/Gr)**0.5 for i in range(n)])  
        else:
            try:
                nu = (g*arr(beta)*arr(dT)**arr(dT)**3/arr(Gr))**0.5
                return Data,nu
            except:
                sys.exit("calcFromGrashof: Mismatching data dimensions for nu.") 
    else:
        sys.exit("calcFromGrashof: input data not set properly.") 
    print('calcFromGrashof:' + Data +'is returned...done')

#================
# Grashof number
#================

def calcFromPrandtl(n=1,Pr=None,nu=None,alf=None):
    #----------
    # Calc Pr
    #----------
    if  isn(Pr) and allnotn([nu,alf]):
        Data = 'Prandtl'
        if alls([nu,alf]):
            Prandtl = np.array([nu/alf for i in range(n)])
        else:
            try:
                Prandtl = arr(nu)/arr(alf)
                return Data,Prandtl
            except:
                sys.exit("calcFromPrandtl: Mismatching data dimensions for Prandtl.")                   
    #----------
    # Calc nu
    #----------
    if  isn(nu) and allnotn([Pr,alf]):
        Data = 'nu'
        if alls([Pr,alf]):
            nu = np.array([Pr*alf for i in range(n)])
        else:
            try:
                nu = arr(Pr)*arr(alf)
                return Data,nu
            except:
                sys.exit("calcFromPrandtl: Mismatching data dimensions for nu.")                   
    #----------
    # Calc alf
    #----------
    if  isn(alf) and allnotn([nu,alf]):
        Data = 'alf'
        if alls([nu,alf]):
            alf = np.array([nu/Pr for i in range(n)])
        else:
            try:
                alf = arr(nu)/arr(Pr)
                return Data,alf
            except:
                sys.exit("calcFromPrandtl: Mismatching data dimensions for alf.")                   
    else:
        sys.exit("calcFromPrandtl: input data not set properly.") 
    print('calcFromPrandtl:' + Data +'is returned...done')
