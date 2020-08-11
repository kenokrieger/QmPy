"""Contains tests for the solvers module"""
from qmpy.solvers import schroedinger
from qmpy.fileio import _read_schrodinger
from qmpy._interpolation import _interpolate
from numpy import loadtxt, allclose
import pytest

PROBLEMS = ['inf_potwell', 'double_well', 'asym_potwell', 'harm_osci']


@pytest.mark.parametrize('problem', PROBLEMS)
def test_computing(problem):
    """
    Tests whether the computed wavefunctions and energies match
    reference data.

    """
    path = 'test_data/{}.inp'.format(problem)
    specs = _read_schrodinger(path)

    xx, yy = (specs['interpolxydecs'][:, 0], specs['interpolxydecs'][:, 1])
    xopt, kind = (specs['xopt'], specs['interpoltype'])
    mass = specs['mass']
    evs = (specs['first_ev'] - 1, specs['last_ev'] - 1)

    xint, yint = _interpolate(xx, yy, xopt, kind=kind)
    energies, wfuncs = schroedinger(mass, xint, yint, select_range=evs)
    wfuncs.T

    ref_energies = loadtxt('test_data/energies_{}.ref'.format(problem))
    ref_wfuncs = loadtxt('test_data/wfuncs_{}.ref'.format(problem))

    assert allclose(ref_energies, energies)
    assert allclose(ref_wfuncs, wfuncs)
