from batch import pnat
from shared import Verific

p = pnat(name="air-Ra-1e8-Pr-0.71",dir=Verific)
p.define(Fluid="Air",dT=10,L=1.0,Pref=3.3177e4,Tref=300)

# if Task == Verf:
#     Y,U   = overLine(fname=join(Verific,MID[Verf]),get=['Y','U'])
#     F     = CRO[Verf]
#     CR    = loadtxt(join(Verific,F))
#     CR    = CR.T
#     CR[0] = CR[0]-ShifT[Verf]
#     Max   = max(fabs(CR),axis=1)
#     CR[0]/= Max[0]
#     CR[1]/= Max[1]
#     ndict  = { 'xlabel': 'U*', 'ylabel': 'Y*', 'title': 'Comparison' }
#     pallet = [ circBlue, lineBlack ]
#     legend = [ CLG[Verf], PLG[Verf] ]
#     x      = [CR[0],U/max(U)]
#     f      = [CR[1],Y/max(Y)]
#     Compare(fname=join(Verific,UCO[Verf]),x=x,f=f,
#             ndict=ndict,pallet=pallet,legend=legend,dk=False)
#     #=== Nusselt number
#     TG = gradient(fname=join(Verific,HTC[Verf]),DT=1,T0=301,X0=0,dir='X',f='T')
#     print(max(TG),min(TG))
#     Linear(fname=LNU[Verf],x=TG,f=Y,dk=False)

