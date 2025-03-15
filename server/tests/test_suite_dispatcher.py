import os
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from SuiteDispatcher import SuiteDispatcher

TEST_DIR = "test_cases"
TEST_SUITE = "test_suite"
PROGRAM_PATH = "test_program.py"

## There's quite a bit of dependency faking going on here,
## so I'm going to comment it heavily to explain what's happening.


## Rig up a fixture that can be reused across tests
@pytest.fixture
def suite_dispatcher():
    return SuiteDispatcher(TEST_DIR)


def test_calls_suite_loader_constructor(suite_dispatcher):
    ## Patch calls to the dependencies
    with patch('SuiteDispatcher.SuiteLoader') as MockLoader:
        ## Run the method under test
        suite_dispatcher.run_suite(TEST_SUITE, PROGRAM_PATH)

        ## Assert
        MockLoader.assert_called_once_with(TEST_DIR)


def test_calls_suite_loader_load_suite(suite_dispatcher):
    ## Patch calls to the dependencies
    with patch('SuiteDispatcher.SuiteLoader') as MockLoader:
        ## Run the method under test
        suite_dispatcher.run_suite(TEST_SUITE, PROGRAM_PATH)

        ## Assert
        mock_loader = MockLoader.return_value
        mock_loader.load_suite.assert_called_once_with(TEST_SUITE)


def test_calls_case_runner_constructor(suite_dispatcher):

    ## Patch calls to the dependencies
    with patch('SuiteDispatcher.SuiteLoader') as MockLoader, \
         patch('SuiteDispatcher.CaseRunner') as MockRunner:

        ## Run the method under test
        suite_dispatcher.run_suite(TEST_SUITE, PROGRAM_PATH)

        ## Assert
        MockRunner.assert_called_once_with(PROGRAM_PATH)
