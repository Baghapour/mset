import mset as mt
import graph as gf
import numpy as np

Case = mt.pod(
    path='My_CODES',
    case='BCAV2D')

field = ['X','Y','T','U','V']

Case.define   (field=field)
Case.decompose(f='T',act='add')
U,S,VT = Case.decompose(f='T',act='get')

# Checking reduction and reconstruction
RED = Case.reduction(f='T',samp=15,dim=14)
REC = Case.reconstruct(f='T',rd=RED)

# Plot Singular Values
x = np.linspace(0,1,len(S))
gf.linear(x=x,f=S,log=(0,1),pallet=gf.dotGreen)

# Plot POD mode
X = Case.domain(f='X',act='get')
Y = Case.domain(f='Y',act='get')
grid = [X,Y]
Z = U[:,0]
gf.plane(fname='PlaneTest',grid=grid,field=Z)

# Compare singular values of T and U
Case.decompose(f='U',act='add')
U2,S2,VT2 = Case.decompose(f='U',act='get')
f = [S,S2]
pal = [gf.lineCircleBlack,gf.lineSqrRed]
gf.compare(f=f,log=(0,1),pallet=pal,legend=['T','U'])










