import tempfile
import os
import pexpect
from pathlib import Path
from typing import Optional

from src.test_runner.output_utility import OutputUtility


class CaseRunner:
    PYTHON = "python3"
    INPUT_PROMPT_PATTERN = rb'.*?:\s*$'

    def __init__(self, program_path: Path):
        self.program_path = program_path
        self.child = None
        self.logfile = None

    def run_program(self, inputs: list[str], timeout: float = 1.0) -> str:
        with tempfile.TemporaryFile(mode='w+b') as self.logfile:
            try:
                self._spawn_process()
                used_inputs = self._handle_inputs(inputs, timeout)
                self._check_timeout(timeout)

                output = self._get_final_output()

                if self.child.exitstatus != 0:
                    raise RuntimeError(OutputUtility.get_error_info(output))

                if used_inputs < len(inputs):
                    raise RuntimeError(
                        "Program terminated before using all test inputs")

                return output
            finally:
                self._cleanup()

    def _spawn_process(self) -> None:
        self.child = pexpect.spawn(f'{self.PYTHON} {self.program_path}',
                                   echo=False,
                                   logfile=self.logfile)

    def _handle_inputs(self, inputs: list[str], timeout: float) -> int:
        used_inputs = 0

        for input_value in inputs:
            try:
                # Wait for a prompt ending with colon and any following whitespace
                self.child.expect(self.INPUT_PROMPT_PATTERN, timeout=timeout)
                self.child.sendline(input_value)
                used_inputs += 1
            except pexpect.EOF:
                # Program exited early - let the caller handle this via used_inputs count
                break

        return used_inputs

    def _check_timeout(self, timeout: float) -> None:
        try:
            self.child.expect(pexpect.EOF, timeout=timeout)
        except pexpect.TIMEOUT:
            raise RuntimeError("Program failed to terminate.")

    def _get_final_output(self) -> str:
        self.child.wait()
        output = self._read_logfile_output()
        return output.replace('\r', '').strip('\n')

    def _read_logfile_output(self) -> str:
        self.logfile.seek(0)
        return self.logfile.read().decode('utf-8')

    def _cleanup(self) -> None:
        if self.child:
            self.child.close()
            self.child = None
