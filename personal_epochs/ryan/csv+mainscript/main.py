import pandas as pd
import numpy as np
import astrobase
from astrobase.services.indentifiers import gaiadr2_to_tic
df=pd.read_csv("Book1.csv")
IDs = np.array(df["GDR2_ID"])
tic_id = gaiadr2_to_tic(IDs)
df["tic_id"] = IDs
