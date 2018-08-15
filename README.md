[![Build Status](https://travis-ci.com/scivision/microbarometer.svg?branch=master)](https://travis-ci.com/scivision/microbarometer)
[![Coverage Status](https://coveralls.io/repos/github/scivision/microbarometer/badge.svg?branch=master)](https://coveralls.io/github/scivision/microbarometer?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/rw1e6a967kg499eu?svg=true)](https://ci.appveyor.com/project/scivision/microbarometer)

# Microbarometer read/plot from Python

Easy Python program for reading and plotting SEED microbarometer data.
Uses ObsPy.


## Install

    python -m pip install -e .

If you have trouble installing PROJ.4, try

    conda install cartopy


## Usage

```python
import microbarometer as mb

data = mb.load('myfile.asc')
```

### Data format

ObsPy is mostly for MiniSEED, and wasn't able to read the particular `.seed` files we had.
An alternative method is to convert SEED to SAC format:

1. Download
   [rdseed utility](http://ds.iris.edu/ds/nodes/dmc/software/downloads/rdseed/).
   The executable `rdseed.rh6.linux_64` worked for me on Ubuntu as well.
2. extract executable. For Ubuntu:
   ```sh
   tar xf rdseedv*.tar.gz rdseedv*/rdseed.rh6.linux_64
   mv rdseedv*/rdseed* rdseed
   ```
3. convert SEED to SAC, for example to write SAC ASCII (readable by Pandas)
   ```sh
   ../rdseed -f myfile.seed -o 6 -d
   ```
Other output formats are possible via the `-o` option.


## Notes

To get help:
```sh
./rdseed -h
```

channel BDO is "Bottom Pressure" in Pascals.

* Convert SEED to SAC (readable by ObsPy, MatSAC, etc.):
  ```sh
  ./rdseed -f myfile.seed -d
  ```
* List time range of data with `-t` option:
  ```sh
  ./rdseed -f myfile.seed -t
  ```
* Read SEED headers (extensive metadata):
  ```sh
  ./rdseed -f myfile.seed -s
  ```
