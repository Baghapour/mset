import mset as mt

Case = mt.pod(
    path='My_CODES',
    case='BCAV2D')

field = ['X','Y','T','U','V']

Case.define   (field=field)
Case.decompose(f='T',act='add')

Case.plot(
    f='T',
    name='S_T',
    save=True,
    show=False,
    ptype='solidCircle',
    atype='semilog')

U = Case.U[Case.indexd('T')][:,5]

Case.draw2D(
    X = U,
    name = 'Field_ST2',
    save = True,
    show = False
)






