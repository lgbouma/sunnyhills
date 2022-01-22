import matplotlib.pyplot as plt

mosaic = """
    AAB
    CCD
    EEF
    """

def identify_axes(ax_dict, fontsize=48):
    """
    Helper to identify the Axes in the examples below.

    Draws the label in a large font in the center of the Axes.

    Parameters
    ----------
    ax_dict : dict[str, Axes]
        Mapping between the title / label and the Axes.
    fontsize : int, optional
        How big the label should be.
    """
    kw = dict(ha="center", va="center", fontsize=fontsize, color="darkgrey")
    for k, ax in ax_dict.items():
        ax.text(0.5, 0.5, k, transform=ax.transAxes, **kw)

fig = plt.figure(constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)
#identify_axes(ax_dict)

x = [1, 2, 3, 4, 5, 6]
ax_dict['A'].plot(x,x, color='blue') # method for accessing an axis? 

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

print(ax_dict)