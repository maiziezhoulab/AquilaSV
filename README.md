## 2023/10/17 update: AquilaSV is moved to the project "RegionIndel" under "https://github.com/maiziezhoulab/RegionIndel".



# :milky_way: AquilaSV :eagle: 
[![BioConda Install](https://img.shields.io/conda/dn/bioconda/aquilasv.svg?style=flag&label=BioConda%20install)](https://anaconda.org/bioconda/aquilasv)
# Install through Bioconda:
```
conda install AquilaSV
```
(Please ensure <a href="https://bioconda.github.io/user/install.html#set-up-channels">channels</a> are properly setup for bioconda before installing) 

```
AquilaSV_step1 --help
AquilaSV_step2 --help
AquilaSV_step3 --help
```

## Dependencies for Github installation:
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
After running "./install.sh", a folder "source" would be download.

## Running The Code:
Put the "AquilaSV/bin" in the ".bashrc" file, and source the ".bashrc" file <br />
Or just use the fullpath of "**AquilaSV_step1.py**", "**AquilaSV_step2.py**" and "**AquilaSV_step3.py**"

*We provide  <a href="https://github.com/maiziezhoulab/AquilaSV/blob/main/example_data/run_example_data.md">a test example dataset</a> to run the whole pipeline. 


### Step 1: 
```
python3 AquilaSV/bin/AquilaSV_step1.py  --bam_file selected.bam --vcf_file test_freebayes.vcf --chr_num 3 --out_dir test_sv

```
#### *Required parameters

**--bam_file:** "selected.bam" is a bam file generated from BWA-MEM/LongRanger/EMA and samtools. How to get the bam file, you can also check <a href="https://github.com/maiziezhoulab/AquilaSV/blob/master/src/How_to_get_bam_and_vcf.md">here</a>.

**--vcf_file:** "test_freebayes.vcf" is a VCF file generated from variant caller like "FreeBayes". How to get the vcf file, you can also check <a href="https://github.com/maiziezhoulab/AquilaSV/blob/master/src/How_to_get_bam_and_vcf.md">here</a>. 

**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.


#### *Optional parameters
**--mole_boundary:** default = 50000 (50kb). We use 50kb to differentiate reads with the same barcode are drawn from different long molecules. 

**--out_dir:** default = ./AquilaSV_results. You can define your own folder name.

**--num_threads:** default = 8. 

**--num_threads_bwa_mem:** number of threads for bwa-mem, default = 20

**--clean:** default = 1. It will delete all assembly files from SPAdes and intermediate bam/fastq files from AquilaSV.



### Step 2: 
```
python3 AquilaSV/bin/AquilaSV_step2.py --out_dir test_sv --chr_num 3 --reference genome_hg19.fa

```
#### *Required parameters
**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.

**--reference:** "genome_hg19.fa" is the human reference fasta file.

#### *Optional parameters
**--out_dir:** default = ./AquilaSV_results, make sure it's the same as "--out_dir" from ***Step1*** if you want to define your own output directory name.

**--num_threads:** default = 10, this determines the number of files assembled simultaneously by SPAdes.  

**--num_threads_spades:** default = 5, this is the "-t" for SPAdes. 



### Step 3: 
```
python3 AquilaSV/bin/AquilaSV_step3.py  --assembly_dir test_sv  --ref_file genome_hg19.fa  --chr_num 3 

```
#### *Required parameters
**--assembly_dir:** folder to store assembly results from step1 and step2 (same as "--out_dir" for step1 and step2).

**--ref_file:** "genome_hg19.fa" is the human reference fasta file.

**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.

#### *Optional parameters
**--out_dir:** default = ./AquilaSV_Step3_Results. Directory to store the final VCF file from AquilaSV, and you can define your own folder name

**--var_size:** default = 1, variant size, cut off size for indel and SV, 

**--num_of_threads:** number of threads, default = 1

**--clean:** default = 1. You can choose to delete 
diate files or no



#### Memory/Time Usage For AquilaSV
Coverage| Memory| Time for one SV on a single node 
--- | --- | --- | 
60X | 20GB | 00:10:32 |


## Final Output:
**test_sv/AquilaSV_step3_results:** Aquila_contig_final.vcf
```
test_sv
|
|-H5_for_molecules 
|   └-target_chr3_sorted.h5    --> (molecule files for target region including barcode, variants annotation (0: ref allele; 1: alt allele), coordinates for each molecule)
|
|-results_phased_probmodel
|   └-chr*.phased_final        --> (Phased molecule files)
|
|
|-Local_Assembly_by_chunks
|   └-chr*_files_cutPBHC
|       |-fastq_by_*_*_hp1.fastq                  --> (reads fastq file for haplotype 1)
|       |-fastq_by_*_*_hp2.fastq                  --> (reads fastq file for haplotype 2)
|       
|
|-Assembly_Contigs_files
|    |-Aquila_Contig_chr*.fasta                    --> (final contigs fasta file for the target region)
|    |-Aquila_Contig_chr*.bam                      --> (final contigs bam file for the target region)
|    |-Aquila_Contig_chr*_hp1.fasta                     --> (final contigs fasta file for haplotype 1)
|    └-Aquila_Contig_chr*_hp2.fasta                     --> (final contigs fasta file for haplotype 2)
|
└-AquilaSV_step3_results
     └-AquilaSV_Contig_final.vcf --> (final VCF including SNPs, small Indels and SVs)
     
     
```

## Final contig bam file (Aquila_Contig_chr*.bam) diplayed in IGV (SV + 25kb left and right flanking regions):
<p align="center">
	<img src="src/igv1.png"  width="650">
</p>

## Cite RegionIndel 
C. Luo, B. A. Peters, X. M. Zhou. Large indel detection in region-based phased diploid assemblies from linked-reads. BMC Genomics (2025) 26:263. 

## Troubleshooting:
##### Please submit issues on the github page for <a href="https://github.com/maiziezhoulab/AquilaSV/issues">AquilaSV</a>. 


