"""Contains tests for the solvers module"""
from numpy import insert, loadtxt, allclose
import pytest
from qmpy.solvers import schroedinger
from qmpy._fileio import _read_schrodinger
from qmpy._interpolation import _interpolate


PROBLEMS = ['inf_potwell', 'fin_potwell', 'double_well', 'asym_potwell',
            'harm_osci']


@pytest.mark.parametrize('problem', PROBLEMS)
def test_computing(problem):
    """
    Tests whether the computed wavefunctions and energies match
    reference data.

    """
    path = 'tests/test_data/{}.inp'.format(problem)
    specs = _read_schrodinger(path)

    xxyy = (specs['interpolxydecs'][:, 0], specs['interpolxydecs'][:, 1])
    xopt, kind = (specs['xopt'], specs['interpoltype'])
    mass = specs['mass']
    evs = (specs['first_ev'] - 1, specs['last_ev'] - 1)

    xint, yint = _interpolate(xxyy[0], xxyy[1], xopt, kind=kind)
    comp_energies, wfuncs = schroedinger(mass, xint, yint, select_range=evs)

    comp_funcs = insert(wfuncs.T, 0, values=xint, axis=1)
    ref_energies = loadtxt('tests/test_data/energies_{}.ref'.format(problem))
    ref_wfuncs = loadtxt('tests/test_data/wfuncs_{}.ref'.format(problem))

    assert allclose(ref_energies, comp_energies)
    assert allclose(ref_wfuncs, comp_funcs)
