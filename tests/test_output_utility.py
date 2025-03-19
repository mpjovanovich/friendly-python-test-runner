import pytest
import pexpect
from src.test_runner.output_utility import OutputUtility


def test_get_error_info_regular_error():
    error_output = """Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero"""
    result = OutputUtility.get_error_info(error_output)
    assert result == "ZeroDivisionError: division by zero"


def test_get_error_info_unused_input_error():
    error_output = """RuntimeError: Program terminated prematurely: consumed 2 of 4 expected inputs:
  1. input1
  2. input2
  3. input3
  4. input4"""
    result = OutputUtility.get_error_info(error_output)
    assert result == """RuntimeError: Program terminated prematurely: consumed 2 of 4 expected inputs:
1. input1
2. input2
3. input3
4. input4"""
