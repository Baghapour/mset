import cmn
import numpy as np

Pr = [0.01,
       0.1,
       1.0,
        10,
        25]

dT = [ 0.1, 
        1,
        3,
        5,
       10,
       15,
       20,
       30]

ntest = len(Pr)*len(dT)

T0   = 300
nu   = [1.5e-5 for i in range(ntest)]
L    = [0.1    for i in range(ntest)]
beta = [1.0/T0 for i in range(ntest)]
g    = [9.81   for i in range(ntest)]

Case = cmn.casePair(v1=Pr,v2=dT)
Pr = cmn.caseBreak(case=Case,idx=0)
dT = cmn.caseBreak(case=Case,idx=1)

alf = cmn.Prandtl.calcAlf(Pr=Pr,nu=nu)
Ra  = cmn.Rayleigh.calc(g=g,beta=beta,dT=dT,L=L,nu=nu,alf=alf)

dir = "C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\current\\batches"

ftr = ['Ra','Pr','dT','nu','alf','beta','g','L']
val = [Ra,Pr,dT,nu,alf,beta,g,L]

cmn.writeBatch(dir=dir,bname='Batch-2',ftr=ftr,val=val) 




