InteractomeSeq 


InteractomeSeq: a web server for the identification and profiling of domains and epitopes from Phage Display and Next Generation Sequencing data. InteractomeSeq is a webtool allowing either genomic or single gene domainome analysis of phage libraries generated and selected by following the interactome-sequencing approach.

InteractomeSeq data analysis workflow is composed of four sequential steps that, starting from raw sequencing reads, generate the list of putative domains with genomic annotations. In the first step, InteractomeSeq checks if the input files (raw reads, reference genome sequence, annotation list) are properly formatted. In the second step low-quality sequencing data are first trimmed and then discarded basing on minimal length requirements. In the third step, the remaining reads are aligned to the reference genome, a SAM file is generated and only reads with high quality score are processed and converted into a BAM file. After alignment, InteractomeSeq performs the step for domains detection and generates a list of CDS portions classified as putative domains/epitopes, the list is ranked taking in consideration the focus which is an index obtained from the ratio between maximal depth and coverage of a specific genic portion.
