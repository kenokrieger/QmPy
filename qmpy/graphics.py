""" Contains functions for plotting the  potential, the eigenvalues and the
    respective wave functions as well as the expected values for each
    eigenvalue from the files that contain the solution of the problem.
"""
import os
import numpy as np
from fileio import _readplotsfiles
import matplotlib.pyplot as plt


def qm_plottings(dirname, xmin, xmax, enmin, enmax, scale):
    """Plots the potential, the eigenvalues and the respective
    wave functions as well as the expected values for each eigenvalue
    from the files that contain the solution of the problem

    Args:
        dirname: Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.
        xmin: Minimal value of the x-axis
        xmax: Maximal value of the x-axis
        enmin: Minimal value of the energy-axis
        enmax: Maximal value of the energy-axis
        scale: Factor to fit the wavefunctions

    Return:
        Plots of the potential, the eigenvalues and the respective
        wave functions

    """
    (xcoordsarray, potsarray, energarray, wfuncsarray,
     expvalsarray, uncertainityarray) = _isolate_plot_data(dirname)
    fig = plt.figure(1)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_xlabel("x [Bohr]")
    ax1.set_ylabel("Energy [Hartree]")
    ax1.set_title(r'Potential, eigenstates, $ \langle x \rangle $')
    ax1.set(xlim=(xmin, xmax), ylim=(enmin, enmax))
    ax1.plot(xcoordsarray, potsarray, color="black")

    wfuncsarray.T
    ii = 0
    for wfunc, energy in zip(wfuncsarray, energarray):
        offsetwfunc = scale * wfunc + energy
        if ii % 2 == 0:
            ax1.plot(xcoordsarray, offsetwfunc, color="red")
        else:
            ax1.plot(xcoordsarray, offsetwfunc, color="blue")
        ii += 1

    ax1.hlines(energarray, xcoordsarray[0], xcoordsarray[-1], color='grey')
    ax1.scatter(expvalsarray, energarray, color="green", marker="x")

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_xlabel("x [Bohr]")
    ax2.set_title(r'$\sigma_{x}$')

    ax2.hlines(energarray, xcoordsarray[0], xcoordsarray[-1], color='grey')
    ax2.scatter(uncertainityarray, energarray, color="purple",
                marker="+")

    plt.show()
    # plt.savefig("QmPy_plots")


def _isolate_plot_data(dirname):
    """ Isolates the necessary data to plot the potential, the eigenvalues
    and the respective wave functions as well as the expected values
    for each eigenvalue

    Args:
        dirname: Name of the directory or path from which
        the files are going to be plotted. The directory must contain
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.

    Return:
        touple: The extracted  data.

            - **xcoords** (*1darray*) - The x-coordinates,

            - **pots** (*1darray*) - The numerical values of the potential

            - **energies** (*ndarray*) - The different energy levels

            - **wfuncs** (*ndarray*) - The wavefunctions where each column
                contains the numerical values of one wavefunction.

            - **expvals** (*1darray*) - The expected values for the
                x-coordinate for each state.

            - **uncertainties** (*1darray*) - The uncertainties of the
                x-coordinate for each state.

    """
    potdata, energdata, wfuncsdata, expvaldata = _readplotsfiles(dirname)
    xcoords = potdata[:, 0].copy()
    pots = potdata[:, 1].copy()
    energies = energdata
    wfuncs = wfuncsdata[:, 1:].copy()
    expvals = expvaldata[:, 0].copy()
    uncertainties = expvaldata[:, 1].copy()

    return xcoords, pots, energies, wfuncs, expvals, uncertainties
