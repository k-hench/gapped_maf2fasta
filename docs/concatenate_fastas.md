### `fasta` concatenation

Concatenate `fasta` files to single file.
The input `fasta` files are specified as space-delimited list as first argument to the script `concat_fastas`:

```sh
# plain input (note how "Y" is being dropped)
conda run -n biopython \
  ./concat_fastas \
  tests/fa/test1.fa tests/fa/test2.fa \
  -s A,C,B,Y \
  -o /dev/stdout 2> logs.log | \
  fold -w 45

# check fail on sequences of different lenghts
conda run -n biopython \
  ./concat_fastas \
  tests/fa/test1.fa tests/fa/test2_shorter.fa \
  -s A,C,B \
  -o /dev/stdout 

# check fail on "gaps only sequences"
conda run -n biopython \
  ./concat_fastas \
  tests/fa/test1.fa.gz tests/fa/test2.fa.gz \
  -s A,C,B,D \
  -o /dev/stdout 

# run on single input file to merge sequences
# (droping 'only-gaps' sequences by selection)
conda run -n biopython \
  ./concat_fastas tests/fa/test1.fa.gz \
  -s A,C,B \
  -o /dev/stdout 

# (failing on 'only-gaps' sequences by default)
conda run -n biopython \
  ./concat_fastas \
  tests/fa/test1.fa.gz \
  -s A,C,B,D,E \
  -o /dev/stdout 

# (keeping 'only-gaps' sequences)
conda run -n biopython \
  ./concat_fastas \
  tests/fa/test1.fa.gz \
  -s A,C,B,D,E \
  -o /dev/stdout \
  --keep-gaps-only
```

just count all bases:

```sh
conda run -n biopython \
  ./concat_fastas tests/fa/test1.fa.gz \
  -l test/samples.txt \
  -o /dev/null \      # omit fasta output
  --keep-gaps-only \  # and
  --base-report       # just compile the base report
```

## Chaining both scripts (dropping gapps-only from fasta)

The behavior with respect to gaps-only sequences can be toggled from an "ERROR" case, to an explicit "INFO" case (keeping gapps-only sequences) using the parameter `--keep-gaps-only`.

Error-case:

```sh
./maf2fasta --maf tests/maf/test2.maf.gz --fa /dev/stdout -s A,C,B,D  | \
  ./concat_fastas /dev/stdin  -s A,C,B,D -o /dev/stdout
```

```
Error: The following sequence(s) contain only gaps: [ D ]
```

Info-case:

```sh
./maf2fasta --maf tests/maf/test2.maf.gz --fa /dev/stdout -s A,C,B,D  | \
  ./concat_fastas /dev/stdin  -s A,C,B,D -o /dev/stdout --keep-gaps-only
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