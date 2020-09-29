#!/usr/bin/env python3
"""Tests for the private _interpolation module"""

from numpy import array, arange, allclose
import pytest
from qmpy._interpolation import _interpolate

POINTS = [5, 10, 100, 1000, 5000, 10000]
XSHAPE = array([0, 7, 25, 100, 150])
YSHAPE = array([-5, 3, 25, -5.5, 10])
KINDS = ['linear', 'cspline', 'polynomial']


@pytest.mark.parametrize('nn', POINTS)
def test_shape_lin(nn):
    """Tests whether computed arrays have the correct shape (linear)"""
    xopt = (0, 150, nn)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt, kind='invalid')

    assert xint.shape[0] == nn and yint.shape[0] == nn


@pytest.mark.parametrize('nn', POINTS)
def test_shape_cspline(nn):
    """Tests whether computed arrays have the correct shape (natural cubical
    spline)"""
    xopt = (0, 150, nn)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt, kind='cspline')

    assert xint.shape[0] == nn and yint.shape[0] == nn


@pytest.mark.parametrize('nn', POINTS)
def test_shape_poly(nn):
    """Tests whether computed arrays have the correct shape (polynomial)"""
    xopt = (0, 150, nn)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt, kind='polynomial')

    assert xint.shape[0] == nn and yint.shape[0] == nn


@pytest.mark.parametrize('kind', KINDS)
def test_ifpivots(kind):
    """Tests whether the interpolation goes through all pivots"""
    pivots = array([-10., -7.5, -5., -2.5, 0., 2.5, 5., 7.5, 10.])
    # indices where the ycords should be located
    comparisons = arange(0, 2249, 250)

    ycords = array([1, -10, 23, 5, 100, -5, 10, 20, 9])
    xopt = (-10, 10, 2001)
    xint, yint = _interpolate(pivots, ycords, xopt, kind=kind)

    assert allclose(ycords, yint[comparisons])
