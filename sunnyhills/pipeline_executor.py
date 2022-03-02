from sunnyhills.pipeline_functions import download_and_preprocess, plot_lightcurve

lc_list, trend_list, raw_list = download_and_preprocess('TIC 165818534')
plot_lightcurve('TIC 165818534', lc_list, trend_list, raw_list, outdir='show')

# 441420236