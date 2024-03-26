import unittest
import subprocess
import filecmp
import os
import shutil
import re

# Define test result directories
test_fa_dir = "tests/fa/"
test_maf_dir = "tests/maf/"
test_results_dir = "tests/results/"

class TestConvertMafToFasta(unittest.TestCase):
    def test_plain_text_input(self):
        test_out = "convert_plain.fa"
        # Run the script with plain text input files
        command = ["./maf2fasta", "-m", test_maf_dir + "test1.maf", "-f", test_results_dir + test_out, "-s", "A,B,C,D,E"]
        # print(" ".join(command))
        subprocess.run(command, stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "test1_sorted.fa"))

    def test_plain_gz_input(self):
        test_out = "convert_gz.fa"
        # Run the script with plain text input files
        command = ["./maf2fasta", "-m", test_maf_dir + "test2.maf.gz", "-f", test_results_dir + test_out, "-s", "A,C,B,D,E"]
        # print(" ".join(command))
        subprocess.run(command, stderr=subprocess.DEVNULL)
        # Compare the output with the target file
        self.assertTrue(filecmp.cmp(test_results_dir + test_out, test_fa_dir + "test2.fa"))

if __name__ == "__main__":
    
    if not os.path.exists(test_results_dir):
        os.makedirs(test_results_dir)
    
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        shutil.rmtree(test_results_dir)
