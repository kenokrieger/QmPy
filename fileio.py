#!/usr/bin/env python3

"""Contains Routines for file I/O such as reading the data
   from an input file and writing the results of the
   Schrodinger's equation into an output file.
"""

import numpy as np

def _read_schrodinger(inputfilepath):
    """Reads the input file "schrodinger.inp" that has the user
    defined data which describes the problem

    Args:
        inputfilepath: Path of the file which is going to be read

    Raises:
        FileNotFoundError: (Needs to be added) If input file could not be found
        PermissionError: (Needs to be added)

    Returns:
        The different parameters: mass, x_min, x_max, nPoint, first_EV,
        last_EV, interpol_type, interpol_num, and interpol_xy_decs
    """
    schrodingerslist = [line.rstrip('\n') for line in open(inputfilepath)]
    mass = list(schrodingerslist[0].spilt(" "))[0]
    x_min = list(schrodingerslist[1].spilt(" "))[0]
    x_max = list(schrodingerslist[1].spilt(" "))[1]
    nPoint = list(schrodingerslist[1].spilt(" "))[2]
    first_EV = list(schrodingerslist[2].spilt(" "))[0]
    last_EV = list(schrodingerslist[2].spilt(" "))[1]
    interpol_type = list(schrodingerslist[3].spilt(" "))[0]
    interpol_num = list(schrodingerslist[4].spilt(" "))[0]
    xy_dec = list()
    for ii in range(5, len(schrodingerslist)):
        xy_dec.append(list(schrodingerslist[ii].split(" ")))
    interpol_xy_decs = np.array(xy_dec)
    return mass, x_min, x_max, nPoint, first_EV, last_EV, interpol_type,
    interpol_num, interpol_xy_decs
