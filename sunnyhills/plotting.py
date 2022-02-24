"""
Re-useable plotting functions can go in this file.  They can be called using
driver scripts.

Contents:
    plot_kerr21_XY
    plot_au_mic_detrending
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


def plot_star_detrending(
    outdir: str,
    ticstr: str,
    dtrdict: dict = {'method':'biweight',
                     'window_length':0.5,
                     'cval':5.0,
                     "break_tolerance":1.0},
    known_ephemeris: dict = None
    ) -> None:
    """
    Args:
        outdir: directory where plots will be written.

        ticstr: e.g., 'TIC 441420236'.  will be passed to lightkurve and used
        in naming plots.

        dtrdict: dictionary with keys "window_length", "method", "cval",
            "break_tolerance", or anything else needed by wotan's `flatten`
            call.  These are documented at
            https://wotan.readthedocs.io/en/latest/Usage.html

    Kwargs:
        known_ephemeris: optional dictionary with keys 't0', 'period', to
        overplot the known transit times.
    """

    import lightkurve as lk
    from wotan import flatten, slide_clip

    plotpath = os.path.join(
        outdir,
        f'{ticstr.replace(" ","_")}_{dtrdict["method"]}_'+
        f'window{dtrdict["window_length"]:.2f}_cval{dtrdict["cval"]:.1f}_'+
        f'breaktol{dtrdict["break_tolerance"]:.1f}.png'
    )
    if os.path.exists(plotpath):
        print(f"Found {plotpath}, skipping.")
        return 1

    # get the light curve
    lcc = lk.search_lightcurve(ticstr).download_all()

    # select only the two-minute cadence SPOC-reduced data; convert to a list.
    # note that this conversion approach works for any LightCurveCollection
    # returned by lightkurve -- no need to hand-pick the right ones.  the exact
    # condition below says "if the interval is between 119 and 121 seconds,
    # take it".
    lc_list = [_l for _l in lcc
         if
         _l.meta['ORIGIN']=='NASA/Ames'
         and
         np.isclose(
             120,
             np.nanmedian(np.diff(_l.remove_outliers().time.value))*24*60*60,
             atol=1
         )
    ]

    # how many sectors of 2-minute cadence TESS data (processed by the Ames
    # group) are available for this object?
    N_sectors = len(lc_list)

    fig, axs = plt.subplots(nrows=2*N_sectors, ncols=1, figsize=(12,4*N_sectors))

    titlestr = os.path.basename(plotpath).replace('.png','').replace('_',' ')
    axs[0].set_title(titlestr, fontsize='small')

    for ix, lc in enumerate(lc_list):

        time = lc.time.value
        flux = lc.pdcsap_flux.value
        qual = lc.quality.value

        # remove non-zero quality flags
        sel = (qual == 0)

        time = time[sel]
        flux = flux[sel]

        # normalize around 1
        flux /= np.nanmedian(flux)

        # remove outliers before local window detrending
        clipped_flux = slide_clip(time, flux, window_length=0.5, low=3,
                                  high=2, method='mad', center='median')

        # see https://wotan.readthedocs.io/en/latest/Usage.html for other
        # possible options.
        flat_flux, trend_flux = flatten(
            time, clipped_flux, return_trend=True,
            method=dtrdict['method'],
            break_tolerance=dtrdict['break_tolerance'],
            window_length=dtrdict['window_length'],
            cval=dtrdict['cval']
        )

        # top axis: the data and model
        axs[2*ix].scatter(time, flux, s=1, c='black', zorder=2)
        axs[2*ix].plot(time, trend_flux, lw=1, c='red',alpha=0.6, zorder=3)

        # bottom axis: the residual
        axs[2*ix+1].scatter(time, flat_flux, s=1, c='black', zorder=2)

    # assume 't0' in known_ephemeris dictionary is given in same time-system as
    # "time".  then make a bunch of vertical lines, but set the x-axis and
    # y-axis limits to hide them.
    for ax in axs:
        if not isinstance(known_ephemeris, dict):
            break
        t0 = known_ephemeris['t0']
        period = known_ephemeris['period']
        epochs = np.arange(-1000,1000,1)
        tra_times = t0 + period*epochs
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        ax.vlines(
            tra_times, ylim[0], ylim[1], colors='darkgray', alpha=0.8,
            linestyles='--', zorder=-2, linewidths=0.5
        )
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    fig.text(-0.01,0.5, 'Relative flux', va='center', rotation=90,
             fontsize='large')
    fig.text(0.5,-0.01, 'Time [BTJD]', va='center', ha='center',
             fontsize='large')

    fig.tight_layout()

    fig.savefig(plotpath, bbox_inches='tight', dpi=400)
    print(f"Made {plotpath}")
