"""
Contains routines for the file I/O such as reading the data
from an input file and writing the results of the
Schrodinger's equation into an output file.
"""
import os
import numpy as np


def _read_config(inputfilepath):
    """Reads the input file "schrodinger.inp" that has the user
    defined data which describes the problem

    Args:
        inputfilepath (str): Path of the file which is going to be read

    Returns:
        specs (dict): A dictionary that contains the different parameters :
        mass, x_min, x_max, nPoint, first_EV, last_EV, interpol_type,
        interpol_num, and interpol_xy_decs
    """
    required_keys = ["mass", "xrange", "evrange", "interpolation", "pivots"]
    pivotlines = [-1, -1]
    specs = dict()
    transforms = {
        "mass": float,
        "xrange": (float, float, int),
        "evrange": (int, int),
        "interpolation": str
    }
    with open(inputfilepath, 'r') as file:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            # if line is a comment
            if line[0] == '#':
                continue
            else:
                if "/pivots" in line:
                    pivotlines[0] = idx + 1
                elif "pivots/" in line:
                    pivotlines[1] = idx - pivotlines[0]
                elif '=' in line:
                    _add_configuration(line, specs, transforms)

    if any([pivotline < 0 for pivotline in pivotlines]):
        errmsg = "Missing declaration for start or end of pivots in file '{}'\n" \
                 "Start of pivot declaration is indicated by '/pivots' and end " \
                 "by 'pivots/'".format(inputfilepath)
        raise ValueError(errmsg)
    else:
        specs["pivots"] = np.loadtxt(inputfilepath, skiprows=pivotlines[0],
                                     max_rows=pivotlines[1])
    missing_keys = _find_missing_keys(specs, required_keys)
    if missing_keys:

        errmsg = "Missing input value(s): {0} in file '{1}'".format(
            ", ".join(missing_keys), inputfilepath)
        raise ValueError(errmsg)
    else:
        return specs


def _add_configuration(line, specs, transforms):
    """
    Takes a line from a configuration file containing a '=' as input. And
    extracts the name for the key and its value from it. Key and value will be
    added to the given dictionary and values will be transformed according to
    the dictionary 'transforms'.

    Args:
        line(str): The line from the configuration file.
        specs(dict): The dictionary to add the extracted information to.
        transforms(dict): Types the the input values shall be casted to.
            The values of the dict are either cast functions or tuples of
            cast functions depending on the type of the input value.

    Returns:
        None.

    """
    key, value = (arg.strip() for arg in line.split('='))
    castings = transforms[key]

    if not isinstance(castings, tuple):
        specs[key] = castings(value)
    else:
        specs[key] = tuple(cast(val.strip())
            for val, cast in zip(value.split(','), castings))


def _find_missing_keys(specs, required_keys):
    """
    Checks whether all keys in a dictionary exist and have the right values.

    Args:
        specs(dict): The dictionary to check.
        required_keys(list): All required keys.

    Returns:
        A list of missing keys.

    """
    missing_keys = [item for item in required_keys if item not in specs.keys()]
    return missing_keys



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
