"""Contains tests for the private _solvers module"""
from numpy import insert, loadtxt, allclose, array
import pytest
from qmpy.solvers import schroedinger
from qmpy._fileio import _read_config


PROBLEMS = ['inf_potwell', 'fin_potwell', 'double_well', 'asym_potwell',
            'harm_osci']


@pytest.mark.parametrize('problem', PROBLEMS)
def test_computing(problem):
    """
    Tests whether the computed wavefunctions and energies match the
    reference data.

    """
    path = 'tests/test_data/{}_parsed.inp'.format(problem)
    specs = _read_config(path)["computation"]
    vals = dict()
    vals["mass"] = specs["mass"]
    vals["xcords"] = array(specs["potential"]["x.values"])
    vals['potential'] = array(specs["potential"]["y.values"])
    vals['xopt'] = (
        specs["xrange"]["xmin"], specs["xrange"]["xmax"],
        specs["xrange"]["npoint"]
    )
    # translate range into python range starting with 0
    ev_range = tuple(evnr - 1 for evnr in specs["evrange"])

    comp_energies, wfuncs, pot = schroedinger(vals, interpol=True,
                                              interpoltype=specs["interpolation.type"],
                                              select_range=ev_range)
    ref_energies = loadtxt('tests/test_data/energies_{}.ref'.format(problem))

    assert allclose(ref_energies, comp_energies)
