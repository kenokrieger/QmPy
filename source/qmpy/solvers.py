"""Contains numerical solver routines for the schroedinger equation"""
import numpy as np
from scipy.linalg import eigh_tridiagonal
from qmpy._interpolation import _interpolate


def schroedinger(vals, select_range=None, interpol=False,
                 interpoltype='linear'):
    """
    Solves the 1-dimensional schroedinger equation for given numerical
    values of x-coordinates and the corresponding value of the potential.
    It also supports interpolation of the given data points aswell as settings
    for higher accuracy.

    Args:
        vals (dict): Needed values for computation. Necessary keys are:

            - **mass** (*float*) - The mass of the system.
            - **xcords** (*1darray*) - The xcoordinates corresponding to the
                                       potential values.
            - **potential** (*1darray*) - The values of the potential.

            Optional keys are:

            - **xopt** (*tuple*) - Options for the x-range of the output of
                form ``(xmin, xmax, npoints)``. If vals does not have a key
                named \'xopt\' he range of the xcords-array and 1999 points
                will be used for the interpolation (if interpol is set to
                True).

        select_range (tuple, optional): Indices of the desired eigenvalues as
            tuple ``(ev_min, ev_max)``. Defaults to None meaning all
            eigenvalues are calculated.

        interpol (bool): Interpolate the given data points. Defaults to False.
        
        interpoltype (str, optional): The kind of interpolation to use.
            Accepted options are 'linear', 'cspline' or 'polynomial'. Defaults
            to 'linear'.

    Returns:
        touple: ``(energies, wfuncs, pot)``

            - **energies** (*1darray*) - The energy levels of each
              wavefunction. The entries correspond to the rows in wfuncs.

            - **wfuncs** (*ndarray*) - Array where each row contains the
              numerical value of a computed  normalized wavefunction. Each
              column corresponds to one x-coordinate of the input array.

            - **pot** (*2darray or None*) - The interpolated values of x- and
              y-coordinates. If interpol is set to False None will be returned
              instead.

    """
    if interpol:
        if 'xopt' in vals.keys():
            xopt = vals['xopt']
        else:
            with vals['xcords'] as xx:
                xopt = (xx[0], xx[-1], 1999)

        xint, yint = _interpolate(vals['xcords'], vals['potential'],
                                  xopt, kind=interpoltype)
        pot = np.vstack((xint, yint)).T
    else:
        xint, yint = vals['xcords'], vals['potential']
        pot = None

    energies, wfuncs = _basic_schroedinger(vals['mass'], xint, yint,
                                           select_range=select_range)

    return energies, wfuncs, pot


def calculate_expval(xcoords, wfuncs):
    """
    Calculates the expected values :math:`<x>` for the x-coordinate by
    numerically calculating the integral

    .. math::

       \\int_{x_{min}}^{x_{max}} | \\psi (x) |^2 x dx

    Args:
        xcoords (1darray): Array containing the x-coordinates.

        wfuncs (ndarray): Array containing the wave functions that correspond to
            the x-coordinates.

    Returns:
        1darray: The expected values of the x-coordinate.

    """
    delta = np.abs(xcoords[0] - xcoords[-1]) / (len(xcoords) + 1)
    expval = np.empty((len(wfuncs), ))
    for index, wfunc in enumerate(wfuncs):
        expval[index] = np.sum((wfunc ** 2) * xcoords) * delta

    return expval


def calculate_uncertainty(xcoords, wfuncs):
    """
    Calculates the uncertainity :math:`\\Delta x` defined as

    .. math::

       \\Delta x = \\sqrt{<x^2> - <x>^2}

    for each wavefunction.

    Args:
        xcoords (1darray): Array containing the x-coordinates.

        wfuncs (ndarray): Array containing the wave functions that
            correspond to the x-coordinates

    Returns:
        1darray: The uncertainity of the x-coordinate.

    """
    delta = np.abs(xcoords[0] - xcoords[-1]) / (len(xcoords) + 1)
    expval = calculate_expval(xcoords, wfuncs)
    uncertainty = np.empty((len(wfuncs), ))
    index = 0
    for wfunc, expv in zip(wfuncs, expval):
        expvalsq = np.sum((wfunc ** 2) * (xcoords ** 2)) * delta
        uncertainty[index] = np.sqrt(expvalsq - expv ** 2)
        index += 1

    return uncertainty


def _basic_schroedinger(mass, xcords, potential, select_range=None):
    """
    Solves the 1-dimensional schroedinger equation for given numerical
    values of x-coordinates and the corresponding value of the potential.

    Args:
        mass (float): The mass of the system in atomic units.
        xcords (1darray): X-coordinates corresponding to the potential
            values.
        potential (1darray): Numerical values of the potential.
        select_range (touple): Indices of the desired eigenvalues. Defaults to
            None meaning all eigenvalues are calculated.

    Returns:
        touple: ``(energies, wfuncs)``

            - **energies** (*1darray*) - The energy levels of each
              wavefunction. The entries correspond to the rows in wfuncs.

            - **wfuncs** (*ndarray*) - Array where each row contains the
              numerical value of a computed  normalized wavefunction. Each
              column corresponds to one x-coordinate of the input array.

    """
    delta = np.abs(xcords[0] - xcords[-1]) / (len(xcords) + 1)
    diag = potential + 1 / (mass * delta ** 2)
    offdiag = -1 / (2 * mass * delta ** 2) * np.ones((len(potential) - 1))

    if select_range:
        energies, wfuncs = eigh_tridiagonal(diag, offdiag, select='i',
                                            select_range=select_range)
    else:
        energies, wfuncs = eigh_tridiagonal(diag, offdiag)

    wfuncs = wfuncs.T

    for index, wfunc in enumerate(wfuncs):
        norm = 1 / np.sqrt(np.sum(wfunc ** 2) * delta)
        wfuncs[index, :] = wfunc * norm

    return energies, wfuncs
