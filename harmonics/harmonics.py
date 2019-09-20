# -*- coding: utf-8 -*- 
import math
import numpy as np
import scipy.constants as constants
from scipy.special import factorial, lpmv, legendre

#############################################################
#   REFERENCE                                               #
#   Formulation of the spherical harmonic coefficients...   #
#   S. Noguchi                                              #
#############################################################

def harm_coeffCyl(Findpoint, r0, z0, I, n, IsOrigin=True, *args):
    # circular line current
    origin = np.array([0, 0, 0])
    if IsOrigin is False:
        for arg in args:
            if type(arg) == np.ndarray:
                origin = arg
                Findpoint = Findpoint - origin                

    cos_th = Findpoint[-1]/np.sqrt(sum(map(lambda x : x*x, Findpoint)))
    cos_a = z0/r0
    sin_a = np.sqrt(1-cos_a**2)
    R_n = lpmv(1, n, cos_th) * constants.mu_0 * I * sin_a * lpmv(1, n+1, cos_a) 
    R_n = R_n / (2 * (n+1) * np.power(r0, n+1))
    
    Pn = legendre(n)
    Z_n = Pn(cos_th) * constants.mu_0 * I * sin_a * lpmv(1, n+1, cos_a)
    Z_n = Z_n / (2 * np.power(r0, n+1))
    return R_n, Z_n



fp = np.array([0,4,3])
r0 = 0.1
z0 = 0
I = 1000
n = np.linspace(0,10,11)
origin = np.array([1,1,2])
for idx in n:
    print("n is %d" %(idx))
    print (harm_coeffCyl(fp, r0, z0, I, idx, False, origin))