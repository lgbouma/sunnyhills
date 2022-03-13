import lightkurve as lk
lcc = lk.search_lightcurve('TIC_82525365').download_all()
print(lcc)