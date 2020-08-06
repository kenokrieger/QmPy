#!/usr/bin/env python3
""" Contains functions for plotting the  potential, the eigenvalues and the
    respective wave functions as well as the expected values for each
    eigenvalue from the files that contain the solution of the problem.
"""
import os
import numpy as np
import matplotlib.pyplot as plt

def qm_plottings(dirname):
    """Plots the potential, the eigenvalues and the respective
    wave functions as well as the expected values for each eigenvalue
    from the files that contain the solution of the problem

    Args:
        dirname: Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.

    Return:
        Plots of the potential, the eigenvalues and the respective
    wave functions
    """
    (xcoordsarray, potsarray, energarray, wfuncsarray,
     expvalsarray, uncertainityarray) = _isolate_plot_data(dirname)
    plt.subplot(1, 2, 1)
    plt.xlabel("x [Bohr]")
    plt.ylabel("Energy [Hartree]")
    plt.title("Potential, eigenstates, <x>")
    plt.plot(xcoordsarray, potsarray, color="black") # Potential
    for ii in range(0, len(wfuncsarray[0])): # Wave functions (eigenstates)
        plt.plot(xcoordsarray, wfuncsarray[:, ii])
    for ii in range(0, len(energarray)): # Energies (Eigenvalues)
        plt.plot(xcoordsarray, energarray[ii], color="grey")
    for ii in range(0, len(expvalsarray)): # expected value plot
        plt.scatter(expvalsarray[ii], energarray[ii], color="green",
                    marker="x")
    plt.show()
    plt.subplot(1, 2, 2)
    plt.xlabel("x [Bohr]")
    plt.ylabel("Energy [Hartree]")
    plt.title("sigma x") # This still needs latex code version
    for ii in range(0, len(energarray)): # Energies (Eigenvalues)
        plt.plot(xcoordsarray, energarray[ii], color="grey")
    for ii in range(0, len(uncertainityarray)): # expected value plot
        plt.scatter(uncertainityarray[ii], energarray[ii], color="purple",
                    marker="+")# sigma x plots
    plt.show()

def _readplotsfiles(dirname):
    """Reads the files and exports the data needed to use the QM_Plottings
    function

    Args:
        dirname: Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.
    Returns:
        potdata
        energiesdata
        wavefuncsdata
        expvaluesdata
    """
    potpath = os.path.join(dirname, "potential.dat")
    energiespath = os.path.join(dirname, "energies.dat")
    wavefuncspath = os.path.join(dirname, "wavefuncs.dat")
    expvaluespath = os.path.join(dirname, "expvalues.dat")
    potdata = np.loadtxt(potpath)
    energdata = np.loadtxt(energiespath)
    wfuncsdata = np.loadtxt(wavefuncspath)
    expvaldata = np.loadtxt(expvaluespath)
    return potdata, energdata, wfuncsdata, expvaldata

def _isolate_plot_data(dirname):
    """ Isolates the necessary data to plot the potential, the eigenvalues
    and the respective wave functions as well as the expected values
    for each eigenvalue

    Args:
        dirname: Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.

    Return:
        xcoordsarray
        potsarray
        energarray
        wfuncsarray
        expvalsarray

    """
    potdata, energdata, wfuncsdata, expvaldata = _readplotsfiles(dirname)
    # Isolate x coordinates from potdata array
    xcoordslist = []
    for ii in range(0, len(potdata)):
        elementsx = potdata[ii]
        xcoords = elementsx[0]
        xcoordslist.append(xcoords)
    xcoordsarray = np.array(xcoordslist)

    # Isolate potentials from potdata array
    potslist = []
    for ii in range(0, len(potdata)):
        elementspot = potdata[ii]
        pots = elementspot[1]
        potslist.append(pots)
    potsarray = np.array(potslist)

    # Energdata has already the wished form
    energarray = energdata

    # Isolate wave functions from wfuncsdata array
    wfuncslist = []
    for ii in range(0, len(potdata)):
        elementswfunc = wfuncsdata[ii]
        wfuncs = list(elementswfunc)
        wfuncs.remove(elementswfunc[0])
        wfuncslist.append(wfuncs)
    wfuncsarray = np.array(wfuncslist)

    # Isolate expected values from expvaldata array
    expvallist = []
    for ii in range(0, len(expvaldata)):
        elementsexpval = expvaldata[ii]
        expvals = list(elementsexpval)
        expvals.remove(elementsexpval[1])
        expvallist.append(expvals)
    expvalsarray = np.array(expvallist)

    # Isolate uncetainity from expvaldata array
    uncertainitylist = []
    for ii in range(0, len(expvaldata)):
        elementsuncertainity = expvaldata[ii]
        uncertains = list(elementsuncertainity)
        uncertains.remove(elementsuncertainity[0])
        uncertainitylist.append(expvals)
    uncertainityarray = np.array(uncertainitylist)

    return (xcoordsarray, potsarray, energarray, wfuncsarray, expvalsarray,
            uncertainityarray)
