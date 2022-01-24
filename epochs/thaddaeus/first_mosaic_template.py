import matplotlib.pyplot as plt

plt.style.use('./other/aesthetics/science.mplstyle') # set style...should work on all our computers because relative

mosaic = """
    AAB
    CCD
    EEF
    """

fig = plt.figure(constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)

# to axis one of the subplots, do it like this: ax_dict['A'] (e.g. for subplot A)

plt.show()

## LC MOSAIC KEY FOR NOW 
"""
A: raw light curve 
B: flare flare frequency plot
C: detrended light curve with annotated flares
D: periodogram with annotated harmonics
E: detrended and iterative 3 sigma clipped light curve
F: Phase folded light curve 
"""