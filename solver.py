#!/usr/bin/env python3
"""
This is an executable script that uses the modules fileio,
_interpolation, graphics, and solvers to solve the Schrodingers
equation and graphicate the results
"""
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

