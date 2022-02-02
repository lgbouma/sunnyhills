import os
from sunnyhills.paths import DATADIR, EPOCHSDIR
from sunnyhills.plotting import plot_kerr21_XY

# NOTE: I'd prefer to have a "results directory", or something similar to keep
# plots that everyone makes!
outdir = os.path.join(EPOCHSDIR, 'lgb')

plot_kerr21_XY(outdir, colorkey=None)
plot_kerr21_XY(outdir, colorkey='Age')
plot_kerr21_XY(outdir, colorkey='P')
plot_kerr21_XY(outdir, colorkey='plx')
