import cmn
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as tri

colorDict = {
                'black': 'k',
                'blue' : 'b',
                'red'  : 'r'
            }

ptypeDict = {
                'solid'      : '-',
                'solidCircle': '-o',
                'circle'     : 'o'
            }

#==========
# POD Class
#==========

class pod(object):

    def indexf(self,idx):
        return self.field.index(idx)
    
    def indexd(self,idx):
        return self.Dec.index(idx)
    
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
        self.Dec = []
        print('POD: Case defined.')
  
    def process(self,f=None,act=None):
        #-----------------------------------
        # Processing on the field: f
        # Action: combine, remove, get, msub
        #-----------------------------------
        if act == 'get':
            try:    idx = self.field.index(f)
            except: sys.exit('process: '+f+' is not found to return')
            print('process: '+f+' is returned.')
            return self.data[idx]
        elif act == 'combine' and len(f)>1:
            try:
                X = self.data[self.field.index(f[0])]
                N = f[0]
                for i in range(1,len(f)):
                    Y = self.data[self.field.index(f[i])]
                    X = np.column_stack((X,Y))
                    N += f[i]
                self.field.append(N)
                self.data.append(X)
            except: sys.exit('process: unexcepted list to combine.')
            print('process: '+N+' is generated and added to field.')
        elif act == 'remove':
            try:
                self.data.pop(self.field.index(f))
                self.field.pop(self.field.index(f))
            except: sys.exit('process: '+f+' is not found to remove.')
            print('process: '+f+' is removed to field')
        elif act == 'msub':
            try:    
                idx = self.field.index(f)
                self.data[idx] = cmn.meanSub(self.data[idx])
            except: sys.exit('process: '+f+' is not found for meanSub.')
            print('process: '+f+' is being meanSub.')
        else:
            sys.exit('process: action is not recognized.')

    def decompose(self,f=None,msub=False,act=None):
        #-----------------------------------
        # SVD decompostion of given field: f
        # Action: add, remove, get
        #-----------------------------------
        try:    Data = self.data[self.field.index(f)]
        except: sys.exit('decompose: '+f+' is not found to decompose.')
        if act == 'add':
            U,S,VT = np.linalg.svd(Data,full_matrices=False)
            self.U.append(U)
            self.S.append(S)
            self.VT.append(VT)
            self.Dec.append(f)
            print('decompose: '+f+' is decomposed and added.')
        elif act == 'remove':
            try:
                self.U.pop(self.Dec.index(f))
                self.S.pop(self.Dec.index(f))
                self.VT.pop(self.Dec.index(f))
                self.Dec.pop(self.Dec.index(f))
                print('decompose: '+f+' is removed from list.')
            except:
                sys.exit('decompose: '+f+' is not in list to remove.')
        elif act == 'get':
            try:
                UR = self.U[self.Dec.index(f)]
                SR = self.S[self.Dec.index(f)]
                VTR = self.VT[self.Dec.index(f)]
                print('decompose: '+f+' is returned in (U,S).')
                return UR,SR,VTR
            except:
                sys.exit('decompose: '+f+' is not in list to return.')
        elif act is None or f is None:
            sys.exit('decompose: field (f) or acttion (act) is not specified.')
        else:
            sys.exit('decompose: wrong action option.')

    def analysis(self,f=None,act=None):
        #---------------------------
        # Analysis SVD decomposition
        # Action: cumsum
        #---------------------------
        if f not in self.Dec:
            sys.exit('analysis: '+f+' is not found.')
        if act == 'cumsum':
            print('analysis: Cumulative-Sum is returned for '+f)
            return cmn.cumSum(self.S[self.Dec.index(f)])
        else:
            sys.exit('analysis: wrong action option.')
      
    def plot(self,f=None,x='POD mode',name='Test',
    color='black',atype='reg',ptype='solid',save=True,show=False):
        if f is None:
            sys.exit('plot: '+f+' is not provied to plot.')
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        plt.ylabel(name)
        plt.xlabel(x)
        try:    cfg = ptypeDict[ptype]
        except: sys.exit('plot: line type not recognized.')
        try:    cfg += colorDict[color]
        except: sys.exit('plot: color not recognized.')
        if isinstance(f,str) == True and f in self.Dec:
            S = self.S[self.Dec.index(f)]
        elif isinstance(f,str) == False: 
            S = f
        else:
            sys.exit('plot: data (f) is not found to plot).')
        n = np.arange(len(S))
        if atype == 'reg':
            ax.plot(n,S,cfg)
        elif atype == 'semilog':
            ax.semilogy(n,S,cfg)
        else:
            sys.exit('plot: axis type not recognized.')
        if save is True:
            plt.savefig(name+'.png',dpi=300)
        if show is True:
            plt.show()
    
    def reduction(self):
        pass

    def reconstruct(self):
        pass

    def draw2D(self,name='Test',X=None,save=True,show=False):
        fig = plt.figure()
        ax  = fig.add_subplot(111) 
        ax.set_aspect(1)  
        #x = self.data[self.field.index('X')]
        #y = self.data[self.field.index('Y')]
        x = self.data[self.indexf('X')]
        y = self.data[self.indexf('Y')]
        trg = tri.Triangulation(x, y)
        tcf = ax.tricontourf(trg,X,cmap='jet')
        clb = fig.colorbar(tcf,format='%.2e')
        clb.set_label(name)
        #plt.ylabel('y')
        #plt.xlabel('x')
        if save == True:
            plt.savefig(name+'.png',dpi=300)
        if show is True:
            plt.show()