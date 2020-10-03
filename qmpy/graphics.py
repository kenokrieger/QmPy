""" Contains functions for plotting the potential, the eigenvalues and the
    respective wave functions as well as the expected values of the
    x-coordinate for each eigenvalue, using the data from the files that
    contain the solution of the problem.
"""
import os
import matplotlib.pyplot as plt
from qmpy._fileio import _readplotsfiles


def qm_plottings(dirname, auto_scale=True, scale=None, xlim=None, ylim=None,
                 sname='qmpy_plot.pdf'):
    """
    Plots the potential, the eigenvalues and the respective
    wave functions as well as the expected values for each eigenvalue,
    using the data from the files that contain the solution of the problem.

    Args:
        dirname(str): Name of the directory or path from which
            the files are going to be plotted. The directory must have
            the four following files: potential.dat, energies.dat,
            wavefuncs.dat, and expvalues.dat.
        auto_scale (bool): Automatically scale the wavefunctions. Defaults to
            True.
        scale (float): Manually set a value for the scale factor. Defaults to
            None.
        xlim (tuple): The limits for the x-axis as a tuple ```(xmin, xmamx)```.
        ylim (tuple): The limits for the y-axis as a tuple ```(ymin, ymax)```.
        sname (str): The name for the file to save the plot to. Defaults to
            'qmpy_plot.pdf'.

    Return:
        touple: The figure and axes of the plot. Where ax1 is the left and
        ax2 is the right subplot.

    """
    plot_data = _isolate_plot_data(dirname)
    fig = plt.figure(1)
    title = r'Potential, eigenstates, $ \langle x \rangle $'
    ax1 = _make_subplot(fig, 121, title)
    _plot_pot(ax1, plot_data)

    if scale is None:
        scale = 1
        if auto_scale:
            scale = _compscale(plot_data)

    auto_xlim, auto_ylim = _findlims(plot_data, scale)

    if xlim is None:
        xlim = auto_xlim
    if ylim is None:
        ylim = auto_ylim

    _plot_wfuncs(ax1, plot_data, scale)
    _plot_expvals(ax1, plot_data)
    ax1.set(xlim=xlim, ylim=ylim)

    title = r'$\sigma_{x}$'
    ax2 = _make_subplot(fig, 122, title)
    # set a custom label for the x-axis
    ax2.set_xlabel(r'$\sigma_x$ [Bohr]')
    _plot_unc(ax2, plot_data)
    ax2.set(ylim=ylim)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(sname)
    plt.show()

    return fig, ax1, ax2


def _isolate_plot_data(dirname):
    """ Isolates the necessary data to plot the potential, the eigenvalues
    and the respective wave functions as well as the expected values
    for each eigenvalue

    Args:
        dirname (str): Name of the directory or path from which
        the files are going to be plotted. The directory must contain
        the four following files: potential.dat, energies.dat,
        wavefuncs.dat, and expvalues.dat.

    Return:
        plot_data: Dictionary that contains the extracted  data.

            - **xcoords** (*1darray*) - The x-coordinates

            - **pots** (*1darray*) - The numerical values of the potential

            - **energies** (*ndarray*) - The different energy levels

            - **wfuncs** (*ndarray*) - The wavefunctions where each column
                contains the numerical values of one wavefunction.

            - **expvals** (*1darray*) - The expected values for the
                x-coordinate for each state.

            - **uncertainties** (*1darray*) - The uncertainties of the
                x-coordinate for each state.

    """
    potdata, energdata, wfuncsdata, expvaldata = _readplotsfiles(dirname)
    plot_data = dict()
    plot_data['xcoords'] = potdata[:, 0].copy()
    plot_data['pots'] = potdata[:, 1].copy()
    plot_data['energies'] = energdata
    plot_data['wfuncs'] = wfuncsdata[:, 1:].copy()
    plot_data['expvals'] = expvaldata[:, 0].copy()
    plot_data['uncertainties'] = expvaldata[:, 1].copy()

    return plot_data


def _make_subplot(fig, subplotnum, title):
    """
    Generates a subplot on the given figure.

    Args:
        fig (matplotlib.Figure): The figure to add the subplot to.
        subplotnum (int): The options for the subplot. Needs to have 3 digits
            where the first digit stands for the total number of rows, the
            second for the number of columns and the third is the index for
            the subplot.
        title (str): The title for the plot.

    Returns:
        ax (matplotlib.Axes): The generated subplot object.

    """
    ax = fig.add_subplot(subplotnum)
    ax.set_xlabel("x [Bohr]")
    ax.set_ylabel("Energy [Hartree]")
    ax.set_title(title)
    return ax


def _plot_expvals(ax, data):
    """
    Adds the expected values for the x-coordinate to a given subplot.

    Args:
        ax (matplotlib.Axes): The subplot to plot to.
        data (dict): The data to plot.

    Returns:
        None.

    """
    xrange = (data['xcoords'][0], data['xcoords'][-1])
    ax.hlines(data['energies'], xrange[0], xrange[-1], color='grey', alpha=.5)
    ax.scatter(data['expvals'], data['energies'], color="green", marker="x")


def _plot_pot(ax, data):
    """
    Plots the values of the potential to a given subplot.

    Args:
        ax (matplotlib.Axes): The subplot to plot to.
        data (dict): The data to plot.

    Returns:
        None.

    """
    ax.plot(data['xcoords'], data['pots'], color="black")


def _plot_unc(ax, data):
    """
    Plots the uncertainity of the x-coordinate to a given subplot.

    Args:
        ax (matplotlib.Axes): The subplot to plot to.
        data (dict): The data to plot.

    Returns:
        None.

    """
    uncs = data['uncertainties']
    xrange = (min(uncs) - 0.5, max(uncs) + 0.5)
    ax.hlines(data['energies'], xrange[0], xrange[-1], color='grey', alpha=.5)
    ax.scatter(data['uncertainties'], data['energies'],
               color="purple", marker="+")
    ax.set(xlim=xrange)


def _plot_wfuncs(ax, data, scale):
    """
    Plots the wavefunctions and energy levels contained in data and applies
    the given scale.

    Args:
        ax (matplotlib.Axes): The subplot to plot to.
        data (dict): The data needed for the plot. Needs to have keys
            'xcoords', 'wfuncs', 'energies'.

    Returns:
        None.

    """
    _ii = 0
    for wfunc, energy in zip(data['wfuncs'].T, data['energies']):
        offsetwfunc = scale * wfunc + energy
        if _ii % 2 == 0:
            ax.plot(data['xcoords'], offsetwfunc, color="red")
        else:
            ax.plot(data['xcoords'], offsetwfunc, color="blue")
        _ii += 1


def _compscale(data):
    """
    Automatically computes a scaling for the wavefunctions in the plot.

    Args:
        data (dict): The data neccesarry for computing the scale factor. Needs
            to contain 'wfuncs' and 'energies'.

    Returns:
        scale (float): The computed scale.

    """
    wfuncs = data['wfuncs'].T
    energies = data['energies']
    scale = 1e6  # choose an arbitray large number

    for index in range(len(energies) - 1):
        new_scale = (energies[index + 1] - energies[index]) / (
            abs(min(wfuncs[index + 1])) + max(wfuncs[index]))
        if new_scale < scale:
            scale = new_scale

    return scale


def _findlims(data, scale):
    """
    Analyses the energy levels and wavefunctions to calculate axis-limits
    for the plot.

    Args:
        data (dict): The data containing x-coordinates, wavefunctions and
            energy levels. Needs to have keys 'xcoords', 'wfuncs', 'energies'.
        scale (float): The scale that will be applied to the wavefunctions.

    Returns:
        touple: The limits for the x- and y-axis.

    """
    energies, wfuncs = data['energies'], data['wfuncs'].T
    minval = min(scale * wfuncs[0] + energies[0])
    maxval = max(scale * wfuncs[-1] + energies[-1])
    extraspace = (maxval - minval) / 10
    xlim = (data['xcoords'][0], data['xcoords'][-1])
    ylim = (minval - extraspace, maxval + extraspace)

    return xlim, ylim
