An important step before AquilaSV pipeline is getting the bam file of your interested region. Here is a hands-on tutorial of extracting selected.bam.

- Sofware:
    
    
    You should have samtools installed.
    
- steps:


step1. make a bed file. ( A bed file is a file that contains the chromosome name, start position and end position of your interested region). A typical bed file's content could be `chr1 123456 223456`. You can name your bed file as `select.bed` for AquilaSV.

step2. extract selected.bam given whole genome bam file and bed file. A typical command should be like

`samtools -b -L select.bed wgs.bam > selected.bam`


step3. make index file of your selected.bam file.

`samtools index selected.bam`


Once you see `selected.bam` and `selected.bam.bai` in your working directory, you are all set to run AquilaSV pipeline.
