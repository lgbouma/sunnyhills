# Kepler Recovery Project

## Goal
* The goal of this project is to recover orbital periods of known exoplanets discovered with the Kepler telescope and compare the periods you derive to the periods derived for these objects in the published literature. 

## Overview
* For this project I started with a massive amount of information from the EU Exoplanet Catalog, and from this I compiled a list of confirmed exoplanets discovered with the Kepler Space Telescope using the transit method. Each exoplanet entry in the ```concise_df.csv``` file has that exoplanet's name, radius (in terms of Jupiter's, so radius of 1.5 would be 1.5 times Jupiter's), mass (see radius), orbital distance from its star (```semi_major_axis``` in ```au```), host star name, host star distance from Earth, and host star coordinates in the sky (```ra``` and ```dec```). 
* Your mission is to randomly select 10 exoplanets from the ```concise_df.csv``` file and attempt to recover their orbital periods. I would use the methods described in this article: https://docs.lightkurve.org/tutorials/3-science-examples/exoplanets-identifying-transiting-planet-signals.html
* Each exoplanet was selected because it is the only confirmed exoplanet in its host star's system, so you should not worry about recovering periods for multiple planets (because for all we know there are no other exoplanets in these stellar systems other than the one given for each). 
* Once you've done this, I would like us to practice writing up our results. Thus, our final results should be nicely formatted mini-reports type set in LaTeX. Here's a template file I made you to use: https://www.overleaf.com/read/jrhrtbwtzrpp
* This project will be our focus in November and I would like us to have it done before December! 
* I think it would be best if we worked in groups of two for this. 
* Make sure to normalize and flatten your data as in the lightkurve documentation demo. 
* Also, as shown in the lightkurve demo linked above, search data by the exoplanet's host star name.  


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

* Map of Stars on the sky:  
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/learning/kepler_experiment/images/skymap.png)

* Orbital Period versus Orbital Distance:  
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/learning/kepler_experiment/images/per_vs_dist.png)

* Distribution of Planetary Radii in your Sample:  
![](https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/learning/kepler_experiment/images/radius_dist.png)
