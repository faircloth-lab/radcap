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
import subprocess
from phyluce.pth import get_user_path, get_user_param

#import pdb

JAVA = get_user_param("java", "executable")
JAVA_PARAMS = get_user_param("java", "mem")
JAR_PATH = get_user_path("java", "jar")
GATK = get_user_param("java", "gatk")


def get_merged_intervals(log, reference, bam, cores, output_dir, min_reads=4):
    sample = os.path.basename(bam)
    intervals = os.path.join(output_dir, "{}.intervals".format(sample))
    gatk_merged_intervals = os.path.join(output_dir, '{}.gatk-merged-intervals.log'.format(sample))
    log.info("Calling indel intervals")
    log.warn("These computations can take a LONG time!")
    log.warn("You can run `tail -f` on {} to track progress".format(gatk_merged_intervals))
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "RealignerTargetCreator",
        "-nt",
        str(cores),
        "-R",
        reference,
        "-I",
        bam,
        "--minReadsAtLocus",
        str(min_reads),
        "-o",
        str(intervals)
    ]
    with open(gatk_merged_intervals, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return intervals


def realign_bam(log, reference, bam, intervals, output_dir, lod=3.0):
    sample = os.path.basename(bam)
    realigned_bam = os.path.join(output_dir, "{}.realigned.bam".format(sample))
    gatk_realign_bam = os.path.join(output_dir, '{}.gatk-realign-bam.log'.format(sample))
    log.info("Realigning BAM file based on indel intervals")
    log.warn("These computations can take a LONG time!")
    log.warn("You can run `tail -f` on {} to track progress".format(gatk_realign_bam))
    # wont run in parallel
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "IndelRealigner",
        "-R",
        reference,
        "-I",
        bam,
        "-targetIntervals",
        intervals,
        "-LOD",
        str(lod),
        "-o",
        realigned_bam
    ]
    with open(gatk_realign_bam, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return realigned_bam


def call_snps(log, reference, bam, cores, output_dir, stand_call=30, stand_emit=10):
    sample = os.path.basename(bam)
    raw_snps_vcf = os.path.join(output_dir, "{}.raw-snps.vcf".format(sample))
    gatk_call_snps = os.path.join(output_dir, '{}.gatk-call-snps.log'.format(sample))
    log.info("Calling SNPs in the realigned BAM")
    log.warn("These computations can take a LONG time!")
    log.warn("You can run `tail -f` on {} to track progress".format(gatk_call_snps))
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "UnifiedGenotyper",
        "-nt",
        str(cores),
        "-R",
        reference,
        "-I",
        bam,
        "-gt_mode",
        "DISCOVERY",
        "-stand_call_conf",
        str(stand_call),
        "-stand_emit_conf",
        str(stand_emit),
        "-o",
        raw_snps_vcf
    ]
    with open(gatk_call_snps, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return raw_snps_vcf


def call_indels(log, reference, bam, cores, output_dir, stand_call=30, stand_emit=10):
    sample = os.path.basename(bam)
    raw_indels_vcf = os.path.join(output_dir, "{}.raw-indels.vcf".format(sample))
    gatk_call_indels = os.path.join(output_dir, '{}.gatk-call-indels.log'.format(sample))
    log.info("Calling Indels in the realigned BAM")
    log.warn("These computations can take a LONG time!")
    log.warn("You can run `tail -f` on {} to track progress".format(gatk_call_indels))
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "UnifiedGenotyper",
        "-nt",
        str(cores),
        "-R",
        reference,
        "-I",
        bam,
        "-gt_mode",
        "DISCOVERY",
        "-glm",
        "INDEL",
        "-stand_call_conf",
        str(stand_call),
        "-stand_emit_conf",
        str(stand_emit),
        "-o",
        raw_indels_vcf
    ]
    with open(gatk_call_indels, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return raw_indels_vcf


def variant_filtration(log, reference, bam, raw_snps_vcf, raw_indels_vcf, output_dir, qual=30.0, gq=20.0):
    log.info("Filtering SNP calls (VariantFiltration) for indels and low quality")
    sample = os.path.basename(bam)
    filtered_variants_vcf = os.path.join(output_dir, "{}.filtered-variants.vcf".format(sample))
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "VariantFiltration",
        "-R",
        reference,
        "-I",
        "-V",
        raw_snps_vcf,
        "--mask",
        raw_indels_vcf,
        "--maskExtension",
        "5",
        "--maskName",
        "InDel",
        "--clusterWindowSize",
        "10",
        "--filterExpression",
        "MQ0 >= 4 && ((MQ0 / (1.0 * DP)) > 0.1)",
        "--filterName",
        "Bad Validation",
        "--filterExpression",
        "QUAL < {}".format(qual),
        "--filterName",
        "LowQual",
        "--filterExpression",
        "QD < 2.0",
        "--filterName",
        "Low Variant Confidence",
        "--genotypeFilterExpression",
        "DP < 5.0",
        "--genotypeFilterName",
        "Low Read Depth Over Sample",
        "--genotypeFilterExpression",
        "GQ < {}".format(gq),
        "--genotypeFilterName",
        "Low GenotypeQuality",
        "-o",
        filtered_variants_vcf
    ]
    gatk_filter_variants = os.path.join(output_dir, '{}.gatk-variant-filtration.log'.format(sample))
    with open(gatk_filter_variants, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return filtered_variants_vcf


def coverage(log, reference, bam, intervals_list, output_dir):
    sample = os.path.basename(bam)
    gatk_coverage = os.path.join(output_dir, '{}.gatk-coverage.log'.format(sample))
    log.info("Computing coverage across {}".format(sample))
    log.warn("These computations can take a LONG time!")
    log.warn("You can run `tail -f` on {} to track progress".format(gatk_coverage))
    coverage_output = os.path.join(output_dir, "{}.coverage.tdt".format(sample))
    # wont run in parallel
    cmd = [
        JAVA,
        JAVA_PARAMS,
        "-jar",
        os.path.join(JAR_PATH, GATK),
        "-T",
        "DepthOfCoverage",
        "-R",
        reference,
        "-I",
        bam,
        "-L",
        intervals_list,
        "-o",
        coverage_output,
    ]
    with open(gatk_coverage, 'w') as gatk_out:
        proc = subprocess.Popen(cmd, stdout=gatk_out, stderr=subprocess.STDOUT)
        proc.communicate()
    return coverage_output
