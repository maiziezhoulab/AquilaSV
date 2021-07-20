# :milky_way: AquilaSV :eagle: 
[![BioConda Install](https://img.shields.io/conda/dn/bioconda/aquila_stlfr.svg?style=flag&label=BioConda%20install)](https://anaconda.org/bioconda/aquila_stlfr)
# Install through Bioconda:
Version <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/src/version_history_tracking.md">history tracking</a> 
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

*We provide  <a href="https://github.com/maiziex/Aquila_stLFR/blob/master/example_data/run_example_data.md">a test example dataset</a> to run the whole pipeline. 


### Step 1: 
```
python3 AquilaSV/bin/AquilaSV_step1.py  --bam_file selected.bam --vcf_file test.vcf --chr_num 3 --out_dir test_sv

```
#### *Required parameters

**--bam_file:** "selected.bam" is a bam file generated from BWA-MEM/LongRanger/EMA. How to get the bam file, you can also check <a href="https://github.com/maiziezhoulab/AquilaSV/blob/master/src/How_to_get_bam_and_vcf.md">here</a>.

**--vcf_file:** "test.vcf" is a VCF file generated from variant caller like "FreeBayes". How to get the vcf file, you can also check <a href="https://github.com/maiziezhoulab/AquilaSV/blob/master/src/How_to_get_bam_and_vcf.md">here</a>. 

**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.


#### *Optional parameters
**--mole_boundary:** default = 50000 (50kb). We use 50kb to differentiate reads with the same barcode are drawn from different long molecules. 

**--out_dir:** default = ./AquilaSV_results. You can define your own folder name.

**--num_threads:** default = 8. 

**--clean:** default = 1. It will delete all assembly files from SPAdes and intermediate bam/fastq files from AquilaSV.

#### Memory/Time Usage For Step 1
##### Running Step 1 

Coverage | Memory| Time for chr3（50kb flanking region) on a single node | 
--- | --- | --- | 
90X | 50GB | 01:47 |


### Step 2: 
```
python3 AquilaSV/bin/AquilaSV_step2.py  --chr_num 3 --out_dir test_sv  --num_threads 40 --num_threads_spades 20 --reference  genome_hg19.fa

```
#### *Required parameters
**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.

**--reference:** "genome_hg19.fa" is the human reference fasta file.

#### *Optional parameters
**--out_dir:** default = ./AquilaSV_results, make sure it's the same as "--out_dir" from ***Step1*** if you want to define your own output directory name.

**--num_threads:** default = 10, this determines the number of files assembled simultaneously by SPAdes.  

**--num_threads_spades:** default = 5, this is the "-t" for SPAdes. 




#### Memory/Time Usage For Step 2
##### Running Step 2 
Coverage| Memory| Time for chr3_53269957 on a single node | --num_threads | --num_threads_spades|
--- | --- | --- | ---|---|
90X| 50GB | 04:44 |40 | 20|


### Step 3: 
```
python3 AquilaSV/bin/AquilaSV_step3.py  --assembly_dir test_sv  --ref_file genome_hg19.fa  --chr_num 3 

```
#### *Required parameters
**--assembly_dir:** folder to store assembly results from step1 and step2 (out_dir for step1 and step2).

**--ref_file:** "genome_hg19.fa" is the human reference fasta file.

**--chr_num:** "3" is the chromosome number you need to define for the target region or the structural variant you are interested in.

#### *Optional parameters
**--out_dir:** default = ./AquilaSV_Step3_Results. Directory to store the final VCF file from AquilaSV, and you can define your own folder name

**--var_size:** default = 1, variant size, cut off size for indel and SV, 

**--num_of_threads:** number of threads, default = 1

**--clean:** default = 1. You can choose to delete intermidiate files or no



#### Memory/Time Usage For Step 3
##### Running Step 3
Coverage| Memory| Time for chr3_53269957 on a single node | --num_threads | 
--- | --- | --- | ---|
90X| 50GB | 03:00 |2 |


## Final Output:
**test_sv/AquilaSV_step3_results:** Aquila_contig_final.vcf
```
NA24385_stLFR_hg19
|
|-H5_for_molecules 
|   └-NA24385_chr3_sorted.h5    --> (Fragment files for interested region including barcode, variants annotation (0: ref allele; 1: alt allele), coordinates for each fragment)
|
|-results_phased_probmodel
|   └-chr*.phased_final        --> (Phased fragment files)
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
|-Assembly_Contigs_files
|    |-Aquila_Contig_chr*.fasta                    --> (final contigs for intersted region)
|    |-Aquila_Contig_chr*_hp1.fasta                     --> (final contigs for hp1)
|    └-Aquila_Contig_chr*_hp2.fasta                     --> (final contigs for hp2)
|
└-AquilaSV_step3_results
     └-AquilaSV_Contig_final.vcf --> (final VCF including SNPs, small indels and SVs)
     
```

## Final Output Format:
Aquila_stLFR outputs an overall contig file `Aquila_Contig_chr*.fasta` for each chromosome, and one contig file for each haplotype: `Aquila_Contig_chr*_hp1.fasta` and `Aquila_Contig_chr*_hp2.fasta`. For each contig, the header, for an instance, “>36_PS39049620:39149620_hp1” includes contig number “36”, phase block start coordinate “39049620”, phase block end coordinate “39149620”, and haplotype number “1”. Within the same phase block, the haplotype number “hp1” and “hp2” are arbitrary for maternal and paternal haplotypes. For some contigs from large phase blocks, the headers are much longer and complex, for an instance, “>56432_PS176969599:181582362_hp1_ merge177969599:178064599_hp1-177869599:177969599_hp1”. “56” denotes contig number, “176969599” denotes the start coordinate of the final big phase block, “181582362” denotes the end coordinate of the final big phase block, and “hp1” denotes the haplotype “1”. “177969599:178064599_hp1” and “177869599:177969599_hp1” mean that this contig is concatenated from minicontigs in small chunk (start coordinate: 177969599, end coordinate: 178064599, and haplotype: 1) and small chunk (start coordinate: 177869599, end coordinate: 177969599, and haplotype: 1). 









### Notes
#### For stLFR assembly or hybrid assembly, stLFR reads with barcode "0_0_0" are removed to get perfect diploid assembly.  


#### Please also check <a href="https://github.com/maiziex/Aquila">Aquila</a> here 

## Troubleshooting:
##### Please submit issues on the github page for <a href="https://github.com/maiziex/Aquila_stLFR/issues">Aquila_stLFR</a>. 
##### Or contact with me through <a href="maizie.zhou@vanderbilt.edu">maizie.zhou@vanderbilt.edu</a>

