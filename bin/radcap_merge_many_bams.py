#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 10 November 2015 15:35 CST (-0600)
"""


import os
import argparse

from radcap import picard
from radcap.log import setup_logging
from radcap.helpers import FullPaths, CreateDir, is_dir, get_all_bams

def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Given an input directory of BAMS, merge them all into a single monolithic BAM"""
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        action=FullPaths,
        default=None,
        help="""The input directory containing BAM files"""
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        action=CreateDir,
        default=None,
        help="""The output directory in which to store the merged BAM"""
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
    parser.add_argument(
        "--follow-links",
        action="store_true",
        default=False,
        help="""Follow symlinks""",
    )
    return parser.parse_args()


def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    all_bams = get_all_bams(args.input_dir, args.follow_links)
    sample = os.path.basename(args.input_dir)
    picard.merge_many_bams(log, sample, all_bams, args.output_dir)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))


if __name__ == '__main__':
    main()
