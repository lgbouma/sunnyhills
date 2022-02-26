# cSpell:ignore lightkurve, biweight, cval, dtrdict, detrended

def download_lightcurve(
    ticstr: str,
    outdir: str = "none"
    ):
    """
    Args:
        outdir: directory where lightcurves will be saved. If not set, data will not be saved.  
        ticstr: e.g., 'TIC 441420236'.  will be passed to lightkurve and used
        in naming plots.
    Returns: 
        lightcurve: stitched lightkurve light curve object 
    """

def process_lightcurve(
    raw_time: float,
    raw_flux: float,
    raw_fluxerr: float,
    flare_method: str = 'sigma-clip',
    dtrdict: dict = {'method':'biweight',
                     'window_length':0.5,
                     'cval':5.0,
                     "break_tolerance":1.0}): 

    """
    Args: 
        raw_time: array of the "raw" primitive float time values (in day terms) from a light curve 
        raw_flux: array of the "raw" primitive float flux values from a light curve 
        raw_fluxerr: array of the "raw" primitive float fluxerr values from a light curve 
        flare_method: the string method to use 
        dtrdict: dictionary with keys "window_length", "method", "cval",
            "break_tolerance", or anything else needed by wotan's `flatten`
            call.  These are documented at
            https://wotan.readthedocs.io/en/latest/Usage.html   

    Returns: 
        time: array of the primitive float time values that has been adjusted for quality flags, flares, and detrended
        flux: array of the primitive float flux values that have been normalized, in addition default done for time
        fluxerr: array of the primitive fluxerr values corresponding to the flux values above 
        trend: the removed trend 

        attributes_dict: dictionary of information relevant to the data processing (e.g. number of points remove due to different reasons, etc.)
    
    """