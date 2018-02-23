#!/usr/bin/env python
"""
1. .seed to .mseed: ./rdseed.rh6.linux_64 -f ~/data/microbarom/524602.seed -d -o 4
2. read and plot:

    python PlotPressure.py ~/data/microbarom/524602.mseed -decimate 10 -yminmax 9e5 1.1e6
    python PlotPressure.py ~/data/microbarom/768852.mseed -i 1 -yminmax 2.525e6 2.65e6

"""
from pathlib import Path
from matplotlib.pyplot import show
import obspy
import seaborn as sns
#
import pymicrobarometer as pmb
import pymicrobarometer.plots as plots

# ./rdseed myfile.seed -s


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='SEED data filename')
    p.add_argument('-i','--ind',help='index of datastream',type=int,default=0)
    p.add_argument('-ext',help='file suffix of data',default='.SAC')
    p.add_argument('-nomap',help='do not show map',action='store_true')
    p.add_argument('-decimate',help='downsample factor',type=int)
    p.add_argument('-yminmax',help='vertical plot limits', nargs=2, type=float)
    p.add_argument('-tlim',help='start and end time to load',nargs=2)
    p.add_argument('-flim',help='spectrogram freq plot limits',type=float,nargs=2)
    p = p.parse_args()

    pp = {'tlim':p.tlim,'flim':p.flim,'yminmax':p.yminmax,'showmap':not p.nomap}

    fn = Path(p.fn).expanduser()

    if p.tlim:
        tlim = (obspy.UTCDateTime(p.tlim[0]), obspy.UTCDateTime(p.tlim[1]))


    if fn.suffix.endswith('ASC'):
        dat = pmb.readasc(fn)
    elif fn.suffix in ('.SAC','.seed','.mseed'):
        dat = pmb.readseed(fn, tlim=tlim)

    print(dat)
    #print(dat[0].stats)
    print(f'shape of data in {fn}',dat[p.ind].count(),'from',
          dat[p.ind].meta.starttime,'to',dat[0].meta.endtime)

    plots.plotmicrobarom(dat[p.ind], pp, decimate=p.decimate)

    show()
