"""
Example driver script for visualizing how wotan's flatten functions do at
removing starspot induced rotation signals.

Some TODOs for Ryan, Kiana, Rachel, Veronica & Thaddaeus:

* Read the ~100 lines of this plotting script, and figure out how it works.

* What is the best wotan *method* to use? (biweight? pspline? cosine? other?)

* What is the corresponding best window length?

* Is it worthwhile to tune the "cval"?

* Does "break_tolerance" affect things?  (probably not...)

* The residuals often have outlying points in addition to the transits.  For
example, they can come from flares.  If we were to identify the flares after
the first round of detrending using altaipony, and then repeat the detrending
on the masked (non-detrended) light curve, would wotan do any better?

    --> Alternatively, just applying slide_clip again might be a better
    approach.  What if we did that instead?

* The residuals often look wonky at the beginning and ends of orbits, because
of how edges in the light curve are trended by the "flateten" windowed slider.
Can we write a reuseable function to mask the edges out?
"""
import numpy as np
import os
from sunnyhills.paths import DATADIR, EPOCHSDIR
from sunnyhills.plotting import plot_star_detrending

outdir = os.path.join(EPOCHSDIR, 'lgb', 'figures', 'AU_Mic')
if not os.path.exists(outdir):
    os.mkdir(outdir)

ticstr = 'TIC 441420236'

# Plavchan+2020 Table 2, with t0 converted to BTJD
known_ephemeris = {
    't0': 2458330.39153 - 2457000,
    'period': 8.46321
}

for window_length in np.arange(0.1, 1.1, 0.1):

    dtrdict = {'method':'biweight',
               'window_length':window_length,
               'cval':5.0,
               'break_tolerance':1.0}

    plot_star_detrending(outdir, ticstr, dtrdict,
                         known_ephemeris=known_ephemeris)
