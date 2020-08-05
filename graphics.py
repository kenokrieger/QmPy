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
        wfuncs.dat, and expvalues.dat.


    Return:
        Plots of the potential, the eigenvalues and the respective
    wave functions
    """
