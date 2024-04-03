### `maf` -> `fasta` conversion

```
usage: maf2fasta [-h] -m MAF_FILE -f FASTA_FILE (-s SAMPLE_ORDER | -l SAMPLE_FILE)

Convert MAF alignment to multi-sample FASTA

options:
  -h, --help            show this help message and exit
  -m MAF_FILE, --maf MAF_FILE
                        Input MAF file (can be gzipped)
  -f FASTA_FILE, --fa FASTA_FILE
                        Output FASTA file
  -s SAMPLE_ORDER, --sample-order SAMPLE_ORDER
                        Sample order as a comma-separated list
  -l SAMPLE_FILE, --sample-list SAMPLE_FILE
                        File containing sample order (one sample per line)
```

convert `maf` to `fasta` file with fixed output order (manual checks)

```sh
# basic conversion
conda run -n biopython ./maf2fasta --maf tests/maf/test1.maf --fa /dev/stdout -s A,C,B,D

# check sequence order
conda run -n biopython \
  ./maf2fasta \
  --maf tests/maf/test1.maf \
  --fa /dev/stdout \
  -s C,B
```

The sample order can also be specified using a plain text file using `--sample-list`:

```sh
cat tests/samples.txt
```
```
A
C
B
```
```sh
conda run -n biopython \
  ./maf2fasta \
  --maf tests/maf/test1.maf \
  --fa /dev/stdout \
  --sample-list tests/samples.txt
```

Files can be gzipped (trailing `.gz` is detected).
Also, note how new samples will appear as "gaps-only" sequence.

```sh
# check gzipped input
conda run -n biopython \
  ./maf2fasta \
  --maf tests/maf/test2.maf.gz \
  --fa /dev/stdout \
  -s Y,A,B,C,D
```
