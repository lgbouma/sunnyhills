import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import lightkurve as lk
#import os.path
#import csv

df = pd.read_csv('https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/data/full_key.csv')
df=df.dropna()
df

rightAscension = df['GDR2_RA'][:500]
declination = df['GDR2_DEC'][:500]
distances = np.array(df['Distance'][:500])

stellarColors = df['bp-rp'][:500]
stellarMags = df['g_mag'][:500]
b=stellarMags-(5*np.log10(distances)+5)
a=stellarColors-(5*np.log10(distances)+5)
#flip x and y axis
ax = plt.scatter(b,a,c=np.log10((distances[:500])),cmap='plasma')
plt.xlabel("Stellar Color")
plt.ylabel("Stellar Magnitude")

c = plt.colorbar()
c.set_label("Log Distance From Earth")
plt.show()
