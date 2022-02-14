# Altai Pony

## Purpose

- flares - violent explosions which penetrate all layers of star's atmosphere
  - enhances brightness within minutes

- purpose of Altai Pony - study and characterize flares
  - evaluate algorithm efficiency
  - statistical analysis

## Functionality

- can access most methods implemented in lightkurve

- `lightkurve.flatten()` is a Savitzky Golay Filter
  - preserve flare signal and remove variability from outside sources

- using `FlareLightCurve.detrend()` lets you use your own detrending functions

- `FlareLightCurve.find_flares()` - returns dataframe for data about flares such as:
  - occurrence time
  - amplitude 
  - duration
- can adjust what is detected as a flare by modifying the sigma clipping procedure

- can use injection-recovery pipeline for synthetic flares
  - allows you to measure performance of flare finding and detrending procedure

- `FlareLightCurve.sample_flare_recovery()` - makes fake data and preforms search

- Flare Frequency Distributions follow power law
f(> E) = β(α − 1)*E^(−α+1)