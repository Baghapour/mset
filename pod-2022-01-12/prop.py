'''
prop module (2022):
provide thermofluid properties
'''

from CoolProp.CoolProp import PropsSI

class Reynolds(object):
    @staticmethod
    def calc(L=None,nu=None,U=None):
        return U*L/nu
    @staticmethod
    def calcU(Re=None,L=None,nu=None):
        return Re*nu/L

class Rayleigh(object):
    @staticmethod
    def calc(g=9.81,beta=None,dT=None,L=None,nu=None,alf=None):
        return g*beta*dT*L**3/(nu*alf)  
    @staticmethod
    def calcDT(g=9.81,Ra=None,beta=None,L=None,nu=None,alf=None):
        return Ra*nu*alf/(g*beta*L**3)
    @staticmethod
    def product(Gr=None,Pr=None):
        return Gr*Pr

class Grashof(object):
    @staticmethod
    def calc(g=9.81,beta=None,dT=None,L=None,nu=None):
        return g*beta*dT*L**3/nu**2  
    @staticmethod
    def calcDT(g=9.81,Gr=None,beta=None,L=None,nu=None):
        return Gr*nu**2/(g*beta*L**3)

class Prandtl(object):
    @staticmethod
    def calc(nu=None,alf=None):
        return nu/alf
    @staticmethod
    def calcAlf(Pr=None,nu=None):
        return nu/Pr

class fluid(object):
    def __init__(self,Fluid=None,Pref=None,Tref=None):
        self.Fluid = Fluid
        self.Pref  = Pref
        self.Tref  = Tref
        self.rho   = PropsSI('D','T',Tref,'P',Pref,Fluid)
        self.mu    = PropsSI('V','T',Tref,'P',Pref,Fluid)
        self.Pr    = PropsSI('PRANDTL','T',Tref,'P',Pref,Fluid)
        self.beta  = PropsSI('ISOBARIC_EXPANSION_COEFFICIENT','T',Tref,'P',Pref,Fluid)
        self.M     = self.rho*1000/PropsSI('DMOLAR','T',Tref,'P',Pref,Fluid)
        self.Cv    = PropsSI('CVMASS','T',Tref,'P',Pref,Fluid)
        self.Cp    = PropsSI('CPMASS','T',Tref,'P',Pref,Fluid)
        self.nu    = self.mu/self.rho