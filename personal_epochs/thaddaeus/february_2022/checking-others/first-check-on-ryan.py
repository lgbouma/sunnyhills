import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv('./personal_epochs/ryan/Tess-Point/Output.csv')
out_ids = np.array(df['-1'])[1:]

set_of_ids = np.array(list(set(out_ids)))

set_of_ids = set_of_ids[np.where(set_of_ids>0)]
counts = np.array([len(np.where(out_ids==i)[0]) for i in out_ids])
print(counts)

counts = counts[np.where(counts)]

counts = counts[np.where(counts<1000)]

plt.hist(counts)
plt.xlabel('# sectors')
plt.ylabel('count')
plt.savefig('./personal_epochs/thaddaeus/february_2022/checking-others/sectors_hist.png',dpi=150)
