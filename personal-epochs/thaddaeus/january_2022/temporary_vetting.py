def make_plot(tic_id, data_dir): 
    import matplotlib.pyplot as plt
    from astropy.timeseries import LombScargle
    import numpy as np
    import pandas as pd
    import lightkurve as lk

    lc_df = pd.read_csv(data_dir+'/TIC '+tic_id+'.CSV')

    ls_df = lc_df[['time', 'flux', 'flux_err']]

    ls_df = ls_df.dropna()

    raw_times = np.array(ls_df['time'])
    raw_fluxes = np.array(ls_df['flux'])
    raw_flux_errs = np.array(ls_df['flux_err'])
    
    light_curve = lk.LightCurve(time=raw_times, flux=raw_fluxes, flux_err=raw_flux_errs)
    light_curve = light_curve.remove_outliers(sigma=3).normalize()

    times = np.array(light_curve.time.value)
    fluxes = np.array(light_curve.flux.value)
    flux_errs = np.array(light_curve.flux_err)

    # FIX to use detrended / clipped lc

    ### MAKE PLOT
    plt.style.use('./other/aesthetics/science.mplstyle') # set style...should work on all our computers because relative


    mosaic = """
        AAB
        CCD
        EEF
        """

    fig = plt.figure(constrained_layout=True, figsize=(12,6))
    ax_dict = fig.subplot_mosaic(mosaic)

    # A is raw light curve
    ax_dict['A'].scatter(raw_times, raw_fluxes, s=3)
    ax_dict['A'].set(xlabel='Time (d)', ylabel='Raw Normalized Flux')

    # to axis one of the subplots, do it like this: ax_dict['A'] (e.g. for subplot A)

    # lomb-periodogram 
    # max frequency = observation window / 3
    # min frequency = ???

    # ls won't work when nans in array 
    
    window_length = np.max(times)-np.min(times)
    periodogram = LombScargle(times, fluxes, flux_errs)

    false_alarm_levels = [0.01]
    faps = periodogram.false_alarm_level(false_alarm_levels)

    frequencies, powers = periodogram.autopower(minimum_frequency=3/window_length, maximum_frequency=10)
    # max freq and min freq 
    periods = 1/frequencies 

    # add FAP and harmonic notation

    ax_dict['D'].plot(periods, powers)
    
    ax_dict['D'].set(xlabel='Period (d)', ylabel='Power')#, yscale='log')

    grey_colors = ['lightgray','darkgray','dimgrey']
    for i in range(len(false_alarm_levels)-1,-1,-1): # Plot them in reverse order so the highest confidence label is 
        #confidence_label = str(100*(1-false_alarm_levels[i]))+'% FAP'
        ax_dict['D'].axhline(y=(faps[i]), xmin=1/10, xmax=window_length/3, color = grey_colors[i],lw=1)
    

    fap_99 = faps[0]
    more_than_fap_mask = np.where(powers>fap_99)
    periods = periods[more_than_fap_mask]
    powers = powers[more_than_fap_mask]

    sorted_indices = np.argsort(powers)[::-1]
    sorted_powers = powers[sorted_indices][0:20]
    sorted_periods = periods[sorted_indices][0:20]

    if len(sorted_periods)>0: 
        best_period = sorted_periods[0] # get period corresponding to highest power
        best_period_power = sorted_powers[0]
    else: 
        best_period = 0

    has_harmonic = False 

    if best_period != 0: 
        for i in range(2,6): 
            lower = best_period/i
            upper = best_period*i

            for test_period in sorted_periods: 
                lower_ratio = lower/test_period
                upper_ratio = test_period/upper

                if 1.01 > lower_ratio > 0.99: 
                    has_harmonic = True
                    ax_dict['D'].axvline(x=lower, ymin=0.8, ymax=1, color='indianred', lw=0.75) # replace with red x line midway through plot
                
                
                
                elif 0.99 < upper_ratio < 1.01: 
                    ax_dict['D'].axvline(x=upper, ymin=0.8, ymax=1, color='indianred', lw=0.75)
                    has_harmonic = True


    # sigma clipped light curve 
    ax_dict['E'].scatter(times, fluxes, s=3)
    ax_dict['E'].set(xlabel='Time (d)', ylabel=r'$\sigma$'+'-clipped Normalized Flux')

    e_xlabel = 'Phase (P='+str(round(best_period,2))+' d)'

    if best_period != 0: 
        phased_dates = np.mod(times, best_period)/best_period # phase the dates
        ax_dict['F'].scatter(phased_dates, fluxes, s=3)
        
    else: 
        e_xlabel = 'Phase (P= nan d)'

    ax_dict['F'].set(xlabel=e_xlabel, ylabel='Normalized Flux (FIX)')


    # metadata to save after each iteration: 
    '''

    Note: end results for the entire iteration should be one .csv with id column and columns for the parameters below, which are populated by row/ID basis  

    LombScargle Related: 
    > top_period
    > top_period_power
    > fap_99 
    > top period has harmonic (True/False)
    
    Flare Related: 
    > 

    '''


    plt.show()

    ## LC MOSAIC KEY FOR NOW 
    """
    A: raw light curve 
    B: flare frequency plot
    C: raw light curve with annotated flares
    D: periodogram with annotated harmonics # detrending is doing weird things
    E: iterative 3 sigma clipped light curve
    F: Phase folded light curve 
    """

lc_dir = './data/LightCurve_keys'
tic_id = '47424873'
make_plot(tic_id, lc_dir)