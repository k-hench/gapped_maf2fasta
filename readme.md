# Conversion of `maf` (Multiple Alignment Format) to `fasta` files

The aim of these scripts is to able to merge the sequence alignments of a maf file in a consistent and predictable way.

Required features are:
- enforceable order of output sequences in the resulting fasta file (`maf2fasta`)
- consistent padding with gaps for samples not included in an alignment block (`maf2fasta`)
- checks for consistent length of the fasta output (`concat_fastas`)
- checks for sequences consisting entirely of gaps (`concat_fastas`) 

The desired output (potentially) concatenates at several places:
- within each maf -> fasta conversion (all sequences with the same header are concatenated)
- combining the results of multiple conversions (combining mafs from different scaffolds in the reference genome)

## Chaining both scripts (dropping gapps-only from fasta)


The behavior with respect to gaps-only sequences can be toggled from an "ERROR" case, to an explicit "INFO" case (keeping gapps-only sequences) using the parameter `--keep-gaps-only`.

Error-case:

```sh
./maf2fasta --maf tests/maf/test2.maf.gz --fa /dev/stdout -s A,C,B,D  | \
  ./concat_fastas /dev/stdin  -s A,C,B,D -o /dev/stdout
```

```
Error: The following sequence(s) contain only gaps: [ D ]
```

Info-case:

```sh
./maf2fasta --maf tests/maf/test2.maf.gz --fa /dev/stdout -s A,C,B,D  | \
  ./concat_fastas /dev/stdin  -s A,C,B,D -o /dev/stdout --keep-gaps-only
```

```
Info: The following sequence(s) contain only gaps: [ D ]
>A
ATCAGTCAGCAGTGTAGCTGTGTGTGCATGCATGC
>C
ATTAG-----AG---AGCTCTGA-----TGCAAGC
>B
ATTATTTAGC--TGA----------GGATGCATGG
>D
-----------------------------------
```

## Dependencies

The python scripts require biopython (eg as specified in the conda environment in `envs/biopython.yml`)

## Running tests:

```sh
# all tests
conda run -n biopython python tests_all.py

# running the maf -> fasta conversion independently
conda run -n biopython python tests_maf_to_fa.py
# running the fasta concatenation independently
conda run -n biopython python tests_fa_concat.py
```

## Manual Checks

convert `maf` to `fasta` file with fixed output order (manual checks)

```sh
# basic conversion
conda run -n biopython ./maf2fasta --maf tests/maf/test1.maf --fa /dev/stdout -s A,C,B,D

# check sequence order
conda run -n biopython ./maf2fasta --maf tests/maf/test1.maf --fa /dev/stdout -s C,B

# check gzipped input
conda run -n biopython ./maf2fasta --maf tests/maf/test2.maf.gz --fa /dev/stdout -s Y,A,B,C,D
```

concatenate `fasta` files to single file

```sh
# plain input (note how "Y" is being dropped)
conda run -n biopython ./concat_fastas tests/fa/test1.fa tests/fa/test2.fa -s A,C,B,Y -o /dev/stdout 2> logs.log | fold -w 45

# check fail on sequences of different lenghts
conda run -n biopython ./concat_fastas tests/fa/test1.fa tests/fa/test2_shorter.fa -s A,C,B -o /dev/stdout 

# check fail on "gaps only sequences"
conda run -n biopython ./concat_fastas tests/fa/test1.fa.gz tests/fa/test2.fa.gz -s A,C,B,D -o /dev/stdout 

# run on single input file to merge sequences
# (droping 'only-gaps' sequences by selection)
conda run -n biopython ./concat_fastas tests/fa/test1.fa.gz -s A,C,B -o /dev/stdout 
# (failing on 'only-gaps' sequences by default)
conda run -n biopython ./concat_fastas tests/fa/test1.fa.gz -s A,C,B,D,E -o /dev/stdout 
# (keeping 'only-gaps' sequences)
conda run -n biopython ./concat_fastas tests/fa/test1.fa.gz -s A,C,B,D,E -o /dev/stdout --keep-gaps-only
```

