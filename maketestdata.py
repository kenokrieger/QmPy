"""Throwaway script to generate reference data for tests"""
from sympy.physics.qho_1d import psi_n
from numpy import pi, sin, cos, exp, sqrt

#infinite well
def infwell(n, L, m):
    energy = n ** 2 * pi ** 2 / (2 * m * L ** 2)
    if n%2:
        def wfunc(x):
            return sqrt(2 / L) * sin(n * pi / L * x)
    else:
        def wfunc(x):
            return sqrt(2 / L) * cos(n * pi / L * x)
    return energy, wfunc


#harmonic oscillator
def osci(n, m, omega, hbar=1):
    def wfunc(x):
        func = str(psi_n(n, x, m, omega)).replace('hbar', '1')
        return eval(func)  
    return wfunc



