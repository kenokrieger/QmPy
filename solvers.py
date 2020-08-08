"""Contains numerical solvers for the schroedinger equation"""
import numpy as np
from scipy.linalg import eigh_tridiagonal


def schroedinger(mass, xcords, potential):
    """
    Solves the 1-dimensional schroedinger equation for given numerical
    values of a potential.

    Args:

        mass (float): The mass of the system in atomic units.
        xcords (1darray): X-coordinates corresponding to the potential
            values.
        potential (1darray): Numerical values of the potential.

    Returns:
        touple: ``energies, wfuncs``

            - **energies** (*1darray*) - The energy levels of each wavefunctions.
              The entries correspond to the rows in wfuncs.

            - **wfuncs** (*ndarray*) - Array where each row contains the numerical
              value of a computed wavefunction. Each column corresponds to one
              x-coordinate of the input array.

    Examples:


    """
    step = np.abs(xcords[0] - xcords[-1]) / len(xcords)
    diag = np.array([1 / (mass * step ** 2) + V for V in potential])
    offdiag = np.array([-1 / (2 * mass * step ** 2)] * (len(potential) - 1))

    energies, wfuncs = eigh_tridiagonal(diag, offdiag)

    return energies, wfuncs


def calculate_expval(xcoordsarray, wfuncsarray, xmin, xmax, npoints):
    """
    Calculates the expected values for the x-coordinate

    Args:
        xcoordsarray (1darray): Array containing the x-coordinates
        wfuncsarray (ndarray): Array containing the wave functions that
        correspond to the x-coordinates
        xmin (float): Minimal value of the x-axis
        xmax (float): Maximal value of the x-axis
        npoints (int): Number of points in the interval [xmin, xmax]
    Returns:
        expval (1darray): The expected values of the x-coordinate
    """
    delta = np.abs(xmin-xmax)/npoints
    summation = 0
    expvalxlist = list()
    for rows in range(0, len(xcoordsarray)):
        for cols in range(0, len(wfuncsarray[0])):
            summation += (wfuncsarray[rows, cols] * xcoordsarray[cols]
                          * wfuncsarray[rows, cols])
        expvalx = delta * summation
        expvalxlist.append(expvalx)
    expval = np.array(expvalxlist)
    return expval


def calculate_uncertainity(xcoordsarray, wfuncsarray, xmin, xmax, npoints):
    """
    Calculates the uncertainity (which is the square root of the expected
    value of x**2 minus the square of the expected value of x) for
    the x-coordinate

    Args:
        xcoordsarray (1darray): Array containing the x-coordinates
        wfuncsarray (ndarray): Array containing the wave functions that
        correspond to the x-coordinates
        xmin (float): Minimal value of the x-axis
        xmax (float): Maximal value of the x-axis
        npoints (int): Number of points in the interval [xmin, xmax]
    Returns:
        uncertainity (1darray): The expected values of the x-coordinate
    """
    delta = np.abs(xmin-xmax)/npoints
    expvalarray = calculate_expval(xcoordsarray, wfuncsarray, xmin, xmax)
    expvalsqlist = list()
    summation = 0
    for rows in range(0, len(xcoordsarray)):
        for cols in range(0, len(wfuncsarray[0])):
            summation += (wfuncsarray[rows, cols] * (xcoordsarray[cols]**2)
                          * wfuncsarray[rows, cols])
        expvalsq = delta * summation
        expvalsqlist.append(expvalsq)
    expvalsqarray = np.array(expvalsqlist)
    uncertainlist = list()
    for ii in range(len(expvalsqarray)):
        element = np.sqrt(expvalsqarray[ii] - expvalarray[ii]**2)
        uncertainlist.append(element)
    uncertainity = np.array(uncertainlist)
    return uncertainity
