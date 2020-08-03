"""Uses routines from scipy.interpolate to interpolate given data sets"""
from scipy.interpolate import interp1d, CubicSpline, KroghInterpolator
from numpy import linspace


def _interpolate(x, y, xopt, kind='linear'):
    """
    Interpolates two given sets of data points by either linear, natural
    cubic spline or polynomial interpolation and returns an array of x-, and
    y-values according to the specified intervall.
    
    Args:
        x (1darray): X-coordinates sorted in increasing order.
        y (1darray): Corresponding y-coordinates.
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
        msg = 'Invalid option {} for  interpolation, using default'
        print(msg.format(kind))
        kind = 'linear'
        
    if kind == 'linear':
        intfunc = _linear(x, y)
    elif kind == 'cspline':
        intfunc = _cspline(x, y)
    else:
        intfunc = _poly(x, y)
    
    xint = _genx(xopt)
    yint = _geny(xint, intfunc)
    return xint, yint


def _linear(x, y):
    """
    Uses linear interpolation to find a function matching a dataset.
    
    Args:
        x (1darray): X-coordinates sorted in increasing order.
        y (1darray): Corresponding y-coordinates.
        
    Returns:
        intfunc (function object): The interpolated function.
    
    """
    intfunc = interp1d(x, y)
    return intfunc


def _cspline(x, y)
    """
    Uses natural cubic spline interpolation to find a function matching
    a dataset.
    
    Args:
        x (1darray): X-coordinates sorted in increasing order.
        y (1darray): Corresponding y-coordinates.
        
    Returns:
        intfunc (PPoly): The interpolated function.    
        
    """
    infunc = CubicSpline(x, y)
    return intfunc


def _poly(x, y)
    """
    Uses polynomial interpolation to find a function matching
    a dataset.
    
    Args:
        x (1darray): X-coordinates sorted in increasing order.
        y (1darray): Corresponding y-coordinates.
        
    Returns:
        intfunc (PPoly): The interpolated function.    
        
    """
    infunc = KroghInterpolator(x, y)
    return intfunc    


def _genx(xopt):
    """
    Generates an array of x-values matching the given minimum and maximum
    value.
    
    Args:
        xopt (touple): Touple of form (xmin, xmax, points) where xmax is
            always excluded. 
            
    Returns:
        x (array): Array ranging from xmin to xmax of shape (points,)
    
    """
    xmin, xmax, points = xopt
    x = linspace(xmin, xmax, points)
    return x
    
    
def _geny(x, func):
    """
    Generates an array containing y-values corresponding to given x-coordinates
    by using a function y = f(x).
    
    Args:
        x (1darray): Array containing the x-values for which matching 
            y-values shall be computed.
        func (callable object): The function used to generate the data.
        
    Returns:
        y (1darray): Array containing y-values matching the supplied
            x-coordinates.
    
    """
    y = func(x)
    return y
    
    
    
    
