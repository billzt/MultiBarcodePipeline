import os
import re
import json
import sys
import time
from glob import glob
import multiprocessing as mp

import distance
import treeswift
from Bio.SeqIO.FastaIO import SimpleFastaParser


# m:ss): 2:33.32 -> 0:23.72

def distance_without_gap(seq1:str, seq2:str)->int:
    dis = 0
    for i in range(0, len(seq1)):
        if seq1[i] != '-' and seq2[i] != '-' and seq1[i] != seq2[i]:
            dis += 1
    return dis

def callback_error(result):
    print('error', result.__cause__, flush=True)

def runSingle(aln_file:str, red_species:set, other_species:set)->bool:
    siblings = []
    tree_file = aln_file.replace('.result', '.tree')
    primer = os.path.basename(aln_file).split('.')[0]
    seqid2aligned_seq = {}
    red_taxid2seqids = {}
    with open(aln_file) as in_handle:
        for (title, seq) in SimpleFastaParser(in_handle):
            (seqid, taxid) = title.split('-')
            seqid2aligned_seq[seqid] = seq
            if taxid in red_species:
                if taxid not in red_taxid2seqids:
                    red_taxid2seqids[taxid] = set()
                red_taxid2seqids[taxid].add(seqid)
    clean_tree = ''
    with open(tree_file) as in_handle:
        for line in in_handle:
            clean_tree += re.sub('^\d+_', '', line.strip())
    with open(tree_file+'.clean', mode='w') as out_handle:
        print(clean_tree, file=out_handle)
    tree_handle = treeswift.read_tree_newick(tree_file+'.clean')
    martix = tree_handle.distance_matrix(leaf_labels=True)
    for (taxid, seqids) in red_taxid2seqids.items():
        if len(seqids) > 0:
            (min_id_1, min_id_2, min_tax_2, min_dis) = ('', '', '', 1e6)
            for seqid in seqids:
                distance_value_for_other_species = [(x,y) for (x,y) in martix[f'{seqid}-{taxid}'].items() if x.split('-')[1] in other_species and x.split('-')[1] != taxid]
                if len(distance_value_for_other_species) > 0:
                    (sibling, sibling_dis) =  min(distance_value_for_other_species, key=lambda item: item[1])
                else:
                    continue
                if sibling_dis < min_dis:
                    (min_id_1, min_dis) = (seqid, sibling_dis)
                    (min_id_2, min_tax_2) = sibling.split('-')
            if min_id_1 != '':
                seq_1 = seqid2aligned_seq[min_id_1]
                seq_2 = seqid2aligned_seq[min_id_2]
                distance_1 = distance_without_gap(seq_1, seq_2)
                seq_1 = seq_1.replace('-', '')
                seq_2 = seq_2.replace('-', '')
                distance_2 = distance.levenshtein(seq_1, seq_2)
                siblings.append({
                    'primer':primer,
                    'tax': taxid,
                    'seqid': min_id_1,
                    'sibling_tax': min_tax_2,
                    'sibling_seqid': min_id_2,
                    'distance': min(distance_1, distance_2)
                })
    with open(tree_file+'.json', mode='w') as out_handle:
        print(json.dumps(siblings, indent=2), file=out_handle)
    return True


def run(workdir:str, red_species:set, other_species:set, prefer_primers='any', threshold_num=5, current_message='', reuse_seq=False, debug=False, cpu_num=8):
    pool = mp.Pool(processes=cpu_num)
    multi_res = []
    if prefer_primers == 'any' or threshold_num > len(prefer_primers.split(',')):
        needed_primers = [os.path.basename(x).split('.')[0] for x in glob(f'{workdir}/aln/*.result')]
    else:
        needed_primers = prefer_primers.split(',')
    for primer in needed_primers:
        aln_file = f'{workdir}/aln/{primer}.aln.fa.result'
        if reuse_seq == True and os.path.isfile(f'{workdir}/aln/{primer}.aln.fa.tree.json'):
            continue
        if os.path.isfile(aln_file):
            multi_res.append(pool.apply_async(runSingle, args=(aln_file,red_species,other_species,), error_callback=callback_error))

    while True:
        complete_count = len([x for x in multi_res if x.ready()])
        all_num = len(multi_res)
        current_message = f'Tree analysis: {complete_count}/{all_num} barcodes finished'
        if debug==True:
            print(current_message, file=sys.stderr)
        if complete_count >= all_num:
            current_message = 'Finished'
            break
        time.sleep(0.5)
