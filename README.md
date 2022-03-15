# <img src="http://qmpy.org/badges/qmpy_logotext.png" height=60>

<img src="https://github.com/kenokrieger/QmPy/blob/master/_imgs/build%20passing.svg"> <img src="https://github.com/kenokrieger/QmPy/blob/master/_imgs/coverage98.svg">
<img src="https://img.shields.io/github/issues/kenokrieger/QmPy"> <img src="https://img.shields.io/github/commit-activity/m/kenokrieger/QmPy">
<img src="https://github.com/kenokrieger/QmPy/blob/master/_imgs/release.svg"> <img src="https://github.com/kenokrieger/QmPy/blob/master/_imgs/license.svg">

QmPy is a python package containing routines to numerically solve and visualize
the schroedinger equation for different potentials. Its main purpose is to
support an executable script called qmsolve which combines the functionalities
above.


## Disclaimer

This is a student project. It utilizes very unstable and simple numerical
algorithms.

## Requirements

This package requires Python 3.6 or higher and the packages numpy, scipy and
matplotlib.

## Installation

For easy installation with pip use:

```shell
pip install -i https://test.pypi.org/simple/ qmpy-schrodinger
```

## Usage

### Using the script

The script requires a configuration file which contains all the necessary
information about the quantum mechanical system. The data is provided in
json format. By default the script will search for a file 'qmsolve_config.json'.
An example of such a file is included below. <br/>
```json
{
  "computation": {
    "mass": 4.0,
    "xrange": {
      "xmin": -20.0,
      "xmax":  20.0,
      "npoint": 1999
    },
    "evrange": [1, 10],
    "interpolation.type": "cspline",
    "potential": {
      "x.values": [-20.0, -10.0, 0.0, 10.0, 20.0],
      "y.values": [35.0, 0.0, 2.0, 0.0, 35.0]
    }
  },
  "visualisation": {
    "autoscale": true,
    "scale": null,
    "xlim": null,
    "ylim": null
  }
}
```
The field 'visualisation' is entirely optional and just for customisation
purposes. The script can be run via the command line by using
```shell
./qmsolve
```
It supports computing energies, wavefunctions and expected values for
the x-coordinate, which is invoked with the command `./qmsolve compute`. The
results may also be visualized by using `./qmsolve visualise`. It also takes
numerous optional arguments which will be listed when using the `-h` option with
one of the commands.

### Using the modules

Calculating the first four energies and wavefunctions of a particle in a box
aswell as the expected values and uncertainties for the x-xoordinate for each
state.

```python

from qmpy.solvers import schroedinger, calculate_expval, calculate_uncertainty
from numpy import linspace, zeros

mass = 2.0
xcords = linspace(-2, 2, 1999)
pot = zeros((1999, ))

vals = {'mass': mass,
        'xcords': xcords,
        'potential': pot}

# returns the first four energies and wavefunctions
energies, wfuncs = schroedinger(vals, select_range=(0, 3))

# calculate the expected value for the x-coordinate for each state
expvals = calculate_expval(xcoords, wfuncs)

# calculate the uncertainty of the x-coordinate for each state
uncs = calculate_uncertainty(xcoords, wfuncs)

```

Plotting numerical data contained in a directory

```python

from qmpy.graphics import qm_plottings

# directory containing the files potential.dat, energies.dat,
# wavefuncs.dat, and expvalues.dat.
datadir = 'myqmdata/'

# plot the data and save the plot as 'my_plot.png'
qm_plottings(datadir, sname='my_plot.png')

```

## Documentation

The documentation can be found at
[kenokrieger.com/code_projects/qmpy](https://kenokrieger.com/code_projects/qmpy).

## Tests

Tests for the package are located in the tests/ directory. The tests can all
be run via pytest through the command line (`python3 -m pytest` in the
highest directory).

## Contributing

Contributions are always welcome. To contribute fork the repository from
github and develop your feature including unit tests. For your contribution
to be incorporated in the main build issue a pull request.

## License

[BSD 2-Clause License](https://choosealicense.com/licenses/bsd-2-clause/) <br/>
See LICENSE.txt for further information.
