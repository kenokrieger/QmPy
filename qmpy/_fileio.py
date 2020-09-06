"""
Contains routines for the file I/O such as reading the data
from an input file and writing the results of the
Schrodinger's equation into an output file.
"""
import os
import numpy as np


def _read_schrodinger(inputfilepath):
    """Reads the input file "schrodinger.inp" that has the user
    defined data which describes the problem

    Args:
        inputfilepath (str): Path of the file which is going to be read

    Returns:
        specs (dict): A dictionary that contains the different parameters :
        mass, x_min, x_max, nPoint, first_EV, last_EV, interpol_type,
        interpol_num, and interpol_xy_decs
    """
    schrodingerslist = [line.rstrip('\n') for line in open(inputfilepath, 'r')]

    specs = dict()
    specs['mass'] = float(list(schrodingerslist[0].split(" "))[0])
    specs['xmin'] = float(list(schrodingerslist[1].split(" "))[0])
    specs['xmax'] = float(list(schrodingerslist[1].split(" "))[1])
    specs['npoint'] = int(list(schrodingerslist[1].split(" "))[2])
    specs['xopt'] = (specs['xmin'], specs['xmax'], specs['npoint'])
    specs['first_ev'] = int(list(schrodingerslist[2].split(" "))[0])
    specs['last_ev'] = int(list(schrodingerslist[2].split(" "))[1])
    specs['interpoltype'] = list(schrodingerslist[3].split(" "))[0]
    specs['interpolnum'] = int(list(schrodingerslist[4].split(" "))[0])
    xy_dec = list()
    for ii in range(5, len(schrodingerslist)):
        xy_dec.append(list(schrodingerslist[ii].split(" ")))
    new_xy_dec = np.array(xy_dec)
    specs['interpolxydecs'] = new_xy_dec.astype(np.float)

    return specs


def _write_data(dirname, potdata, energdata, wfuncsdata, expvaldata):
    """Writes the potentials(with the respective x coordinates), the energies,
    the eigestates(with the respective x coordinates), and the expected values
    with the respective uncertainities on files named respectively:
    potentials.dat, energies.dat, wavefuncs.dat, and expvalues.dat.

    Args:
        dirname (str): Path of the file in which data should be written
        potdata (array): The data to be written on potentials.dat
        energdata (array): The data to be written on energies.dat
        wfuncsdata (array): The data to be written on wavefuncs.dat
        expvaldata (array): The data to be written on expvalues.dat
    """
    potpath = os.path.join(dirname, "potential.dat")
    energiespath = os.path.join(dirname, "energies.dat")
    wavefuncspath = os.path.join(dirname, "wavefuncs.dat")
    expvaluespath = os.path.join(dirname, "expvalues.dat")
    np.savetxt(potpath, potdata)
    np.savetxt(energiespath, energdata)
    np.savetxt(wavefuncspath, wfuncsdata)
    np.savetxt(expvaluespath, expvaldata)


def _readplotsfiles(dirname):
    """Reads the files in the given directory and exports the data needed
    to use the QM_Plottings function on the _graphics module

    Args:
        dirname (str): Name of the directory or path from which
        the files are going to be ploted. The directory must have
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.
    Returns:
        potdata (array): Contains the potentials and its respective
        x-coordinates
        energiesdata (array): Contains the energies of the eigenstates
        wavefuncsdata (array): Contains the eigestates and its respective
        x-coordinates
        expvaluesdata (array): the expected values with the respective
        uncertainities
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
