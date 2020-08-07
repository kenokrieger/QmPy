#!/usr/bin/env python3
"""Tests for the fileio module"""
import os.path
import numpy as np
from fileio import _read_schrodinger

TESTDATADIR = "test_data"


def test_inf_potwell():
    """Tests the _read_schrodinger function for the infinite potential well"""
    datapath = os.path.join(TESTDATADIR, "inf_potwell.inp")
    specs = _read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[-2.0, 0.0], [2.0, 0.0]], dtype=float)
    assert specs['mass'] == 2.0
    assert specs['xmin'] == -2.0
    assert specs['xmax'] == 2.0
    assert specs['npoint'] == 1999
    assert specs['xopt'] == (-2.0, 2.0, 1999)
    assert specs['first_ev'] == 1
    assert specs['last_ev'] == 5
    assert specs['interpoltype'] == "linear"
    assert specs['interpolnum'] == 2
    assert np.all(specs['interpolxydecs'] == expected_interpolxydecs)


def test_asym_potwell():
    """Tests the _read_schrodinger function for the asymetric potential well"""
    datapath = os.path.join(TESTDATADIR, "asym_potwell.inp")
    specs = _read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[0.0, 30.0], [1.0, 11.8], [2.0, 1.7],
                                        [3.0, 0.0], [5.0, 0.6], [7.0, 1.6],
                                        [9.0, 2.4], [11.0, 3.0], [13.0, 3.4],
                                        [15.0, 3.6], [19.0, 3.79],
                                        [20.0, 3.8]], dtype=float)
    assert specs['mass'] == 1.0
    assert specs['xmin'] == 0.0
    assert specs['xmax'] == 20.0
    assert specs['npoint'] == 1999
    assert specs['xopt'] == (0.0, 20.0, 1999)
    assert specs['first_ev'] == 1
    assert specs['last_ev'] == 7
    assert specs['interpoltype'] == "cspline"
    assert specs['interpolnum'] == 12
    assert np.all(specs['interpolxydecs'] == expected_interpolxydecs)


def test_harm_osci():
    """Tests the _read_schrodinger function for the asymetric potential well"""
    datapath = os.path.join(TESTDATADIR, "harm_osci.inp")
    specs = _read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[-1.0, 0.5], [0.0, 0.0], [1.0, 0.5]],
                                       dtype=float)
    assert specs['mass'] == 4.0
    assert specs['xmin'] == -5.0
    assert specs['xmax'] == 5.0
    assert specs['npoint'] == 1999
    assert specs['xopt'] == (-5.0, 5.0, 1999)
    assert specs['first_ev'] == 1
    assert specs['last_ev'] == 5
    assert specs['interpoltype'] == "polynomial"
    assert specs['interpolnum'] == 3
    assert np.all(specs['interpolxydecs'] == expected_interpolxydecs)
