#!/usr/bin/env python3
"""Tests for the private _interpolation module"""
from _interpolation import _interpolate
from numpy import array
import pytest

POINTS = [5, 10, 100, 1000, 5000, 10000]


@pytest.mark.parametrize('n', POINTS)
def test_shape_lin(n):
    """Tests whether computed arrays have the correct shape"""
    x = array([0, 7, 25, 100, 150])
    y = array([-5, 3, 25, -5.5, 10])
    xopt = (0, 150, n)
    xint, yint = _interpolate(x, y, xopt)

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n


@pytest.mark.parametrize('n', POINTS)
def test_shape_csplin(n):
    """Tests whether computed arrays have the correct shape"""
    x = array([0, 7, 25, 100, 150])
    y = array([-5, 3, 25, -5.5, 10])
    xopt = (0, 150, n)
    xint, yint = _interpolate(x, y, xopt, kind='csplin')

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n


@pytest.mark.parametrize('n', POINTS)
def test_shape_poly(n):
    """Tests whether computed arrays have the correct shape"""
    x = array([0, 7, 25, 100, 150])
    y = array([-5, 3, 25, -5.5, 10])
    xopt = (0, 150, n)
    xint, yint = _interpolate(x, y, xopt, kind='polynomial')

    if xint.shape != yint.shape:
        assert xint.shape != yint.shape
    else:
        assert xint.shape[0] == n and yint.shape[0] == n