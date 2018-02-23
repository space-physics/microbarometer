#!/usr/bin/env python
"""
1. .seed to .mseed: ./rdseed.rh6.linux_64 -f ~/data/microbarom/524602.seed -d -o 4
2. read and plot:

    python PlotPressure.py ~/data/microbarom/524602.mseed -decimate 10 -yminmax 9e5 1.1e6
    python PlotPressure.py ~/data/microbarom/768852.mseed -i 1 -yminmax 2.525e6 2.65e6

"""
from pathlib import Path
import scipy.signal
from matplotlib.pyplot import figure, show, colorbar
import matplotlib.dates as md
import cartopy
from datetime import timedelta
import seaborn as sns
#
import pymicrobarometer as pmb

GREF = cartopy.crs.PlateCarree()

Nfft = 512

# ./rdseed myfile.seed -s
loc = {'TA-BGNE-BDO':(-98.150200, 41.408298, 573.000000, 'Belgrade, Nebraska'),  # fs= 40 Hz
       'IU-CCM-LDO':(-91.244598, 38.055698, 222.000000, 'Cathedral Cave, Missouri')}   # fs= 1 Hz

cities = [#[-117.1625, 32.715, 'San Diego'],
          [-87.9073, 41.9742, 'KORD' ],
          [-90.3755, 38.7503,'KSUS'],
          [-97.040443,32.897480,'KDFW'],
          [-104.6731667,39.8616667,'KDEN'],
          [ -111.1502604,45.7772358,'KBZN'],
          [ -106.6082622,35.0389316,'KABQ']]


def plotmicrobarom(dat, showmap:bool, yminmax:tuple=None, decimate:int=None):
    if decimate is not None:
        #dat.filter('lowpass', freq=0.01))
        dat.decimate(factor=decimate)

    t = pmb.t2dt(dat)

    fs = dat.meta.sampling_rate

    fg = figure(figsize=(12,8))
    ax = fg.gca()

    ax.plot(t, dat)
    ax.set_ylabel('int32 data numbers')
    ax.set_title(f'station {dat.meta.network}-{dat.meta.station}, $f_s$ = {fs} Hz')
    ax.grid(True)
    ax.set_ylim(yminmax)

    if t[-1] - t[0] > timedelta(days=1):
        fmt = None
        ss= ''
    else:
        fmt = md.DateFormatter('%H:%M')
        ss = t[0].date()

    ax.set_xlabel(f'UTC time: {ss}')
    if fmt is not None:
        ax.xaxis.set_major_formatter(fmt)
    fg.autofmt_xdate()
# %% spectrogram
    fg = figure()
    ax = fg.gca()
    ax.specgram(dat, Fs=fs)
#    f,t,Sxx = scipy.signal.spectrogram(dat,
#                                     fs=fs,
#                                     nfft= Nfft,
#                                     nperseg= Nfft,
#                                     noverlap= None,
#                                     return_onesided=True) # [V**2/Hz]

    #fg.colorbar(ax=ax)
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [sec]')

# %% Map
    if showmap:
        am = figure(figsize=(15,10)).gca(projection=GREF)
        am.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
        am.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                      '50m',
                                      linestyle=':',linewidth=0.5, edgecolor='grey', facecolor='none'))

        for k,l in loc.items():
            am.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
            am.annotate(k, xy = (l[0], l[1]), xytext = (3, 3), textcoords = 'offset points')

        for c in cities:
            am.plot(c[0], c[1], 'bo', markersize=7, transform=GREF)
            am.annotate(c[2], xy = (c[0], c[1]), xytext = (3, 3), textcoords = 'offset points')


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory where SEED data files are (or filename)')
    p.add_argument('-i','--ind',help='index of datastream',type=int,default=0)
    p.add_argument('-ext',help='file suffix of data',default='.SAC')
    p.add_argument('-nomap',help='do not show map',action='store_true')
    p.add_argument('-decimate',help='downsample factor',type=int)
    p.add_argument('-yminmax',help='vertical plot limits',nargs=2, type=float)
    p = p.parse_args()

    if isinstance(p.datadir,(str,Path)):
        datadir = Path(p.datadir).expanduser()
        if datadir.is_dir():
            flist = datadir.glob('*'+p.ext)
        elif datadir.is_file():
            flist = [datadir]
        else:
            raise FileNotFoundError(f'No SEED data in {datadir}')
    else: # list of files
        flist = [Path(d).expanduser() for d in p.datadir]

    dat = []
    for f in flist:
        if f.suffix.endswith('ASC'):
            dat = pmb.readasc(f)
        elif f.suffix in ('.SAC','.seed','.mseed'):
            dat = pmb.readseed(f)

    print(dat)
    #print(dat[0].stats)
    print(f'shape of data in {f}',dat[p.ind].count(),'from',dat[p.ind].meta.starttime,'to',dat[0].meta.endtime)

    plotmicrobarom(dat[p.ind], not p.nomap, yminmax=p.yminmax, decimate=p.decimate)

    show()
