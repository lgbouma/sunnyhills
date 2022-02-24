import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from altaipony.flarelc import FlareLightCurve
from altaipony.lcio import from_mast
import lightkurve as lk
from wotan import flatten

from astropy.stats import sigma_clip

full_raw = lk.search_lightcurve('TIC 441420236').download_all()
raw_lc = full_raw[2,8]
raw_lc = raw_lc.stitch()

raw_times = raw_lc.time.value
raw_fluxes = raw_lc.flux.value

mask = sigma_clip(raw_fluxes, lower_sigma=5, masked=True)

mask = np.invert(mask.recordmask)

print(mask)

flatten_lc, trend_lc = flatten(raw_times,raw_fluxes,method='cosine',window_length=.15,break_tolerance=0.5,return_trend=True)

#half = np.where(times<1700)