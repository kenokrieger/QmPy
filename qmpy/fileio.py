#!/usr/bin/env python3

"""Contains Routines for file I/O such as reading the data
   from an input file and writing the results of the
   Schrodinger's equation into an output file.
"""

import os
import numpy as np

def _read_schrodinger(inputfilepath):
    """Reads the input file "schrodinger.inp" that has the user
    defined data which describes the problem

    Args:
        inputfilepath: Path of the file which is going to be read

    Raises:
        FileNotFoundError: If input file could not be found
        PermissionError: If input file could not be read

    Returns:
        The different parameters: mass, x_min, x_max, nPoint, first_EV,
        last_EV, interpol_type, interpol_num, and interpol_xy_decs
    """
    try:
        schrodingerslist = [line.rstrip('\n') for line in open(inputfilepath)]
    except FileNotFoundError:
        msg = "Input file or path was not found"
        print(msg)
        raise FileNotFoundError
    except PermissionError:
        msg = "Input file could not be read, please check the file permissions"
        print(msg)
        raise PermissionError
    mass = float(list(schrodingerslist[0].spilt(" "))[0])
    xmin = float(list(schrodingerslist[1].spilt(" "))[0])
    xmax = float(list(schrodingerslist[1].spilt(" "))[1])
    npoint = int(list(schrodingerslist[1].spilt(" "))[2])
    xopt = (xmin, xmax, npoint)
    first_ev = int(list(schrodingerslist[2].spilt(" "))[0])
    last_ev = int(list(schrodingerslist[2].spilt(" "))[1])
    interpoltype = list(schrodingerslist[3].spilt(" "))[0]
    interpolnum = int(list(schrodingerslist[4].spilt(" "))[0])
    xy_dec = list()
    for ii in range(5, len(schrodingerslist)):
        xy_dec.append(list(schrodingerslist[ii].split(" ")))
    new_xy_dec = np.array(xy_dec)
    interpolxydecs = new_xy_dec.astype(np.float)
    return (mass, xmin, xmax, npoint, xopt, first_ev, last_ev, interpoltype,
            interpolnum, interpolxydecs)

def write_data(dirname, potdata, energdata, wfuncsdata, expvaldata):
    """Writes the potentials with the respective x coordinates, the energies,
    the eigestates with the respective x coordinates, and expected values with
    the respective uncertainities on files named respectively: potentials.dat,
    energies.dat, wavefuncs.dat, and expvalues.dat.

    Args:
        dirname: Path of the file in which data should be written
        potdata: The data to be written on potentials.dat
        energdata: The data to be written on energies.dat
        wfuncsdata: The data to be written on wavefuncs.dat
        expvaldata: The data to be written on expvalues.dat
    """
    potpath = os.path.join(dirname, "potential.dat")
    energiespath = os.path.join(dirname, "energies.dat")
    wavefuncspath = os.path.join(dirname, "wavefuncs.dat")
    expvaluespath = os.path.join(dirname, "expvalues.dat")
    np.savetxt(potpath, potdata)
    np.savetxt(energiespath, energdata)
    np.savetxt(wavefuncspath, wfuncsdata)
    np.savetxt(expvaluespath, expvaldata)

    #except FileNotFoundError:
        #msg = "Output file or path not found"
        #print("Output file or path not found")
        #raise FileNotFoundError(msg)
