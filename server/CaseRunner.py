import os
import pexpect
from pathlib import Path

from OutputUtility import OutputUtility


class CaseRunner:
    """Runs a program with the given inputs and returns the output.
    State is scoped to one and only one program. Then it should be
    discarded."""

    PYTHON = "python3"

    def __init__(self, program_path: Path):
        self.program_path = program_path
        self.child = None

    def run_program(self, inputs: list[str], timeout: float = 1.0) -> str:
        try:
            self.child = pexpect.spawn(f'{self.PYTHON} {self.program_path}')

            for input_value in inputs:
                self.child.sendline(input_value)

            ## If all inputs are consumed (or if there were none)
            ## and the program is still running, it's stuck.
            if not self._is_program_ended(timeout):
                raise RuntimeError(f"Program failed to terminate.")

            self.child.wait()

            output = OutputUtility.get_program_output(self.child)

            if self.child.exitstatus != 0:
                raise RuntimeError(OutputUtility.get_error_info(output))

            return output
        finally:
            if self.child:
                self.child.close()
                self.child = None

    def _is_program_ended(self, timeout: int):
        result = True
        try:
            self.child.expect(pexpect.EOF, timeout=timeout)
        except pexpect.TIMEOUT:
            result = False
        return result
