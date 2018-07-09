from pathlib import Path
from datetime import datetime, timedelta
import obspy
import pandas


def t2dt(dat):
    """convert SEED time to Python datetime"""
    step = timedelta(seconds=1/dat.meta.sampling_rate)
    t = datetimerange(dat.meta.starttime.datetime, dat.meta.endtime.datetime+step, step)

    return t


def datetimerange(start: datetime, end: datetime, step: timedelta) -> list:
    """like range() for datetime!"""
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i*step for i in range((end-start) // step)]


def readasc(fn: Path, Nrows: int=1000) -> pandas.DataFrame:
    """Use Pandas to load 100s of MB SAC_ASC text data."""
    dat = pandas.read_csv(fn, sep='\s+', nrows=Nrows, skiprows=30)

    return dat


def readseed(fn: Path, tlim: tuple=None):
    """read mSEED format microbarometer data

    fn: path to mSEED data

    https://docs.obspy.org/packages/obspy.io.mseed.html?highlight=mseed#module-obspy.io.mseed
    """

    if tlim is None:
        return obspy.read(str(fn))
    else:
        return obspy.read(str(fn), starttime=tlim[0], endtime=tlim[1])
