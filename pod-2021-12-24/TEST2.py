import mset as mt
import graph as gf
import numpy as np

Folder = "C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\data\\BCAV2D"

Case = mt.pod(folder=Folder)

field = ['X','Y','T','U','V']

Case.define(field=field)
Case.domain(f=['U','V','T'],act = 'combine')
#Case.normalize(f='UVT',method='min-max')
Case.decompose(f='UVT',act='add')
U,S,VT = Case.decompose(f='UVT',act='getsplit')

print(S)

# Checking reduction and reconstruction
RED = Case.reduction(f='UVT',samp=5,dim=15)
Trc = Case.reconstruct(f='UVT',rc=RED,split='T')


# X = Case.domain(f='X',act='get')
# Y = Case.domain(f='Y',act='get')
# grid = [X,Y]
# gf.plane(fname='PlaneTest',grid=grid,field=Trc,show=True,save=False)

# Torg = Case.domain(f='T',act='getsamp',samp=5)
# gf.plane(fname='PlaneTest',grid=grid,field=Torg,show=True,save=False)


'''
# Plot POD mode
X = Case.domain(f='X',act='get')
Y = Case.domain(f='Y',act='get')
grid = [X,Y]
Z = U[0][:,0]
gf.plane(fname='PlaneTest',grid=grid,field=Z,show=True,save=False)
Z = U[1][:,0]
gf.plane(fname='PlaneTest',grid=grid,field=Z,show=True,save=False)
Z = U[2][:,0]
gf.plane(fname='PlaneTest',grid=grid,field=Z,show=True,save=False)
'''






