import pickle 
import numpy as np
with open('./data/current/processed/lightcurves/TIC_160329609_lc.pickle', 'rb') as handle:
    content = pickle.load(handle)
    time = content['stitched_lc'][0]['time']
    flux = content['stitched_lc'][0]['flux']

    raw_time = content['stitched_raw'][0]['time']
    raw_flux = content['stitched_raw'][0]['flux']
    
    trend_time = content['stitched_trend'][0]['time']
    trend_flux = content['stitched_trend'][0]['flux']

    print(time)
    print(np.argwhere(np.isnan(flux)))
    print(raw_flux)