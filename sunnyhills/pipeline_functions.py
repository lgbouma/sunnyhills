# cSpell:ignore lightkurve, biweight, cval, dtrdict, detrended
# cSpell: disable

## DATA PROCESSING RELATED ##

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
        data_found: boolean variable telling you if data were found or not 
    '''

    import numpy as np 
    import lightkurve as lk 
    import os 
    import pickle 

    # get the light curve
    data_found = False
    
    '''
    lcset = lk.search_lightcurve(ticstr) # otherwise it'll fail for TIC IDs without 120 second cadence data.
    if len(lcset) > 0:
        lcc = lcset[(lcset.author=='SPOC') & (lcset.exptime.value==120)].download_all()
        data_found = True
    '''

    lcc = lk.search_lightcurve(ticstr.replace('_', ' ')).download_all() # FIX THIS! 
    if len(lcc)>0: 
        data_found = True 

    # select only the two-minute cadence SPOC-reduced data; convert to a list.
    # note that this conversion approach works for any LightCurveCollection
    # returned by lightkurve -- no need to hand-pick the right ones.  the exact
    # condition below says "if the interval is between 119 and 121 seconds,
    # take it".

    if data_found: 
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
        
        if len(raw_list) == 0: 
            data_found = False 

        if data_found: 
            new_raw_list = []

            for lc in raw_list: 
                time = lc.time.value
                flux = lc.pdcsap_flux.value
                qual = lc.quality.value

                # remove non-zero quality flags
                sel = (qual == 0)

                time = time[sel]
                flux = flux[sel]

                not_nan_mask = ~np.isnan(flux)
                time, flux = (time[not_nan_mask], flux[not_nan_mask])

                # normalize around 1
                flux /= np.nanmedian(flux)

                new_raw_list.append({'time':time, 'flux':flux})

            raw_list = new_raw_list 
    
    if data_found: 
        if outdir != 'none': 
            joined = {'raw_list':raw_list}
            outfile = outdir + '/' + ticstr.replace(' ', '_') + '_raw_lc.pickle'
            
            with open(outfile, 'wb') as handle:
                pickle.dump(joined, handle, protocol=pickle.HIGHEST_PROTOCOL)


    if not data_found: 
        raw_list = []

    '''
    if logdir != 'none': 
            logfile = logdir + '/' + ticstr.replace(" ",'_')+'_log.pickle'

            logfile = convert_to_absolute_path(logfile)
            if os.path.exists(logfile): 
                with open(logfile, 'rb') as f: 
                    content = pickle.load(f)
                    content['sectors']=len(raw_list)

            else: 
                content = {'sectors':len(raw_list)}

            with open(logfile, 'wb') as f: 
                    pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)
    '''
    return raw_list, data_found

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
    from wotan import flatten, slide_clip
    from astropy.stats import sigma_clip
    import pickle

    lc_times = np.array([])
    lc_fluxes = np.array([])
    trend_times = np.array([])
    trend_fluxes = np.array([])
    raw_times = np.array([])
    raw_fluxes = np.array([])

    for lc in raw_list:

        time = lc['time']
        flux = lc['flux']

        # remove outliers before local window detrending-- wotan does this before detrend, and sigma clip after detrend 
        clipped_flux = slide_clip(time, flux, window_length=0.5, low=3,
                                  high=2, method='mad', center='median')

        clipped_mask = ~np.isnan(clipped_flux)

        clipped_time = time[clipped_mask]
        clipped_flux = clipped_flux[clipped_mask]

        # see https://wotan.readthedocs.io/en/latest/Usage.html for other
        # possible options.
        flat_flux, trend_flux = flatten(
            clipped_time, clipped_flux, return_trend=True,
            method=dtrdict['method'],
            break_tolerance=dtrdict['break_tolerance'],
            window_length=dtrdict['window_length'],
            cval=dtrdict['cval']
        )

        flat_mean, flat_sigma = (np.nanmean(flat_flux), np.nanstd(flat_flux))

        #_, *bounds = sigma_clip(flat_flux, sigma_lower=10, sigma_upper=1, maxiters=1, masked=False, return_bounds=True) # okay flex LOL

        bounds = [flat_mean-sigma_bounds[0]*flat_sigma, flat_mean+sigma_bounds[1]*flat_sigma] # save these bounds to log file? 

        flat_mask = np.logical_and(flat_flux<bounds[1], flat_flux>bounds[0])

        flat_time = clipped_time[flat_mask]
        flat_flux = flat_flux[flat_mask]

        lc_times = np.concatenate((lc_times, flat_time))
        lc_fluxes = np.concatenate((lc_fluxes, flat_flux))

        trend_times = np.concatenate((trend_times, clipped_time))
        trend_fluxes = np.concatenate((trend_fluxes, trend_flux))

        raw_times = np.concatenate((raw_times, time))
        raw_fluxes = np.concatenate((raw_fluxes, flux))
    
    stitched_lc = {'time':lc_times, 'flux':lc_fluxes}
    stitched_trend = {'time':trend_times, 'flux':trend_fluxes}
    stitched_raw = {'time':raw_times, 'flux':raw_fluxes}

    if outdir != 'none': 
        outfile = outdir+'/'+ticstr.replace(' ','_')+'_lc.pickle'
        joined = {'stitched_lc':stitched_lc, 'stitched_trend':stitched_trend, 'stitched_raw':stitched_raw}
        with open(outfile, 'wb') as handle:
            pickle.dump(joined, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return stitched_lc, stitched_trend, stitched_raw   

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
        data_found: if data was not found during download, returns empty lists for the above three and false for this
    '''

    from sunnyhills.pipeline_functions import download, preprocess # lol troll
    import numpy as np

    raw_list, data_found = download(ticstr=ticstr, logdir=logdir, outdir=outdir) 

    if data_found: 
        stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_list, ticstr=ticstr, outdir=outdir, dtrdict=dtrdict, sigma_bounds=sigma_bounds)

    else: 
        stitched_lc, stitched_trend, stitched_raw = (np.array([]), np.array([]), np.array([]))
    
    return stitched_lc, stitched_trend, stitched_raw, data_found

## PERIOD SEARCH ROUTINES ##

## BLS ##

def run_bls(stitched_lc, 
            bls_params: dict = {'min_per':0.5, 'max_per':15, 
                                'minimum_n_transit':2, 
                                'freq_factor':1,
                                'durations':[0.05, 0.06666666666666668, 
                                             0.08333333333333334, 0.1,
                                             0.11666666666666668, 
                                             0.13333333333333336,
                                             0.15000000000000002, 
                                             0.16666666666666669, 
                                             0.18333333333333335, 0.2], 
                                'objective':'snr'}, 
            compute_stats: bool = True): 

    '''
    args: 
        stitched_lc: list of stitched light curve arrays [time, flux]
        bls_params: params for bls execution. see documentation
        compute_stats: compute statistics on best period/duration combination? default False
    returns: 
        results: the BLS results array 
        bls_model: the BLS model  
        in_transit_mask: mask for the in_transit points. to get not in transit, do ~in_transit_mask
        stats: if compute_stats==True, then the stats on the best period/duration/t0 are returned
    '''

    from astropy.timeseries import BoxLeastSquares
    import numpy as np

    time = stitched_lc['time']
    flux = stitched_lc['flux']

    durations = np.array(bls_params['durations'])
    bls_model = BoxLeastSquares(t=time, y=flux)
    results = bls_model.autopower(durations, frequency_factor=bls_params['freq_factor'], 
                            minimum_period=bls_params['min_per'], 
                            maximum_period=bls_params['max_per'],
                            objective=bls_params['objective'])

    index = np.argmax(results.power)
    period = results.period[index]
    t0 = results.transit_time[index]
    duration = results.duration[index]
    in_transit = bls_model.transit_mask(time, period, 2*duration, t0)
    if compute_stats: 
        stats = bls_model.compute_stats(period, duration, t0)
        return results, bls_model, in_transit, stats

    else: 
        return results, bls_model, in_transit 

def iterative_bls_runner(stitched_lc, 
                     iterations: int=1, 
                     bls_params: dict = {'min_per':0.5, 'max_per':15, 
                                'minimum_n_transit':2, 
                                'freq_factor':1,
                                'durations':[0.05, 0.06666666666666668, 
                                             0.08333333333333334, 0.1,
                                             0.11666666666666668, 
                                             0.13333333333333336,
                                             0.15000000000000002, 
                                             0.16666666666666669, 
                                             0.18333333333333335, 0.2], 
                                'objective':'snr'}, 
                    compute_stats: bool = True): 

    '''
    Args:
        stitched_lc: stitched_lc, per usual  
        iterations: number of times to run the search, can be between 1 and 10 
        bls_params: per usual, dictionary of BLS parameters
        compute_stats: will be set to true by default? 

    Returns: 
        results_dict: dictionary of results from each iteration 
        models_dict: dicitonary of bls models from each iteration
        in_transits_dict: dictionary of in_transit arrays from each iteration
        stats_dict: dictionary of stats from each iteration if compute_stats==True
    '''

    from astropy.timeseries import BoxLeastSquares
    import numpy as np
    import matplotlib.pyplot as plt

    time = stitched_lc['time']
    flux = stitched_lc['flux']

    durations = np.array(bls_params['durations'])

    if iterations < 1:
        iterations = 1
    elif iterations > 10: 
        iterations = 10 

    results_dict = {} 
    models_dict = {} 
    in_transits_dict = {} 
    stats_dict = {} 

    iteration_names = ['first', 'second', 'third', 'fourth',
                       'fifth', 'sixth', 'seventh', 'eigth',
                       'ninth', 'tenth']

    for index in range(iterations):
        iter_name = iteration_names[index] 
        bls_model = BoxLeastSquares(t=time, y=flux)

        results = bls_model.autopower(durations, frequency_factor=bls_params['freq_factor'], 
                                minimum_period=bls_params['min_per'], 
                                maximum_period=bls_params['max_per'],
                                objective=bls_params['objective'])
        
        results_dict[iter_name] = results

        index = np.argmax(results.power)
        period = results.period[index]
        t0 = results.transit_time[index]
        duration = results.duration[index]
        
        in_transit = bls_model.transit_mask(time, period, 2*duration, t0)

        in_transits_dict[iter_name] = in_transit

        models_dict[iter_name] = bls_model

        if compute_stats: 
            stats = bls_model.compute_stats(period, duration, t0)
            stats_dict[iter_name] = stats

        time = time[~in_transit]
        flux = flux[~in_transit]

    if compute_stats: 
        return results_dict, models_dict, in_transits_dict, stats_dict

    else: 
        return results_dict, models_dict, in_transits_dict