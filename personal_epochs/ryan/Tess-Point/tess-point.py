#CSV OUTPUT CELL
import pandas as pd
import numpy as np
from tess_stars2px import tess_stars2px_function_entry
print("Libraries imported successfully")
counter=0
f = open("Output.csv", "a")
df = pd.read_csv('https://raw.githubusercontent.com/HarritonResearchLab/sunnyhills/main/data/current/full_key.csv')
df = df.dropna()
dfRA = df['GDR2_RA'][:30000]
dfDEC = df['GDR2_DEC'][:30000]
dfTIC = df['GDR2_ID'][:30000]
propRA = 0
print("csv parsed successfully...")
#propTIC = 12345678
for propRA, propDEC, propTIC in zip(dfRA, dfDEC, dfTIC):
  #print(propRA, propDEC)
  ##################################
  outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
          outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
                  propTIC, propRA, propDEC)
  for i in range(len(outID)):
    #print('{0:d}, {1:d}, {2:d}, {3:d}, {4:f}, {5:f},'.format(outID[i], outSec[i], \
    #outCam[i], outCcd[i], outColPix[i], outRowPix[i]))
    a = '{0:d}, {1:d}, {2:d}, {3:d}, {4:f}, {5:f}'.format(outID[i], outSec[i], \
    outCam[i], outCcd[i], outColPix[i], outRowPix[i])
    f.write(a)
    f.write("\n")
    #print(a)
    
  ##################################
  outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
          outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
                  propTIC, propRA, propDEC, scInfo=scinfo)
#
  for i in range(len(outID)):
    #print('{0:d}, {1:d}, {2:d}, {3:d}, {4:f}, {5:f},'.format(outID[i], outSec[i], \
    #outCam[i], outCcd[i], outColPix[i], outRowPix[i]))
    b = '{0:d}, {1:d}, {2:d}, {3:d}, {4:f}, {5:f}'.format(outID[i], outSec[i], \
    outCam[i], outCcd[i], outColPix[i], outRowPix[i])
    f.write(b)
    f.write("\n")
    #print(b)
  counter+=1
  if(counter==7500):
    print("25%")
  elif(counter==15000):
    print("50%")
  elif(counter==22500):
    print("75%")
  elif(counter==30000):
    print("Action complete...")
  elif(counter==1):
    print("First iteration complete...")
f.close()
print("File saved")
  ##################################
