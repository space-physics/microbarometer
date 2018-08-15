from pathlib import Path
import pandas
import numpy as np
from typing import Tuple
from datetime import datetime
try:
    import obspy
except ImportError:
    obspy = None


def load(fn: Path, tlim: Tuple[datetime, datetime]=None) -> np.ndarray:

    if fn.suffix.lower().endswith('asc'):
        dat = readasc(fn, 1000)
    elif fn.suffix in ('.SAC', '.seed', '.mseed'):
        dat = readseed(fn, tlim=tlim)
    else:
        raise ValueError(f'unknown format file: {fn}')

    return dat


def readasc(fn: Path, Nrows: int) -> pandas.DataFrame:
    """Use Pandas to load 100s of MB SAC_ASC text data."""
    dat = pandas.read_csv(fn, sep='\s+', nrows=Nrows, skiprows=30)

    return dat


def readseed(fn: Path, tlim: Tuple[datetime, datetime]=None):
    """read mSEED format microbarometer data

    fn: path to mSEED data

    https://docs.obspy.org/packages/obspy.io.mseed.html?highlight=mseed#module-obspy.io.mseed
    """
    if obspy is None:
        raise ImportError('pip install obspy')

    if tlim is None:
        return obspy.read(str(fn))
    else:
        return obspy.read(str(fn), starttime=tlim[0], endtime=tlim[1])
