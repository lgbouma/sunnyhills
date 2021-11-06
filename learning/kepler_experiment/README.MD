# Kepler Recovery Project

## Overview
* 

## Code Hints
* Create map of your stars in the sky based on their ```ra``` and ```dec``` coordinate values: 

```python
# Create a figure and then apply the aitoff projection
plt.figure(figsize=(12, 8))
plt.subplot(projection="aitoff")

# Plot Star Locations
plt.scatter(concise_df['ra'], concise_df['dec'])

# Replace the standard x ticks (longitude) with the ecliptic coordinates
plt.xticks(ticks=np.radians([-150, -120, -90, -60, -30, 0, \
                             30, 60, 90, 120, 150]),
           labels=['150°', '120°', '90°', '60°', '30°', '0°', \
                   '330°', '300°', '270°', '240°', '210°'])

# Set the axes labels
plt.xlabel('Right Ascension (deg)')
plt.ylabel('Declination (deg)')

# Plot grid
plt.grid(True)

plt.show()
```

## Example Outputs
* Phase-folded transit light curve:  
![](https://docs.lightkurve.org/_images/tutorials_3-science-examples_exoplanets-identifying-transiting-planet-signals_19_1.png)

* Periods distribution histogram:  
![](https://raw.githubusercontent.com/HarritonResearchLab/learning/main/images/period_dist.png)

* Map of Stars on Sky: 
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/learning/kepler_experiment/images/skymap.png)

* Orbital Period versus Orbital Distance: 
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/learning/kepler_experiment/images/per_vs_dist.png)

* Distribution of Planetary Radii in your Sample:
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/learning/kepler_experiment/images/radius_dist.png)