## Intersect `maf` and `bed` file

Note that this will parse the `bed` in such a way that overlaps of individual overlapping bed entries are being merged before the intersection with the `maf` file:

![](img/maf_intersection.svg)

```sh
conda run -n biopython \
  ./intersect_maf_bed \
  -m tests/maf/test3.maf \
  -b tests/bed/A.bed \
  -r A \
  -o /dev/stdout
```