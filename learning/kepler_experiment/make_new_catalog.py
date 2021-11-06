import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# choose n random kepler objects that have confirmed planet and were detected with transit method
# perhaps only choose systems with one planet
# create a little write-up highlighting results
raw_df = pd.read_csv('https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/learning/kepler_experiment/eu_exoplanet_catalog.csv')

columns = ['name', 'orbital_period', 'radius', 'semi_major_axis', 'detection_type', 'star_name', 'ra', 'dec', 'star_distance']

names = np.array(raw_df['name'])
good_indices = []

for name_index, name in enumerate(names): 
    if 'Kepler' in name: 
        good_indices.append(name_index)

concise_df = raw_df.iloc[good_indices, :] 
concise_df = concise_df[columns]

one_planet_indices = []

star_names = np.array(concise_df['star_name'])

for star_index, star in enumerate(star_names): 
    count = len(np.where(star_names==star)[0])
    if count == 1: 
        one_planet_indices.append(star_index)

concise_df = concise_df.iloc[one_planet_indices, :]

detection_indices = []
for detection_index, detection_type in enumerate(concise_df['detection_type']): 
    if detection_type =='Primary Transit': 
        detection_indices.append(detection_index)

concise_df = concise_df.iloc[detection_indices, :]
concise_df = concise_df.drop(columns=['detection_type'])

concise_df.to_csv('concise_df.csv', index=False)
