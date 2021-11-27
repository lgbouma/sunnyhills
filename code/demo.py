import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family']='serif'
plt.style.use('ggplot')

years = []
sea_ages = []
with open(r'C:\Users\Research\Documents\GitHub\sunnyhills\code\salmon_data.txt', 'r') as f: 
    for line in f: 
        linelist = line.split(',')
        year = int(linelist[0])
        years.append(year)
        sea_age = int(linelist[1])
        sea_ages.append(sea_age)

plt.scatter(years,sea_ages)
plt.plot(years, sea_ages)
plt.xlabel('Year')
plt.ylabel('Sea Age')
plt.show()
