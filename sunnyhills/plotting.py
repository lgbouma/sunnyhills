"""
Re-useable plotting functions can go in this file.  They can be called using
driver scripts.
"""
import os
from glob import glob
import numpy as np, matplotlib.pyplot as plt, pandas as pd
import matplotlib as mpl

from numpy import array as nparr
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from astropy import units as u, constants as const
from astropy.coordinates import SkyCoord
from astropy.table import Table

from sunnyhills.paths import DATADIR, EPOCHSDIR

def plot_kerr21_XY(outdir, colorkey=None):
    """
    Make a top-down plot like Figure 7 of Kerr+2021
    (https://ui.adsabs.harvard.edu/abs/2021ApJ...917...23K/abstract).

    Optionally color by stellar age, similar to Fig 24 of McBride+2021.
    (https://ui.adsabs.harvard.edu/abs/2021AJ....162..282M/abstract).

    Args:

        outdir (str): path to output directory

        colorkey (str or None): column string from Kerr+2021 table to color
        points by: for instance "Age", "bp-rp", "plx", or "P" (latter means
        "Probability of star being <50 Myr old).
    """

    assert isinstance(outdir, str)
    assert isinstance(colorkey, str) or (colorkey is None)

    #
    # get data, calculate galactic X,Y,Z positions (assuming well-measured
    # parallaxes).
    #
    kerrpath = os.path.join(DATADIR, "Kerr_2021_Table1.txt")
    df = Table.read(kerrpath, format='cds').to_pandas()

    from sunnyhills.physicalpositions import calculate_XYZ_given_RADECPLX
    x,y,z = calculate_XYZ_given_RADECPLX(df.RAdeg, df.DEdeg, df.plx)

    #
    # make the plot
    #
    fig, ax = plt.subplots(figsize=(4,4))

    x_sun, y_sun = -8122, 0
    ax.scatter(
        x_sun, y_sun, c='black', alpha=1, zorder=1, s=20, rasterized=True,
        linewidths=1, marker='x'
    )

    if colorkey is None:
        # By default, just show all the stars as the same color.  The
        # "rasterized=True" kwarg here is good if you save the plots as pdfs,
        # to not need to save the positions of too many points.
        ax.scatter(
            x, y, c='black', alpha=1, zorder=2, s=2, rasterized=True,
            linewidths=0, marker='.'
        )

    else:
        # Add a colorbar.
        color = df[colorkey]

        # Only show points for which color is defined (e.g., not all stars have
        # ages reported in the table).
        sel = ~pd.isnull(color)

        # Define the colormap.  See
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html, there
        # are better choices, but this one is OK for comparing against
        # McBride+21.
        cmap = mpl.cm.get_cmap('rainbow')

        _p = ax.scatter(
            x[sel], y[sel], c=color[sel], alpha=1, zorder=3, s=2, rasterized=True,
            linewidths=0, marker='.', cmap=cmap
        )

        # For the colorbar, inset it into the main plot to keep the square
        # aspect ratio.
        axins1 = inset_axes(ax, width="3%", height="20%", loc='lower right',
                            borderpad=0.7)

        cb = fig.colorbar(_p, cax=axins1, orientation="vertical",
                          extend="neither")
        cb.ax.tick_params(labelsize='x-small')
        cb.ax.yaxis.set_ticks_position('left')
        cb.ax.yaxis.set_label_position('left')

        KEYLABELDICT = {
            'Age': 'Age [years]',
            'P': 'P$_{\mathrm{<50\ Myr}}$',
            'plx': 'Parallax [mas]',
        }
        if colorkey in KEYLABELDICT:
            cb.set_label(KEYLABELDICT[colorkey], fontsize='x-small')
        else:
            cb.set_label(colorkey, fontsize='x-small')

    ax.set_xlabel("X [pc]")
    ax.set_ylabel("Y [pc]")

    s = ''
    if colorkey:
        s += f"_{colorkey}"

    outpath = os.path.join(outdir, f'kerr21_XY{s}.png')
    fig.savefig(outpath, bbox_inches='tight', dpi=400)
    print(f"Made {outpath}")
