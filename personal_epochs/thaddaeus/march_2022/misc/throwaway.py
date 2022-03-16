import pickle 
with open('./data/current/processed/lightcurves/TIC_416358769_lc.pickle', 'rb') as handle:
    content = pickle.load(handle)
    print(content.keys())
    print(content['stitched_raw'][0]['time'])