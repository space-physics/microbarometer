import numpy as np
from datetime import timedelta
import scipy.signal
import cartopy
from matplotlib.pyplot import figure
import matplotlib.dates as md
#
import pymicrobarometer as pmb

GREF = cartopy.crs.PlateCarree()

Nperseg = 16384

loc = {'TA-BGNE-BDO': (-98.150200, 41.408298, 573.000000, 'Belgrade, Nebraska'),  # fs= 40 Hz
       'IU-CCM-LDO': (-91.244598, 38.055698, 222.000000, 'Cathedral Cave, Missouri')}   # fs= 1 Hz

cities = [  # [-117.1625, 32.715, 'San Diego'],
    [-87.9073, 41.9742, 'KORD'],
    [-90.3755, 38.7503, 'KSUS'],
    [-97.040443, 32.897480, 'KDFW'],
    [-104.6731667, 39.8616667, 'KDEN'],
    [-111.1502604, 45.7772358, 'KBZN'],
    [-106.6082622, 35.0389316, 'KABQ']]


def timelbl(t):
    if t[-1] - t[0] > timedelta(days=1):
        fmt = None
        txt = 'UTC time'
    else:
        fmt = md.DateFormatter('%H:%M')
        txt = f'UTC time: {t[0].date()}'

    return fmt, txt


def plotraw(dat, fs, yminmax=None):

    t = pmb.t2dt(dat)

    fg = figure(figsize=(12, 8))
    ax = fg.gca()

    ax.plot(t, dat)
    ax.set_ylabel('int32 data numbers')
    ax.set_title(f'station {dat.meta.network}-{dat.meta.station}, $f_s$ = {fs} Hz')
    ax.grid(True)
    ax.set_ylim(yminmax)

    fmt, xtxt = timelbl(t)

    ax.set_xlabel(xtxt)
    if fmt is not None:
        ax.xaxis.set_major_formatter(fmt)
    fg.autofmt_xdate()


def plotmap(showmap: bool):
    if showmap:
        am = figure(figsize=(15, 10)).gca(projection=GREF)
        am.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
        am.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                                           '50m',
                                                           linestyle=':', linewidth=0.5, edgecolor='grey', facecolor='none'))

        for k, l in loc.items():
            am.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
            am.annotate(k, xy=(l[0], l[1]), xytext=(3, 3), textcoords='offset points')

        for c in cities:
            am.plot(c[0], c[1], 'bo', markersize=7, transform=GREF)
            am.annotate(c[2], xy=(c[0], c[1]), xytext=(3, 3), textcoords='offset points')


def plotspecgram(dat, fs: int, flim: tuple, clim: tuple):
    fg = figure()
    ax = fg.gca()
    if 0:
        h = ax.specgram(dat, Fs=fs)[3]
    if 1:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
        f, t, Sxx = scipy.signal.spectrogram(dat.data,
                                             fs=fs, nperseg=Nperseg)  # ,
        #  nfft= Nfft,

        #  noverlap= None) # [V**2/Hz]
        step = timedelta(seconds=t[1]-t[0])
        t = pmb.datetimerange(dat.meta.starttime.datetime,
                              dat.meta.endtime.datetime+step,
                              step)
        h = ax.pcolormesh(t, f, 10*np.log10(Sxx))

    fg.colorbar(h, ax=ax).set_label('dB [V$^2$/Hz]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title(
        f'Barometric Pressure Spectrum \n station {dat.meta.network}-{dat.meta.station}, $f_s$ = {fs} Hz, window Ns={Nperseg}')
    if flim is not None:
        ax.set_ylim(flim)
    if clim is not None:
        h.set_clim(clim)

    fmt, xtxt = timelbl(t)

    ax.set_xlabel(xtxt)
    if fmt is not None:
        ax.xaxis.set_major_formatter(fmt)

    fg.autofmt_xdate()


def plotmicrobarom(dat, pp, decimate: int=None):
    if decimate is not None:
        # dat.filter('lowpass', freq=0.01))
        dat.decimate(factor=decimate)

    fs = dat.meta.sampling_rate

    if 0:
        plotraw(dat, fs, pp['yminmax'])
# %% spectrogram
    if 1:
        plotspecgram(dat,  fs, pp['flim'], pp['clim'])
# %% Map
    plotmap(pp['showmap'])
