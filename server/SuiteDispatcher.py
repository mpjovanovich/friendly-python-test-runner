from CaseRunner import CaseRunner
from SuiteLoader import SuiteLoader
from SuiteRunner import SuiteRunner
from ResultFormatter import ResultFormatter


class SuiteDispatcher:

    def __init__(self, test_cases_dir: str):
        self._test_cases_dir = test_cases_dir

    def run_suite(self, suite_name: str, program_path: str) -> str:
        suite_loader = SuiteLoader(self._test_cases_dir)
        cases = suite_loader.load_suite(suite_name)

        case_runner = CaseRunner(program_path)
