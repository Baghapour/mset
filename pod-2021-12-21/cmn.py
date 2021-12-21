import sys
import os
import os.path
from time import gmtime, strftime
import numpy as np
import pandas as pd

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

def fileRemove(name):
    #-----------------------
    # Remove file if exists.
    #-----------------------
    if os.path.isfile(name):
        os.remove(name)

def arr(a):
    #-----------------------
    # numpy-array conversion
    #-----------------------
    return np.array(a)

def isc(a):
    #--------------------------------
    # Check if element "a" is scalar.
    #--------------------------------
    if np.isscalar(a) is True: return True
    else: return False

def nots(a):
    #------------------------------------
    # Check if element "a" is NOT scalar.
    #------------------------------------
    if np.isscalar(a) is False: return True
    else: return False

def alls(a):
    #-----------------------
    # Check if all elements
    # of list "a" is scalar.
    #-----------------------
    for aa in a:
        if np.isscalar(aa) is not True: return False
    return True

def isn(a):
    #------------------------------
    # Check if element "a" is NONE.
    #------------------------------
    if a is None: return True
    else: return False

def notn(a):
    #----------------------
    # Check if an element
    # "a" is not NONE.
    #----------------------
    if a is not None: return True
    else: return False

def alln(a):
    #----------------------
    # Check if all elements
    # of list "a" are NONE. 
    #----------------------
    for aa in a: 
        if aa is not None: return False
    return True

def allnotn(a):
    #----------------------
    # Check if list "a" has 
    # no NONE element
    #----------------------
    for aa in a: 
        if aa is None: return False
    return True

def checklen(a):
    #-------------------------------
    # CHECK if all elements of the
    # give list "a" has same length.
    #-------------------------------
    L = []
    for aa in a: L.append(len(aa))
    for LL in L:
        if LL is not L[0]: 
            return False
    return True

def writeBatch(dir=None,bname='Batch',ftr=None,val=None): 
    #------------------------------   
    # Write a Running-Batch File:
    # fname: name of the batch file
    # ftr  : feature's name (list)
    # val  : values[ftr][case]
    #------------------------------
    if ftr is None or val is None:
        sys.exit("cmn-writeBatch: ftr or val not set.")
    L = len(val[0]) # number of cases
    N = len(ftr)    # number of features
    if checklen(val) is False: sys.exit("cmn-writeBatch: Mismatch in val-element lengths.")
    if len(ftr)!=len(val):     sys.exit("cmn-writeBatch: Mismatch in ftr-val lengths.")
    if dir is None: F = bname+'.txt'
    else:           F = os.path.join(dir,bname+'.txt')        
    with open(F,'w') as file:
        for i in range(L): # case number
            for n in range(N): # feature number          
                file.write("%s: %6.2e    "%(ftr[n],val[n][i]))
            file.write("\n")
    print("cm-writeBatch: Running-Batch File %s.txt was written." % bname)

def readBatch(dir=None,bname='Btch'):
    #----------------------------
    # Return data of a batch:
    # ftr: feature's name (list)
    # val: values[ftr][case]
    #----------------------------  
    if dir is None: F = bname+'.txt'
    else:           F = os.path.join(dir,bname+'.txt')     
    if os.path.exists(F) is False:
        sys.exit('cmn-readBatch: '+bname+' does not exist.')
    batch = []
    with open(F,'r') as file:
        for line in file:
            L1 = line.split()
            for i in range(len(L1)): L1[i] = L1[i].replace(":","")
            batch.append(L1)
    ftr = batch[0][0::2]
    val = [batch[i][1::2] for i in range(len(batch))]
    val = np.array(val).astype(np.float).T
    return ftr,val

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

#==================
# Fluid Properties:
#==================

class Grashof(object):
    def __call__(self,g=9.81,beta=None,dT=None,L=None,nu=None):
        return np.array(g*beta*dT*L**3/nu**2)
    
    @staticmethod
    def calcDT(g=9.81,Gr=None,beta=None,L=None,nu=None):
        return np.array(Gr*nu**2/(g*beta*L**3))

class Prandtl(object):
    def __call__(self,nu=None,alf=None):
        return np.arra(nu/alf)
    
    @staticmethod
    def calcAlf(Pr=None,nu=None):
        return np.array(nu/Pr)
    
    @staticmethod
    def calcNu(Pr=None,alf=None):
        return np.array(Pr*alf)

