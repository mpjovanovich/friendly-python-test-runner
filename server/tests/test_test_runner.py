import pytest
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from CodeRunner import CodeRunner
from IoUtility import IoUtility

TEMP_FILE = "test.py"


## The tmp_path is a pytest fixture that creates a temporary directory for the test
def test_writes_temp_file(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("test", file_path)
    with open(file_path, "r") as file:
        assert file.read() == "test"


# We do want this, but skip for now
def test_program_exits_on_runtime_error(tmp_path):
    file_path = tmp_path / TEMP_FILE
    # IoUtility.write_temp_file("bad code", file_path)
    test_runner = CodeRunner(file_path)

    with pytest.raises(RuntimeError):
        test_runner.run_program()


def test_runs_valid_program(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("x=5\nprint(x)", file_path)
    test_runner = CodeRunner(file_path)
    test_runner.run_program()
    ## Just checking that it doesn't raise an error
    assert True


def test_captures_program_output(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("x=5\nprint(x)", file_path)
    test_runner = CodeRunner(file_path)
    output = test_runner.run_program()
    assert output == "5"


def test_captures_program_prompts(tmp_path):
    file_path = tmp_path / TEMP_FILE
    IoUtility.write_temp_file("input('test input')", file_path)
    test_runner = CodeRunner(file_path)
    output = test_runner.run_program(inputs=[""])
    assert "test input" in output
