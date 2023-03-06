#!/usr/bin/env python3

'''MLeDNA
MLeDNA: selecting combinations of eDNA metabarcoding primers
'''

__author__ = 'Tao Zhu'
__copyright__ = 'Copyright 2023'
__license__ = 'GPL'
__version__ = '0.1'
__email__ = 'zhutao.bioinfo@gmail.com'
__status__ = 'Development'

import argparse
import re
import sys
import os
import json

from operator import itemgetter

from MLeDNA.core import pipeline

parser = argparse.ArgumentParser(description='MLeDNA: selecting combinations of eDNA metabarcoding primers', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('amplicons', help='a four-column-amplicon table in TSV format. Do not use non-word characters. <Primer> <SeqID> <Species> <Seq>')
parser.add_argument('-d', '--threshold-diff', help='minimum DNA difference required for nearest siblings', type=int, default=1)
parser.add_argument('-p', '--primers', help='preferred primers separated by comma. eg. primer1,primer2', default='any')
parser.add_argument('-n', '--threshold-num', help='maximum number of selected primers.', type=int, default=5)
parser.add_argument('-t', '--threads', help='number of CPUs', type=int, default=4)
parser.add_argument('-o', '--output-dir', help='directory for output', default='MLeDNAResult')
args = parser.parse_args()

def main():
    taxID2seq = {}
    red_species = set()
    primer2lengthes = {}
    with open(args.amplicons) as in_handle:
        for line in in_handle:
            if line.startswith('#'):
                continue
            (primer_name, seqid, tax, seq) = line.strip().split('\t')
            primer_name = re.sub('[^\w]+', '_', primer_name)
            seqid = re.sub('[^\w]+', '_', seqid)
            taxID = re.sub('[^\w]+', '_', tax)
            if primer_name not in taxID2seq:
                taxID2seq[primer_name] = {}
                primer2lengthes[primer_name] = []
            if taxID not in taxID2seq[primer_name]:
                taxID2seq[primer_name][taxID] = {}
            if seqid not in taxID2seq[primer_name][taxID]:
                taxID2seq[primer_name][taxID][seqid] = seq
            else:
                print(f'ERROR: duplicate seqID {seqid} in {primer_name} in {taxID}', file=sys.stderr)
                exit(0)
            red_species.add(taxID)
            primer2lengthes[primer_name].append(len(seq))
    workdir = args.output_dir
    if os.path.isdir(workdir) is False:
        os.makedirs(workdir)

    primer2length = {}
    for (primer_name, lengthes) in primer2lengthes.items():
        primer2length[primer_name] = sum(lengthes)/len(lengthes)
    pipeline.run(workdir, red_species, red_species, taxID2seq, primer2length, args.threshold_diff, \
                 args.threshold_num, args.primers, cpu_num=args.threads)
    
    print(f'Finished', file=sys.stderr)

    with open(f'{workdir}/result.json') as in_handle:
        result_data = json.load(in_handle)
        print(f'###########', file=sys.stderr)
        num_taxes = len(result_data['tax_red'])
        print(f'Number of Species: {num_taxes}', file=sys.stderr)
        print(f'###########', file=sys.stderr)
        print(f'Selected Primers', file=sys.stderr)
        rank = 1
        for primer in result_data['selected_primers']:
            addition = 'additional' if rank > 1 else ''
            print(f"{rank}: {primer['name']}, resolve {addition} {primer['num_positive']} species")
            rank += 1
        print(f'###########', file=sys.stderr)
        print(f'Number of Unresolved Species under diff={args.threshold_diff}: {len(result_data["tax_uncovered"])}', file=sys.stderr)
        print(f'###########', file=sys.stderr)
    print(f'See {workdir}/matrix.xlsx for details', file=sys.stderr)
