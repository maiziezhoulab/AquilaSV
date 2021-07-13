from argparse import ArgumentParser
parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--output_dir','-o')
args = parser.parse_args()
output_dir =  args.output_dir

import numpy as np
import os

fastq_list = [output_dir+path for path in os.listdir(output_dir) if '.fastq' in path]

print('hey',fastq_list)

for fastq_path in fastq_list:
    with open(fastq_path,'r') as f:
        s = f.readlines()
    name_list = [s[i] for i in range(0,len(s),4)]
    block_list = [''.join(s[i:i+4]) for i in range(0,len(s),4)]
    idx = np.argsort(name_list)
    ct = np.unique(name_list,return_counts = True)
    unpaired_name = set(ct[0][ct[1]!=2])
    print('up:',unpaired_name)
    block_list = np.array(block_list)[idx]
    name_list = np.array(name_list)[idx]
    block_list = [ block_list[i] for i in range(len(block_list)) if name_list[i] not in unpaired_name]
    print(len(block_list))
    with open(fastq_path,'w') as f:
        f.writelines(block_list)