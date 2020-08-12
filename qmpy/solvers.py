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

    Examples:
        .. code-block::

            import qmpy
            import matplotlib.pyplot as plt
            import numpy as np

            mass = 2.0
            xcords = np.linspace(-2, 2, 1999)
            pot = np.zeros((1999, ))

            energies, wfuncs = qmpy.solvers.schroedinger(mass, xcords, pot,
                                                         select_range=(0, 3))
            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            title = 'First four wavefunctions of the infinite potential well'
            ax.set_title(title, fontsize=20, fontweigt='bold')
            ax.set_xlabel('Location in atomic units')

            for wfunc, energy in zip(wfuncs, energies):
                ax.plot(xcords, 0.7 * wfunc + energy)

            ax.hlines(energies, color='k', alpha=0.7)
            plt.show()

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
        1darray: The expected values of the x-coordinate

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
    Calculates the uncertainity :math:`\\Delta x` defined as

    .. math::

       \\Delta x = \\sqrt{<x^2> - <x>^2}

    for each wavefunction.

    Args:
        xcoordsarray (1darray): Array containing the x-coordinates
        wfuncsarray (ndarray): Array containing the wave functions that
        correspond to the x-coordinates
        xmin (float): Minimal value of the x-axis
        xmax (float): Maximal value of the x-axis
        npoints (int): Number of points in the interval [xmin, xmax]

    Returns:
        1darray: The uncertainty of the x-coordinate.

    """
    delta = np.abs(xmin-xmax)/npoints
    expvalarray = calculate_expval(xcoordsarray, wfuncsarray, xmin, xmax)
    expvalsqlist = list()
    summation = 0
    for rows in range(len(xcoordsarray)):
        for cols in range(len(wfuncsarray[0])):
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