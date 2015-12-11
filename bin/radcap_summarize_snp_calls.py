#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 11 December 2015 14:24 CST (-0600)
"""

import argparse
from collections import Counter

import numpy

from radcap.log import setup_logging
from radcap.helpers import FullPaths


def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Summarize SNP calls in a VCF file"""
    )
    parser.add_argument(
        "--input-vcf",
        required=True,
        action=FullPaths,
        default=None,
        help="""The input directory containing BAM files"""
    )
    return parser.parse_args()


def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    cnt_loci = Counter()
    cnt_status = Counter()
    with open(args.input_vcf, 'r') as infile:
        for line in infile:
            if line.startswith("#"):
                pass
            else:
                ls = line.strip().split("\t")
                cnt_loci[ls[0]] += 1
                cnt_status[ls[6]] += 1
    snps_per_locus = numpy.array([v[1] for v in cnt_loci.iteritems()])
    ordered_status = cnt_status.keys()
    ordered_status.sort()
    for status in ordered_status:
        log.info("SNPs with {}\t\t= {}".format(cnt_status[status]))
    log.info("Mean SNPs per locus\t\t = {}".format(numpy.mean(snps_per_locus)))
    log.info("95 CI SNPs per locus\t\t = {}".format(1.96 * (numpy.std(snps_per_locus, ddof=1) / numpy.sqrt(len(snps_per_locus)))))
    log.info("Max SNPs per locus\t\t = {}".format(numpy.min(snps_per_locus)))
    log.info("Min SNPs per locus\t\t = {}".format(numpy.max(snps_per_locus)))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))


if __name__ == '__main__':
    main()
