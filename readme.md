# Conversion of `maf` to `fasta` files

The aim of these scripts is to able to merge the sequence alignments of a maf (Multiple Alignment Format) file in a consistent and predictable way.

Required features are:
- enforceable order of output sequences in the resulting fasta file (`maf2fasta`)
- consistent padding with gaps for samples not included in an alignment block (`maf2fasta`)
- checks for consistent length of the fasta output (`concat_fastas`)
- checks for sequences consisting entirely of gaps (`concat_fastas`) 

The desired output (potentially) concatenates at several places:
- within each maf -> fasta conversion (all sequences with the same header are concatenated)
- combining the results of multiple conversions (combining mafs from different scaffolds in the reference genome)


## Dependencies

The python scripts require biopython (eg as specified in the conda environment in `envs/biopython.yml`)


## Intersect `maf` and `bed` file

Note that this will parse the `bed` in such a way that overlaps of individual overlapping bed entries are being merged before the intersection with the `maf` file:

![](docs/img/maf_intersection.svg)

```sh
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/A.bed \
  -r A \
  -o /dev/stdout
```