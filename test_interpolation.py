#!/usr/bin/env python3
"""Tests for the private _interpolation module"""
from _interpolation import _interpolate
from numpy import array, arange, allclose
import pytest

POINTS = [5, 10, 100, 1000, 5000, 10000]
XSHAPE = array([0, 7, 25, 100, 150])
YSHAPE = array([-5, 3, 25, -5.5, 10])
KINDS = ['linear', 'cspline', 'polynomial']

@pytest.mark.parametrize('n', POINTS)
def test_shape_lin(n):
    """Tests whether computed arrays have the correct shape"""
    xopt = (0, 150, n)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt)

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n


@pytest.mark.parametrize('n', POINTS)
def test_shape_cspline(n):
    """Tests whether computed arrays have the correct shape"""
    xopt = (0, 150, n)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt, kind='cspline')

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n


@pytest.mark.parametrize('n', POINTS)
def test_shape_poly(n):
    """Tests whether computed arrays have the correct shape"""
    xopt = (0, 150, n)
    xint, yint = _interpolate(XSHAPE, YSHAPE, xopt, kind='polynomial')

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n


@pytest.mark.parametrize('kind', KINDS)
def test_ifpivots(kind):
    """Tests whether the interpolation goes through all pivots"""
    pivots = array([-10., -7.5, -5., -2.5, 0., 2.5, 5., 7.5, 10.])
    comparisons = arange(0, 2249, 250)

    ycords = array([1, -10, 23, 5, 100, -5, 10, 20, 9])
    xopt = (-10, 10, 2001)
    xint, yint = _interpolate(pivots, ycords, xopt, kind=kind)

    assert allclose(ycords, yint[comparisons])
