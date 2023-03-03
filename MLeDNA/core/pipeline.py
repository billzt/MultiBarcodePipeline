import os
import json
import sys

from glob import glob

from MLeDNA.core import MSA, sibling, matrix

def rescue_num(primer:str, uncovered_taxes:set, primer2goodtax:dict) -> int:
    taxes_for_this_primer = primer2goodtax[primer] if primer in primer2goodtax else set()
    rescue_from_uncovered_taxes = taxes_for_this_primer & uncovered_taxes
    return len(rescue_from_uncovered_taxes)

def run(workdir:str, red_species:set, other_species:set, taxID2seq:dict, primer2length:dict, \
    threshold_diff=8, threshold_num=5, prefer_primers='any', \
    current_task='', current_message='', debug=True, cpu_num=8):
    (previous_red_species, previous_other_species) = (set(), set())

    if os.path.isfile(f'{workdir}/previous_data.json'):
        with open(f'{workdir}/previous_data.json') as in_handle:
            previous_data = json.load(in_handle)
            previous_red_species = set(previous_data['red_taxID'])
            previous_other_species = set(previous_data['other_taxID'])
    
    current_task = ''
    current_message = ''

    # Step 1: Multiple Sequence Alignment
    if (red_species | other_species).issubset(previous_red_species | previous_other_species):
        reuse_seq = True
    else:
        reuse_seq = False
    
    current_task = f'Step 1: Fetch Barcodes and Conduct Multiple Sequence Alignment'
    if debug==True:
        print(current_task, file=sys.stderr)

    MSA.run(workdir, cpu_num, taxID2seq, prefer_primers, threshold_num, current_message, reuse_seq, debug)

    # Step 2: Find Siblings
    if red_species.issubset(previous_red_species) and other_species == previous_other_species:
        reuse_seq = True
    else:
        reuse_seq = False
    current_task = f'Step 2: Find Siblings for Each Target Species'
    if debug==True:
        print(current_task, file=sys.stderr)
    sibling.run(workdir, red_species, other_species, prefer_primers, threshold_num, current_message, reuse_seq, debug)

    # Step 3: Find Best Locus Combination
    current_task = f'Step 3: Find Best Locus Combination'
    if debug==True:
        print(current_task, file=sys.stderr)
    primer2goodtax = {}
    primer2rescue_num = {}
    all_siblings_data = []
    for file in glob(f'{workdir}/aln/*.json'):
        with open(file) as in_handle:
            for sibling_record in json.load(in_handle):
                all_siblings_data.append(sibling_record)
                if sibling_record['distance'] < threshold_diff:
                    continue
                primer = sibling_record['primer']
                if primer not in primer2goodtax:
                    primer2goodtax[primer] = set()
                primer2goodtax[primer].add(sibling_record['tax'])

    selected_primers = []
    if prefer_primers != 'any':
        selected_primers = prefer_primers.split(',')
    uncovered_taxes = red_species
    for selected_primer in selected_primers:
        if selected_primer in primer2goodtax:
            primer2rescue_num[selected_primer] = len(uncovered_taxes & primer2goodtax[selected_primer])
            uncovered_taxes = uncovered_taxes - primer2goodtax[selected_primer]
    for i in range(threshold_num - len(selected_primers)):
        remain_primers = {x for x in taxID2seq.keys() if x not in selected_primers}
        if len(remain_primers) == 0:
            break
        best_primer = max(remain_primers, key=lambda ele:(rescue_num(ele, uncovered_taxes, primer2goodtax), -primer2length[ele]))
        new_uncovered_taxes = uncovered_taxes - primer2goodtax[best_primer]
        primer2rescue_num[best_primer] = len(uncovered_taxes & primer2goodtax[best_primer])
        if uncovered_taxes == new_uncovered_taxes:
            break
        else:
            selected_primers.append(best_primer)
            uncovered_taxes = new_uncovered_taxes
    with open(f'{workdir}/result.json', mode='w') as out_handle:
        print(json.dumps({'tax_red': list(red_species),
        'tax_other': list(other_species),
        'selected_primers': [{'name':x, 'num_positive': primer2rescue_num[x]} for x in selected_primers],
        'tax_uncovered': list(uncovered_taxes)}, indent=2), file=out_handle)

    # Matrix
    matrix.run(workdir, all_siblings_data, selected_primers, red_species, threshold_diff, uncovered_taxes)

    # store previous species
    if red_species.issubset(previous_red_species) is False:
        previous_red_species = red_species
    if previous_other_species != other_species:
        previous_other_species = other_species
    with open(f'{workdir}/previous_data.json', mode='w') as out_handle:
        json.dump({'red_taxID': list(previous_red_species), \
            'other_taxID': list(previous_other_species)}, out_handle)

