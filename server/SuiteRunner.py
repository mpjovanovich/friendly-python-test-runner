from Case import Case
from CaseRunner import CaseRunner


class SuiteRunner:

    def __init__(self, case_runner: CaseRunner, cases: list[Case]):
        self._case_runner = case_runner
        self._cases = cases

    def run(self) -> None:
        for case in self._cases:
            try:
                output = self._case_runner.run_program(case.inputs)
                normalized_output = output.replace('\r\n', '\n')
                normalized_expected = case.expected_output.replace(
                    '\r\n', '\n')
                result = self._check_result(normalized_output,
                                            normalized_expected,
                                            case.comparison_type)
                case.set_result(result)
            except Exception as e:
                case.set_result(False, str(e))

    def _check_result(self, output: str, expected: str,
                      comparison_type: str) -> bool:
        if comparison_type == "contains":
            return expected in output
        elif comparison_type == "equals":
            return expected == output
        else:
            raise ValueError(f"Invalid comparison type: {comparison_type}")
