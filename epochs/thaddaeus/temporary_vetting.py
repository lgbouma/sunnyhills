def make_plot(tic_id, data_dir): 
    import matplotlib.pyplot as plt
    from astropy.timeseries import LombScargle
    import numpy as np
    import pandas as pd

    lc_df = pd.read_csv(data_dir+'/TIC '+tic_id+'.CSV')

    ls_df = lc_df[['time', 'flux', 'flux_err']]

    ls_df = ls_df.dropna()

    times = np.array(ls_df['time'])
    fluxes = np.array(ls_df['flux'])
    mean_flux = np.mean(fluxes)
    fluxes = fluxes/mean_flux
    flux_errs = np.array(ls_df['flux_err'])/mean_flux # FIX NORMALIZATION
    # FIX to use detrended / clipped lc

    ### MAKE PLOT
    plt.style.use('./other/aesthetics/science.mplstyle') # set style...should work on all our computers because relative


    mosaic = """
        AAB
        CCD
        EEF
        """

    fig = plt.figure(constrained_layout=True)
    ax_dict = fig.subplot_mosaic(mosaic)

    # to axis one of the subplots, do it like this: ax_dict['A'] (e.g. for subplot A)

    # lomb-periodogram 
    # max frequency = observation window / 3
    # min frequency = ???

    # ls won't work when nans in array 
    
    window_length = np.max(times)-np.min(times)
    frequencies, powers = LombScargle(times, fluxes, flux_errs).autopower(minimum_frequency=1/window_length, maximum_frequency=10)
    # max freq and min freq 
    periods = 1/frequencies 

    # add FAP and harmonic notation

    ax_dict['D'].plot(periods, powers)
    ax_dict['D'].set(xlabel='Period (d)', ylabel='Power')

    period = periods[np.argmax(powers)] # get period corresponding to highest power
    phased_dates = np.mod(times, period)/period # phase the dates

    ax_dict['F'].scatter(phased_dates, fluxes, s=3)
    ax_dict['F'].set(xlabel='Phase (P='+str(round(period,2))+' d)', ylabel='Normalized Flux (FIX)')


    plt.show()

    ## LC MOSAIC KEY FOR NOW 
    """
    A: raw light curve 
    B: flare flare frequency plot
    C: detrended light curve with annotated flares
    D: periodogram with annotated harmonics
    E: detrended and iterative 3 sigma clipped light curve
    F: Phase folded light curve 
    """

lc_dir = './data/LightCurve_keys'
tic_id = '118807628'
make_plot(tic_id, lc_dir)