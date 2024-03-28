### `maf` -> `fasta` conversion

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
