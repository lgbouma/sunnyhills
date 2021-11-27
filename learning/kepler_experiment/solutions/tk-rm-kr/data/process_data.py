=import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import lightkurve as lk
import os

root_dir = 'C:/Users/Research/Documents/GitHub/sunnyhills/learning/kepler_experiment/solutions/tk-rm-kr'

concise_df = pd.read_csv('https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/learning/kepler_experiment/data/concise_df.csv')

sample_df = concise_df.sample(n=10)

sample_csv = root_dir+'/data/sample_df.csv'
sample_df.to_csv(sample_csv, index=False)

for star_id in sample_df['star_name']: 

    search_result = lk.search_lightcurve(star_id, author='Kepler', cadence='long')
    lc_collection = search_result.download_all()

    lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()

    lc_path = root_dir + '/data/light_curves/'+star_id+'.csv'
    lc.to_csv(lc_path)

for star_id in sample_df['star_name']: 

    period = np.linspace(1, 20, 10000)

    lc_path = root_dir + '/data/light_curves/'+star_id+'.csv'
    lc = lk.read(lc_path)

    bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)

    powers = np.array(bls.power)
    periods = np.array(bls.period)

    mask = np.argsort(powers)[::-1]
    mask = mask[0:5] # top five

    # Periodogram Plot

    fig, ax = plt.subplots()

    bls.plot(ax=ax)

    plot_root = root_dir+'/period_vetting/plots/'+star_id
    os.mkdir(plot_root)
    plt.savefig(plot_root+'/periodogram.png', bbox_inches='tight')

    plt.clf()

    counter = 0
    for period, power in zip(periods[mask], powers[mask]): 
        
        title_str = 'Star ID: '+star_id +'\n'+'Period: ' +str(round(period,5))
        title_str += '\n' + 'Power: ' + str(round(power, 2))
        
        fig, ax = plt.subplots()
        ax = lc.fold(period=period).scatter(ax=ax)
        ax.set(title=title_str)
        plt.savefig(plot_root+'/'+star_id+'_per'+str(counter)+'.png', bbox_inches='tight')
        plt.clf()

    zipped = zip(periods[0:5], powers[0:5])
    results_df = pd.DataFrame(zipped, columns=['Period', 'Power'])
    results_df.to_csv(root_dir+'/data/'+star_id+'_results.csv', index=False)