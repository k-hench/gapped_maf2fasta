Running the tests:

```sh
# all tests
conda run -n biopython python tests_all.py

# running the maf -> fasta conversion independently
conda run -n biopython python tests_maf_to_fa.py
# running the fasta concatenation independently
conda run -n biopython python tests_fa_concat.py
```

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

