from Case import Case


class ResultFormatter:

    def __init__(self, cases=None):
        self._cases = cases if cases is not None else []

    def format_cases(self) -> str:
        return "\n\n\n".join([self.format_case(case) for case in self._cases])

    def format_case(self, case: Case) -> str:
        separator = "=" * 60
        sub_separator = "-" * 55
        return f"""{separator}
{"⭐ BONUS: " if case.is_bonus else "🎮 "}{case.title}
{sub_separator}
Program Output:
┌─────────────────────────────────────────────────────┐
{case.output}
└─────────────────────────────────────────────────────┘

Checking if output {"contains" if case.comparison_type == "contains" else "equals"}:
"{case.expected_output}"

Result: {"✅ PASSED" if case.passed else "❌ FAILED"}
{separator}"""
