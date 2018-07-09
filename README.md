# PyMicrobarometer

Easy Python program for reading and plotting SEED microbarometer data.
Uses ObsPy.

## Data

Unfortunately, ObsPy is mostly for MiniSEED, and wasn't able to read
the particular .seed files we had. An alternative method is to convert
SEED to SAC format by the [rdseed
utility](http://ds.iris.edu/ds/nodes/dmc/software/downloads/rdseed/).

The executable `rdseed.rh6.linux_64` worked for me on Ubuntu as
well--use the `-d` option to convert SEED to SAC. Other output formats
are possible via the `-o` option.

## Install

    python -m pip install -e .

If you have trouble installing PROJ.4, try

    conda install cartopy


## Usage

To get help:

    ./rdseed.rh6.linux_64 -h

channel BDO is "Bottom Pressure" in Pascals.

* Convert SEED to SAC (readable by ObsPy, MatSAC, etc.):
  ```sh
  rdseed.rh6.linux_64 -f myfile.seed -d
  ```
* List time range of data with `-t` option:
  ```sh
  ./rdseed.rh6.linux_64 -f myfile.seed -t
  ```
* Read SEED headers (extensive metadata):
  ```sh
  ./rdseed.rh6.linux_64 -f myfile.seed -s
  ```
