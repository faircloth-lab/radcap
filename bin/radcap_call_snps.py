#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 10 November 2015 16:12 CST (-0600)
"""

import os
import argparse

from radcap import gatk
from radcap import picard
from radcap import samtools
from radcap.log import setup_logging
from radcap.helpers import FullPaths, CreateDir, is_dir

import pdb

def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Use GATK to re-align BAMs, call SNPs, call indels, and filter SNP calls for indels and quality"""
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
        "--cores",
        type=int,
        default=1,
        help="""The number of compute cores/threads to use, when possible"""
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
    reference_dir, reference = os.path.split(args.input_reference)
    pdb.set_trace()
    # create samtools index
    samtools.index(log, args.input_bam)
    samtools.faidx(log, args.input_reference)
    # create picard reference dictionary
    picard.create_reference_dict(log, reference, reference_dir, args.input_reference)
    # run GATK steps
    intervals = gatk.get_merged_intervals(log, args.input_reference, args.input_bam, args.cores, args.output_dir)
    realigned_bam = gatk.realign_bam(log, args.input_reference, args.input_bam, intervals, args.output_dir)
    raw_snps_vcf = gatk.call_snps(log, args.input_reference, realigned_bam, args.cores, args.output_dir)
    raw_indels_vcf = gatk.call_indels(log, args.input_reference, realigned_bam, args.cores, args.output_dir)

if __name__ == '__main__':
    main()
