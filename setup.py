#!/usr/bin/env python


install_requires = ['obspy','cartopy']
tests_require = ['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='pymicrobarometer',
      packages=find_packages(),
      version = '0.1.0',
      description='Read SEED microbarometer data and plot.',
      long_description=open('README.rst').read(),
      author = 'Michael Hirsch, Ph.D.',
      url = 'https://github.com/scivision/pymicrobarometer',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 3 - Alpha',
      'Topic :: Scientific/Engineering :: GIS',
      'Programming Language :: Python',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plot':['matplotlib']},
      python_requires='>=3.6', 
	  )

