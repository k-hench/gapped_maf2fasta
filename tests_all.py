import tests_fa_concat
import tests_maf_to_fa
import tests_intersect_maf
import unittest
import subprocess
import filecmp
import os
import shutil
import re

# ANSI color escape codes
COLOR_BLUE = "\033[94m"
COLOR_PURPLE = "\033[95m"
COLOR_ORANGE = "\033[93m"
COLOR_RESET = "\033[0m"

if __name__ == "__main__":
    # Define test result directories
    test_tsv_dir = "tests/tsv/"
    test_fa_dir = "tests/fa/"
    test_maf_dir = "tests/maf/"
    test_bed_dir = "tests/bed/"
    test_results_dir = "tests/results/"

    # Create the test results directory if it doesn't exist
    if not os.path.exists(test_results_dir):
        os.makedirs(test_results_dir)
    
    # Run the MAF to FASTA conversion tests
    print(f"Testing <<{COLOR_BLUE}MAF conversion{COLOR_RESET}>> module")
    suite_maf = unittest.TestLoader().loadTestsFromModule(tests_maf_to_fa)
    result_maf = unittest.TextTestRunner().run(suite_maf)

    # Run the FASTA concatenation tests
    print(f"Testing <<{COLOR_PURPLE}fasta concatination{COLOR_RESET}>> module")
    suite_fa = unittest.TestLoader().loadTestsFromModule(tests_fa_concat)
    result_fa = unittest.TextTestRunner().run(suite_fa)

    # Run the BED / MAF intersection tests
    print(f"Testing <<{COLOR_ORANGE}bed intersection{COLOR_RESET}>> module")
    suite_bed = unittest.TestLoader().loadTestsFromModule(tests_intersect_maf)
    result_bed = unittest.TextTestRunner().run(suite_bed)

    # Remove the test results directory if all tests passed
    if result_fa.wasSuccessful() and result_maf.wasSuccessful() and result_bed.wasSuccessful():
        shutil.rmtree(test_results_dir)
