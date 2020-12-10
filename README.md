# <img src="http://qmpy.org/badges/qmpy_logotext.png" height=60>

<img src="http://qmpy.org/badges/build_passing.svg"> <img src="http://qmpy.org/badges/coverage98.svg">
<img src="https://img.shields.io/github/issues/kenokrieger/QmPy"> <img src="https://img.shields.io/github/commit-activity/m/kenokrieger/QmPy">
<img src="http://qmpy.org/badges/release.svg"> <img src="http://qmpy.org/badges/license.svg">

QmPy is a python package containing routines to numerically solve and visualize
the schroedinger equation for different potentials. Its main purpose is to
support an executable script called qmsolve which combines the functionalities
above.


## Disclaimer

This is a student project. It utilizes very unstable and simple numerical
algorithms.

## Requirements

This package requires Python 3.6 or higher and the packages numpy, scipy,
matplotlib and os.

## Installation

For easy installation with pip use:

```shell
pip install -i https://test.pypi.org/simple/ qmpy-schrodinger
```

## Usage

### Using the script

The script requires a configuration file which contains all the necessary
information about the quantum mechanical system. This file needs to be named
'schrodinger.inp' and must have the following structure: <br/>
```
float # mass
flaot float float/int # xMin xMax nPoint
int int # first and last eigenvalue to include in the output
str # interpolation type
int # nr. of interpolation points and xy declarations
float float
float float
... ...
```
By default qmsolve will look for the 'schrodinger.inp' file in the directory
where it is run. You can, however, specify the path to the file with the `-i`
option. <br/>
The script can be run via the command line by either using
```shell
./qmsolve -C -V
```
where the script file is stored, or
```shell
qmsolve -C -V
```
anywhere if the package was installed using pip.

It supports computing energies, wavefunctions and expected values for
the x-coordinate, which is done by selecting the option `-C`. The results may
also be visualized by selecting `-V`. It also takes numerous optional arguments
which will be listed when using the `-h` option.

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

The documentation can be found at [kenokrieger.github.io/qmpy](http://kenokrieger.github.io/QmPy).
If you want to create the documentation yourself using sphinx you may do so by
changing in the docs/ directory and executing the command `make html`.

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
