from Case import Case
from CaseRunner import CaseRunner


class SuiteRunner:

    @staticmethod
    def run(case_runner: CaseRunner, cases: list[Case]) -> None:
        for case in cases:
            try:
                output = case_runner.run_program(case.inputs)
                normalized_output = output.replace('\r\n', '\n')
                normalized_expected = case.expected_output.replace(
                    '\r\n', '\n')
                result = SuiteRunner._check_result(normalized_output,
                                                   normalized_expected,
                                                   case.comparison_type)
                case.set_result(result)
            except Exception as e:
                case.set_result(False, str(e))

    @staticmethod
    def _check_result(output: str, expected: str,
                      comparison_type: str) -> bool:
        if comparison_type == "contains":
            return expected in output
        elif comparison_type == "equals":
            return expected == output
        else:
            raise ValueError(f"Invalid comparison type: {comparison_type}")
