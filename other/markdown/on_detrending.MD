# Things to Possibly try regarding detrending

## Wotan + Altai Pony

- since AltaiPony only supports 2 methods of detreding : `k2sc` `savgol`, we could possibly detrend the light curves using `wotan` and then construct a `FlareLightCurve` to view data about flares
  - look into using `biweight` or `robust spline`
    - robust spline had better computational performance with larger data
  - avoid wrapping data for edge treatment
    - we should probably sigma clip light curve after detrending
  - wotan offers a `slide_clip` method for edge treatment prior to detrending 

## Notes When Using Wotan

- rectangular window shape
- use the smallest size possible

## Data Regarding Recoveries from Tess Stars

- all detrending methods had a fairly low recovery rate
  - 33.6% sliding median
  - 37.2% for robust spline

- However since most planets we will be looking for will be smaller than jupiter it shouldn't be too much of a problem
  - there was a nearly 100% recovery rate for planets that had half the radius of Jupiter

- Most methods had similar performance
  - parameters had small effect on recovery rate

- mostly overlap in different detrending methods but not completely
  - 43.8% recovery rate combined

## Altai Pony

- make sure to verify that detrending algorithm can account for ramp ups at the end of TESS orbits
  - can often cause false positive detections

- can evaluate the accuracy of detrending algorithm by injecting fake flares `sample_flare_recovery`
  - can plot results to figure out how many fake flares are recovered and what amplitude and frequency they are

- ALtai Pony also has sigma clipping functionality through sigma parameter in `find_flares()`
  - defaults to `flux_err`
