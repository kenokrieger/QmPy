"""Contains tests for the private _solvers module"""
from numpy import insert, loadtxt, allclose
import pytest
from qmpy.solvers import schroedinger
from qmpy._fileio import _read_schrodinger


PROBLEMS = ['inf_potwell', 'fin_potwell', 'double_well', 'asym_potwell',
            'harm_osci']


@pytest.mark.parametrize('problem', PROBLEMS)
def test_computing(problem):
    """
    Tests whether the computed wavefunctions and energies match the
    reference data.

    """
    path = 'tests/test_data/{}.inp'.format(problem)
    specs = _read_schrodinger(path)
    vals = dict()
    vals['mass'] = specs['mass']
    vals['xcords'] = specs['interpolxydecs'][:, 0]
    vals['potential'] = specs['interpolxydecs'][:, 1]
    vals['xopt'], kind = (specs['xopt'], specs['interpoltype'])

    evs = (specs['first_ev'] - 1, specs['last_ev'] - 1)

    comp_energies, wfuncs, pot = schroedinger(vals, interpol=True,
                                              interpoltype=kind,
                                              select_range=evs)

    comp_funcs = insert(wfuncs.T, 0, values=pot[:, 1].T, axis=1)
    ref_energies = loadtxt('tests/test_data/energies_{}.ref'.format(problem))
    ref_wfuncs = loadtxt('tests/test_data/wfuncs_{}.ref'.format(problem))

    assert allclose(ref_energies, comp_energies)
    assert allclose(ref_wfuncs, comp_funcs)
