from sys import exit
import os.path
from time import gmtime, strftime
import numpy as np
import inspect

csvDict = { 
# Field types in CSV file
           'X': 'Points:0',
           'Y': 'Points:1',
           'Z': 'Points:2',
           'U': 'U:0',
           'V': 'U:1',
           'W': 'U:2',
           'P': 'p',
           'T': 'T'
          }

def meanSub(T):
    return T - T.mean(axis=1).reshape(T.shape[0],1)

def cumSum(S):
    return np.cumsum(S)/np.sum(S)

def Time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def countFile(dir,ext='csv'):
    count = 0
    for file in os.listdir(dir):
        if file.endswith("."+ext): count += 1
    if count == 0: Exit('No %s file found [error]',arg=ext)
    return count

def fileRemove(name):
    if os.path.isfile(name): os.remove(name)

#def checklen(a):
#    if isinstance(a,list) is False: return True
#    # Check for same element length
#    L = []
#    for aa in a: L.append(len(aa))
#    for LL in L:
#        if LL is not L[0]: return False
#    return True

def Exit(msg,arg=None):
    if arg is None: exit(msg)
    else: exit(msg%tuple(arg))

def Lagrange(x,xp=None,order=None):
    if order == 2:
        L0 = (x-xp[1])*(x-xp[2])/((xp[0]-xp[1])*(xp[0]-xp[2]))
        L1 = (x-xp[0])*(x-xp[2])/((xp[1]-xp[0])*(xp[1]-xp[2]))
        L2 = (x-xp[0])*(x-xp[1])/((xp[2]-xp[0])*(xp[2]-xp[1]))
        return np.array([L0,L1,L2])

def dx_Lagrange(x,xp=None,order=None):
    if order == 2:
        dx_L0 = ((x-xp[1])+(x-xp[2]))/((xp[0]-xp[1])*(xp[0]-xp[2]))
        dx_L1 = ((x-xp[0])+(x-xp[2]))/((xp[1]-xp[0])*(xp[1]-xp[2]))
        dx_L2 = ((x-xp[0])+(x-xp[1]))/((xp[2]-xp[0])*(xp[2]-xp[1]))
        return np.array([dx_L0,dx_L1,dx_L2])

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

Verific  = 'C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\current\\verific'
TestCase = 'C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\current\\testcase'

def Make(var=None,cte=None,mode=None):
    #---------------------------------
    # Making cases in format [var,cte]
    # mode-cross: Combination of vars
    # mode-Single: Point-to-Point var
    # For the single mode, all vars
    # should have same length
    #---------------------------------
    c1 = mode is not "cross" and not "single"
    if c1 is True: Exit("[error] batch: mode incorrect")
    if mode == "cross":
        t = 1
        for v in var: t *= len(v) 
        K = len(var)
        C = np.zeros((t,K))
        S = 1
        for k in range(0,K):
            D = np.zeros(t).astype(int)
            d2 = 0
            for d in range(t):
                if d%S == 0 and d>0: d2 += 1
                if d2 > len(var[k])-1: d2 = 0
                D[d] = d2
            for i in range(t):
                C[i,k] = var[k][D[i]]
            S = S*len(var[k])
    elif mode == "single":
        #if checklen(var) is False:
        #    Exit("[error] batch: single mismatch")
        t = len(var[0])
        K = len(var)
        C = np.zeros((t,K))
        for i in range(K): C[:,i] = var[i]
    G = len(cte)
    CTE  = np.zeros((t,G))
    for i in range(t): CTE[i,:] = cte
    Case = np.column_stack((C,CTE))
    #-------------------------------
    # Flattening for one-case output 
    #-------------------------------
    LM = max([len(v) for v in var])
    if LM == 1:  
        C = Case.flatten()
        Case = [[c for c in C]]
    return Case

def Extend(v=None,len=None):
    return [v for i in range(len)] 
