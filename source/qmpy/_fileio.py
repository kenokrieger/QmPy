"""
Contains routines for the file I/O such as reading the data
from an input file and writing the results of the
Schrodinger's equation into an output file.
"""
import os
import numpy as np
import json
from json.decoder import JSONDecodeError

KEYS_REQUIRED_FOR_COMPUTATION = [
    "mass", "xrange", "evrange", "interpolation.type", "potential"
]
KEYS_REQUIRED_FOR_XRANGE = ["xmin", "xmax", "npoint"]
KEYS_REQUIRED_FOR_POTENTIAL = ["x.values", "y.values"]

DEFAULT_VISUALISATION_CONFIGURATION = {
    "autoscale": True,
    "scale": None,
    "xlim": None,
    "ylim": None
}

def _read_config(filename):
    """
    Extracts information for compuation and visualisation from a configuration
    file.

    Args:
        filename(str or path): The path to the file.

    Return:
        dict: The configuration as a dictionary.

    Raises:
        ValueError: If an exception while parsing occured or the configuration
            is missing required entries.

    """
    configuration = _read_json(filename)

    if configuration is None:
        raise ValueError("Error when parsing file content.")
    if "computation" not in configuration:
        err_msg = "Missing required field 'computation' in configuration file."
        raise ValueError(err_msg)
    if "visualisation" not in configuration:
        configuration["visualisation"] = DEFAULT_VISUALISATION_CONFIGURATION
    # if a path to a file instead of explicit values was specified,
    # read values from file
    if type(configuration["computation"].get("potential")) is str:
        potential = _read_potential(configuration["computation"]["potential"])
        configuration["computation"]["potential"] = potential

    _validate_configuration(configuration)
    return configuration


def _read_json(filename):
    """
    Parses the json configuration data to a python dictionary.

    Args:
        filename(str or path): The path to the file.

    Returns:
        dict: The parsed data.

    """
    try:
        with open(filename, "r") as f:
            content = f.read()
    except OSError as e:
        err_msg = "Error reading config file '{}': {}".format(filename, e)
        print(err_msg)
        return None

    try:
        data = json.loads(content)
    except JSONDecodeError as e:
        print("Decode error when parsing file '{}': {}".format(filename, e))
        return None
    return data


def _validate_configuration(data):
    """
    Checks if all the values needed for computation and visualisation
    were provided in the input and that they have the correct type.

    Args:
        data(dict): The configuration to validate.

    Returns:
        None.

    Raises:
        ValueError: If keys are missing.

    """
    #recursively check if all keys and 'sub keys' exist
    missing_keys = _find_missing_keys(data["computation"],
                                      KEYS_REQUIRED_FOR_COMPUTATION)
    if missing_keys:
        errmsg = "Missing input value(s) required for computation: {0} ".format(
            ", ".join(missing_keys))
        raise ValueError(errmsg)

    missing_keys = _find_missing_keys(data["computation"]["xrange"],
                                      KEYS_REQUIRED_FOR_XRANGE)
    if missing_keys:
        errmsg = \
            "Missing input value(s) required in field 'xrange': {0} ".format(
                ", ".join(missing_keys)
            )
        raise ValueError(errmsg)


    if type(data["computation"]["potential"]) is not dict:
        missing_keys = KEYS_REQUIRED_FOR_POTENTIAL
    else:
        missing_keys = _find_missing_keys(data["computation"]["potential"],
                                          KEYS_REQUIRED_FOR_POTENTIAL)
    if missing_keys:
        errmsg = \
            "Missing input value(s) required in field 'potential': {0} ".format(
            ", ".join(missing_keys)
            )
        raise ValueError(errmsg)


def _read_potential(filename):
    """
    Reads the values for the potential from a data file.

    Args:
        filename(str or path): The path to the data file.

    Returns:
        dict: The values of the file separated in x and y values.

    """
    try:
        data = np.loadtxt(filename)
    except OSError as e:
        print("Error when reading data file: '{}".format(e))
        return None
    return {
        "x.values": data[:, 0],
        "y.values": data[:, 1]
    }


def _find_missing_keys(specs, required_keys):
    """
    Given a list of keys and a dictionary, find keys missing in the dictionary.

    Args:
        specs(dict): The dictionary to check.
        required_keys(list): All required keys.

    Returns:
        list: A list of missing keys.

    """
    missing_keys = [item for item in required_keys if item not in specs]
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


def _read_data_files(dirname):
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
