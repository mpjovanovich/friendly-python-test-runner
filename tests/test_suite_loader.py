import os
import pytest
from pathlib import Path
from src.test_runner.suite_loader import SuiteLoader


def test_registry_fails_if_bad_directory():
    with pytest.raises(FileNotFoundError):
        SuiteLoader('nonexistent_directory')


@pytest.fixture
def suite_loader():
    test_cases_path = Path(__file__).parent / 'test_cases'
    return SuiteLoader(str(test_cases_path))


def test_registry_loads_yaml(suite_loader):
    assert suite_loader._registry == {
        'test': 'suites/test.yaml',
        'missing_file': 'suites/missing_file.yaml'
    }


def test_fails_if_missing_suite_key(suite_loader):
    with pytest.raises(KeyError):
        suite_loader.load_suite('missing_suite_key')


def test_fails_if_missing_suite_file(suite_loader):
    with pytest.raises(FileNotFoundError):
        suite_loader.load_suite('missing_file')


def test_returns_test_case_list(suite_loader):
    test_cases = suite_loader.load_suite('test')
    assert len(test_cases) == 2
    assert test_cases[0].title == 'test1'
    assert test_cases[0].inputs == ['input1']
    assert test_cases[0].expected_output == 'input1'
    assert test_cases[0].comparison_type == 'contains'
    assert test_cases[0].is_bonus == False
    assert test_cases[1].title == 'test2'
    assert test_cases[1].inputs == ['*input2*']
    assert test_cases[1].expected_output == 'input2'
    assert test_cases[1].comparison_type == 'equals'
    assert test_cases[1].is_bonus == True
