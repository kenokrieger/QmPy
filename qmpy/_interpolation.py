"""Uses routines from scipy.interpolate to interpolate given data sets"""
from scipy.interpolate import interp1d, CubicSpline, KroghInterpolator
from numpy import linspace


def _interpolate(xx, yy, xopt, kind='linear'):
    """
    Interpolates two given sets of data points by either linear, natural
    cubic spline or polynomial interpolation and returns an array of x-, and
    y-values according to the specified intervall.

    Args:
        xx (1darray): X-coordinates sorted in increasing order.
        yy (1darray): Corresponding y-coordinates.
        xopt (touple): Options for the generated x-coordinates. Has to be of
            form (xmin, xmax, points).
        kind (str): The kind of interpolation to use. Accepted options are
            'linear', 'cspline' or 'polynomial'. Defaults to 'linear'.

    Returns:
        xint (array): The x-coordinates corresponding the computed
            y-values.
        yint (array): The interpolated y-coordinates.

    """
    legal_choices = ['linear', 'cspline', 'polynomial']
    if kind not in legal_choices:
        msg = """OptionWARNING: Invalid option {} for  interpolation, using
        default. Valid options are {}"""
        print(msg.format(kind, legal_choices))
        kind = 'linear'

    if kind == 'linear':
        intfunc = _linear(xx, yy)
    elif kind == 'cspline':
        intfunc = _cspline(xx, yy)
    else:
        intfunc = _poly(xx, yy)

    xint = _genx(xopt)
    yint = _geny(xint, intfunc)
    return xint, yint


def _linear(xx, yy):
    """
    Uses linear interpolation to find a function matching a dataset.

    Args:
        xx (1darray): X-coordinates sorted in increasing order.
        yy (1darray): Corresponding y-coordinates.

    Returns:
        intfunc (function object): The interpolated function.

    """
    intfunc = interp1d(xx, yy)
    return intfunc


def _cspline(xx, yy):
    """
    Uses natural cubic spline interpolation to find a function matching
    a dataset.

    Args:
        xx (1darray): X-coordinates sorted in increasing order.
        yy (1darray): Corresponding y-coordinates.

    Returns:
        intfunc (PPoly): The interpolated function.

    """
    intfunc = CubicSpline(xx, yy)
    return intfunc


def _poly(xx, yy):
    """
    Uses polynomial interpolation to find a function matching
    a dataset.

    Args:
        xx (1darray): X-coordinates sorted in increasing order.
        yy (1darray): Corresponding y-coordinates.

    Returns:
        intfunc (PPoly): The interpolated function.

    """
    intfunc = KroghInterpolator(xx, yy)
    return intfunc


def _genx(xopt):
    """
    Generates an array of x-values matching the given minimum and maximum
    value.

    Args:
        xopt (touple): Touple of form (xmin, xmax, points) where xmax is
            always excluded.

    Returns:
        xx (array): Array ranging from xmin to xmax of shape (points,)

    """
    xmin, xmax, points = xopt
    xx = linspace(xmin, xmax, points)
    return xx


def _geny(xx, func):
    """
    Generates an array containing y-values corresponding to given x-coordinates
    by using a function y = f(x).

    Args:
        xx (1darray): Array containing the x-values for which matching
            y-values shall be computed.
        func (callable object): The function used to generate the data.

    Returns:
        y (1darray): Array containing y-values matching the supplied
            x-coordinates.

    """
    yy = func(xx)
    return yy
