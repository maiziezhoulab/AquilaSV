#!/usr/bin/env python
import pdb
#pdb.set_trace()
import pysam
from collections import defaultdict
from subprocess import Popen
from argparse import ArgumentParser
import os
import time
import pandas as pd
import numpy as np
script_path = os.path.dirname(os.path.abspath( __file__ ))
code_path = script_path + "/" 
parser = ArgumentParser(description="extract fastq files from bam:")
parser.add_argument('--out_dir','-o', help="output folder")
parser.add_argument('--bam_dir','-bam_o', help="bam folder")
parser.add_argument('--bam_file','-bam', help="bam file")
parser.add_argument('--chr_start','-start',type=int,help="chr start", default=1)
parser.add_argument('--chr_end','-end',type=int,help="chr end", default=23)
parser.add_argument('--num_threads','-t',type=int,help="number of threads", default=20)
args = parser.parse_args()
out_dir = args.out_dir
bam_dir = args.bam_dir
chr_start = int(args.chr_start)
chr_end = int(args.chr_end)

if os.path.exists(out_dir):
    print("using existing output folder: " + out_dir)
else:
    os.makedirs(out_dir)

chr_dict = {"chr1":1,"chr2":2,"chr3":3,"chr4":4,"chr5":5,"chr6":6,"chr7":7,"chr8":8,"chr9":9,"chr10":10,"chr11":11,"chr12":12,"chr13":13,"chr14":14,"chr15":15,"chr16":16,"chr17":17,"chr18":18,"chr19":19,"chr20":20,"chr21":21,"chr22":22,"chrX":23}

fw_curr = defaultdict()
for chr_num in range(chr_start, chr_end+1):
    fw_curr[chr_num] = open(out_dir + "fastq_by_Chr_" + str(chr_num),"w")

tab = str.maketrans("ACTGN", "TGACN")

def reverse_complement(seq):
    return seq.translate(tab)[::-1]


def write_pair_reads(prev_read,read,use_chr_num):
    prev_read_seq = prev_read.seq
    prev_read_qual = prev_read.qual
    if prev_read.is_reverse:
        prev_read_seq = reverse_complement(prev_read_seq)
        prev_read_qual = prev_read_qual[::-1]
    read_seq = read.seq
    read_qual = read.qual
    if read.is_reverse:
        read_seq = reverse_complement(read_seq)
        read_qual = read_qual[::-1]
    fw_use = fw_curr[use_chr_num]
    if prev_read.is_read1:
        cur_line = "@" + prev_read.qname + "\n" + prev_read_seq + "\n" + "+\n" + prev_read_qual + "\n" + "@" + read.qname + "\n" + read_seq + "\n" + "+\n" + read_qual + "\n"
        fw_use.write(cur_line)
    elif prev_read.is_read2:
        cur_line = "@" + read.qname + "\n" + read_seq + "\n" + "+\n" + read_qual + "\n" + "@" + prev_read.qname + "\n" + prev_read_seq + "\n" + "+\n" + prev_read_qual + "\n"
        fw_use.write(cur_line)


# def read_fastqs_from_sorted_bam(sorted_bam_file,chr_start,chr_end):
#     sam_file = pysam.AlignmentFile(sorted_bam_file, "rb")
#     count = 0
#     count_unmapped = 0
#     count_line = 0
#     use_chr_dict = defaultdict(int)
#     for ii in range(chr_start,chr_end + 1):
#         use_chr_dict[ii] == 1
#     for read in sam_file.fetch(until_eof=True):
#         if not read.is_secondary:
#             count += 1
#             if count == 2:
#                 if prev_read.is_unmapped and read.is_unmapped:
#                     count_unmapped += 1
#                 else:
#                     chr_name_1 = prev_read.reference_name
#                     chr_name_2 = read.reference_name
#                     if chr_name_1 == chr_name_2:
#                         if chr_name_1 in chr_dict:
#                             use_chr_num = chr_dict[chr_name_1]
#                             if use_chr_num in use_chr_dict:
#                                 write_pair_reads(prev_read,read,use_chr_num)
#                     else:
#                         if chr_name_1 in chr_dict:
#                             use_chr_num = chr_dict[chr_name_1]
#                             if use_chr_num in use_chr_dict:
#                                 write_pair_reads(prev_read,read,use_chr_num)
#                         elif chr_name_2 in chr_dict:
#                             use_chr_num = chr_dict[chr_name_2]
#                             if use_chr_num in use_chr_dict:
#                                 write_pair_reads(prev_read,read,use_chr_num)
#                 count = 0
#             if count == 1:
#                 prev_read = read

def read_fastqs_from_sorted_bam(sorted_bam_file,chr_start,chr_end):
    for chr_num in range(chr_start,chr_end + 1):
        read_fastqs_one_chrom(sorted_bam_file,chr_num)
        
def read_fastqs_one_chrom(sorted_bam_file,chr_num):
    read_pair_dict={}
    sam_file = pysam.AlignmentFile(sorted_bam_file, "rb")
    count = 0

    name_list = []
    read1_list =[]
    read2_list =[]
    mapq_list =[]

    seq_list =[]
    qual_list = []
    #print('luocan chr'+str(chr_num))
    if str(chr_num)=='23':
        chr_num_idx ='X'
    else:
        chr_num_idx = chr_num
    for read in sam_file.fetch('chr'+str(chr_num_idx),until_eof=True):
        # chr_name = read.reference_name
        # if chr_name == 'chr'+str(chr_num):
        if not read.is_secondary:
            
            read_seq=read.seq
            read_qual=read.qual
            read_qname=read.qname
            if read.is_reverse:
                read_seq = reverse_complement(read_seq)
                read_qual = read_qual[::-1]
            #write fastq
            read1 = int(read.is_read1)
            read2 = int(read.is_read2)
            mapq = read.mapping_quality


            name_list.append(read_qname)
            read1_list.append(read1)
            read2_list.append(read2)
            mapq_list.append(mapq)

            seq_list.append(read_seq)
            qual_list.append(read_qual)

    df = pd.DataFrame({'name':name_list,
     'read1':read1_list,
     'read2':read2_list,
     'mapq':mapq_list,
     'seq':seq_list,
     'qual':qual_list})
    
    df['seq_len'] = df.seq.apply(lambda x :len(x))
    df = df.sort_values(['name','read1','mapq','seq_len'],ascending = [True,False,False,False]).reset_index(drop=True)
    #df.to_csv('inf.csv')
    df1 = df.groupby(['name','read1']).head(1)
    #print(df1.shape,'luocan')
    # # df to fastq
    seq_list = df1.seq.values
    qual_list = df1.qual.values
    name_list = df1.name.values

    import numpy as np
    ct = np.unique(name_list,return_counts = True)
    unpaired_name = set(ct[0][ct[1]!=2])

    #s =''
    new_name_list = []
    block_list = []
    for i in range(len(seq_list)):
        if name_list[i] not in unpaired_name:
            new_name_list.append(name_list[i])
            block = '@'+name_list[i]+'\n'+seq_list[i]+'\n+\n'+\
                    qual_list[i]+'\n'
            block_list.append(block)
            #line = '@'+name_list[i]+'\n'+seq_list[i]+'\n+\n'+\
            #qual_list[i]+'\n'
            #s = s+line
    idx = np.argsort(new_name_list)
    block_list = np.array(block_list)[idx]
    s = ''.join(block_list)
    # with open(output_path,'w') as f:
    #     f.write(s)
    fw_use = fw_curr[chr_num]
    fw_use.write(s)

def close_file(chr_start,chr_end):
    for chr_num in range(chr_start, chr_end+1):
        fw_curr[chr_num].close()




if __name__ == "__main__":
    bam_file = args.bam_file
    num_threads = int(args.num_threads)
    bam_sorted_idx_file = bam_dir + "finish_bam.txt"
    bam_sorted_file = bam_dir + "sorted_bam.bam"
    if os.path.exists(bam_dir):
        print("using existing output folder: " + bam_dir)
        while not os.path.exists(bam_sorted_idx_file):
            time.sleep(1)
    else:
        os.makedirs(bam_dir)
        try:
            sort_bam_cmd = "samtools sort -@ " + str(num_threads) + " -n " + bam_file + " -o " + bam_sorted_file
        except:
            sort_bam_cmd = code_path + "samtools/" + "samtools sort -@ " + str(num_threads) + " -n " + bam_file + " -o " + bam_sorted_file

        Popen(sort_bam_cmd,shell=True).wait()
        Popen("touch " + bam_dir + "finish_bam.txt",shell=True).wait()
#======================= bam file , bam_sorted_file
    read_fastqs_from_sorted_bam(bam_file,chr_start,chr_end)
    close_file(chr_start,chr_end)

