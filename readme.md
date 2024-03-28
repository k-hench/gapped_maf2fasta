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

The purpose of the `intersect_maf_bed` script is to clip a sequence alignment in `maf` format to regions specified within a bed file:

![](docs/img/maf_intersection.svg)

Note that this will parse the `bed` in such a way that overlaps of individual overlapping bed entries are being merged before the intersection with the `maf` file.

The clipped alignment is then re-exported as `maf` file.

```sh
./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/A.bed \
  -r A \
  -o file_out.maf
```

## Convert `maf` file to multi-sample `fasta` file

![](docs/img/maf2fa_basic.svg)

```sh
./maf2fasta \
  --maf tests/maf/test1.maf \
  --fa file_out.fa \
  -s A,C,B,D
```

Note that the order of the output `fasta` sequences it enforced with the `--sample-order` flag.
Also, including a sample ID that is not included in the `maf` file will create an entirely blank sequence for that ID (only consisting of `-` characters).

![](docs/img/maf2fa_reorder.svg)

## Concatenate several multi-sample `fasta` files

The main purpose of the `concat_fastas` script is to concatenate several multi-sample `fasta` files.
This should happen on a sample by sample basis:

![](docs/img/concat_fa.svg)

```sh
./concat_fastas \
  tests/fa/test1.fa tests/fa/test2.fa \
  -s A,C,B,Y \
  -o /dev/stdout | \
  fold -w 45 > concat_out.fa
```

```
Warning: The following sample(s) were dropped from the output: [ D, E, Y ]
(either because they are missing from --sample-order, or from the input fasta file(s))
```

If there are multiple sequences with the same name within the `fasta` file they will be merged in the order of appearance.

![](docs/img/concat_fa_multiple.svg)

```sh
./concat_fastas \
  tests/fa/test1_split1.fa \
  -s A \
  -o /dev/stdout
```


The script can also be used to create a summary of the created `fasta` file (eg. to check the gap content per sequence).

```sh
./concat_fastas \
  tests/fa/test1.fa tests/fa/test2.fa \
  -s A,C,B,D \
  -o /dev/null \
  --keep-gaps-only \
  --base-report
```
```
Warning: The following sample(s) were dropped from the output: [ E ]
(either because they are missing from --sample-order, or from the input fasta file(s))
Info: The following sequence(s) contain only gaps: [ D ]
# Summary of gaps and bases counts for each sample:
# sample        gaps    gaps%   A       C       G       T       N       n
# A     0       0.0     21      19      24      26      0       90
# C     34      37.8    17      10      14      15      0       90
# B     12      13.3    19      15      19      25      0       90
# D     90      100.0   0       0       0       0       0       90
```

