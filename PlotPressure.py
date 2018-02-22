#!/usr/bin/env python
from pathlib import Path
import pymicrobarometer as pmb





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

    print(dat)