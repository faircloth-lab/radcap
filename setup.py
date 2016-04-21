#!/usr/bin/env python
# encoding: utf-8

import glob
from distutils.core import setup

binaries = ["{}".format(i) for i in glob.glob("bin/*")]

scrpt = []
scrpt.extend(binaries)

setup(
    name='radcap',
    version='1.0.0',
    description='software for processing RADcap data using BWA/Picard/GATK',
    url='https://github.com/faircloth-lab/radcap',
    author='Brant C. Faircloth',
    author_email='borg@faircloth-lab.org',
    license='BSD',
    platforms='any',
    packages=[
        'radcap',
    ],
    data_files=[('config', ['config/radcap.conf'])],
    scripts=scrpt,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    )
