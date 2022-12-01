


# Numpy Series
# Numpy array
#from numpy import linspace, arange, shape
# Numpy common math function
#from numpy import exp
# Numpy constant
from numpy import pi
from scipy.integrate import solve_ivp
import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')

class Resonator():
    """
    Properties of resonator
    Dictionary like structure

    """
    def __init__( self ):
        self.f_r = None
        self.kappa_i = None
        self.kappa_c = None
        self.kappa = None

class TransmissionLine():
    """
    Properties of Transmission Line
    """
    def __init__( self ):
        self.s21 = None

class TransmonModel():
    """
    Properties of ideal Transmon
    Dictionary like structure
    """
    def __init__( self ):
        
        self.f_q = None
        self.anharmonicity = None
        self.gamma_1 = None
        self.gamma_phi = None

    @property
    def Ec( self ) -> float:
        """
        Ec in unit of MHz
        Calculated from anharmonicity
        """
        return -self.anharmonicity

class SQUIDTransmonModel(TransmonModel):
    """
    Properties of ideal tunable Transmon 
    Dictionary like structure
    """
    def __init__( self ):
        super().__init__()
        self.flux = None

class SingleReadableTransmon():
    """
    This class is used for record information of a Qubit-Cavity coupling system.
    Dictionary like structure
    property
    g_qc : Unit in MHz
    flux : Unit in magnetic flux quantum
    zSensitivity : Unit in magnetic flux quantum per mA 
    """
    def __init__( self ):

        self.qubit = SQUIDTransmonModel()
        self.dressed_cavity_g = Resonator()
        self.bare_cavity = Resonator()
        self.g = None
        self.detuning = None
        self.chi_01 = None
        self.chi_eff = None
    
    def get_chi_01( self, f_q=None, f_r=None, g=None ):
        """
        chi_01 is -g**2/delta
        """
        if f_q == None:
            f_q = self.qubit.f_q
        if f_r == None:
            f_r = self.bare_cavity.f_r
        if g == None:
            g = self.g

        detuning = (f_q-f_r)

        self.detuning = detuning
        self.chi_01 = -g**2/detuning
        return self.chi_01

    def get_chi_eff ( self, f_q=None, f_r=None, g=None, E_c=None ):

        if E_c == None:
            E_c = -self.qubit.anharmonicity
        chi_01 = self.get_chi_01( f_q, f_r, g )
        detuning = self.detuning
        self.chi_eff = chi_01 *E_c/(detuning-E_c)

        return self.chi_eff

    def qubit_resonator_evo( self, t, f_rd, f_qd, E_rd, E_qd ):
        # coeff
        D_rm = 2*pi*(f_rd -self.dressed_cavity_g.f_r)
        print(D_rm)
        D_as = 2*pi*(f_qd -self.qubit.f_q)
        chi = 2*pi*(self.get_chi_eff())
        kappa = 2*pi*self.dressed_cavity_g.kappa
        eps_m = E_rd # Cavity driving envelope
        Omega = E_qd # Qubit driving envelope
        gamma = 0 # Qubit decay rate
        gamma_phi = 0
        ODE_pars = (D_rm, D_as, chi, kappa, eps_m, Omega, gamma, gamma_phi)
        X0 = 0j
        Y0 = 0j
        Z0 = -1j
        a0 = 0j
        N0 = a0**2
        aX0 = a0*X0
        aY0 = a0*Y0
        aZ0 = a0*Z0
        y0 = [ a0, Z0, X0, Y0, aZ0, aX0, aY0, N0]
        sol = solve_ivp(evoODE, (t[0],t[-1]), y0, t_eval=t, args=ODE_pars)
        return sol

def evoODE(t, y, D_rm, D_as, chi, kappa, eps_m, Omega, gamma, gamma_phi):
    """
    The coupled ODE to simulate time dependent evolution under EM wave driving 
    """

    # Assign vector element to ODE

    a = y[0] # Creation operator
    pz = y[1] # Pauli z 
    px = y[2] # Pauli x
    py = y[3] # Pauli y
    a_pz = y[4]
    a_px = y[5]
    a_py = y[6]
    ad_a = y[7] # Number operator a dagger a

    # 
    d_a = -1j*D_rm*a -1j*chi*a_pz -1j*eps_m -kappa/2*a
    d_pz = Omega*py-gamma*(1+pz)

    as_stark_1 = D_as+2*chi*(ad_a+0.5)
    gamma_a = gamma/2. +gamma_phi
    d_px = -as_stark_1*py -gamma_a*px
    d_py =  as_stark_1*px -gamma_a*py -Omega*pz

    gamma_ar = gamma +kappa/2
    d_a_pz = -1j*D_rm*a_pz -1j*chi*a +Omega*a_py -1j*eps_m*pz -gamma*a -gamma_ar*a_pz
    
    as_stark_2 = D_as+2*chi*(ad_a+1.)
    gamma_apr = gamma/2 +gamma_phi +kappa/2
    d_a_px = -1j*D_rm*a_px -as_stark_2*a_py -1j*eps_m*px -gamma_apr*a_px
    d_a_py = -1j*D_rm*a_py +as_stark_2*a_px -1j*eps_m*py -gamma_apr*a_py -Omega*a_pz
    d_ad_a = -2*eps_m*a.imag -kappa*ad_a

    return [d_a, d_pz, d_px, d_py, d_a_pz, d_a_px, d_a_py, d_ad_a]