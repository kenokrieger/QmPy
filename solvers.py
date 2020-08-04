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
        energies (1darray): The energy levels of each wavefunctions. The
            entries correspond to the rows in wfuncs.
        wfuncs (ndarray): Array where each row contains the numerical value
            of a computed wavefunction. Each column corresponds to one
            x-coordinate of the input array.

    """
    step = np.abs(xcords[0] - xcords[-1]) / len(xcords)
    diag = np.array([1 / (mass * step ** 2) + V for V in potential])
    offdiag = np.array([-1 / (2 * mass * step ** 2)] * (len(potential) - 1))

    energies, wfuncs = eigh_tridiagonal(diag, offdiag)

    return energies, wfuncs
