import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import numpy as np
import pandas as pd
import lightkurve as lk

search_result = lk.search_lightcurve('Kepler-69', author='Kepler', cadence='long')

lc_collection = search_result.download_all()

lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()

t = lc.time.value
flux = lc.flux.value
flux_err = lc.flux_err.value

plt.scatter(t,flux)
plt.show()


'''TLS STUFF -- last checked, not working'''
'''
from transitleastsquares import transitleastsquares

model = transitleastsquares(t, flux)
results = model.power()

periods = results.periods
best_period = results.period
powers = results.power
'''