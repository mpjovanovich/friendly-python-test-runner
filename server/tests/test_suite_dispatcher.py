import os
import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from Case import Case
from SuiteDispatcher import SuiteDispatcher
from SuiteRunner import SuiteRunner

TEST_DIR = Path(__file__).parent / 'test_cases'
TMP_DIR = Path(__file__).parent / 'tmp'
TEST_SUITE = "test"
PROGRAM = "print(1)"

# ## This is an integration test of the whole system
# def test_run_suite():
#     dispatcher = SuiteDispatcher(TMP_DIR, TEST_DIR)
#     results = dispatcher.run_suite(TEST_SUITE, PROGRAM)
#     assert results is not None

# def test_run_good_suite_end_to_end():
#     ## Run with good input
#     ## Should return a formatted string of results
#     sample_program = """
# def greet(name):
#     return f"Hello, {name}!"
# """
#     dispatcher = SuiteDispatcher(TMP_DIR, TEST_DIR)
#     results = dispatcher.run_suite(TEST_SUITE, sample_program)
#     assert results is not None


def test_run_bad_suite_end_to_end():
    ## Run with bad input
    ## Should return an error message
    dispatcher = SuiteDispatcher(TMP_DIR, TEST_DIR)
    results = dispatcher.run_suite(TEST_SUITE, "bad code")

    print(results)
    assert results is not None


# def test_system_recovers_from_errors():
#     ## Run with bad input
#     dispatcher = SuiteDispatcher(TMP_DIR, TEST_DIR)
#     results = dispatcher.run_suite(TEST_SUITE, "bad code")
#     assert results is not None

#     ## System should work for subsequent valid input
#     ## It shouldn't case a system crash
#     results = dispatcher.run_suite(TEST_SUITE, "print('hello')")
#     assert results is not None
