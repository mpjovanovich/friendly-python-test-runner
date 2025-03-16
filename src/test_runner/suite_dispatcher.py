from src.test_runner.case_runner import CaseRunner
from src.test_runner.io_utility import IoUtility
from src.test_runner.suite_loader import SuiteLoader
from src.test_runner.suite_runner import SuiteRunner
from src.test_runner.result_formatter import ResultFormatter
from pathlib import Path


## There is one SuiteDispatcher per test set (test case directory).
## There should only be one instance of this class alive at any time
## per test set. Right now there is only the SDEV 140 test set.
class SuiteDispatcher:
    TMP_FILE = "program.py"

    def __init__(self, tmp_dir: str, test_cases_dir: str):
        self._tmp_dir = tmp_dir
        self._test_cases_dir = test_cases_dir

    def run_suite(self, suite_name: str, program: str) -> str:
        try:
            ## Setup the file system
            IoUtility.delete_dir_if_exists(self._tmp_dir)
            IoUtility.create_dir_if_not_exists(self._tmp_dir)
            program_path = Path(self._tmp_dir) / self.TMP_FILE
            IoUtility.write_temp_file(program, program_path)

            ## Load and run the test cases
            suite_loader = SuiteLoader(self._test_cases_dir)
            cases = suite_loader.load_suite(suite_name)
            case_runner = CaseRunner(program_path)
            SuiteRunner.run_cases(case_runner, cases)
            formatted_cases = ResultFormatter.format_cases(cases)

            return formatted_cases
        except Exception as e:
            ## Errors should be in a user-friendly format at this point,
            ## so we can just return the error message.
            return str(e)
        finally:
            IoUtility.delete_dir_if_exists(self._tmp_dir)
