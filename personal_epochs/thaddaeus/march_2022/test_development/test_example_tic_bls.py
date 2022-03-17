def test_download_lc_and_read_it_from_pickle(ticstr: str = 'TIC_173103335'): 
    '''
    Purpose: tests if you can download an object for which tess 2 min data exists, process the data, save the processed data to local file
             then tests if you can read the data and confirms all the subarrays of time and flux in the sub-dicts are plain numpy arrays
    '''
    
    
    from sunnyhills.pipeline_functions import download, preprocess 
    import pickle 
    import os

    raw_lc, data_found = download(ticstr=ticstr)

    verdict = True 

    if data_found: 
        stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=ticstr, outdir='.') 

        try: 
            lc_file = './'+ticstr+'_lc.pickle'
            with open(lc_file, 'rb') as handle:
                content = pickle.load(handle)

                time = content['stitched_lc']['time']
                flux = content['stitched_lc']['flux']

                trend_time = content['stitched_trend']['time']
                trend_flux = content['stitched_trend']['flux']

                raw_time = content['stitched_raw']['time']
                raw_flux = content['stitched_raw']['flux']

                # this checks if they're all the same data type ... for a bit before this there were errors because 
                # the raw lc was saving as a masked numpy array object from astropy 
                print(verdict)
                content_list = [time, flux, trend_time, trend_flux, raw_time, raw_flux]
                for arr in content_list: 
                    if not isinstance(arr, type(content_list[0])):
                        verdict = False 
                        break
                        
            os.remove(lc_file)

        except: 
            verdict = False
    else: 
        verdict = False

    assert verdict 

def test_mini_pipeline_to_bls(ticstr: str = 'TIC_173103335', 
                              true_period: float = 10.05556): 
    '''
    Purpose: test if you can download and preprocess lightkurve, then run bls and get correct period for it (within 1% of true, provided period)
    '''
    from sunnyhills.pipeline_functions import download, preprocess, run_bls
    import numpy as np

    raw_lc, data_found = download(ticstr=ticstr)

    print(data_found)

    verdict = False 

    if data_found: 
        stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=ticstr) 
        results, bls_model, in_transit, stats = run_bls(stitched_lc)
        period = results.period[np.argmax(results.power)] 
        print(0.99*true_period, period, 1.01*true_period)
        if 0.99*true_period < period < 1.01*true_period: 
            verdict = True 

    assert verdict 

#test_mini_pipeline_to_bls()
test_download_lc_and_read_it_from_pickle()