def run_bulk_download_and_bls(
    key: str = './data/current/current_key.csv', 
    lc_out_dir: str = './data/current/processed/lightcurves', 
    results_file: str = './personal_epochs/thaddaeus/march_2022/bulk_routine/bulk_cursory.csv'): 

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
            raw_lc, data_found = download(ticstr=tic_id)
            if data_found: 
                stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=tic_id, outdir=lc_out_dir)
                results, bls_model, in_transit, stats = run_bls(stitched_lc)
                with open(results_file, 'a') as f: 
                    index = np.argmax(results.power)
                    out_list = [tic_id, results.power[index], results.period[index]]
                    out_list += [results.transit_time[index], results.duration[index]]
                    out_list += [stats['depth'][0]]
                    out_str = ','.join([str(i) for i in out_list])
                    results_file.write(out_str+'\n')
        except: 
            continue  

#run_bulk_download_and_bls()

def run_bulk_download(
    key: str = './data/current/current_key.csv', 
    lc_out_dir: str = './data/current/processed/better_lightcurves', 
    results_file: str = './personal_epochs/thaddaeus/march_2022/bulk_routine/bulk_cursory.csv'): 

    import numpy as np 
    import pandas as pd 
    from sunnyhills.pipeline_functions import download, preprocess, run_bls
    from tqdm import tqdm 
    import os 
    import pickle 
    import matplotlib.pyplot as plt 

    df = pd.read_csv(key)

    tic_ids = np.array(df['TIC_ID'])

    downloaded = 0
    downloaded_ids = os.listdir('./data/current/processed/lightcurves')
    downloaded_ids = [i.replace('_lc.pickle', '') for i in downloaded_ids if i!='.gitkeep']

    with open(results_file, 'w') as f: 
        f.write('TIC_ID'+'\n')

    with open(results_file, 'a') as f: 
        for tic_id in tic_ids:
            if tic_id in downloaded_ids: 
                #try: 
                raw_lc, data_found = download(ticstr=tic_id)
                
                if data_found: 
                    stitched_lc, stitched_trend, stitched_raw = preprocess(raw_list=raw_lc, ticstr=tic_id, outdir=lc_out_dir)

                    results, bls_model, in_transit, stats = run_bls(stitched_lc)

                    time = stitched_lc['time']
                    flux = stitched_lc['flux']
                    fig = plt.figure(constrained_layout=True, figsize=(7, 7))
                    mosaic = """
                    ab
                    cd"""

                    ax_dict = fig.subplot_mosaic(mosaic)
                    
                    period = results.period[np.argmax(results.power)]

                    ax = ax_dict['a']
                    ax.axvline(period, alpha=0.4, lw=3)
                    for n in range(2, 10):
                        ax.axvline(n*period, alpha=0.4, lw=1, linestyle="dashed")
                        ax.axvline(period / n, alpha=0.4, lw=1, linestyle="dashed")
                    ax.plot(results.period, results.power, color='black', lw=0.5)
                    ax.set(xlim=(0, max(results.period)), ylabel='SDE BLS', xlabel='Period (days)')

                    index = np.argmax(results.power)
                    period = results.period[index]
                    t0 = results.transit_time[index]
                    duration = results.duration[index]

                    ax = ax_dict['b']
                    x = (time - t0 + 0.5*period) % period - 0.5*period
                    m = np.abs(x) < 0.5
                    ax.scatter(
                        x[m],
                        flux[m],
                        color='blue',
                        s=10,
                        alpha=0.5,
                        zorder=2)

                    x = np.linspace(-0.13, 0.13, 1000)
                    f = bls_model.model(x + t0, period, duration, t0)
                    ax.plot(x, f, color='red')
                    #ax.set_xlim(-0.13, 0.13)
                    #plt.ylim(0.9985, 1.00025)
                    ax.set_xlabel("Time from mid-transit (days)")
                    ax.set_ylabel("Flux")

                    ax = ax_dict['c']

                    ax.scatter(stitched_raw['time'], stitched_raw['flux'])

                    ax.scatter(stitched_trend['time'], stitched_trend['flux'])

                    plt.show()

                    plt.clf()
                    plt.close()

                    break 
                        
                        
                    out_dict = {'stitched_lc':stitched_lc, 'stitched_trend':stitched_trend, 'stitched_raw':stitched_raw}
                    file_path = lc_out_dir+'/'+tic_id+'_lc.pickle' 
                    with open(file_path, 'wb') as handle:
                        pickle.dump(out_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

                    f.write(tic_id+'\n')
                
                #except: 
                    #continue  
        
run_bulk_download()