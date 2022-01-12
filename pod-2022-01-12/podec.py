'''
==========================================
podec module:
* proper-orthognal decomposition
* class pod:
  POD analysis on CSV data
  * field: original info (data,indexf)
  * dec  : decomposed info (U,S,VT,indexd)
  * nsamp: number of samples
  * init: 
    set data folder and nsamp
  * define:
    read all csv files (CFD) and add them
    to data. If mesh is constant, 
    take geometry from the first sample.
  * domain: 
    managing field data,
    get: return all samples of a field f
    getsamp: return a spec sample of field
    combine: merge row-wise list of fileds
    msub: subtract mean from a field
  * decompose: find S,U,VT
  * normalize: scaling field data
  * reduction:
  * reconstruction:
==========================================
'''
import shared
import sys
import numpy as np
import pandas as pd

class pod(object):
    def indexf(self,idx):
        return self.field.index(idx)
    
    def indexd(self,idx):
        return self.dec.index(idx)
    
    def __init__(self,folder=None):
        #-----------------------------
        # Assign self.folder and count
        # CSV files to set self.nsamp
        #-----------------------------
        print('\n')
        print('=======================================')
        print('POD Analysis, Time:',shared.Time())   
        print('=======================================')
        self.folder = folder
        try:    self.nsamp = shared.countFile(self.folder,ext='csv')
        except: sys.exit('pod-init: '+self.folder+' not exists.')
        print('Folder:',self.folder,', samples:',self.nsamp)

    def define(self,field=None,mesh='constant'):
        if field is None: sys.exit('pod-defile: \"field\" not set.')
        #----------------------------------
        # Take CSV header form first sample
        #----------------------------------
        try:    total = pd.read_csv(self.folder+'/1.csv').columns.tolist()
        except: sys.exit('pod-define: Reading samples faild, \"1.csv\" not found.')  
        #-------------------------------          
        # Append data from current Field
        #-------------------------------          
        self.field = field
        self.data = [[0] for i in range(len(field))]
        for i in range(self.nsamp):
            file = self.folder+'/'+str(i+1)+'.csv'
            data = pd.read_csv(file).to_numpy()
            for f in field:
                tcol = total.index(shared.csvDict[f])
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
        self.dec = []         
        self.U   = []
        self.S   = []   
        self.VT  = []
        self.nrm_minmax  = []  
        self.min         = []
        self.max         = []
        self.nrm_meanstd = []
        self.mean        = []
        self.std         = []
        self.nrm_divide  = []
        self.divide      = []
        print('pod-define: Case defined.')
  
    def domain(self,f=None,act=None,samp=1):
        #-----------------------------------
        # Processing on original data field
        # Field: f
        # Action: get
        #-----------------------------------
        if act == 'get':
            try:    idx = self.indexf(f)
            except: sys.exit('pod-domain: '+f+' is not found to return')
            print('pod-domain: '+f+' is returned.')
            return self.data[idx]
        if act == 'getsamp':
            if samp<1 or samp>self.nsamp:
                sys.exit('pod-domain: samp must be between 1 and %d',self.nsamp)
            try:    idx = self.indexf(f)
            except: sys.exit('pod-domain: '+f+' is not found to return')
            print('pod-domain: sample %d of field %s is returned.'%(self.nsamp,f))
            return self.data[idx][:,samp-1]
        elif act == 'combine':
            if len(f) < 2 or isinstance(f,list) is False:
                sys.exit('pod-domain: f must be list and >=2 to combine.')
            try:
                X = self.data[self.indexf(f[0])]
                N = f[0]
                for i in range(1,len(f)):
                    Y = self.data[self.indexf(f[i])]
                    X = np.vstack((X,Y))
                    N += f[i]
                self.field.append(N)
                self.data.append(X)
            except: sys.exit('pod-domain: unexcepted f to combine.')
            print('pod-domain: '+N+' is generated and added.')
        elif act == 'split':
            if isinstance(f,str) is False:
                sys.exit('pod-domain: f must be str for split.')
            try:    idx = self.indexf(f)
            except: sys.exit('pod-domain: '+f+' is not defined in field.')
            F = [ff for ff in f]
            S = np.split(self.data[idx],len(F),axis=0)   
            print('pod-domain: '+f+' is split to ',F)
            return S     
        elif act == 'remove':
            try:
                self.data.pop(self.indexf(f))
                self.field.pop(self.indexf(f))
            except: sys.exit('pod-domain: '+f+' is not found to remove.')
            print('pod-domain: '+f+' is removed.')
        elif act == 'msub':
            try:    
                idx = self.indexf(f) 
                self.data[idx] = shared.meanSub(self.data[idx])
            except: sys.exit('pod-domain: '+f+' is not found for meanSub.')
            print('pod-domain: '+f+' is being meanSub.')
        else:
            sys.exit('pod-domain: action is not recognized.')

    def normalize(self,f=None,method=None,input=None):
        if isinstance(f,str) is False: sys.exit('pod-normalize: f must be str.')
        if method is None:             sys.exit('pod-normalize: method not set.')
        try:    idx = self.indexf(f)
        except: sys.exit('pod-normalize: '+f+' was not found.')
        dat = self.data[idx]
        if method == 'min-max':
            min = np.min(dat,axis=0) 
            max = np.max(dat,axis=0)
            self.data[idx] = (dat-min)/(max-min)
            self.nrm_minmax.append(f)
            self.min.append(min) 
            self.max.append(max)
        elif method == 'mean-std':
            mean = np.mean(dat,axis=0) 
            std  = np.std (dat,axis=0)
            self.data[idx] = (dat-mean)/std
            self.nrm_meanstd.append(f)
            self.mean.append(mean) 
            self.std.append(std)
        elif method == 'divide':
            if input is None: sys.exit('pod-normalize: input must be set for divide.') 
            if shared.isc(input): inp = np.array([input for i in range(self.nsamp)])
            else:              inp = np.array(input)
            self.data[idx] /= inp 
            self.nrm_divide.append(f)
            self.divide.append(inp)
        else:
            sys.exit('pod-normalize: method is not recognized.')
        print('pod-normalize: field '+ f +' was normized with '+method)

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
            print('pod-decompose: '+f+' is added.')
        elif act == 'remove':
            try:
                self.U.pop(self.indexd(f))
                self.S.pop(self.indexd(f))
                self.VT.pop(self.indexd(f))
                self.dec.pop(self.indexd(f))
                print('decompose: '+f+' is removed.')
            except:
                sys.exit('pod-decompose: '+f+' is not found to remove.')
        elif act == 'get':
            try:
                U = self.U[self.indexd(f)]
                S = self.S[self.indexd(f)]
                VT = self.VT[self.indexd(f)]
                print('pod-decompose: '+f+' is returned (U,S,VT).')
                return U,S,VT
            except:
                sys.exit('pod-decompose: '+f+' is not found to return.')
        elif act == 'getsplit':
            if isinstance(f,str) is False:
                sys.exit('pod-decompose: f must be str for split.')
            try:    idx = self.indexd(f)
            except: sys.exit('pod-domain: '+f+' is not defined to return.')
            F = [ff for ff in f]
            S = self.S[idx] # np.split(self.S[idx],len(F))   
            U = np.split(self.U[idx],len(F),axis=0)
            VT= self.S[idx] #np.split(self.VT[idx],len(F),axis=1)
            print('pod-decompose: '+f+' is returned as U'+str(F)+', S[\''+f+'\'], VT[\''+f+'\']')
            return U,S,VT     

        elif act is None:
            sys.exit('pod-decompose: Acttion (act) is not recognized.')
        else:
            sys.exit('pod-decompose: inappropriate input.')

    def cumulative(self,f=None):
        #---------------------------
        # Return cumulative sum on 
        # the given singular values.
        #---------------------------
        if f not in self.dec: sys.exit('pod-acumulative: '+f+' is not found.')
        return shared.cumSum(self.S[self.indexd(f)])

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
        idx = self.indexf(f)
        data = self.data[idx][:,samp-1]
        #------------------------
        # Check for normalization
        #------------------------
        if f in self.nrm_minmax:
            g = self.nrm_minmax.index(f)
            min = self.min[g][samp-1]
            max = self.max[g][samp-1]
            data = (max-min)*data+min
            print('pod-reduction: renormarlization (min-max) for '+f+', sample =',samp)
        try:
            for i in range(dim):         
                u = self.U[self.indexd(f)][:,i]
                rd.append(np.dot(data,u))
        except:
            sys.exit('pod-reduction: faild to reduction, check field.')
        print('pod-reduction: reducting sample %d, dim=%d.'%(samp,dim))
        return np.array(rd)

    def reconstruct(self,f=None,rc=None,split=None):
        if f is None: 
            sys.exit('pod-reconstruct: f is not set.')
        if rc is None: 
            sys.exit('pod-reconstruct: rc is not set.')
        if len(rc) > self.nsamp: 
            sys.exit('pod-reconstruct: larger rc data (>%d).',self.nsamp)
        if f not in self.field:
            sys.exit('pod-reconstruct: '+f+' does not exist in field list.')
        RD = np.array(rc).flatten()
        UR = self.U[self.indexd(f)][:,:len(RD)]
        REC = np.sum(UR*RD,axis=1)
        if split is None:
            print('pod-reconstruct: reconstructing, dim=%d.'%len(RD))
            return REC
        if split is not None:
            F = [ff for ff in f]
            REC = np.split(REC,len(F))[F.index(split)]
            print('pod-reconstruct: reconstructing, dim=%d, split return %s'%(len(RD),split))
        return REC
