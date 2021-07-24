#!/usr/bin/env python
import pdb
#pdb.set_trace()
from subprocess import Popen
from argparse import ArgumentParser
import os
import sys
script_path = os.path.dirname(os.path.abspath( __file__ ))
code_path = script_path + "/" 
__author__ = "Maizie&Can@Vandy"
parser = ArgumentParser(description="Author: maiziezhoulab@gmail.com\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bam_file','-bam',help="bam file, called by Longranger/bwa-mem/EMA",required=True)
parser.add_argument('--vcf_file','-v',help="vcf file, called by FreeBayes",required=True)
parser.add_argument('--chr_num','-chr',type=int,help="chromosome number for target variant or region", required=True)
parser.add_argument('--out_dir','-o', help="Directory to store assembly results, default = ./AquilaSV_results",default="./AquilaSV_results")
parser.add_argument('--num_threads','-t_chr',type=int,help="number of threads, default = 8 (recommended)", default=8)
parser.add_argument('--num_threads_for_bwa_mem','-t',type=int,help="number of threads for bwa-mem, default = 20", default=20)
parser.add_argument('--mole_boundary','-mb',type=int,help="We use 50kb to differentiate reads with the same barcode are drawn from different long molecules,50kb for 10X and 20kb for stLFR, default = 50000",default=50000)
parser.add_argument('--clean','-cl',type=int,help="delete intermediate file or not, default = 1", default = 1)

args = parser.parse_args()


def Get_fragment_files(bam_file,vcf_file,chr_start,chr_end,h5_dir,num_threads,cut_limit):
    use_cmd = "python3 " + code_path + "Run_h5_all_multithreads.py" + " --bam_file " + bam_file + " --vcf_file " + vcf_file + " --sample_name " + sample_name + " --chr_start " + str(chr_start) + " --chr_end " + str(chr_end) + " --mbq 13 --mmq 0 --boundary %s "%cut_limit + " --num_threads " + str(num_threads) + " --out_dir " + h5_dir
    Popen(use_cmd,shell=True).wait()


def Haplotying_fragments(chr_start,chr_end,phased_file_dir,h5_dir,sample_name):
    use_cmd = "python3 " + code_path + "Run_phase_alg_multithreads2.py" + " --chr_start " + str(chr_start) + " --chr_end " + str(chr_end) + " --overlap_threshold 3 --support_threshold 5 " + " --out_dir " + phased_file_dir  + " --h5_dir " + h5_dir + " --sample_name " + sample_name
    Popen(use_cmd,shell=True).wait()


def Get_fastq_files_total(bam_file,chr_start,chr_end,num_threads,Raw_fastqs_dir,Sorted_bam_dir):
    use_cmd = "python3 " + code_path + "Read_fastqs_from_sortedbam_v2.py " + " --num_threads " + str(num_threads) + " --chr_start " + str(chr_start) + " --chr_end " + str(chr_end) + " --out_dir " + Raw_fastqs_dir + " --bam_file " + bam_file + " --bam_dir " + Sorted_bam_dir
    Popen(use_cmd,shell=True).wait()


def Extract_reads_for_small_chunks(chr_start,chr_end,h5_dir,phased_file_dir,Local_Assembly_dir,Raw_fastqs_dir,sample_name,num_threads):
    use_cmd = "python3 " + code_path + "Run_extract_reads_for_smallchunks_all_lessmem.py" + " --phase_cut_folder " + phased_file_dir + " --chr_start " + str(chr_start) + " --chr_end " + str(chr_end) + " --out_dir " + Local_Assembly_dir + " --h5_folder " + h5_dir +  " --fastq_folder " + Raw_fastqs_dir  + " --sample_name " + sample_name + " --num_threads " +   str(num_threads)
    Popen(use_cmd,shell=True).wait()

def delete_files(del_dir):
    del_cmd = "rm -r "+del_dir
    Popen(del_cmd, shell= True).wait()
    return()


def main():
    if len(sys.argv) == 1:
        Popen("python3 " + "AquilaSV_step1.py -h",shell=True).wait()
    else:
        bam_file = args.bam_file
        vcf_file = args.vcf_file
        chr_start = args.chr_num
        chr_end = args.chr_num
        #block_len_use = args.block_len_use
        #block_threshold = args.block_threshold
        cut_limit = args.mole_boundary
        num_threads = int(args.num_threads)
        num_threads_for_bwa_mem = int(args.num_threads_for_bwa_mem)
        #sample_name = args.sample_name
        global sample_name
        sample_name = "target"
        deletion_mode = args.clean
        h5_dir = args.out_dir + "/H5_for_molecules/"
        phased_file_dir = args.out_dir + "/results_phased_probmodel/"
        Raw_fastqs_dir = args.out_dir + "/Raw_fastqs_chr" + str(chr_start) + "_" + str(chr_end) +  "/"
        Sorted_bam_dir = args.out_dir + "/sorted_bam/"
        Local_Assembly_dir = args.out_dir + "/Local_Assembly_by_chunks/"
        
        Get_fragment_files(bam_file,vcf_file,chr_start,chr_end,h5_dir,num_threads,cut_limit)
        Haplotying_fragments(chr_start,chr_end,phased_file_dir,h5_dir,sample_name)
        
        Get_fastq_files_total(bam_file,chr_start,chr_end,num_threads_for_bwa_mem,Raw_fastqs_dir,Sorted_bam_dir)
        Extract_reads_for_small_chunks(chr_start,chr_end,h5_dir,phased_file_dir,Local_Assembly_dir,Raw_fastqs_dir,sample_name,12)
        #with open(h5_dir+"log",'w') as f:
         #   f.write(str(deletion_mode))
        if deletion_mode==1:
            #with open(h5_dir+"log",'a') as f:
             #   f.write("del")
       
            delete_files(Sorted_bam_dir)
            delete_files(Raw_fastqs_dir)
            del_cmd = "find %s -type f ! -name '*.phased_final' -delete"%phased_file_dir
            Popen(del_cmd,shell=True).wait()
    
    
if __name__ == "__main__":
    main()
