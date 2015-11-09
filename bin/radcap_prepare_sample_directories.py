#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 09 November 2015 10:16 CST (-0600)
"""

import re
import os
import glob
import argparse
from itertools import tee, izip

from radcap.log import setup_logging
from radcap.helpers import FullPaths, CreateDir, is_dir, is_file

import pdb


def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Prepare a directory of file for radcap processing"""
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        action=FullPaths,
        default=None,
        help="""The directory holding the de-muxed, de-cloned radcap sequence reads"""
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        action=CreateDir,
        default=None,
        help="""The directory to hold the prepared sample read files"""
    )
    parser.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="""The logging level to use"""
    )
    parser.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="""The path to a directory to hold logs."""
    )
    return parser.parse_args()


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)


def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    log.info("Output files are in {}".format(args.output_dir))
    reads = glob.glob("{}/*.fq.gz".format(args.input_dir))
    reads.sort()
    read_pairs = pairwise(reads)
    for sample in read_pairs:
        read_1_filename = os.path.basename(sample[0])
        read_2_filename = os.path.basename(sample[1])
        read_1_sample_name = re.search("(.*).\d.\d.fq.gz", read_1_filename).groups()[0]
        read_2_sample_name = re.search("(.*).\d.\d.fq.gz", read_2_filename).groups()[0]
        #pdb.set_trace()
        assert read_1_sample_name == read_2_sample_name, IOError("Input fastq names do not match (or reads are not paired)")
        sample_name = read_1_sample_name
        log.info("Creating output and symlinking {}".format(sample_name))
        outdir = os.path.join(args.output_dir, sample_name)
        os.mkdir(outdir)
        for fastq in sample:
            os.symlink(
                fastq, os.path.join(outdir, os.path.basename(fastq))
                )
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))




if __name__ == '__main__':
    main()
