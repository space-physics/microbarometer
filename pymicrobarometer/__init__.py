from pathlib import Path
import obspy


def readseed(datadir:Path, ext:str):
    """read SEED format microbarometer data

    datadir: path to SEED data or filename
    ext: filename suffix to search for

    """

    if isinstance(datadir,(str,Path)):
        datadir = Path(datadir).expanduser()
        if datadir.is_dir():
            flist = datadir.glob('*.seed')
        elif datadir.is_file():
            flist = [datadir]
        else:
            raise FileNotFoundError(f'No SEED data in {datadir}')
    else: # list of files
        flist = [Path(d).expanduser() for d in datadir]
# %% read data

    dat = []
    for f in flist:
        try:
            dat.append(obspy.read(str(f)))
        except Exception as e:
            print(f,e)