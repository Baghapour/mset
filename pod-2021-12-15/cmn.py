import sys
import os
import os.path
from time import gmtime, strftime
import numpy as np
import pandas as pd

#================================================
# File Management:
# path: The path set to read data folder (case)
# batch: The running batch for solver simulations
#================================================

def clear():
    #-------------
    # Clear screen
    #-------------
    _ = os.system('cls')

def Time():
    #---------------------
    # Report date and time
    #---------------------
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def countFile(dir,ext='csv'):
    #-----------------------------
    # Count sample files in given
    # extension in given directory
    #-----------------------------
    count = 0
    for file in os.listdir(dir):
        if file.endswith("."+ext):
            count += 1
    if count == 0:
        os.exit('No '+ext+' file is found in '+dir)
    return count

def fileRewrite(name):
    if os.path.isfile(name):
        os.remove(name)

def arr(a):
    return np.array(a)

def isc(a):
    if np.isscalar(a) is True: return True
    else: return False

def nots(a):
    if np.isscalar(a) is False: return True
    else: return False

def alls(a):
    for aa in a:
        if np.isscalar(aa) is not True: return False
    return True

def isn(a):
    if a is None: return True
    else: return False

def notn(a):
    if a is not None: return True
    else: return False

def alln(a):
    for aa in a: 
        if aa is not None: return False
    return True

def allnotn(a):
    for aa in a: 
        if aa is None: return False
    return True

def checklen(a):
    #------------------------------
    # CHECK if all lists in a has
    # same No of elements (length)
    # a: the list of lists to check
    #------------------------------
    L = []
    for aa in a: L.append(len(aa))
    for LL in L:
        if LL is not L[0]: 
            return False
    return True

def writeBatch(Name=None,List=None):     
    if len(Name) is not len(List):
        sys.exit("writeBatch: Name and List have not same dimension.")
    L = len(List[0])
    N = len(Name) 
    fileRewrite('batch.txt')
    file = open('batch.txt','w')
    for i in range(L):
        for n in range(N):
            file.write("%s: %6.2e    "%(Name[n],List[n][i]))
        file.write("\n")
    file.close()
    print("writeBatch: Running bath-file was written...done")

def readBatch(Name=None):
    try:
        file = open('batch.txt','r')
    except:
        sys.exit('readBatch: batch does not exist.')
    if Name is None:
        sys.exit('readBatch: Name was not specified.')
    name = Name+':'
    Data = []
    with file as f:
        for line in f:
            L1 = line.replace(':','')
            L1 = line.replace('\n','')
            L1 = L1.split()
            idx = L1.index(name)
            Data.append(float(L1[idx+1]))
    if len(Data) == 0:
        sys.exit('readBatch: '+Name+' is not found in batch.')    
    return Data      

def readPath(name):
    try: file = open('path.txt','r')
    except: sys.exit('readPath: path.txt not found.')
    for line in file:
        L1 = line.split()
        if name == L1[0]:
            return L1[1]
    sys.exit('readPath: '+ name + ' does not exist in path.txt.')

csvDict = { 
#-------------------------
# Field types in CSV file
#-------------------------
           'X': 'Points:0',
           'Y': 'Points:1',
           'Z': 'Points:2',
           'U': 'U:0',
           'V': 'U:1',
           'W': 'U:2',
           'P': 'p',
           'T': 'T'
          }

#==================
# Data Manangement:
#==================

def meanSub(T):
    return T - T.mean(axis=1).reshape(T.shape[0],1)

def cumSum(S):
    return np.cumsum(S)/np.sum(S)

'''
def checkGrashf(p=None):
    # Check required data for Grashof definition
    # Gr = g*beta*dT*L^3/nu^2
    # If dT is con
    if 'beta' not in p: sys.exit('Grashof: \"beta\" not defined')
    if 'nu' not in p: sys.exit('Grashof: \"nu\" not defined')
    if 'L' not in p: sys.exit('Grashof: \"L\" not defined')
    if 'dT' not in p: sys.exit('Grashof: \"dT\" not defined')
    set = 'variable'
    if np.isscalar(p['dT']): set = 'constant'
    return set

def calcGrashof(set='variable',n=1,dict=None):   
    L  = dict['L']
    nu = dict['nu']
    dT = dict['dT']
    beta = dict['beta']
    g = 9.806
    if set == 'constant':
        Grashof = [g*beta*dT*L**3/nu**2 for i in range(n)]
        Grashof = np.array(Grashof)
    elif set == 'variable':
        Grashof =  g*np.array(beta)*np.array(dT)*L**3/np.array(nu)**2
    else:
        sys.exit('Grashof: invalid setup')
    return Grashof

# Check required data for Prandtl definition
def checkPrandtl(p=None):
    if 'nu' not in p: sys.exit('Prandtl: \"nu\" not defined')
    if 'alf' not in p: sys.exit('Prandtl: \"alf\" not defined')
    set = 'variable'
    if np.isscalar(p['nu']) and np.isscalar(p['alf']): set = 'constant'
    return set

def calcPrandtl(set='variable',n=1,dict=None):
    nu = dict['nu']
    alf = dict['alf']
    if set == 'constant': 
        Prandtl = [(nu/alf) for i in range(n)]
        Prandtl = np.array(Prandtl)
    elif set == 'variable':  
        Prandtl = np.array(nu)/np.array(alf)
    else:
        sys.exit('Prandtl: invalid setup')
    return Prandtl
'''  

