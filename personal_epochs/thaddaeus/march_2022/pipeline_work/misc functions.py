def mask_transit(
    lc_dict : dict, 
    transit_dict : dict = {'period':1, 
                           'duration':1, 
                           'T0':1}, 
): 
    '''
    Args
        lc_dict: the light curve dictionary (time, flux) to mask 
        transit_dict: dictionary of the values needed to mask out the transit 
    Returns: 
        lc_dict: the light curve dictionary (time, flux) with the given transit masked out 
        trend_dict: the transit dict (time, flux) with the trend as flux 
    '''

    from wotan import transit_mask, flatten

    time = lc_dict['time']
    flux = lc_dict['flux']
    
    mask = transit_mask(
        time=time,
        period=transit_dict['period'],
        duration=transit_dict['duration'],
        T0=transit_dict['T0'])
    
    flatten_lc, trend_lc = flatten(
        time,
        flux,
        method='cosine',
        window_length=0.5,
        return_trend=True,
        robust=True,
        mask=mask
        )

    lc_dict = {'time':time, 'flux':flatten_lc}
    trend_dict = {'time':time, 'flux':trend_lc}

    return lc_dict, trend_dict

def plot_lightcurve(
    lc_list,
    trend_list,
    raw_list, 
    ticstr:str = '',
    outdir:str = 'none' 
): 
    """
    Args:
        ticstr: ticid, e.g. TIC 441420236
        lc_list: list of light curve objects from NASA Ames 
        lc_list: list of light curve ojects that have met all criteria, been removed of outliers, normalized, and flattened. 
        trend_list: list of light curve objects with x = time, y = trend
        raw_list: list of the raw light curve objects 
        outdir: directory into which plots should be saved. None are saved if set to default

    Returns: 

    """

    import numpy as np
    import matplotlib.pyplot as plt

    #plt.style.use('/.other/aesthetics/science.mplstyle')

    # how many sectors of 2-minute cadence TESS data (processed by the Ames
    # group) are available for this object?

    N_sectors = len(lc_list)

    fig, axs = plt.subplots(nrows=2*N_sectors, ncols=1, figsize=(12,4*N_sectors), sharey=True)

    fig.tight_layout()

    for ix in range(N_sectors):

        lc = lc_list[ix]
        trend_lc = trend_list[ix]
        raw_lc = raw_list[ix]

        # top axis: the data and model
        axs[2*ix].scatter(raw_lc['time'], raw_lc['flux'], s=1, c='black', zorder=2)
        axs[2*ix].plot(trend_lc['time'], trend_lc['flux'], lw=1, c='red',alpha=0.6, zorder=3)

        # bottom axis: the residual
        axs[2*ix+1].scatter(lc['time'], lc['flux'], s=1, c='black', zorder=2)

    if outdir=='show': 
        plt.show()
    
    elif outdir!='none': 
        plt.savefig(outdir+'/'+ticstr+'.png', bbox_inches='tight')

    plt.clf()
    #plt.close()

def bls_plot(lc_dict): 
    '''
    Args
        lc_list: 
    Returns: 
    '''

    import matplotlib.pyplot as plt
    from astropy.timeseries import BoxLeastSquares
    import numpy as np

    time = lc_dict['time']
    flux = lc_dict['flux']

    t = np.random.uniform(5,7, 1000)
    model = BoxLeastSquares(t, flux)
    periodogram = model.autopower(0.2, objective='snr')

    periodogram.plot()
    
