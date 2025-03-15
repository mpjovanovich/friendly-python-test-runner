import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from SuiteRunner import SuiteRunner
from IoUtility import IoUtility
from Case import Case
from CaseRunner import CaseRunner


def test_runs_case(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.side_effect = Exception("test error")
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    cases = [case]
    SuiteRunner.run_cases(mock_case_runner, cases)
    mock_case_runner.run_program.assert_called_once_with(case.inputs)


def test_handles_exception(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.side_effect = Exception("test error")
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    cases = [case]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert case.passed is False
    assert case.error == "test error"


def test_contains_passes(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "bla test123 bla"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test",
             comparison_type="contains",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is True


def test_contains_fails(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "bla"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test",
             comparison_type="contains",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is False


def test_equals_passes(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "test"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test",
             comparison_type="equals",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is True


def test_equals_fails(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "test1"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test",
             comparison_type="equals",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is False


def test_equals_passes_multiline(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "test\n123"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test\n123",
             comparison_type="equals",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is True


def test_equals_fails_multiline(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "test123"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test\n123",
             comparison_type="equals",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].passed is False


def test_captures_output(mocker):
    mock_case_runner = mocker.Mock()
    mock_case_runner.run_program.return_value = "test"
    cases = [
        Case(title="",
             inputs=[],
             expected_output="test",
             comparison_type="equals",
             is_bonus=False),
    ]
    SuiteRunner.run_cases(mock_case_runner, cases)
    assert cases[0].output == "test"
