#!/usr/bin/env python3
"""Tests for the fileio module"""
from file.io import _read_schrodinger
import numpy as np
import pytest
import os.path

TESTDATADIR = "test_data"

def test_inf_potwell():
    """Tests the _read_schrodinger function for the infinite potential well"""
    datapath = os.path.join(TESTDATADIR, "inf_potwell")
    (mass, xmin, xmax, nPoint, xopt, firstEV, lastEV, interpoltype,
     interpolnum, interpolxydecs) =_read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[-2.0, 0.0], [2.0, 0.0]], dtype=float)
    assert mass == 2.0
    assert xmin == -2.0
    assert xmax == 2.0
    assert nPoint == 1999
    assert xopt == (-2.0, 2.0, 1999)
    assert firstEV == 1
    assert lastEV == 5
    assert interpoltype == "linear"
    assert interpolnum == 2
    assert np.all(interpolxydecs == expected_interpolxydecs)

def test_asym_potwell():
    """Tests the _read_schrodinger function for the asymetric potential well"""
    datapath = os.path.join(TESTDATADIR, "asym_potwell")
    (mass, xmin, xmax, nPoint, xopt, firstEV, lastEV, interpoltype,
     interpolnum, interpolxydecs) =_read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[0.0, 30.0], [1.0, 11.8], [2.0, 1.7],
                                        [3.0, 0.0], [5.0, 0.6], [7.0, 1.6],
                                        [9.0, 2.4], [11.0, 3.0], [13.0, 3.4],
                                        [15.0, 3.6], [19.0, 3.79],
                                        [20.0, 3.8]], dtype=float)
    assert mass == 1.0
    assert xmin == 0.0
    assert xmax == 20.0
    assert nPoint == 1999
    assert xopt == (0.0, 20.0, 1999)
    assert firstEV == 1
    assert lastEV == 7
    assert interpoltype == "cspline"
    assert interpolnum == 12
    assert np.all(interpolxydecs == expected_interpolxydecs)

def test_harm_osci():
    """Tests the _read_schrodinger function for the asymetric potential well"""
    datapath = os.path.join(TESTDATADIR, "asym_potwell")
    (mass, xmin, xmax, nPoint, xopt, firstEV, lastEV, interpoltype,
     interpolnum, interpolxydecs) =_read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[-1.0, 0.5], [0.0, 0.0], [1.0, 0.5]],
                                        dtype=float)
    assert mass == 4.0
    assert xmin == -5.0
    assert xmax == 5.0
    assert nPoint == 1999
    assert xopt == (-5.0, 5.0, 1999)
    assert firstEV == 1
    assert lastEV == 5
    assert interpoltype == "polynomial"
    assert interpolnum == 3
    assert np.all(interpolxydecs == expected_interpolxydecs)