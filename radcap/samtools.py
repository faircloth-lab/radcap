#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 10 November 2015 14:25 CST (-0600)
"""


import os
import re
import subprocess

from radcap.pth import get_user_param, get_user_path

import pdb


def flagstats(log, bam):
    cmd = [get_user_path("samtools", "samtools"), "flagstat", bam]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    result = re.search("(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n(\d+)\s+.*\n", stdout)
    result = [int(i) for i in result.groups()]
    names = [
        "total",
        "duplicates",
        "mapped",
        "paired",
        "read1",
        "read2",
        "properly_paired",
        "mate_mapped",
        "singletons",
        "diff_chromo",
        "hq_diff_chromo"
    ]
    result = dict(zip(names, result))
    log.info("{},{},{},{},{},{},{}".format(
        os.path.basename(bam),
        result['total'],
        result['duplicates'],
        result['mapped'],
        round(float(result['mapped'])/result['total'] * 100, 2),
        result['mate_mapped'],
        round(float(result['mate_mapped'])/result['mapped'] * 100, 2)
    ))


def index(log, bam):
    sample_dir, sample = os.path.split(bam)
    log.info("Indexing BAM for {}".format(os.path.basename(sample)))
    cmd = [get_user_path("samtools", "samtools"), "index", bam]
    samtools_index_out = os.path.join(sample_dir, '{}.samtools-index.log'.format(sample))
    with open(samtools_index_out, 'w') as samtools_out:
        proc = subprocess.Popen(cmd, stdout=samtools_out, stderr=subprocess.STDOUT)
        proc.communicate()


def faidx(log, fasta):
    sample_dir, sample = os.path.split(fasta)
    log.info("Indexing FASTA for {}".format(os.path.basename(sample)))
    cmd = [get_user_path("samtools", "samtools"), "faidx", fasta]
    samtools_fasta_index_out = os.path.join(sample_dir, '{}.samtools-fasta-index.log'.format(sample))
    with open(samtools_fasta_index_out, 'w') as samtools_out:
        proc = subprocess.Popen(cmd, stdout=samtools_out, stderr=subprocess.STDOUT)
        proc.communicate()
