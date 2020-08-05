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
    potdata, energiesdata, wavefuncsdata, expvaluesdata = _readplotsfiles(dirname)



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
    energiesdata = np.loadtxt(energiespath)
    wavefuncsdata = np.loadtxt(wavefuncspath)
    expvaluesdata = np.loadtxt(expvaluespath)
    return potdata, energiesdata, wavefuncsdata, expvaluesdata
