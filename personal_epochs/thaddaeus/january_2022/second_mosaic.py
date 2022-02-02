def make_plot(tic_id, data_dir): 
    import matplotlib.pyplot as plt
    from astropy.timeseries import LombScargle
    import numpy as np
    import pandas as pd
    import lightkurve as lk


    ### MAKE PLOT
    plt.style.use('./other/aesthetics/science.mplstyle') # set style...should work on all our computers because relative


    mosaic = """
        AAB
        CC.
        DDE
        FFG
        """

    '''
    subplot key: 
        > A: flares annotated on raw light curve
        > B: Flare frequency plot
        > C: flares annotated on other plot (discuss) 
        > D: Light curve with trend highlighted
        > E: tls periodogram 
        > F: detrended light curve with transists plotted (if detected)
        > G: phase folded transit least squares with model 

    '''

    fig = plt.figure(constrained_layout=True, figsize=(12,6))
    ax_dict = fig.subplot_mosaic(mosaic)

    ## FIX WHEN VERONICA IS DONE WITH DETRENDING! ADD FOR DIFFERENT STARS!!!
    '''remove'''
    import numpy
    import scipy
    import lightkurve as lk
    
    search_result = lk.search_lightcurve('Kepler-69', author='Kepler', cadence='long')
   
    lc_collection = search_result.download_all()

    lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()

    t = lc.time.value
    flux = lc.flux.value
    flux_err = lc.flux_err.value
    '''remove'''

    from transitleastsquares import transitleastsquares
    
    model = transitleastsquares(t, flux)
    results = model.power(oversampling_factor=5, duration_grid_step=1.02)

    ax = ax_dict['E']

    # examples of using axes
    ax.set(xlabel='', ylabel='', xlim=(0,1))
    # or individually
    ax.set_xlim(0,1)
    ax.scatter([1], [1])

    plt.show()

make_plot('', '')
