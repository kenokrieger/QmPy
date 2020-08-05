#!/usr/bin/env python3
import numpy as np
import os
import matplotlib.pyplot as plt

def QM_Plottings(dirname):
    """Plots the potential, the eigenvalues and the respective
    wave functions from the files that contain the solution
    of the problem

    Args:
        dirname: Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.

    Return:
        Plots of the potential, the eigenvalues and the respective
    wave functions
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

    # Isolate wave functions from wfuncsdata array
    wfuncslist = []
    for ii in range(0, len(potdata)):
        elementswfunc = wfuncsdata[ii]
        wfuncs = list(elementswfunc)
        wfuncs.remove(elementswfunc[0])
        wfuncslist.append(wfuncs)
    wfuncsarray = np.array(wfuncslist)

    # Isolate expected values from expvaldata array



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
    potdata =  np.loadtxt(potpath)
    energdata = np.loadtxt(energiespath)
    wfuncsdata = np.loadtxt(wavefuncspath)
    expvaldata = np.loadtxt(expvaluespath)
    return potdata, energdata, wfuncsdata, expvaldata
