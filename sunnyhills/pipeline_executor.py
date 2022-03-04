import pandas as pd

lc_one = pd.DataFrame.from_dict({'time':[1,2,3,4], 'flux':[1,2,3,4]}) 

'''
with open('all_dfs.csv','w') as f:
    for df in [lc_one, lc_one]:
        df.to_csv(f, index=False)
        f.write("\n")

'''

dfs = pd.read_csv('all_dfs.csv')
print(dfs)