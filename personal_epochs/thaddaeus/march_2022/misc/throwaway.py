def check_load(): 

    import pickle 
    import numpy as np
    with open('./data/current/processed/better_lightcurves/TIC_37777866_lc.pickle', 'rb') as handle:
        content = pickle.load(handle)

        time = content['stitched_lc']['time']
        flux = content['stitched_lc']['flux']

        trend_time = content['stitched_trend']['time']
        trend_flux = content['stitched_trend']['flux']

        raw_time = content['stitched_raw']['time']
        raw_flux = content['stitched_raw']['flux']


        print(time)
        print(raw_flux)

#check_load()

def check_download(tic_id: str = 'TIC_37777866', lc_dir='./data/current/processed/better_lightcurves'): 
    from sunnyhills.pipeline_functions import download, preprocess
    raw_lc, data_found = download(ticstr=tic_id)
                
    if data_found: 
        stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=tic_id, outdir=lc_dir)

check_download()

#check_load()