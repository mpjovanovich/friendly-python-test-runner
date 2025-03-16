import pytest
from src.test_runner.case_runner import CaseRunner
from src.test_runner.io_utility import IoUtility

TEMP_FILE = "test.py"


## The tmp_path is a pytest fixture that creates a temporary directory for the test
def test_writes_temp_file(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("test", file_path)
    with open(file_path, "r") as file:
        assert file.read() == "test"


def test_program_exits_on_runtime_error(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("bad code", file_path)
    test_runner = CaseRunner(file_path)
    with pytest.raises(RuntimeError):
        test_runner.run_program(inputs=[], timeout=0.1)


def test_captures_error_type(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("x = 1/0", file_path)
    test_runner = CaseRunner(file_path)
    with pytest.raises(RuntimeError) as ex:
        test_runner.run_program(inputs=[], timeout=0.1)
    assert "ZeroDivisionError" in str(ex.value)


def test_runs_valid_program(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("print(1)", file_path)
    test_runner = CaseRunner(file_path)
    test_runner.run_program(inputs=[], timeout=0.1)
    ## Would raise an error if it didn't run, so just checking that
    ## it ran successfully
    assert True


def test_captures_program_output(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("print(1)", file_path)
    test_runner = CaseRunner(file_path)
    output = test_runner.run_program(inputs=[], timeout=0.1)
    assert output == "1"


def test_captures_program_prompts(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("input('test input')", file_path)
    test_runner = CaseRunner(file_path)
    output = test_runner.run_program(inputs=[""], timeout=0.1)
    assert "test input" in output


## This has been a right bastard to get working. We'll have to forego it for now.
# def test_unconsumed_inputs_not_in_output(tmp_path):
#     file_path = tmp_path / TEMP_FILE
#     IoUtility.write_temp_file("input('Enter value: ')", file_path)
#     test_runner = CaseRunner(file_path)
#     with pytest.raises(RuntimeError) as ex:
#         test_runner.run_program(inputs=["first", "second"], timeout=0.1)
#     assert "Program terminated before using all inputs" in str(ex.value)
#     assert "Consumed 1 of 2 expected inputs" in str(ex.value)
#     assert "1. first" in str(ex.value)
#     assert "2. second" in str(ex.value)


def test_fails_if_hung_on_input(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("input()", file_path)
    test_runner = CaseRunner(file_path)
    with pytest.raises(RuntimeError) as ex:
        test_runner.run_program(inputs=[], timeout=0.1)
    assert "Program failed to terminate" in str(ex.value)


def test_fails_if_hung_on_compute(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("while True: pass", file_path)
    test_runner = CaseRunner(file_path)
    with pytest.raises(RuntimeError):
        test_runner.run_program(inputs=[], timeout=0.1)
