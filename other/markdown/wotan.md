
# Wotan

## Intro

- need to detrend to get rid of irrelevant signals
  - sometimes can induce false positives

- simpler methods that preform systematics first and signal search after
  - has higher signal recovery rates

## Algorithims

- 4 categories
  - sliding filters
  - splines
  - polynomials
  - Gaussian processes

### Sliding Filters

- mean or median
  - scatterplot smoother (fitting function through points of a scatterplot)

- Cadence based filters
  - applied to fixed number of data points
  - simple and fast
    - require equally spaced data without gaps
  - test sliding median
    - fits successive sub-sets of points with low order polynomial
      - second or third degree

- Time windowed filters
  - use window fixed in second dimension
  - define window length which will contain given data points

- mean and median
  - most common location estimators
  - mean = most efficient for normal distribution
    - very uncertain
      - bias variance tradeoff

- Trimmed mean and median
  - rejects most extreme values
    - more robust than mean and more efficient than median

- Huber Function
  - more robust than trimmed mean and median
    - **M-Estimators**
      - estimator is optimal if data is close to assumed distribution

- maximally efficient estimator = least variance of location estimate

### Splines

- smooth piecewise approximation
  - univariate splines
    - all knots lie in single dimension + equally spaced

- fit by minimizing sum of squared residuals
  - greatly effected by outliers

- cosine filtering
  - developed for application of exomoon hunting
    - optimal detrending is determine iteratively
  - sum of sines and cosines can be fit to data

#### Edge Treatment

- all detrending methods are challenge near edges
  - data missing on one side

- data can be padded to enlarge full window
  - add constant value, mirroring values, wrapping beginning and end

- data near edge can be discarded after detrending

- savitzky golay filter
  - fits polynomial to end segments

### Tukey's Biweight

- has weights at distance from central location
  - large weights make estimate more robust but more efficient

- can be used as a one-step estimate
  - also can be approximated with iterative algorithms

#### Comparisons of different algorithims

- time windowed sliders had the best overall preformance

- shallowest planets
  - biweight slightly better than Welsch and Median
  - **Savitzky-Golay should be avoid for light curve preperation before transit search**
    - removes 10-20 percent transits
    - Relative sensitivity and robustness of detrending method dont depend on data quality

- injected samples from TESS
  - all methods preform very similarly
    - parameter settings had little influence on recovery rates

- sliding biweight was really good in Kepler and K2 but was beat by robust spline in **young TESS stars**

- edge treatment
  - worst results occured when wrapping data  from begining to end
    - works well if data is periodic and period = length of time series

- window shape
  - longer windows leave substantial residue after detrending when stellar noise periodicity is short
  - reccomended to use rectangular window

- window length
  - short as possible to maximize removal of stellar variability

## Overall

- it is often better to use robust methods over Gaussian Processes and Splines when doing transit searches
  - assumes that the distribution is gaussian

- timed windowed sliding mean is fastest
- biweight is slower
- splines are slower at first but get better with more data
- iterative biweight benefits from run-time compliation

- filters can sometimes cause distortion on transit shape
  - can use `transit_mask` to mitigate this problem

- ideal method - time-windowed slider with iterative robust location estimator
  - Tukey's biweight
