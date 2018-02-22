#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import figure, show
import obspy
import pymicrobarometer as pmb



def plotmicrobarom(dat,t):
    ax = figure().gca()
    ax.plot(dat[0].times()[:10000],dat[0].data[:10000])
    ax.set_xlabel(f'seconds elapsed since {t[0]}')
    ax.set_ylabel('Pressure [relative]')



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory where SEED data files are (or filename)')
    p.add_argument('-ext',help='file suffix of data',default='.SAC')
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
        elif f.suffix in ('.SAC','.seed'):
            dat = pmb.readseed(f)
            t = obspy.io.mseed.util.get_start_and_end_time(str(f))

    print(dat)
    print(dat[0].stats)
    print(f'shape of data in {f}',dat[0].count(),'from',t[0],'to',t[1])

    plotmicrobarom(dat,t)
    show()