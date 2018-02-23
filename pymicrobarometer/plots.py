import numpy as np
from datetime import timedelta
import scipy.signal
from matplotlib.pyplot import figure
import matplotlib.dates as md

def timelbl(t):
    if t[-1] - t[0] > timedelta(days=1):
        fmt = None
        txt= 'UTC time'
    else:
        fmt = md.DateFormatter('%H:%M')
        txt = f'UTC time: {t[0].date()}'

    return fmt,txt


def plotraw(dat, fs, yminmax=None):

    t = pmb.t2dt(dat)

    fg = figure(figsize=(12,8))
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


def plotmap(showmap:bool):
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


def plotspecgram(dat, fs):
    fg = figure()
    ax = fg.gca()
    if 0:
        h = ax.specgram(dat, Fs=fs)[3]
    if 1:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
        f,t,Sxx = scipy.signal.spectrogram(dat.data,
                                     fs=fs)#,
                                   #  nfft= Nfft,
                                   #  nperseg= Nfft,
                                   #  noverlap= None) # [V**2/Hz]
        step = timedelta(seconds=t[1]-t[0])
        t = pmb.datetimerange(dat.meta.starttime.datetime,
                              dat.meta.endtime.datetime+step,
                              step)
        h = ax.pcolormesh(t,f, 10*np.log10(Sxx))

    fg.colorbar(h, ax=ax).set_label('dB [V$^2$/Hz]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title(f'station {dat.meta.network}-{dat.meta.station}, $f_s$ = {fs} Hz')

    fmt, xtxt = timelbl(t)

    ax.set_xlabel(xtxt)
    if fmt is not None:
        ax.xaxis.set_major_formatter(fmt)
    fg.autofmt_xdate()


def plotmicrobarom(dat, showmap:bool, yminmax:tuple=None, decimate:int=None):
    if decimate is not None:
        #dat.filter('lowpass', freq=0.01))
        dat.decimate(factor=decimate)

    fs = dat.meta.sampling_rate

    if 0:
        plotraw(dat, fs, yminmax)
# %% spectrogram
    if 1:
        plotspecgram(dat,  fs)
# %% Map
    plotmap(showmap)