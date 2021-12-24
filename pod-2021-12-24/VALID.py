import graph as gf
import numpy as np
import os

Folder = 'C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\BCAV2D'
File = '15.csv'

Path = os.path.join(Folder,File)
X,Y,U = gf.take(csv=Path,f='U')

xi = 0.05
yi = np.linspace(0,0.1,10)
line = [xi,yi]
Z = gf.interpolate(grid=[X,Y],field=U,line=line)

gf.linear(fname='v1',x=Z,f=yi)