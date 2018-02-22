from pathlib import Path
from datetime import datetime, timedelta
import obspy
import pandas

def t2dt(dat):
    """convert SEED time to Python datetime"""
    step = timedelta(seconds=dat.meta.sampling_rate)
    t = datetimerange(dat.meta.starttime.datetime, dat.meta.endtime.datetime+step, step)

    return t


def datetimerange(start:datetime, end:datetime, step:timedelta) -> list:
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i*step for i in range((end-start) // step)]


def readasc(fn:Path, Nrows:int=1000):
    """Use Pandas to load 100s of MB SAC_ASC text data."""
    dat = pandas.read_csv(fn, sep='\s+', nrows=Nrows, skiprows=30)

    return dat

def readseed(fn:Path):
    """read SEED format microbarometer data

    datadir: path to SEED data or filename

    https://docs.obspy.org/packages/obspy.io.mseed.html?highlight=mseed#module-obspy.io.mseed
    """

    return obspy.read(str(fn), debug_headers=True)
