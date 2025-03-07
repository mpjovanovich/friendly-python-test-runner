import os
import pexpect
from pathlib import Path


class CodeRunner:
    TEMP_DIR = "tmp"
    STUDENT_CODE_FILE = "student_code.py"

    def __init__(self, program_path: Path):
        # Should do this at startup
        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)
        self.program_path = program_path
        self.child = None

    def run_program(self, inputs: list[str] = []) -> str:
        try:
            self.child = pexpect.spawn(f'python3 {self.program_path}')
            # Don't know if I need this...
            # child.logfile = None
            for input_value in inputs:
                self.child.sendline(input_value)
            self.child.expect(pexpect.EOF)
            self.child.wait()
            output = self.get_program_output()

            if self.child.exitstatus != 0:
                raise RuntimeError(self.get_error_info(output))

            return output
        finally:
            if self.child:
                self.child.close()
                self.child = None

    ## Gets the output of the program after it has finished running
    def get_program_output(self) -> str:
        return self.child.before.decode('utf-8').strip()

    ## Gets the error info from the program after it has finished running
    def get_error_info(self, error_output: str) -> str:
        return error_output.split("\n")[-1].strip()
