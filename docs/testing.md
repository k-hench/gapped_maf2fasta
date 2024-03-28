## Running tests:

```sh
# all tests
conda run -n biopython python tests_all.py

# running the maf -> fasta conversion independently
conda run -n biopython python tests_maf_to_fa.py
# running the fasta concatenation independently
conda run -n biopython python tests_fa_concat.py
# running the bed/maf interception independently
conda run -n biopython python tests_intersect_maf.py
```
