def plot_star_detrending(
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
    import numpy as np
    import matplotlib.pyplot as plt

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

    plt.show()

plot_star_detrending('TIC 441420236')

print('test')