import os 
import numpy as np
import pickle 
from sunnyhills.pipeline_functions import run_bls
import matplotlib.pyplot as plt 

data_dir = './data/current/processed/lightcurves'

for file in os.listdir(data_dir):  
    if file!='.gitkeep': 
        with open(data_dir+'/'+file,"rb") as handle: 
            content = pickle.load(handle)

            stitched_lc = content['stitched_lc'][0]
            time = stitched_lc['time']
            flux = stitched_lc['flux']

            raw_time = content['stitched_raw'][0]['time']
            raw_flux = content['stitched_raw'][0]['flux']
            
            trend_time = content['stitched_trend'][0]['time']
            trend_flux = content['stitched_trend'][0]['flux']

            results, bls_model, in_transit, stats = run_bls(stitched_lc)

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

            ax.scatter(raw_time, raw_flux)

            ax.scatter(trend_time, trend_flux)

            plt.show()

            plt.clf()
            plt.close() 

            break 