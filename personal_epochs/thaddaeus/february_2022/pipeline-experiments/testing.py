from astropy.stats import sigma_clip
from numpy.random import randn
randvar = randn(10000)
_, *bounds = sigma_clip(randvar, sigma_lower=10, sigma_upper=1, maxiters=1, masked=False, return_bounds=True)

print(bounds)