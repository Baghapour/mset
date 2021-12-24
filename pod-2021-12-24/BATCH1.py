import cmn

# Testing Running-Batch File
ftr = ['Gr', 'Pr', 'nu', 'Tw']
Gr = [1e2,    1e3,   1e4,    1e5,  1e6]
Pr = [1e-2,   1e-1,  1e0,    1e1,  1e2]
nu = [1e-6, 1.5e-5, 1e-5, 1.5e-5, 1e-4]
Tw = [300,     302,  304,    306,  308]
val = [Gr,Pr,nu,Tw]

dir = "C:\\Users\\Behzad\\Dropbox\\current\\code-repo\\Current\\ML-Code\\MY_CODES\\current\\batches"

cmn.writeBatch(dir=dir,bname='Batch-1',ftr=ftr,val=val)

Ftr, Val = cmn.readBatch(dir=dir,bname='Batch-1')
print(Ftr)
print(Val)
