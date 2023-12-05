#!/bin/env python

#### libraries
import pybedtools as bedtools

# extract promoter regions
def get_promoter(feature, upstream, downstream):
    if feature.strand == '+':
        start = feature.start - upstream
        end = feature.start + downstream
    else:
        start = feature.end - downstream
        end = feature.end + upstream
    
    # Ensure start is not negative
    start = max(start, 0)
    
    # Extract gene_id and remove version number if present
    gene_id = feature.attrs['gene_id'].split('.')[0]
    
    # Create a new feature with the promoter region coordinates
    promoter = bedtools.create_interval_from_list([
        feature.chrom,
        start,
        end,
        gene_id,
#         feature.attrs['gene_name'] if 'gene_name' in feature.attrs else feature.attrs['gene_id'],
        '.',
        feature.strand
    ])
    
    return promoter

#### configurations

# input
gtf_file = snakemake.config["gencode_gtf"]

# output
promoter_regions_path = snakemake.output["promoter_regions"]

# parameters
TSS_up = snakemake.config["proximal_size_up"]
TSS_dn = snakemake.config["proximal_size_dn"]

# load the genome annotation file using pybedtools
gtf = bedtools.BedTool(gtf_file)

# filter for features that are genes and create promoters
promoters = gtf.filter(lambda x: x[2] == 'gene').each(get_promoter, TSS_up, TSS_dn)

# save the promoter regions to a BED file
promoters.saveas(promoter_regions_path)
