from sunnyhills.pipeline_functions import download_and_preprocess, plot_lightcurve

lc_list, trend_list, raw_list = download_and_preprocess('TIC 165818534')
plot_lightcurve('TIC 261136679', lc_list, trend_list, raw_list, outdir='show')

# 441420236 is au mic ... TIC 261136679 is Pi Mensae and has period of ~6.27 days