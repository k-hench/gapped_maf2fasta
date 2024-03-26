import tests_fa_concat
import tests_maf_to_fa
import unittest
import subprocess
import filecmp
import os
import shutil
import re

# ANSI color escape codes
COLOR_BLUE = "\033[94m"
COLOR_PURPLE = "\033[95m"
COLOR_RESET = "\033[0m"

if __name__ == "__main__":
    # Define test result directories
    test_fa_dir = "tests/fa/"
    test_maf_dir = "tests/maf/"
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

    # Remove the test results directory if all tests passed
    if result_fa.wasSuccessful() and result_maf.wasSuccessful():
        shutil.rmtree(test_results_dir)
