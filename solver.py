#!/usr/bin/env python3
"""
This is an executable script that uses the modules fileio,
_interpolation, graphics, and solvers to solve the Schrodingers
equation and graphicate the results
"""
import qmpy
import numpy as np

def schrodingers_solver(schrodingers_path):
    """Solves the 1D Schrodinger's time-independent equation
    for any type of Potential and graphicates its solution.
    It needs an input file named schrodinger.inp with the data
    needed to solve the equation.

    Args:
        schrodingers_path: Path or directory of the schrodinger.inp
        file which needs to have following format:
            (float) # mass
            (float) (float) (int) # xMin xMax nPoint
            (int) (int) # first and last eigenvalue to print
            (str(can be linear, polynomial, or cspline)) # interpolation type
            (int) # nr. of interpolation points and xy declarations
            (float) (float) ...
            ...
    Example:
        2.0 # mass
        -2.0 2.0 1999 # xMin xMax nPoint
        1 5 # first and last eigenvalue to print
        linear # interpolation type
        2 # nr. of interpolation points and xy declarations
        -2.0 0.0
        2.0 0.0
    Returns:

    """
    # Read Schrodinger.inp
    specs = qmpy._read_schrodinger(schrodingers_path)
    # Generate xx and yy arrays
    xx = qmpy._interpolation.genx(specs['xopt'])
    yy = qmpy._interpolation.geny(xx, specs['interpoltype'])
    # Interpolate to get the x coords and the Potential
    xint, pots = qmpy._interpolation._interpolate(xx, yy, specs['xopt'],
                                                  specs['interpoltype'])
    # Calculate the energies and wave functions
    energies, wfuncs = qmpy.solvers.schroedinger(specs['mass'], xint, pots)
    # Calculate the expected values for x and the uncertainities
    expvals = qmpy.solvers.calculate_expval(xint, wfuncs, specs['xmin'],
                                           specs['xmax'], specs['npoint'])
    uncertainities = qmpy.solvers.calculate_uncertainity(xint, wfuncs,
                                                       specs['xmin'],
                                                       specs['xmax'],
                                                       specs['npoint'])
    # Make an array out of expvals and uncertainities
    expvallist = (expvals, uncertainities)
    expvaldata = np.array(expvallist)
    # Write the calculated data in an output file
    qmpy.fileio.write_data(schrodingers_path, pots, energies, wfuncs,
                           expvaldata)
    # Graphicate the results of the equation
    qmpy.graphics.qm_plottings(schrodingers_path)
