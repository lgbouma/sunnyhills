import pandas as pd
import numpy as np

### IMPORTANT! #1 use of pandas: reading data from .csv files: 

df = pd.read_csv(r'C:\Users\Research\Documents\GitHub\sunnyhills\lectures\references\lotka-voltara.csv')
# r is for windows only; quotations around path are for all operating systems

### IMPORTANT! #2 use of pandas: reading columns into numpy arrays: 
years = np.array(df['Year'])
print(years)