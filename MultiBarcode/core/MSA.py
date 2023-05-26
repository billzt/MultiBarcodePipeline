import os
import multiprocessing as mp
import time
import sys

def runSingle(input_file:str)->bool:
    os.system(f'mafft --thread -1 --quiet --treeout {input_file} >{input_file}.result')
    return True

def callback_error(result):
    print('error', result.__cause__, flush=True)

def run(workdir:str, cpu_num: int, taxID2seq: dict, prefer_primers='any', threshold_num=5, current_message='', reuse_seq=False, debug=False):
    if os.path.isdir(f'{workdir}/aln') is False:
        os.system(f'mkdir {workdir}/aln')
    
    pool = mp.Pool(processes=cpu_num)
    multi_res = []
    if prefer_primers == 'any' or threshold_num > len(prefer_primers.split(',')):
        needed_primers = taxID2seq.keys()
    else:
        needed_primers = prefer_primers.split(',')
    for primer in needed_primers:
        seq_num = 0
        if reuse_seq == True and os.path.isfile(f'{workdir}/aln/{primer}.aln.fa.tree.json'):
            continue
        if primer in taxID2seq:
            with open(f'{workdir}/aln/{primer}.aln.fa', mode='w') as out_handle:
                for taxID in taxID2seq[primer].keys():
                    for (seqID, seq) in taxID2seq[primer][taxID].items():
                        print(f'>{seqID}-{taxID}\n{seq}', file=out_handle)
                        seq_num += 1
            if seq_num > 1:
                input_file = f'{workdir}/aln/{primer}.aln.fa'
                multi_res.append(pool.apply_async(runSingle, args=(input_file,), error_callback=callback_error))
    
    while True:
        complete_count = len([x for x in multi_res if x.ready()])
        all_num = len(multi_res)
        current_message = f'Sequence alignment: {complete_count}/{all_num} barcodes finished'
        if debug==True:
            print(current_message, file=sys.stderr)
        if complete_count >= all_num:
            break
        time.sleep(0.5)