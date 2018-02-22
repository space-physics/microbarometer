from pathlib import Path
import obspy
import pandas


def readasc(fn:Path):
    """Use Pandas to load 100s of MB SAC_ASC text data."""
    dat = pandas.read_csv(fn, sep='\s+', nrows=1000, skiprows=30)

    return dat

def readseed(fn:Path):
    """read SEED format microbarometer data

    datadir: path to SEED data or filename

    """

    return obspy.read(str(fn), debug_headers=True)
