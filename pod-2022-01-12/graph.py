import sys
import shared
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def dark():
    plt.style.use("dark_background")

# Plot setting:  color    line    width  
lineBlack       = [    'k',     '-',    2     ]
lineBlue        = [    'b',     '-',    2     ]
lineRed         = [    'r',     '-',    2     ]
lineGreen       = [    'g',     '-',    2     ]
lineWhite       = [    'w',     '-',    2     ]
dotBlack        = [    'k',    '--',    2     ]
dotBlue         = [    'b',    '--',    2     ]
dotRed          = [    'r',    '--',    2     ]
dotGreen        = [    'g',    '--',    2     ]
circBlack       = [    'k',     'o',    1     ]
circBlue        = [    'b',     'o',    1     ]
circRed         = [    'r',     'o',    1     ]
circGreen       = [    'g',     'o',    1     ]
triBlack        = [    'k',     '^',    1     ]
triBlue         = [    'b',     '^',    1     ]
triRed          = [    'r',     '^',    1     ]
triGreen        = [    'g',     '^',    1     ]
sqrBlack        = [    'k',     's',    1     ]
sqrBlue         = [    'b',     's',    1     ]
sqrRed          = [    'r',     's',    1     ]
sqrGreen        = [    'g',     's',    1     ]
starBlack       = [    'k',     '*',    1     ]
starBlue        = [    'b',     '*',    1     ]
starRed         = [    'r',     '*',    1     ]
starGreen       = [    'g',     '*',    1     ]
lineCircleBlack = [    'k',    '-o',    2     ]
lineCircleBlue  = [    'b',    '-o',    2     ]
lineCircleRed   = [    'r',    '-o',    2     ]
lineCircleGreen = [    'g',    '-o',    2     ]
lineTriBlack    = [    'k',    '-^',    2     ]
lineTriBlue     = [    'b',    '-^',    2     ]
lineTriRed      = [    'r',    '-^',    2     ]
lineTriGreen    = [    'g',    '-^',    2     ]
lineSqrBlack    = [    'k',    '-s',    2     ]
lineSqrBlue     = [    'b',    '-s',    2     ]
lineSqrRed      = [    'r',    '-s',    2     ]
lineSqrGreen    = [    'g',    '-s',    2     ]

palletList = [
    lineBlack, lineBlue, lineRed, lineGreen,
    dotBlack ,  dotBlue,  dotRed,  dotGreen,
    circBlack, circBlue, circRed, circGreen,
    triBlack ,  triBlue,  triRed,  triGreen,
    sqrBlack ,  sqrBlue,  sqrRed,  sqrGreen,
    starBlack, starBlue, starRed, starGreen,
    lineCircleBlack, lineCircleBlue, lineCircleRed, lineCircleGreen,
    lineTriBlack   , lineTriBlue   , lineTriRed   , lineTriGreen,
    lineSqrBlack   , lineSqrBlue   , lineSqrRed   , lineSqrGreen
    ]

def Linear(fname='Test',
               x=None,
               f=None,
           ndict=None,
          pallet=lineBlack,
             log=(0,0),
            save=True,
            show=False,
              ar=False,
              dk=True):
    if f is None or isinstance(f,str):
        sys.exit('graph-linear: '+f+' is not properly set.')
    if ndict is None:
        xlabel = 'Variable'; ylabel = 'Function'
        title  = 'Sequence'; legend = 'Case'
    else:
        xlabel = ndict['xlabel']; ylabel = ndict['ylabel']
        title  = ndict['title'] ; legend = ndict['legend']
    if dk is True: dark()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    plt.ylabel(ylabel); plt.xlabel(xlabel)
    plt.title(title);   plt.legend(legend)
    fmt = pallet[0]+pallet[1]
    lw  = pallet[2]
    if log[0] == 1:  ax.set_xscale('log')
    if log[1] == 1:  ax.set_yscale('log')
    if ar is True : ax.set_aspect(1.0)            
    try:
        f = np.array(f).flatten()
        if x is None:
            x = np.arange(1,len(f)+1)
            print('graph-linear: sequential plot.')
        else:
            x = np.array(x).flatten()
        ax.plot(x,f,fmt,linewidth=lw)
    except:
        sys.exit('graph-linear: failed to plot, check dimension.')
    if save is True: plt.savefig(fname+'.png',dpi=300)
    if show is True: plt.show()

def Compare(fname='Compare',
                x=None,
                f=None,
              log=(0,0),
            ndict=None,
           legend=None,
           pallet=None,
             save=True,
             show=False,
               ar=False,
               dk=True):
    if f is None:     
        sys.exit('graph-compare: f is not set.')
    if x is None:     
        x = [np.arange(1,len(f[0])+1)]
        print('graph-compare: sequential plot.')
    elif isinstance(x,list) is False:
        sys.exit('graph-compare: x must be list.')
    if isinstance(f,list) is False:
        sys.exit('graph-compare: f must be list.')    
    if isinstance(legend,list) is False: 
        sys.exit('graph-compare: legend must be list.')
    if len(x)==1:
        X2 = []
        L = len(f[0])
        for ff in f:
            if len(ff)!=L: 
                sys.exit('graph-compare: single x, f dim not matched.')
            X2.append(x)
        print('graph-compare: single x.')
    else: 
        if len(x)!=len(f):
            sys.exit('graph-compare: x and f must have same length.')        
        X2 = x
    if len(legend)!=len(X2):
        sys.exit('graph-compare: x and ndict must have same length.')
    if ndict is None:
        xlabel = 'Variable'; ylabel = 'Function'; title  = 'Sequence'; 
    else:
        xlabel = ndict['xlabel']; ylabel = ndict['ylabel']; title  = ndict['title'] ; 
    if dk is True: dark()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    plt.ylabel(ylabel); plt.xlabel(xlabel)
    plt.title(title);   plt.legend(legend)
    if log[0] == 1:  ax.set_xscale('log')
    if log[1] == 1:  ax.set_yscale('log')
    PAL = []
    if pallet is None:
        for i in range(len(f)):
            PAL.append(palletList[i])
    else:
        if len(pallet)!=len(f):
            sys.exit('graph-compare: pallet and f must have same length.')
        PAL = pallet
    for i in range(len(f)):
        fmt = PAL[i][0]+PAL[i][1]
        lw  = PAL[i][2]
        X   = np.array(X2[i]).flatten()
        F   = np.array(f[i]).flatten()
        ax.plot(X,F,fmt,linewidth=lw)
    ax.legend(legend)
    if ar is True :  ax.set_aspect(1.0)          
    if save is True: plt.savefig(fname+'.png',dpi=300)
    if show is True: plt.show()   

def Plane(fname='Test',grid=None,field=None,save=True,show=False):
    if grid[0] is None or grid[1] is None:
        sys.exit('graph-plane: grid is not set.') 
    if field is None: 
        sys.exit('graph-plane: field is not set.')
    fig = plt.figure()
    ax  = fig.add_subplot(111) 
    ax.set_aspect(1)  
    try:
        x = np.array(grid[0]).flatten()
        y = np.array(grid[1]).flatten()
        z = np.array(field).flatten()
        trg = tri.Triangulation(x,y)
    except:
        sys.exit('graph-plane: failed to plot, check dimension.')
    tcf = ax.tricontourf(trg,z,cmap='jet')
    clb = fig.colorbar(tcf,format='%.2e')
    clb.set_label(fname)
    if save == True: plt.savefig(fname+'.png',dpi=300)
    if show is True: plt.show()

def Take(csv=None,f=None):
    if open(csv,'r') is False:
        sys.exit('graph-take: File '+csv+' not found.')
    head = pd.read_csv(csv).columns.tolist()  
    data = pd.read_csv(csv).to_numpy()
    X    = data[:,head.index(shared.csvDict['X'])]
    Y    = data[:,head.index(shared.csvDict['Y'])]
    if f is None:
        return X,Y
    else:
        F = data[:,head.index(shared.csvDict[f])]
        return X,Y,F

def overLine(fname=None,get=None):
    header = pd.read_csv(fname).columns.tolist()
    data   = pd.read_csv(fname).to_numpy()
    List = []
    for g in get: 
        tcol = header.index(shared.csvDict[g])
        List.append(data[:,tcol])
    return List

def gradient(fname=None,T0=None,X0=None,dir=None,f=None,DT=None):
    header = pd.read_csv(fname).columns.tolist()
    data   = pd.read_csv(fname).to_numpy()
    fcol = header.index(shared.csvDict[f])
    xcol = header.index(shared.csvDict[dir])
    print(xcol,fcol)
    T1 = data[:,fcol]
    X1 = data[:,xcol]
    return (T0-T1)/(DT*(X1-X0))

if __name__ == "__main__":
    x0 = np.full(10,0)
    x1 = np.full(10,0.0025)
    x2 = np.full(10,0.0050)
    T0 = np.full(10,310)
    T1 = np.full(10,305)
    T2 = np.full(10,303)
    dx = shared.dx_Lagrange(x=0,xp=[x0,x1,x2],order=2) 
    xx = shared.Lagrange(x=0.00,xp=[x0,x1,x2],order=2) 
    print(xx)
    T = xx[0]*T0+xx[1]*T1+xx[2]*T2
    print(dx)
    TG = dx[0]*T0+dx[1]*T1+dx[2]*T2
    print(TG)