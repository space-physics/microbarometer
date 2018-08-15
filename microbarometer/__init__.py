from datetime import datetime, timedelta
from .io import load  # noqa: F401


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
