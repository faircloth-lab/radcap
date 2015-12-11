#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 11 December 2015 12:17 CST (-0600)
"""

import os
import argparse
import ConfigParser

from Bio import SeqIO

from radcap import gatk

from radcap.log import setup_logging
from radcap.helpers import FullPaths, is_dir, is_file
from radcap.raw_reads import get_input_files

import pdb


def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Get coverage across alignments"""
    )
    parser.add_argument(
        "--input-bam",
        required=True,
        action=FullPaths,
        default=None,
        help="""The input directory containing BAM files"""
    )
    parser.add_argument(
        "--input-reference",
        required=True,
        action=FullPaths,
        default=None,
        help="""The input reference sequence (fasta) against which to call SNPs"""
    )
    parser.add_argument(
        "--cores",
        type=int,
        default=1,
        help="""The number of compute cores/threads to use"""
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

def get_interval_file(reference):
    #read_in_sequence_dict and write to top of interval_list file
    sequence_dict = os.path.splitext(reference)[0] + ".dict"
    interval_list = os.path.splitext(reference)[0] + ".interval_list"
    with open(sequence_dict, "rU") as infile:
        with open(interval_list, "w") as outfile:
            for line in infile:
                outfile.write(line)
    # get intervals of reference and write out to interval_list
    with open(interval_list, "a") as outfile:
        for seq in SeqIO.read(reference, "fasta"):
            pdb.set_trace()

def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    get_interval_file(args.input_reference)

    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))

if __name__ == '__main__':
    main()
