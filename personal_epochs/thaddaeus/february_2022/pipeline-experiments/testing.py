def test(
    message:str, 
    test:str="hey"): 
    print(message, test)

test('mealjselkfaj')

import numpy as np
import mpl_scatter_density
from mpl_scatter_density import scatter_density_artist
import matplotlib.pyplot as plt
import pandas as pd
import lightkurve as lk

#Gaia MS
df_MS = pd.read_csv(r'personal_epochs\kiana\gaia_catalog_99999.csv')
df_MS = df_MS.dropna()
df_MS

parallax = np.array(df_MS['Plx'])
distances_MS = 1000/parallax
BPmag=np.array(df_MS['BPmag'])
RPmag=np.array(df_MS['RPmag'])

bprp = BPmag-RPmag

stellarColors_MS = bprp
stellarMags_MS = df_MS['Gmag']

x = np.array(stellarColors_MS)
y = np.array(stellarMags_MS-5*np.log10(distances_MS)+5)

print(len(x),len(y))

is_nan = np.isnan(y)
not_nan = np.invert(is_nan)

x = x[not_nan]
y = y[not_nan]

df = pd.read_csv(r'data\current\full_key.csv')
df=df.dropna()
df

rightAscension = df['GDR2_RA']
declination = df['GDR2_DEC']
distances = np.array(df['Distance'])

stellarColors = df['bp-rp']
stellarMags = df['absolute_mag']
b=stellarMags#-(5*np.log10(distances)+5)
a=stellarColors

fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='scatter_density')
ax.scatter_density(x, y, dpi=30, cmap='viridis',zorder=1,label='Density MS')
axkerr = plt.scatter(a,b,cmap='viridis',zorder=2,label='Kerr Table 1',s=0.1)

plt.xlabel("BP-RP (mag)") 
plt.ylabel("Absolute G (mag)")
plt.title("Main Sequence Density")
plt.gca().invert_yaxis()
plt.legend()
plt.show()