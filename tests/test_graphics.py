from qmpy.graphics import qm_plottings
from qmpy.fileio import _read_schrodinger, write_data
from qmpy.solvers import calculate_expval, calculate_uncertainity
from qmpy._interpolation import _interpolate
import numpy as np


def test_plotting():
    specs = _read_schrodinger('test_data/asym_potwell.inp')
    xint, yint = _interpolate(specs['interpolxydecs'][:, 0],
                              specs['interpolxydecs'][:, 1], specs['xopt'])

    energies = np.loadtxt('test_data/energies_asym_potwell.ref')
    wfuncsdata = np.loadtxt('test_data/wfuncs_asym_potwell.ref')
    potdata = np.vstack((xint, yint)).T

    expval = calculate_expval(xint, wfuncsdata[:, 1:])
    uncval = calculate_uncertainity(xint, wfuncsdata[:, 1:])

    expvaldata = np.vstack((expval, uncval)).T
    write_data('test_data', potdata, energies, wfuncsdata, expvaldata)

    qm_plottings('test_data', auto_scale=False)


test_plotting()
