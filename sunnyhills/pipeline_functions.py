# cSpell:ignore lightkurve, biweight, cval, dtrdict, detrended
# cSpell: disable

def download_and_preprocess(
    ticstr: str,
    outdir: str = "none", 
    dtrdict: dict = {'method':'biweight',
                     'window_length':0.5,
                     'cval':5.0,
                     "break_tolerance":1.0}, 
    sigma_bounds: list = [10, 2]
    ):
    """
    Args:
        outdir: directory where lightcurves will be saved. If not set, data will not be saved.  --> FIX!
        ticstr: e.g., 'TIC 441420236'.  
        dtrdict: dictionary with keys "window_length", "method", "cval",
                 "break_tolerance", or anything else needed by wotan's `flatten`
                 call.  These are documented at
                 https://wotan.readthedocs.io/en/latest/Usage.html 
        sigma_bounds: list of the lower and upper sigma bounds to use for post detrend sigma-clipping 
    Returns: 
        lc_list: list of light curve ojects that have met all criteria, been removed of outliers, normalized, and flattened. 
        trend_list: list of light curve objects with x = time, y = trend
        raw_list: list of the raw light curve objects 
    """

    import numpy as np 
    import lightkurve as lk 
    from wotan import flatten, slide_clip
    from astropy.stats import sigma_clip

    # get the light curve
    lcc = lk.search_lightcurve(ticstr).download_all()

    # select only the two-minute cadence SPOC-reduced data; convert to a list.
    # note that this conversion approach works for any LightCurveCollection
    # returned by lightkurve -- no need to hand-pick the right ones.  the exact
    # condition below says "if the interval is between 119 and 121 seconds,
    # take it".
    raw_list = [_l for _l in lcc
         if
         _l.meta['ORIGIN']=='NASA/Ames'
         and
         np.isclose(
             120,
             np.nanmedian(np.diff(_l.remove_outliers().time.value))*24*60*60,
             atol=1
         )
    ]

    raw_list = [_l for _l in raw_list if _l.meta['FLUX_ORIGIN']=='pdcsap_flux']
    
    lc_list = [] # for detrended and "cleaned" light curves
    trend_list = []

    new_raw_list = []

    for lc in raw_list:

        time = lc.time.value
        flux = lc.pdcsap_flux.value
        qual = lc.quality.value

        # remove non-zero quality flags
        sel = (qual == 0)

        time = time[sel]
        flux = flux[sel]

        # normalize around 1
        flux /= np.nanmedian(flux)

        new_raw_list.append({'time':time, 'flux':flux})

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

        flat_mean, flat_sigma = (np.nanmean(flat_flux), np.nanstd(flat_flux))

        #_, *bounds = sigma_clip(flat_flux, sigma_lower=10, sigma_upper=1, maxiters=1, masked=False, return_bounds=True) # okay flex LOL

        bounds = [flat_mean-sigma_bounds[0]*flat_sigma, flat_mean+sigma_bounds[1]*flat_sigma]

        print(bounds)

        flat_mask = np.logical_and(flat_flux<bounds[1], flat_flux>bounds[0])

        flat_time = time[flat_mask]
        flat_flux = flat_flux[flat_mask]

        processed_lc = {'time':flat_time, "flux":flat_flux}
        trend_lc = {'time':time, 'flux':trend_flux}

        lc_list.append(processed_lc)
        trend_list.append(trend_lc)

    raw_list = new_raw_list 
    # return processed_list, trends_list, raw_list 

    return lc_list, trend_list, raw_list  

#download_and_preprocess('TIC 441420236')

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
    ticstr:str,
    lc_list,
    trend_list,
    raw_list, 
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
    