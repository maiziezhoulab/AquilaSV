# :milky_way: AquilaSV :eagle: 
[![BioConda Install](https://img.shields.io/conda/dn/bioconda/aquila_stlfr.svg?style=flag&label=BioConda%20install)](https://anaconda.org/bioconda/aquila_stlfr)
# Install through Bioconda (The updated version 1.2.11):
Version <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/src/version_history_tracking.md">history tracking</a> 
```
conda install AquilaSV
```
(Please ensure <a href="https://bioconda.github.io/user/install.html#set-up-channels">channels</a> are properly setup for bioconda before installing) 

```
AquilaSV_step1 --help
AquilaSV_step2 --help
AquilaSV_step3 --help


## Dependencies for Github install:
AquilaSV utilizes <a href="https://www.python.org/downloads/">Python3 (+ numpy, pysam, sortedcontainers, and scipy)</a>, <a href="http://samtools.sourceforge.net/">SAMtools</a>, and <a href="https://github.com/lh3/minimap2">minimap2</a>. To be able to execute the above programs by typing their name on the command line, the program executables must be in one of the directories listed in the PATH environment variable (".bashrc"). <br />
Or you could just run "./install.sh" to check their availability and install them if not, but make sure you have installed "python3", "conda" and "wget" first. 

# Install through Github:

```
git clone https://github.com/maiziex/AquilaSV.git
cd AquilaSV
chmod +x install.sh
./install.sh
```


## source folder:
After running "./install.sh", a folder "source" would be download, it includes human GRCh38 reference fasta file, or you could also just download it by yourself from the corresponding official websites. 

## Running The Code:
Put the "AquilaSV/bin" in the ".bashrc" file, and source the ".bashrc" file <br />
Or just use the fullpath of "**AquilaSV_step1.py**" and "**AquilaSV_step2.py**"

*We provide  <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/example_data/run_example_data.md">a small chromosome (chr21) example dataset</a> to run the whole pipeline before you try it into the large dataset. 

### Step 0:

set input file path and working directory

```
software_path=/data/maiziezhou_lab/CanLuo/Software/AquilaSV/bin
test_dir=/data/maiziezhou_lab/CanLuo/10x/wgs/chr3_fix_50000/SV245_53269957
vcf_file=/data/maiziezhou_lab/Datasets/L5_NA24385_10x/Freebayes_results_hg19/L5_hg19_ref_freebayes.vcf
ref_file=/data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa 
```
**software_path:** this is the directory of AquilaSV
**test_dir:** this is the working directory where all output files will be saved
**vcf_file:** VCF file generated from variant caller like "FreeBayes"
**ref_file:** human reference genome file


### Step 1: 
```
python3 $software_path/AquilaSV_step1.py  --bam_file $test_dir/selected.bam --vcf_file  $vcf_file --cut_limit 50000  --sample_name NA24385 --chr_start 3 --chr_end 3 --out_dir $test_dir/NA24385_stLFR_hg19

```
#### *Required parameters

**--bam_file:** "selected.bam" is bam file generated from bwa-mem. How to get bam file, you can also check <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/src/How_to_get_bam_and_vcf.md">here</a>.

**--vcf_file:** "L5_hg19_ref_freebayes.vcf" is VCF file generated from variant caller like "FreeBayes". How to get vcf file, you can also check <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/src/How_to_get_bam_and_vcf.md">here</a>. 

**--cut_limit:** this is the parameter to adjust the largest distance limit between any two reads within same molecule, default is 50000

**--sample_name:** "NA24385" are the sample name you can define. 



#### *Optional parameters
**--out_dir:** default = ./Asssembly_results. You can define your own folder, for example "Assembly_results_NA24385". 

**--block_threshold:** default = 200000 (200kb)
 
**--block_len_use:** default = 100000 (100kb)

**--num_threads:** default = 8. It's recommended not to change this setting unless large memory node could be used (2*memory capacity(it suggests for assembly below)), then try to use "--num_threads 12". 

**--chr_start --chr_end:**  Since AquilaSV is a region based assembly tool, you should set the two paramters to be the same (your intended chromsome), for exmaple, use "--chr_start 3 --chr_end 3" will only assembly chromosome 3. 
(*Notes: Use 23 for "chrX")

**--deletion_mode:** determine whether you want to delete unnecessary files or not. default = 1 (will delete those files)
If your hard drive storage is limited(AquilaSV could generate a lot of intermediate files), it is suggested to quickly clean some data by setting this to 1. Or you can keep them for some analysis (check the above output directory tree for details). 
#### Memory/Time Usage For Step 1
##### Running Step 1 

Coverage | Memory| Time for chr3（50kb flanking region) on a single node | 
--- | --- | --- | 
90X | 50GB | 01:47 |







### Step 2: 
```
python3 $software_path/AquilaSV_step2.py  --chr_start 3 --chr_end 3 --out_dir $test_dir/NA24385_stLFR_hg19  --num_threads 40 --num_threads_spades 20 --reference  $ref_file

```
#### *Required parameters
**--reference:** "genome.fa" is the reference fasta file you can download by "./install".

#### *Optional parameters
**--out_dir:** default = ./Asssembly_results, make sure it's the same as "--out_dir" from ***Step1*** if you want to define your own output directory name.

**--num_threads:** default = 30, this determines the number of files assembled simultaneously by SPAdes.  

**--num_threads_spades:** default = 5, this is the "-t" for SPAdes. 

**--block_len_use:** default = 100000 (100kb)

**--chr_start --chr_end:** if you only want to assembly some chromosomes or only one chromosome. For example: use "--chr_start 1 --chr_end 2" 


#### Memory/Time Usage For Step 2
##### Running Step 2 
Coverage| Memory| Time for chr1 on a single node | --num_threads | --num_threads_spades|
--- | --- | --- | ---|---|
90X| 50GB | 04:44 |40 | 20|




### Step 3: 
```
python3 $software_path/AquilaSV_step3.py  --assembly_dir $test_dir/NA24385_stLFR_hg19  --ref_file  $ref_file  --num_of_threads 2 --out_dir $test_dir/NA24385_stLFR_hg19/AquilaSV_Step3_Results --var_size 1  --chr_start 3 --chr_end 3 --all_regions_flag 1

```
#### *Required parameters
**--reference:** "genome.fa" is the reference fasta file you can download by "./install".
**--all_regions_flag:** 
#### *Optional parameters



## Final Output:
**Assembly_Results_S12878/Assembly_Contigs_files:** Aquila_contig.fasta and Aquila_Contig_chr*.fasta 
```
Assembly_results_S12878
|
|-H5_for_molecules 
|   └-S12878_chr*_sorted.h5    --> (Fragment files for each chromosome including barcode, variants annotation (0: ref allele; 1: alt allele), coordinates for each fragment)
|
|-HighConf_file
|   └-chr*_global_track.p      --> (Pickle file for saving coordinates of high-confidence boundary points)
|
|-results_phased_probmodel
|   └-chr*.phased_final        --> (Phased fragment files)
|
|-phase_blocks_cut_highconf
|
|-Raw_fastqs
|   └-fastq_by_Chr_*           --> (fastq file for each chromosome)
|
|-ref_dir
|
|-Local_Assembly_by_chunks
|   └-chr*_files_cutPBHC
|       |-fastq_by_*_*_hp1.fastq                  --> (fastq file for a small phased chunk of haplotype 1)
|       |-fastq_by_*_*_hp2.fastq                  --> (fastq file for a small phased chunk of haplotype 2)
|       |-fastq_by_*_*_hp1_spades_assembly        --> (minicontigs: assembly results for the small chunk of haplotype 1) 
|       └-fastq_by_*_*_hp2_spades_assembly        --> (minicontigs: assembly results for the small chunk of haplotype 2)
|
└-Assembly_Contigs_files
    |-Aquila_cutPBHC_minicontig_chr*.fasta        --> (final minicontigs for each chromosome)
    |-Aquila_Contig_chr*.fasta                    --> (final contigs for each chromosome)
    └-Aquila_contig.fasta                         --> (final contigs for WGS)
```

## Final Output Format:
Aquila_stLFR outputs an overall contig file `Aquila_Contig_chr*.fasta` for each chromosome, and one contig file for each haplotype: `Aquila_Contig_chr*_hp1.fasta` and `Aquila_Contig_chr*_hp2.fasta`. For each contig, the header, for an instance, “>36_PS39049620:39149620_hp1” includes contig number “36”, phase block start coordinate “39049620”, phase block end coordinate “39149620”, and haplotype number “1”. Within the same phase block, the haplotype number “hp1” and “hp2” are arbitrary for maternal and paternal haplotypes. For some contigs from large phase blocks, the headers are much longer and complex, for an instance, “>56432_PS176969599:181582362_hp1_ merge177969599:178064599_hp1-177869599:177969599_hp1”. “56” denotes contig number, “176969599” denotes the start coordinate of the final big phase block, “181582362” denotes the end coordinate of the final big phase block, and “hp1” denotes the haplotype “1”. “177969599:178064599_hp1” and “177869599:177969599_hp1” mean that this contig is concatenated from minicontigs in small chunk (start coordinate: 177969599, end coordinate: 178064599, and haplotype: 1) and small chunk (start coordinate: 177869599, end coordinate: 177969599, and haplotype: 1). 



## Assembly Based Variants Calling and Phasing:
##### For example, you can use `Assemlby_results_S12878` as input directory to generate a VCF file which includes SNPs, small Indels and SVs. 



## Aquila assembly for other version of human referece: hg19
##### 1. Download hg19 reference from <a href="https://support.10xgenomics.com/genome-exome/software/downloads/latest">10x Genomics website</a>





### Notes
#### For stLFR assembly or hybrid assembly, stLFR reads with barcode "0_0_0" are removed to get perfect diploid assembly.  


#### Please also check <a href="https://github.com/maiziex/Aquila">Aquila</a> here 

## Troubleshooting:
##### Please submit issues on the github page for <a href="https://github.com/maiziex/Aquila_stLFR/issues">Aquila_stLFR</a>. 
##### Or contact with me through <a href="maizie.zhou@vanderbilt.edu">maizie.zhou@vanderbilt.edu</a>

