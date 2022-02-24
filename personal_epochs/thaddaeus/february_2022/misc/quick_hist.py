import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./data/current/full_key.csv')

distances_mask = np.where(df['Distance']<=100)

ages = np.array(df['age_myr'])[distances_mask] 
probs = np.array(df['probability'])[distances_mask]

plt.style.use('ggplot')

fig, axs = plt.subplots(1,3, figsize=(9,3))

sums = []


ax = axs[0]

ax_ages = ages[np.where(probs>0.68)]
sums.append(len(ax_ages))
ax.hist(ax_ages)

ax.set(xlabel='Age (myr; probability > 0.68)')

ax = axs[1]

ax_ages = ages[np.where(probs>0.95)]
sums.append(len(ax_ages))
ax.hist(ax_ages)

ax.set(xlabel='Age (myr; probability > 0.95)')

ax = axs[2]

ax_ages = ages[np.where(probs>0.99)]
sums.append(len(ax_ages))
ax.hist(ax_ages)
ax.set(xlabel='Age (myr; probability > 0.99)')

for i in range(3): 
    axs[i].set(ylabel='Count (sum='+str(sums[i])+')')

fig.tight_layout()

plt.savefig('./personal_epochs/thaddaeus/february_2022/misc/age_dists.png', dpi=150)