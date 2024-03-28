# basic use case
#  ./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/A.bed -r A -o /dev/stdout

# gzipped input
#  ./intersect_maf_bed -m tests/maf/test3.maf.gz -b tests/bed/A.bed.gz -r A -o /dev/stdout

# no hits case
# ./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/A_reverse.bed -r A -o /dev/stdout

# negative strand case
# ./intersect_maf_bed -m tests/maf/test4.maf -b tests/bed/A_reverse.bed -r A -o /dev/stdout

# bad maf reference
#./intersect_maf_bed -m tests/maf/test3_bad.maf -b tests/bed/multiple_hits.bed -r A -o /dev/stdout

# merge bed regions
#./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/overlaps.bed -r A -o /dev/stdout

# spanning several maf sequences
#./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/spanning_multiple_maf_seqs.bed -r A -o /dev/stdout

# extract mutliple regions from single maf block
# ./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/multiple_hits.bed -r A -o /dev/stdout

# wrong ref
# ./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/A.bed -r B -o /dev/stdout

