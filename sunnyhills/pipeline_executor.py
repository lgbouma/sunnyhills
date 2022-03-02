from sunnyhills.pipeline_functions import download_and_preprocess, plot_lightcurve

lc_list, trend_list, raw_list = download_and_preprocess('TIC 441420236')
plot_lightcurve('TIC 441420236', lc_list, trend_list, raw_list)