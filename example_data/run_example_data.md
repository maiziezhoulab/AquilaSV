#### We provide an example dataset to run the whole pipeline. 

Please download the example data <a href="https://zenodo.org/record/5032380">from Zenodo</a>.
```
Aquila_stLFR_exampledata
|-selected.bam (hg19)
|-selected.bam.bai
|
|-test_freebayes.vcf (hg19)
|
|-genome_hg19.fa         


Run the whole pipeline:
```
python AquilaSV/bin/AquilaSV_step1.py --bam_file test.bam --vcf_file test_freebayes.vcf --sample_name test --chr_start 21 --chr_end 21 --out_dir test_asm --uniq_map_dir Uniqness_map_hg19 --fastq_file test.fastq

python AquilaSV/bin/AquilaSV_step2.py --chr_start 21 --chr_end 21 --out_dir test_asm --num_threads 30 --num_threads_spades 20 --reference genome_hg19.fa

python AquilaSVbin/AquilaSV_step3.py  --assembly_dir test_asm  --ref_file genome_hg19.fa  --num_of_threads 2 --out_dir test_variant_results --var_size 1 --chr_start 21 --chr_end 21 --all_regions_flag 1
```
