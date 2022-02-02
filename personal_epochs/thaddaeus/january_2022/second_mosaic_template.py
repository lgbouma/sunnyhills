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

    def identify_axes(ax_dict, fontsize=48):
        kw = dict(ha="center", va="center", fontsize=fontsize, color="darkgrey")
        for k, ax in ax_dict.items():
            ax.text(0.5, 0.5, k, transform=ax.transAxes, **kw)

    


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

    
    
    identify_axes(ax_dict) # comment this out!

    plt.show()

make_plot('', '')
