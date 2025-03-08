from Case import Case


class ResultFormatter:

    def __init__(self, cases=None):
        self._cases = cases if cases is not None else []

    def format_cases(self) -> str:
        return "\n".join([self._format_case(case) for case in self._cases])

    def format_case(self, case: Case) -> str:
        separator = "=" * 60
        sub_separator = "-" * 60
        return f"""{separator}
🎮 {case.title}
{sub_separator}
{case.output}

Checking for:
"{case.expected_output}"

Result: {"✅ PASSED" if case.passed else "❌ FAILED"}
{separator}"""
