from numpy import loadtxt
import json
import sys


def _read_config_legacy(inputfilepath):
    """Reads the input file "schrodinger.inp" that has the user
    defined data which describes the problem
    Args:
        inputfilepath: Path of the file which is going to be read
    Raises:
        FileNotFoundError: If input file could not be found
        PermissionError: If input file could not be read
    Returns:
        dict: Dictionary containing mass, x_min, x_max, nPoint, first_EV,
        last_EV, interpol_type, interpol_num, and interpol_xy_decs
    """
    try:
        lines = [line.rstrip('\n') for line in open(inputfilepath)]
    except OSError as e:
        err_msg = "Error reading config file '{}': {}".format(inputfilepath, e)
        raise OSError(err_msg)
    specs = dict()
    specs['mass'] = float(list(lines[0].split())[0])
    specs['xmin'] = float(list(lines[1].split())[0])
    specs['xmax'] = float(list(lines[1].split())[1])
    specs['npoint'] = int(list(lines[1].split())[2])
    specs['xopt'] = (specs['xmin'], specs['xmax'], specs['npoint'])
    specs['first_ev'] = int(list(lines[2].split())[0])
    specs['last_ev'] = int(list(lines[2].split())[1])
    specs['interpoltype'] = list(lines[3].split())[0]
    specs['interpolnum'] = int(list(lines[4].split())[0])
    specs["interpolxydecs"] = loadtxt(inputfilepath, skiprows=5, dtype=float)
    return specs


def _parse_config_legacy(filename):
    """
    Parse the old configuration dictionary into the new json format and save it
    to a file with a '_parsed' suffix.

    Args:
        filename(str or path): The name of the old configuration file.

    Returns:
        None.

    """
    specs = _read_config_legacy(filename)
    new_specs = {
        "computation": {
            "mass": 0.0,
            "xrange": {
                "xmin": 0.0,
                "xmax": 0.0,
                "npoint": 0
            },
            "evrange": [0, 0],
            "interpolation.type": "",
            "potential": {
                "x.values": [],
                "y.values": []
            }
        }
    }

    new_specs["computation"]["mass"] = specs["mass"]
    new_specs["computation"]["xrange"] = {
        "xmin": specs["xmin"],
        "xmax": specs["xmax"],
        "npoint": specs["npoint"]
    }
    new_specs["computation"]["evrange"] = [specs["first_ev"], specs["last_ev"]]
    new_specs["computation"]["interpolation.type"] = specs["interpoltype"]
    new_specs["computation"]["potential"]["x.values"] = list(specs["interpolxydecs"][:, 0])
    new_specs["computation"]["potential"]["y.values"] = list(specs["interpolxydecs"][:, 1])

    parsed_content = json.dumps(new_specs, indent=2)
    tmp = filename.split(".")
    tmp[-2] += "_parsed"
    new_filename = ".".join(tmp)
    with open(new_filename, "w") as f:
        f.write(parsed_content)


if __name__ == "__main__":
    _parse_config_legacy(sys.argv[1])
