## Intersect `maf` and `bed` file

Note that this will parse the `bed` in such a way that overlaps of individual overlapping bed entries are being merged before the intersection with the `maf` file:

![](img/maf_intersection.svg)

```sh
# basic use case
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/A.bed \
  -r A \
  -o /dev/stdout

# gzipped input
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf.gz \
  -b tests/bed/A.bed.gz \
  -r A \
  -o /dev/stdout
```

```sh
# merge bed regions
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/overlaps.bed \
  -r A \
  -o /dev/stdout
```
```
Info: Overlapping bed regions were merged:
n input regions was 3, after merging 2 regions remain.
```

```sh
# spanning several maf sequences
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/spanning_multiple_maf_seqs.bed \
  -r A \
  -o /dev/stdout

# extract mutliple regions from single maf block
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/multiple_hits.bed \
  -r A \
  -o /dev/stdout

# failure because wrong ref
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/A.bed \
  -r B \
  -o /dev/stdout
```
```
Error: The maf file does not seem to use the expected sample (--ref B), but instead it uses sample A as reference.
See following first entry of maf block (note that the 4th value is the last alignment position, and NOT the `size` like in the maf itself):
('A', 'Chromosome1', 10, 65, '+', '275', 'GTACGTACGTACGTACGTACGATTTACGTAACGTTACGTACGTACGTACGTACGT')
```