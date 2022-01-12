'''
batch module (2022):
prepare running-CFD case
'''
import os.path
import itertools
from shared import Exit,retrieve_name
from prop   import fluid,Prandtl,Rayleigh

class batch(object):
    def __init__(self,name=None,dir=None):
        if dir is None: F = name+'.txt'
        else:           F = os.path.join(dir,name+'.txt') 
        self.file = F   

    def feature(self,ftr):
        self.ftr = ftr

    def include(self,val=None):
        self.val = val

    def write(self,w="wrtie",change="yes"):
        if change is "no": return
        with open(self.file,"w") as file:
            for n in range(len(self.ftr)): 
                file.write("%5s\t%.4e\n"%(self.ftr[n],self.val[n]))

    def get(self,f=None):
        if f is None: Exit("batch-get: set f.")
        try:    return self.val[self.ftr.index(f)]       
        except: Exit("[ERROR] batch-get: %s not exists",arg=f)

def get_features(ftr=None):
    feature = []
    for f in ftr:
        feature.append(retrieve_name(f))
    feature = list(itertools.chain(*feature))
    return feature

class pnat(batch):
    def __init__(self,name=None,dir=None):
        super().__init__(name,dir)

    def define(self,g=9.81,Fluid=None,dT=None,L=None,Pref=None,Tref=None,wrt=True):
        f    = fluid(Fluid,Pref,Tref)
        beta = f.beta
        rho  = f.rho
        mu   = f.mu
        Pr   = f.Pr
        nu   = f.nu
        M    = f.M
        Cv   = f.Cv
        Cp   = f.Cp
        alf  = Prandtl.calcAlf(Pr=Pr,nu=nu)
        Ra   = Rayleigh.calc(dT=dT,g=g,L=L,beta=beta,nu=nu,alf=alf)
        ftr  = [Ra,Pr,dT,Pref,rho,mu,nu,alf,M,Cv,Cp,Tref,beta,L,g]
        batch.feature(self,get_features(ftr))
        batch.include(self,val=ftr)
        if wrt == True: batch.write(self,w="write")

if __name__ == "__main__":
    print(__doc__)
