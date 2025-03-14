import os
import pexpect
from pathlib import Path


## Runs a program with the given inputs and returns the output.
## State is scoped to one and only one program. Then it should be
## discarded.
class CaseRunner:
    PYTHON = "python3"
    TEMP_DIR = "tmp"

    def __init__(self, program_path: Path):
        # Should do this at startup
        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)
        self.program_path = program_path
        self.child = None

    def run_program(self, inputs: list[str], timeout: int = 10) -> str:
        try:
            self.child = pexpect.spawn(f'{self.PYTHON} {self.program_path}')

            for input_value in inputs:
                self.child.sendline(input_value)

            ## If we can't reach EOF in a reasonable time, program is either stuck
            ## on a prompt or on compute (e.g. bad loop)
            try:
                self.child.expect(pexpect.EOF, timeout=timeout)
            except pexpect.TIMEOUT:
                raise RuntimeError("Program is stuck.")

            self.child.wait()
            output = self.__get_program_output()

            if self.child.exitstatus != 0:
                raise RuntimeError(self.__get_error_info(output))

            return output
        finally:
            if self.child:
                self.child.close()
                self.child = None

    ## Gets the error info from the program after it has finished running
    def __get_error_info(self, error_output: str) -> str:
        return error_output.split("\n")[-1].strip()

    ## Gets the output of the program after it has finished running
    def __get_program_output(self) -> str:
        return self.child.before.decode('utf-8').strip()
