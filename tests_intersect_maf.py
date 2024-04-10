import unittest
import subprocess
import filecmp
import os
import shutil
import re

# Define test result directories
test_tsv_dir = "tests/tsv/"
test_fa_dir = "tests/fa/"
test_maf_dir = "tests/maf/"
test_bed_dir = "tests/bed/"
test_results_dir = "tests/results/"

class TestIntersectMafBed(unittest.TestCase):
    # basic use case
    def test_plain_text_input(self):
        test_out = "check_bed_plain.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "A.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_basic.maf"))

   # basic use case (gz input)
    def test_gzip_input(self):
        test_out = "check_bed_gz.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf.gz", "-b", test_bed_dir + "A.bed.gz", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_basic.maf"))

   # do not report length=0 maf blocks (leading edge)
    def test_empty(self):
        test_out = "check_empty.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test1.maf", "-b", test_bed_dir + "A_edge.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_empty.maf"))

   # do not report length=0 maf blocks (trailling edge)
    def test_empty_2(self):
        test_out = "check_empty2.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test1.maf", "-b", test_bed_dir + "A_edge_trailling.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_empty.maf"))

   # test that minimum overlap filter works (1)
    def test_min_overlap(self):
        test_out = "check_min_overlap1.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "multiple_hits.bed", "-r", "A", "-l", "4" , "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_min_length_4.maf"))

   # test that minimum overlap filter works (2)
    def test_min_overlap(self):
        test_out = "check_min_overlap2.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "multiple_hits.bed", "-r", "A", "-l", "16" , "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_empty.maf"))

   # include maf blocks without hits in bed
    def test_no_hits(self):
        test_out = "check_no_hits.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "A_reverse.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_no_hit.maf"))

   # strand awarenes (flip bed coordinates for "-" sequences in maf)
    def test_reverse(self):
        test_out = "check_reverse.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test4.maf", "-b", test_bed_dir + "A_reverse.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_reverse.maf"))

   # strand awarenes (flip bed coordinates for "-" sequences in maf)
    def test_reverse(self):
        test_out = "check_reverse.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test4.maf", "-b", test_bed_dir + "A_reverse.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_reverse.maf"))

    # merge overlapping bed regions
    def test_merge_overlaps(self):
        test_out = "check_merge.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "overlaps.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_basic.maf"))

    # merge overlapping bed regions
    def test_spanning_maf_regions(self):
        test_out = "check_spanning_regions.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "spanning_multiple_maf_seqs.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_spanning.maf"))

    # multiple bed regions in single maf block
    def test_multiple_bed_regions_in_seq(self):
        test_out = "check_multiple_hits.maf"
        subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3.maf", "-b", test_bed_dir + "multiple_hits.bed", "-r", "A", "-o", test_results_dir + test_out ], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_maf_dir + "target_multiple_hits.maf"))

    # failure upon asking for the wrong sample with `--ref`
    def test_failure_wrong_ref(self):
        process = subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test4.maf", "-b", test_bed_dir + "A_reverse.bed", "-r", "B", "-o", "/dev/stdout"], stderr=subprocess.PIPE)

        # Check if the process failed (non-zero exit code)
        self.assertNotEqual(process.returncode, 0)
    
        # Check if the error message contains the expected error string
        expected_error = "maf file does not seem to use"
        self.assertIn(expected_error, process.stderr.decode("utf-8"))

    # failure with inconsistent refernce sample name in maf
    def test_failure_inconsistent_ref(self):
        process = subprocess.run(["./intersect_maf_bed", "-m", test_maf_dir + "test3_bad.maf", "-b", test_bed_dir + "A.bed", "-r", "A", "-o", "/dev/stdout"], stderr=subprocess.PIPE)

        # Check if the process failed (non-zero exit code)
        self.assertNotEqual(process.returncode, 0)
    
        # Check if the error message contains the expected error string
        expected_error = "maf file does not seem to use"
        self.assertIn(expected_error, process.stderr.decode("utf-8"))
# wrong ref
# ./intersect_maf_bed -m tests/maf/test3.maf -b tests/bed/A.bed -r B -o /dev/stdout

if __name__ == "__main__":
    
    if not os.path.exists(test_results_dir):
        os.makedirs(test_results_dir)
    
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        shutil.rmtree(test_results_dir)


