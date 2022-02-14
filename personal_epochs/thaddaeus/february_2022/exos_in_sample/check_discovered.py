import pandas as pd
import numpy as np
from soupsieve import match
from tqdm import tqdm 

def clean_nasa_catalog(): 

    file_path = './personal_epochs/thaddaeus/february_2022/nasa_exo_archive_results.csv'

    df = pd.read_csv(file_path)


    #print(list(df))

    keep_columns = ['hostname', 'ra', 'dec', 'sy_snum', 'sy_pnum', 'discoverymethod', ]

    drop_columns = [i for i in list(df) if i not in keep_columns]

    df = df.drop(columns=drop_columns)

    df = df.drop_duplicates(subset='hostname', keep='first')

    df.to_csv('concise_nasa_exoplanet_catalog.csv', index=False)

def check_overlap(): 

    from astropy.coordinates import SkyCoord
    from astropy import units as u

    nasa_df = pd.read_csv('./personal_epochs/thaddaeus/february_2022/exos_in_sample/concise_nasa_exoplanet_catalog.csv').sample(frac=1)

    nasa_ids = np.array(nasa_df['hostname'])
    nasa_ras = np.array(nasa_df['ra'])
    nasa_decs = np.array(nasa_df['dec'])

    our_df = pd.read_csv('./data/current/full_key.csv')

    our_gaia_ids = np.array(our_df['GDR2_ID'])
    our_ras = np.array(our_df['GDR2_RA'])
    our_decs = np.array(our_df['GDR2_DEC'])

    our_matched_ids = np.array([])
    nasa_matched_ids = np.array([])

    for nasa_id, nasa_ra, nasa_dec in tqdm(zip(nasa_ids, nasa_ras, nasa_decs)): 
        
        for our_id, our_ra, our_dec in zip(our_gaia_ids, our_ras, our_decs): 
            approx_sep = 3600*np.sqrt((nasa_ra-our_ra)**2+(nasa_dec-our_dec)**2)
            if approx_sep <= 2: 
                our_matched_ids = np.append(our_matched_ids, our_id)
                nasa_matched_ids = np.append(nasa_matched_ids, nasa_id)
                break 

    matched_df = pd.DataFrame(list(zip(our_matched_ids, nasa_matched_ids)), columns=['GDR2_ID','hostname'])
    matched_df.to_csv('matched_results.csv', index=True)

def fix_small_check():
    from astropy.coordinates import SkyCoord
    from astropy import units as u

    coord_one = SkyCoord(170,20,frame='fk5',unit=(u.deg,u.deg))
    coord_two = SkyCoord(171,21,frame='fk5',unit=(u.deg,u.deg))

    sep = coord_one.separation(coord_two).arcsecond

    print(sep, 3600*np.sqrt((1)**2+(1)**2))

def reformat_small_df(): 
    df = pd.read_csv('matched_results.csv')
    df = df[['GDR2_ID','hostname']]
    df.to_csv('matched_results.csv', index=False)

#fix_small_check()
#check_overlap()
reformat_small_df()