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

from Bio import SeqIO

from radcap import gatk

from radcap.log import setup_logging
from radcap.helpers import FullPaths, is_dir, CreateDir

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
        "--output-dir",
        required=True,
        action=CreateDir,
        default=None,
        help="""The output directory in which to store the resulting log files and SNP calls"""
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


def get_interval_file(log, reference):
    log.info("Creating .intervals_list file from input radnome")
    #read_in_sequence_dict and write to top of interval_list file
    sequence_dict = os.path.splitext(reference)[0] + ".dict"
    interval_list = os.path.splitext(reference)[0] + ".interval_list"
    with open(sequence_dict, "rU") as infile:
        with open(interval_list, "w") as outfile:
            for line in infile:
                outfile.write(line)
    # get intervals of reference and write out to interval_list
    with open(interval_list, "a") as outfile:
        for seq in SeqIO.parse(reference, "fasta"):
            # need 1-indexed position
            start = str(seq.seq).find("N") + 1
            end = str(seq.seq).rfind("N") + 1
            outfile.write("{}\t{}\t{}\t+\t{}\n".format(
                seq.id,
                "1",
                start,
                seq.id
            ))
            outfile.write("{}\t{}\t{}\t+\t{}\n".format(
                seq.id,
                end,
                len(seq),
                seq.id
            ))
    return interval_list


def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    interval_list = get_interval_file(log, args.input_reference)
    # get coverage
    gatk.coverage(log, args.input_reference, args.input_bam, interval_list, args.output_dir)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))

if __name__ == '__main__':
    main()
