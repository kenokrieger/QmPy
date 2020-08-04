"""Throwaway script to generate reference data for tests"""
from sympy.physics.qho_1d import psi_n
from numpy import pi, sin, cos, exp, sqrt
import numpy as np
import matplotlib.pyplot as plt

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
    energy = omega * (n + 0.5)
    return energy, wfunc


if __name__ == '__main__':
    """
    #infinite well
    wfuncs = np.empty((2001, 11))
    xi = np.linspace(0, 20, 2001)
    wfuncs[:, 0] = xi
    energies = list()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    for n in range(1, 11):
        energy, wfunc = infwell(n, 20, 1)
        energies.append(energy)
        wfuncs[:, n] = wfunc(xi)
        ax.plot(xi, wfuncs[:, n] + 1 * n)

    np.savetxt('test_data/wfuncs_infwell.ref', wfuncs)
    np.savetxt('test_data/energies_infwell.ref', np.array(energies))
    """
    """
    #harmonic oscillator
    wfuncs = np.empty((2001, 11))
    xi = np.linspace(0, 20, 2001)
    wfuncs[:, 0] = xi
    energies = list()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    for n in range(0, 10):
        energy, wfunc = osci(n, 1, 1)
        energies.append(energy)
        wfuncs[:, n + 1] = wfunc(xi)
        ax.plot(xi, wfuncs[:, n + 1] + 3 * n)

    np.savetxt('test_data/wfuncs_osci.ref', wfuncs)
    np.savetxt('test_data/energies_osci.ref', np.array(energies))
    """




