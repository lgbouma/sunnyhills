import pandas as pd
import numpy as np

import pickle 

a = {'lc_list':[{'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}, {'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}],
     'trend_list':[{'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}, {'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}],
     'raw_list':[{'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}, {'time':[1,2,3,4,5], 'flux':[1,2,3,4,5]}]}

with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
    lc_list = b['lc_list']
    print(lc_list)