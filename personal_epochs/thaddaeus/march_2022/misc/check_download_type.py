import lightkurve as lk 
import numpy as np 

lc_list =lk.search_lightcurve('TIC 345324572').download_all()

time, flux = 2*[np.array([])]

for lc in lc_list: 
    if lc.FLUX_ORIGIN=='pdcsap_flux': 
        if np.isclose(
                    120,
                    np.nanmedian(np.diff(lc.remove_outliers().time.value))*24*60*60,
                    atol=1
                ): 
                time = np.concatenate((time, lc.time))
                #flux = np.concatenate((flux, lc.PDCSAP_FLUX))
                #print(lc.time.value, type(lc.time.value))
                print(lc.PDCSAP_FLUX['flux'], type(lc.PDCSAP_FLUX))
                print(lc.flux)
                #print(lc.keys())
