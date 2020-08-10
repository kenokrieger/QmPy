#!usr/bin/env python3

from qmpy import fileio
from qmpy import solvers
from qmpy import _interpolation
import matplotlib.pyplot as plt
from numpy import insert, savetxt


if __name__ == '__main__':
    filename = 'test_data/harm_osci.inp'
    specs = fileio._read_schrodinger(filename)
    xy_decs = specs['interpolxydecs']
    xx = xy_decs[:, 0]
    yy = xy_decs[:, 1]
    xopt = specs['xopt']
    interpolkind = specs['interpoltype']
    xint, yint = _interpolation._interpolate(xx, yy, xopt)
    mass = specs['mass']
    energies, wfuncs = solvers.schroedinger(mass, xint, yint,
                                            select_range=(0, 4))

    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    for index in range(len(energies)):
        ax.plot(xint, wfuncs[index] + energies[index] + 5 * index,
                color='blue')
        ax.hlines(energies[index] + 5 * index, xint[0], xint[-1], color='k')

    if bool(input('Data correct? ',)):
        save_funcs = insert(wfuncs.T, 0, values=xint, axis=1)
        savetxt('test_data/wfuncs_inf_potwell.ref', save_funcs)

        savetxt('test_data/energies_inf_potwell.ref', energies)
