# cSpell:ignore lightkurve, biweight, cval, dtrdict, detrended
# cSpell: disable

def download(
    ticstr: str, 
    outdir: str = 'none', 
    logdir: str = 'none'): 
    
    ''' 
    Args:
        outdir: directory where lightcurves will be saved. If not set, data will not be saved. 
        ticstr: e.g., 'TIC 441420236'
        logdir: directory for log file
    Returns: 
        raw_list: list of light curve ojects that mean criteria but have not been processed (i.e. not detrended, normalized, or sigma-clipped) 
    '''

    import numpy as np 
    import lightkurve as lk 
    import os 
    import pickle 
    from sunnyhills.pipeline_functions import convert_to_absolute_path

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

    raw_list = new_raw_list 
    
    if logdir != 'none': 
        logfile = logdir + '/' + ticstr.replace(" ",'_')+'_log.pickle'

        logfile = convert_to_absolute_path(logfile)
        if os.path.exists(logfile): 
            with open(logfile, 'rb') as f: 
                content = pickle.load(f)
                content['sectors']=len(raw_list)

        else: 
            content = {'sectors':raw_list}

        with open(logfile, 'wb') as f: 
                pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)

    if outdir != 'none': 
        joined = {'raw_list':raw_list}
        outfile = outdir + '/' + ticstr.replace(' ', '_') + '_raw_lc.pickle'
        
        outfile = convert_to_absolute_path(outfile)

        with open(outfile, 'wb') as handle:
            pickle.dump(joined, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return raw_list

def preprocess(
    raw_list: list,
    ticstr: str = '',
    outdir: str = "none", 
    dtrdict: dict = {'method':'biweight',
                     'window_length':0.5,
                     'cval':5.0,
                     "break_tolerance":1.0}, 
    sigma_bounds: list = [10, 2]
    ):
    """
    Args:
        raw_list: raw list of light curves; see download() 
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
    import pickle
    from sunnyhills.pipeline_functions import convert_to_absolute_path
    
    lc_list = [] # for detrended and "cleaned" light curves
    trend_list = []

    for lc in raw_list:

        time = lc['time']
        flux = lc['flux']

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

        bounds = [flat_mean-sigma_bounds[0]*flat_sigma, flat_mean+sigma_bounds[1]*flat_sigma] # save these bounds to log file? 

        flat_mask = np.logical_and(flat_flux<bounds[1], flat_flux>bounds[0])

        flat_time = time[flat_mask]
        flat_flux = flat_flux[flat_mask]

        processed_lc = {'time':flat_time, "flux":flat_flux}
        trend_lc = {'time':time, 'flux':trend_flux}

        lc_list.append(processed_lc)
        trend_list.append(trend_lc)

    if outdir != 'none': 
        outfile = outdir+'/'+ticstr.replace(' ','_')+'_lc.pickle'
        joined = {'lc_list':lc_list, 'trend_list':trend_list, 'raw_list':raw_list}
        outfile = convert_to_absolute_path(outfile)
        with open(outfile, 'wb') as handle:
            pickle.dump(joined, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return lc_list, trend_list, raw_list  

def download_and_preprocess(
    ticstr: str = '',
    outdir: str = "none", 
    logdir: str = 'none', 
    dtrdict: dict = {'method':'biweight',
                     'window_length':0.5,
                     'cval':5.0,
                     "break_tolerance":1.0}, 
    sigma_bounds: list = [10, 2]
    ): 
    
    '''
    Args: 
        ticstr: 
        outdir: dir to save light curve to. default is none
        logdir: dir to save log file to. default is none
        dtrdict: detrending dictionary 
        sigma_bounds: bounds for sigma clipping 
        
    Returns: 
        lc_list: list of light curve ojects that have met all criteria, been removed of outliers, normalized, and flattened. 
        trend_list: list of light curve objects with x = time, y = trend
        raw_list: list of the raw light curve objects 
    '''

    from sunnyhills.pipeline_functions import download, preprocess # lol troll

    raw_list = download(ticstr=ticstr, logdir=logdir, outdir=outdir) 

    lc_list, trend_list, raw_list = preprocess(raw_list=raw_list, ticstr=ticstr, outdir=outdir, dtrdict=dtrdict, sigma_bounds=sigma_bounds)

    return lc_list, trend_list, raw_list 

def convert_to_absolute_path(rel_path): 
    import os 
    import platform 
    full_path = os.path.abspath('')
    rel_path = './personal_epochs/thaddaeus/march_2022/misc/log'
    
    sys = platform.system()

    if sys=='Windows': 
        rel_path = rel_path.replace('./', '\\')
        rel_path = rel_path.replace('/', '\\')

    else: 
        rel_path = rel_path[1:]

    break_index = full_path.index('sunnyhills')
    abs_path = full_path[0:break_index+10] + rel_path

    return abs_path 