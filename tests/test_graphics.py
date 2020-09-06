"""Tests for the private _graphics module"""
import numpy as np
from qmpy.graphics import qm_plottings
from qmpy._fileio import _read_schrodinger, _write_data
from qmpy.solvers import calculate_expval, calculate_uncertainty
from qmpy._interpolation import _interpolate

PROBLEM = 'fin_potwell'


def test_plotting():
    """Tests the visualization of quantum mechanical problems"""
    specs = _read_schrodinger('tests/test_data/{}.inp'.format(PROBLEM))
    xint, yint = _interpolate(specs['interpolxydecs'][:, 0],
                              specs['interpolxydecs'][:, 1], specs['xopt'])

    energies = np.loadtxt('tests/test_data/energies_{}.ref'.format(PROBLEM))
    wfuncsdata = np.loadtxt('tests/test_data/wfuncs_{}.ref'.format(PROBLEM))
    potdata = np.vstack((xint, yint)).T

    expval = calculate_expval(xint, wfuncsdata[:, 1:].T)
    uncval = calculate_uncertainty(xint, wfuncsdata[:, 1:].T)

    expvaldata = np.vstack((expval, uncval)).T
    _write_data('tests/test_data', potdata, energies, wfuncsdata, expvaldata)

    qm_plottings('tests/test_data')
    assert True
