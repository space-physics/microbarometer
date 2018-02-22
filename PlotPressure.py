#!/usr/bin/env python
import pymicrobarometer as pmb





if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory where SEED data files are (or filename)')
    p.add_argument('-ext',help='file suffix of SEED data',default='.seed')
    p = p.parse_args()

    dat = pmb.readseed(p.datadir, p.ext)