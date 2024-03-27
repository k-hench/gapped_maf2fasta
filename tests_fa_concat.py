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
test_results_dir = "tests/results/"

class TestConcatenateFastas(unittest.TestCase):
    def test_plain_text_input(self):
        test_out = "check_plain.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1.fa", test_fa_dir + "test2.fa", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_sample_order_from_file(self):
        test_out = "check_from_list.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1.fa", test_fa_dir + "test2.fa", "-l", "tests/samples.txt", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target_ACB.fa"))

    def test_gzipped_input(self):
        test_out = "check_gz.fa"
        # Run the script with gzipped input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1.fa.gz", test_fa_dir + "test2.fa.gz", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_mixed_input(self):
        test_out = "check_mixed.fa"
        # Run the script with mixed input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1.fa", test_fa_dir + "test2.fa.gz", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_mixed_seq_ordes(self):
        test_out = "check_mixed_order.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1_sorted.fa", test_fa_dir + "test2.fa", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_split_text_input(self):
        test_out = "check_split1.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1_split1.fa", test_fa_dir + "test2.fa", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_split_text_input_fail(self):
        test_out = "check_split2.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1_split2.fa", test_fa_dir + "test2.fa", "-s", "A,B,C", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertFalse(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target.fa"))

    def test_merge_split_ids(self):
        test_out = "check_merge.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1_split1.fa", "-s", "A,C,B", "-o", test_results_dir + test_out], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "target_merge.fa"))

    def test_merge_split_ids_with_gaps(self):
        test_out = "check_merge2.fa"
        # Run the script with plain text input files
        subprocess.run(["./concat_fastas", test_fa_dir + "test1_split1.fa", "-s", "A,B,C,D,E", "-o", test_results_dir + test_out, "--keep-gaps-only"], stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "test1_sorted.fa"))

    def test_failure_gaps(self):
        # Run the script with an input that should fail
        process = subprocess.run(["./concat_fastas", test_fa_dir + "test2.fa", "-s", "A,B,C,D", "-o", "/dev/stdout"], stderr=subprocess.PIPE)

        # Check if the process failed (non-zero exit code)
        self.assertNotEqual(process.returncode, 0)
    
        # Check if the error message contains the expected error string
        expected_error = "sequence(s) contain only gaps"
        self.assertIn(expected_error, process.stderr.decode("utf-8"))

    def test_failure_legth_differences(self):
        # Run the script with an input that should fail
        process = subprocess.run(["./concat_fastas", test_fa_dir + "test1.fa", test_fa_dir + "test2_shorter.fa", "-s", "A,B,C", "-o", "/dev/stdout"], stderr=subprocess.PIPE)

        # Check if the process failed (non-zero exit code)
        self.assertNotEqual(process.returncode, 0)
    
        # Check if the error message contains the expected error string
        expected_error = "Not all sequences are of the same length:"
        self.assertIn(expected_error, process.stderr.decode("utf-8"))

    def test_base_count(self):
        test_out = "check_base_count.tsv"
        # Run the script with plain text input files
        result = subprocess.run(["./concat_fastas", test_fa_dir + "base_counting.fa", "-s", "case_gap,case_case,case_n,case_na", "-o", "/dev/null", "--keep-gaps-only", "--base-report"], capture_output=True, text=True)
        with open(test_results_dir + test_out, "w") as f:
            f.write(result.stdout)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_tsv_dir + "base_count.tsv"))

if __name__ == "__main__":
    
    if not os.path.exists(test_results_dir):
        os.makedirs(test_results_dir)
    
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        shutil.rmtree(test_results_dir)
