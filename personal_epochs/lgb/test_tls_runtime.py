"""
Script that checks how long TLS takes to run on a single core
for typical single sector TESS data.

Usage:
    $(venv) python -u test_tls_runtime.py &> tls_runtime.log &
    $(venv) tail -f tls_runtime.log

See also:
https://github.com/hippke/tls/blob/master/tutorials/11%20A%20planet%20from%20TESS%20with%20TLS.ipynb
"""
import matplotlib.pyplot as plt, numpy as np
from astropy.io import fits
from datetime import datetime
from transitleastsquares import transitleastsquares, cleaned_array

# pull the WASP-169 TESS alert data
url = 'https://archive.stsci.edu/hlsps/tess-data-alerts/hlsp_tess-data-alerts_tess_phot_00159951311-s03_tess_v1_lc.fits'
hdu = fits.open(url)
time = hdu[1].data['TIME']
flux = hdu[1].data['PDCSAP_FLUX']  # values with non-zero quality are nan or zero'ed
time, flux = cleaned_array(time, flux)  # remove invalid values such as nan, inf, non, negative
flux = flux / np.median(flux)

WRITE_PLOT = 1
if WRITE_PLOT:
	plt.figure()
	plt.xlabel('Time (days)')
	plt.ylabel('Flux (relative)')
	plt.scatter(time, flux, color='black', s=1, alpha=0.5);
	plt.savefig('wasp-139_tess_lightcurve.png', bbox_inches='tight')
	plt.close('all')

start = datetime.utcnow()
print(f"Start: {start.isoformat()}")

model = transitleastsquares(time, flux)
results = model.power(use_threads=1)

end = datetime.utcnow()
print(f"End: {end.isoformat()}")

runtime = end - start
print(f"TLS runtime: {runtime}")
