#!usr/bin/env python3

import fileio
import solvers
import _interpolation
import matplotlib.pyplot as plt
from maketestdata import infwell
import numpy as np


if __name__ == '__main__':
    filename = 'test_data/inf_potwell.inp'
    specs = fileio._read_schrodinger(filename)
    xy_decs = specs['interpolxydecs']
    xx = xy_decs[:, 0]
    yy = xy_decs[:, 1]
    xopt = specs['xopt']
    interpolkind = specs['interpoltype']
    xint, yint = _interpolation._interpolate(xx, yy, xopt)
    mass = specs['mass']
    energies, wfuncs = solvers.schroedinger(mass, xint, yint)

    en = energies[:11]
    wfuncss = wfuncs[:11]

    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    for index in range(11):
        ax.plot(xint, 10 * wfuncss[index] + en[index], color='blue')
        ax.hlines(en[index], xint[0], xint[-1], color='k')

    ref_energies = np.empty((10, ))
    ref_wfuncs = np.empty((10, 1999))
    for n in range(1, 11):
        ref_energy, ref_func = infwell(n, 4, 2)
        ref_energies[n - 1] = ref_energy
        ref_wfuncs[n - 1] = ref_func(xint)
        ax.plot(xint, ref_func(xint + 2) + ref_energy, color='red')
