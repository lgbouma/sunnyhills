ID=0
import time
import astropy
import astroquery
from astroquery.simbad import Simbad
File_object = open("run.txt", "r")
try:
    for ID in File_object:
        print(ID)
        result_table = Simbad.query_object("Gaia DR2 ",ID)
        time.sleep(1)
except:
    print("Tag not found")
