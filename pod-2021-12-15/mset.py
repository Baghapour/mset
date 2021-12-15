import cmn
import os
import sys
import numpy as np
import pandas as pd

#==========
# POD Class
#==========

class pod(object):

    def indexf(self,idx):
        return self.field.index(idx)
    
    def indexd(self,idx):
        return self.dec.index(idx)
    
    def __init__(self,path=None,case=None):
        cmn.clear()
        print('\n')
        print('POD Analysis, Time:',cmn.Time())   
        Path = cmn.readPath(path)
        self.folder = Path+'/'+case
        try:    self.nsamp = cmn.countFile(self.folder,ext='csv')
        except: sys.exit('POD: '+self.folder+' not exists.')
        print('Case:',case,', samples:',self.nsamp)

    def define(self,field=None,mesh='constant'):
        if field is None: 
            sys.exit('Field not defined.')
        #----------------
        # Take CSV header
        #----------------
        try:    
            total = pd.read_csv(self.folder+'/1.csv').columns.tolist()
        except: 
            sys.exit
            (
                'Reading: 1st sample not found in: %s\n'%(self.folder)
            )  
        #-------------------------------          
        # Append data from current Field
        #-------------------------------          
        self.field = field
        self.data = [[0] for i in range(len(field))]
        for i in range(self.nsamp):
            file = self.folder+'/'+str(i+1)+'.csv'
            data = pd.read_csv(file).to_numpy()
            for f in field:
                tcol = total.index(cmn.csvDict[f])
                fcol = field.index(f)
                self.data[fcol].append(data[:,tcol])
        #------------------
        # Remove extra zero
        #------------------
        for f in field: 
            fcol = field.index(f)
            self.data[fcol].pop(0)
            self.data[fcol] = np.asarray(self.data[fcol]).T
        #-------------------------------
        # Reduce mesh data to one sample
        # for 'constant' mesh condition
        #-------------------------------
        if mesh == 'constant':
            if 'X' in field:
                self.data[field.index('X')] = self.data[field.index('X')][:,0]
            if 'Y' in field:
                self.data[field.index('Y')] = self.data[field.index('Y')][:,0]   
            if 'Z' in field:
                self.data[field.index('Z')] = self.data[field.index('Z')][:,0]   
        #----------------------------
        # Decompostion arrays defined
        #----------------------------
        self.U = []
        self.S = []
        self.VT = []
        self.dec = []
        print('POD: Case defined.')
  
    def domain(self,f=None,act=None):
        #-----------------------------------
        # Processing on the data
        # Field: f
        # Action: combine, remove, get, msub
        #-----------------------------------
        if act == 'get':
            try:    idx = self.indexf(f)
            except: sys.exit('pod-domain: '+f+' is not found to return')
            print('pod-field: '+f+' is returned.')
            return self.data[idx]
        elif act == 'combine':
            if len(f) < 2:
                sys.exit('pod-domain: len(f) must be >=2 to combine.')
            try:
                X = self.data[self.indexf(f[0])]
                N = f[0]
                for i in range(1,len(f)):
                    Y = self.data[self.indexf(f[i])]
                    X = np.column_stack((X,Y))
                    N += f[i]
                self.field.append(N)
                self.data.append(X)
            except: sys.exit('pod-domain: unexcepted f to combine.')
            print('pod-domain: '+N+' is generated and added.')
        elif act == 'remove':
            try:
                self.data.pop(self.indexf(f))
                self.field.pop(self.indexf(f))
            except: sys.exit('pod-domain: '+f+' is not found to remove.')
            print('pod-domain: '+f+' is removed.')
        elif act == 'msub':
            try:    
                idx = self.indexf(f) 
                self.data[idx] = cmn.meanSub(self.data[idx])
            except: sys.exit('pod-domain: '+f+' is not found for meanSub.')
            print('pod-domain: '+f+' is being meanSub.')
        else:
            sys.exit('pod-domain: action is not recognized.')

    def decompose(self,f=None,msub=False,act=None):
        #-----------------------------------
        # SVD decompostion of given data
        # Field: f, Action: add, remove, get
        #-----------------------------------
        try:    Data = self.data[self.field.index(f)]
        except: sys.exit('decompose: '+f+' is not found.')
        if act == 'add':
            U,S,VT = np.linalg.svd(Data,full_matrices=False)
            self.U.append(U)
            self.S.append(S)
            self.VT.append(VT)
            self.dec.append(f)
            print('decompose: '+f+' is added.')
        elif act == 'remove':
            try:
                self.U.pop(self.indexd(f))
                self.S.pop(self.indexd(f))
                self.VT.pop(self.indexd(f))
                self.dec.pop(self.indexd(f))
                print('decompose: '+f+' is removed.')
            except:
                sys.exit('decompose: '+f+' is not found to remove.')
        elif act == 'get':
            try:
                UR = self.U[self.indexd(f)]
                SR = self.S[self.indexd(f)]
                VTR = self.VT[self.indexd(f)]
                print('decompose: '+f+' is returned (U,S,VT).')
                return UR,SR,VTR
            except:
                sys.exit('decompose: '+f+' is not found to return.')
        elif act is None:
            sys.exit('decompose: Acttion (act) is not recognized.')
        else:
            sys.exit('decompose: inappropriate input.')

    def cumulative(self,f=None):
        if f not in self.dec:
            sys.exit('analysis: '+f+' is not found.')
        return cmn.cumSum(self.S[self.indexd(f)])

    def reduction(self,f=None,samp=1,dim=1):
        #------------------------------------------
        # reduction: projection of sample onto PODS
        # f   : the name in the field-list
        # samp: Sample number in field f [1,nsamp]
        # dim : POD modes for projection [1,nsamp]
        # return rd[dim]
        #------------------------------------------
        if samp>self.nsamp or samp==0:
            sys.exit('pod-reduction: sample out of range [1,%d].',self.nsamp)
        if dim>self.nsamp or dim==0:
            sys.exit('pod-reduction: dim out of range [1,>%d].',self.nsamp)
        rd = []
        data = self.data[self.indexf(f)][:,samp-1]
        try:
            for i in range(dim):         
                u = self.U[self.indexd(f)][:,i]
                rd.append(np.dot(data,u))
        except:
            sys.exit('pod-reduction: faild to reduction, check field.')
        print('pod-reduction: reducting sample %d, dim=%d.'%(samp,dim))
        return np.array(rd)

    def reconstruct(self,f=None,rd=None):
        if f is None: 
            sys.exit('pod-reconstruct: f is not set.')
        if rd is None: 
            sys.exit('pod-reconstruct: red is not set.')
        if len(rd) > self.nsamp: 
            sys.exit('pod-reconstruct: larger rd data (>%d).',self.nsamp)
        if f not in self.field:
            sys.exit('pod-reconstruct: '+f+' does not exist in field list.')
        RD = np.array(rd).flatten()
        UR = self.U[self.indexd(f)][:,:len(RD)]
        print('pod-reconstruct: reconstructing, dim=%d.'%len(RD))
        return np.sum(UR*RD,axis=1)
