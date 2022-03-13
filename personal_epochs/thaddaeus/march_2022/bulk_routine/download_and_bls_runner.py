def run_bulk_download_and_bls(
    key: str = './data/current/current_key.csv', 
    lc_out_dir: str = './data/current/processed/lightcurves', 
    results_file: str = './personal_epochs/thaddaeus/march_2022/bulk_routine/.gitkeep'): 

    import numpy as np 
    import pandas as pd 
    from sunnyhills.pipeline_functions import download, preprocess, run_bls
    from tqdm import tqdm 

    df = pd.read_csv(key)

    tic_ids = np.array(df['TIC_ID'])

    cols = ['TIC_ID', 'power', 'period', 't0', 'duration', 'depth']
    with open(results_file, 'w') as f: 
        f.write(','.join(cols)+'\n')

    for tic_id in tqdm(tic_ids):
        try: 
            raw_lc, data_found = download(tic_str=tic_id)
            if data_found: 
                stitched_lc, stitched_trend, stitched_raw = preprocess(ticstr=tic_id, outdir=lc_out_dir)
                results, bls_model, in_transit, stats = run_bls(stitched_lc)

                with open(results_file, 'a') as f: 
                    index = np.argmax(results.power)
                    out_list = [tic_id, results.power[index], results.period[index]]
                    out_list += [results.transit_time[index], results.duration[index]]
                    out_list += [stats['depth']]
                    out_str = ','.join([str(i) for i in out_list])
                    results_file.write(out_str+'\n')
        except: 
            continue 
    
        break 

run_bulk_download_and_bls()