"""Tests for the graphics module"""
from qmpy.graphics import qm_plottings
from qmpy.fileio import _read_schrodinger, write_data
from qmpy.solvers import calculate_expval, calculate_uncertainty
from qmpy._interpolation import _interpolate
import numpy as np

PROBLEM = 'asym_potwell'


def test_plotting(problem):
    """Visualize quantum mechanical problems"""
    specs = _read_schrodinger('test_data/{}.inp'.format(problem))
    xint, yint = _interpolate(specs['interpolxydecs'][:, 0],
                              specs['interpolxydecs'][:, 1], specs['xopt'])

    energies = np.loadtxt('test_data/energies_{}.ref'.format(problem))
    wfuncsdata = np.loadtxt('test_data/wfuncs_{}.ref'.format(problem))
    potdata = np.vstack((xint, yint)).T

    expval = calculate_expval(xint, wfuncsdata[:, 1:].T)
    uncval = calculate_uncertainty(xint, wfuncsdata[:, 1:].T)

    expvaldata = np.vstack((expval, uncval)).T
    write_data('test_data', potdata, energies, wfuncsdata, expvaldata)

    qm_plottings('test_data')


if __name__ == '__main__':
    test_plotting(PROBLEM)
