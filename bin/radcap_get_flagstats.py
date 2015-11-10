#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 10 November 2015 14:32 CST (-0600)
"""

import os
import argparse

from radcap import samtools
from radcap.log import setup_logging
from radcap.helpers import FullPaths, is_dir, get_all_bams


import pdb

def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Given an input directory containing bam files, output samtools flagstat info for all BAM files"""
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        action=FullPaths,
        default=None,
        help="""The input directory containing BAM files"""
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


def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    all_bams = get_all_bams(args.input_dir)
    # pretty print taxon status
    text = " samtools flagstat output"
    log.info(text.center(65, "-"))
    log.info("bam,reads,duplicates,mapped,percent-mapped,mate-mapped,percent-mate-mapped")
    for bam in all_bams:
        samtools.flagstats(log, bam)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))


if __name__ == '__main__':
    main()
