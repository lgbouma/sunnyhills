import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/personal_epochs/ryan/Tess-Point/Output.csv')

full_out_ids = np.array(df['-1'])

out_ids = full_out_ids[1:]

all_sectors = np.array(df[' -1'])

set_of_ids = np.array(list(set(out_ids)))

set_of_ids = set_of_ids[np.where(set_of_ids>0)]

counts = np.array([])

for id in set_of_ids: 
    df_mask = np.where(full_out_ids==id)
    count = len(list(set(all_sectors[df_mask])))

    counts = np.append(counts, count)
    
    
print(list(df))
print(np.mean(counts))

plt.hist(counts)
plt.xlabel('# sectors')
plt.ylabel('count')
plt.show()
