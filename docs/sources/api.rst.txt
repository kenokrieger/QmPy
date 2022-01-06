#################
API-Documentation
#################

*******
solvers
*******

.. automodule:: solvers
   :members:

Examples
========

    .. code-block:: python

       from qmpy.solvers import schroedinger, calculate_expval, calculate_uncertainty
       from numpy import linspace, zeros

       mass = 2.0
       xcords = linspace(-2, 2, 1999)
       pot = zeros((1999, ))

       vals = {'mass': mass,
               'xcords': xcords,
               'potential': pot}

       # returns the first four energies and wavefunctions
       energies, wfuncs = schroedinger(vals, select_range=(0, 3))

       # calculate the expected value for the x-coordinate for each state
       expvals = calculate_expval(xcoords, wfuncs)

       # calculate the uncertainty of the x-coordinate for each state
       uncs = calculate_uncertainty(xcoords, wfuncs)

********
graphics
********

.. automodule:: graphics
   :members:

Examples
========

    .. code-block:: python

       from qmpy.graphics import qm_plottings

       # directory containing the files potential.dat, energies.dat,
       # wavefuncs.dat, and expvalues.dat.
       datadir = 'myqmdata'

       # plot the data and save the plot as 'my_plot.png'
       qm_plottings(datadir, sname='my_plot.png')