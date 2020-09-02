#!/usr/bin/env python3
"""
This is an executable script that uses the modules fileio,
_interpolation, graphics, and solvers to solve the Schrodingers
equation and graphicate the results
"""

import argparse
import os
import numpy as np
import qmpy

_DESCRIPTON = 'Solves the Schrodinger equation and graphicates its results'
PARSER = argparse.ArgumentParser(description=_DESCRIPTON)
MSG = "Input directory"
PARSER.add_argument('-i', '--idirectory', default='.', help=MSG)
MSG = "Output directory"
PARSER.add_argument('-o', '--odirectory', default='.', help=MSG)
MSG = "Scale factor for the wave functions"
PARSER.add_argument('-s', '--sfactor', default=None, help=MSG)
ARGS = PARSER.parse_args()
# Also necessary to add parsers for the range of the plots, this also needs to
# be added to the graphics module

def schrodingers_solver():
    """Solves the 1D Schrodinger's time-independent equation
    for any type of potential and graphicates its solution. The
    output graphs are shown on screen after executing the program and
    the data generated by solving the Schrodinger's equation is written
    in a series of output files (potentials.dat, energies.dat, wavefuncs.dat,
    and expvalues.dat). It needs an input file named schrodinger.inp with
    the data needed to solve the equation.Path or directory of the schrodinger.inp
    file which needs to have following format:
        (float) # mass
        (float) (float) (int) # xMin xMax nPoint
        (int) (int) # first and last eigenvalue to print
        (str(can be linear, polynomial, or cspline)) # interpolation type
        (int) # nr. of interpolation points and xy declarations
        (float) (float)
        ...
    Example:
        2.0 # mass
        -2.0 2.0 1999 # xMin xMax nPoint
        1 5 # first and last eigenvalue to print
        linear # interpolation type
        2 # nr. of interpolation points and xy declarations
        -2.0 0.0
        2.0 0.0
    """
    ipath = ARGS.idirectory
    opath = ARGS.odirectory
    schrodingers_path = os.path.join(ipath, "schrodinger.inp")
    specs = qmpy._fileio._read_schrodinger(schrodingers_path) #pylint : disable=W0212
    xx = qmpy._interpolation._genx(specs['xopt'])
    yy = qmpy._interpolation._geny(xx, specs['interpoltype']) # Not sure if funcs is specs['interpoltype']
    xint, pots = qmpy._interpolation._interpolate(xx, yy, specs['xopt'],
                                                  specs['interpoltype'])
    energies, wfuncs = qmpy.solvers.schroedinger(specs['mass'], xint, pots)
    expvals = qmpy.solvers.calculate_expval(xint, wfuncs)
    uncertainities = qmpy.solvers.calculate_uncertainity(xint, wfuncs)
    expvallist = (expvals, uncertainities)
    expvaldata = np.array(expvallist)
    qmpy._fileio._write_data(opath, pots, energies, wfuncs,
                             expvaldata)
    qmpy.graphics.qm_plottings(opath, auto_scale, ARGS.sfactor, sname)

if __name__ == "_main_":
    schrodingers_solver()
