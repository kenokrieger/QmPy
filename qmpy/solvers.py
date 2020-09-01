"""Contains numerical solvers for the schroedinger equation"""
import numpy as np
from scipy.linalg import eigh_tridiagonal


def schroedinger(mass, xcords, potential, select_range=None):
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
    delta = np.abs(xcords[0] - xcords[-1]) / len(xcords)
    diag = np.array([1 / (mass * delta ** 2) + V for V in potential])
    offdiag = np.array([-1 / (2 * mass * delta ** 2)] * (len(potential) - 1))

    if select_range:
        energies, wfuncs = eigh_tridiagonal(diag, offdiag, select='i',
                                            select_range=select_range)
    else:
        energies, wfuncs = eigh_tridiagonal(diag, offdiag)

    wfuncs = wfuncs.copy().T

    for index, wfunc in enumerate(wfuncs):
        norm = 1 / np.sqrt(np.sum(wfunc ** 2) * delta)
        wfuncs[index, :] = wfunc * norm

    return energies, wfuncs


def calculate_expval(xcoords, wfuncs):
    """
    Calculates the expected values :math:`<x>` for the x-coordinate by
    numerically calculating the integral

    .. math::

       \\int_{x_{min}}^{x_{max}} | \\psi (x) |^2 x dx

    Args:
        xcoordsarray (1darray): Array containing the x-coordinates
        wfuncsarray (ndarray): Array containing the wave functions that
            correspond to the x-coordinates

    Returns:
        1darray: The expected values of the x-coordinate

    """
    delta = np.abs(xcoords[0] - xcoords[-1]) / len(xcoords)
    expval = np.array([])
    for wfunc in wfuncs:
        expval = np.append(expval, [np.sum((wfunc ** 2) * xcoords) * delta],
                           axis=0)

    return expval


def calculate_uncertainty(xcoords, wfuncs):
    """
    Calculates the uncertainity :math:`\\Delta x` defined as

    .. math::

       \\Delta x = \\sqrt{<x^2> - <x>^2}

    for each wavefunction.

    Args:
        xcoords (1darray): Array containing the x-coordinates
        wfuncs (ndarray): Array containing the wave functions that
            correspond to the x-coordinates

    Returns:
        1darray: The uncertainty of the x-coordinate.

    """
    delta = np.abs(xcoords[0] - xcoords[-1]) / len(xcoords)
    expval = calculate_expval(xcoords, wfuncs)
    uncertainty = np.array([])

    for wfunc, expv in zip(wfuncs, expval):
        expvalsq = np.sum((wfunc ** 2) * (xcoords ** 2)) * delta
        uncertainty = np.append(uncertainty, [np.sqrt(expvalsq - expv ** 2)],
                                axis=0)

    return uncertainty
