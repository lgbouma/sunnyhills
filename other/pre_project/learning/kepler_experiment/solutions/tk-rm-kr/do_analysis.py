import pandas as pd

base_dir = '/Users/Research/Documents/GitHub/sunnyhills/learning/kepler_experiment/solutions/tk-rm-kr'
#input('base dir:~$ ')

def do_analysis(star_id, base_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import lightkurve as lk
    import os 

    plt.rcParams['font.family']='serif'
    plt.style.use('ggplot')

    plot_dir =  base_dir + '/plots'

    results_file = base_dir+'/results.csv'

    search_result = lk.search_lightcurve(star_id, author='Kepler', cadence='long')
    lc_collection = search_result.download_all()

    lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()

    # Create array of periods to search
    periods = np.linspace(1, 20, 10000)
    # Create a BLSPeriodogram
    bls = lc.to_periodogram(method='bls', period=periods, frequency_factor=500)

    planet_period = bls.period_at_max_power
    planet_t0 = bls.transit_time_at_max_power
    planet_dur = bls.duration_at_max_power

    title_str = 'Star ID: '+star_id +'\n'+'Period: ' +str(round(planet_period.value,5))
    
    fig, ax = plt.subplots()
    ax = lc.fold(period=planet_period).scatter(ax=ax)
    ax.set(title=title_str)
    plt.savefig(plot_dir+'/'+star_id+'.png', bbox_inches='tight')
    plt.clf()
    plt.close()

    with open(results_file, 'a') as f:
        f.write(star_id+','+str(planet_period).replace(' d', '')+'\n')

import os 
for star_id in pd.read_csv(base_dir+'/data/sample_df.csv')['star_name']: 
    used_ids = os.listdir(r'C:\Users\Research\Documents\GitHub\sunnyhills\learning\kepler_experiment\solutions\tk-rm-kr\plots')

    used_ids = [i.replace('.png', '') for i in used_ids if i != '.gitkeep']
    if star_id not in used_ids:
        do_analysis(star_id, base_dir)

#/Users/Research/Documents/GitHub/sunnyhills/learning/kepler_experiment/solutions/tk-rm-kr