import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(0, 1, 100)
y = 3*x+np.random.normal(0,0.2,100)

# make plot

fig, axs = plt.subplots(1, 2, figsize=(6,3))

axs[0].hist(x)

axs[1].scatter(x,y)

axs[1].set(xlabel='x', ylabel='y')
axs[1].invert_yaxis()

plt.show()