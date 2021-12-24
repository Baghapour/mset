import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from shapely.geometry import Polygon as sPolygon
import graph as gf
import os

Folder = 'C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\BCAV2D'
File = '15.csv'
Path = os.path.join(Folder,File)

fig, ax1 = plt.subplots(ncols=1)
ax1.set_aspect('equal')

#setting up basic shape
X,Y = gf.take(csv=Path)
phi = np.linspace(0,2*np.pi,200)
#r = 1 + 2*np.sin(phi)**2
x = 0.05+np.cos(phi)*0.01
y = 0.05+np.sin(phi)*0.01
ax1.plot(x,y,'ro-', lw=3, ms=6, zorder= 1, label='edge')

x2 = 0.05+np.cos(phi)*0.03
y2 = 0.05+np.sin(phi)*0.03
ax1.plot(x2,y2,'ro-', lw=3, ms=6, zorder= 1, label='edge')
#======================
#original triangulation
triang1 = tri.Triangulation(X, Y)
#ax1.triplot(triang1, 'ko--', lw=1, ms=4, zorder=2, label='all')
#==== Single Mask =====
#outline = sPolygon(zip(x,y))
#mask = [
#     outline.contains(sPolygon(zip(X[tri], Y[tri])))
#     for tri in triang1.get_masked_triangles()
#]
#triang1.set_mask(mask)
#=== Combined Mask ====
outline1 = sPolygon(zip(x,y))
outline2 = sPolygon(zip(x2,y2))
outline = outline1.union(outline2)
mask1 = [
     outline1.contains(sPolygon(zip(X[tri], Y[tri])))
     for tri in triang1.get_masked_triangles()
]
mask2 = [
     not outline2.contains(sPolygon(zip(X[tri], Y[tri])))
     for tri in triang1.get_masked_triangles()
]
mask = [mask1[i] or mask2[i] for i in range(len(mask1))]
triang1.set_mask(mask)
ax1.triplot(triang1, 'b-', lw=1, zorder=3, label='inner')
fig.legend()
plt.show()