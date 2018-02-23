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
import cartopy
import seaborn as sns
#
import pymicrobarometer as pmb
import pymicrobarometer.plots as plots

GREF = cartopy.crs.PlateCarree()

Nfft = 1024

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
    p = p.parse_args()

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

    plots.plotmicrobarom(dat[p.ind], not p.nomap, yminmax=p.yminmax, decimate=p.decimate)

    show()
