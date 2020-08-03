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
    mass, xmin, xmax, nPoint, firstEV, lastEV, interpoltype, interpolnum, interpolxydecs =_read_schrodinger(datapath)
    expected_interpolxydecs = np.array([[-2.0, 0.0], [2.0, 0.0]], dtype=float)
    assert mass == 2.0
    assert xmin == -2.0
    assert xmax == 2.0
    assert nPoint == 1999
    assert firstEV == 1
    assert lastEV == 5
    assert interpoltype == "linear"
    assert interpolnum == 2
    assert np.all(interpolxydecs == expected_interpolxydecs)