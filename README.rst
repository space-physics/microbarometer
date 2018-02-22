==================
PyMicrobarometer
==================

Easy Python program for reading and plotting SEED microbarometer data.
Uses ObsPy.

Data
====
Unfortunately, ObsPy is mostly for MiniSEED, and wasn't able to read the particular .seed files we had.
An alternative method is to convert SEED to SAC format by the
`rdseed utility <http://ds.iris.edu/ds/nodes/dmc/software/downloads/rdseed/>`_.

The executable ``rdseed.rh6.linux_64`` worked for me on Ubuntu as well--use the ``-d`` option to convert SEED to SAC.
Other output formats are possible via the ``-o`` option.




Install
=======
::

    python -m pip install -e .


Usage
=====

To get help::

    ./rdseed.rh6.linux_64 -h

* channel BDO is "Bottom Pressure" in Pascals.


Convert SEED to SAC (readable by ObsPy, MatSAC, etc.)::

    rdseed.rh6.linux_64 -f myfile.seed -d

List time range of data with ``-t`` option::

    ./rdseed.rh6.linux_64 -f myfile.seed -t


Read SEED headers (extensive metadata)::

    ./rdseed.rh6.linux_64 -f myfile.seed -s


