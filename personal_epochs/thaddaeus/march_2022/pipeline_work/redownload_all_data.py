from sunnyhills.pipeline_functions import download, preprocess
import os
from tqdm import tqdm

files = os.listdir('./data/current/processed/lightcurves')
lc_dir = './data/current/processed/better_lightcurves'
downloaded_ids = [i.replace('_lc.pickle', '') for i in files if i!='.gitkeep']

for tic_id in tqdm(downloaded_ids): 
    raw_lc, data_found = download(ticstr=tic_id)

    if data_found: 
        stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=tic_id, outdir=lc_dir) 
