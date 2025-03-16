from src.test_runner.case import Case


class ResultFormatter:

    @staticmethod
    def format_cases(cases: list[Case]) -> str:
        return "\n" + "\n\n".join(
            [ResultFormatter.format_case(case) for case in cases])

    @staticmethod
    def format_case(case: Case) -> str:
        separator = "=" * 60
        sub_separator = "-" * 55

        title = f"{'⭐ BONUS: ' if case.is_bonus else '🎮 '}{case.title}"

        error = "ERROR:\n"
        error += "┌─────────────────────────────────────────────────────┐\n"
        error += f"{case.error}\n"
        error += "└─────────────────────────────────────────────────────┘"

        program_output = "PROGRAM OUTPUT:\n"
        program_output += "┌─────────────────────────────────────────────────────┐\n"
        program_output += f"{case.output}\n"
        program_output += "└─────────────────────────────────────────────────────┘"

        expected_output = f'CHECKING FOR OUTPUT ({"contains" if case.comparison_type == "contains" else "equals"}):\n'
        expected_output += case.expected_output

        result = f'RESULT: {"✅ PASSED" if case.passed else "❌ FAILED"}'

        formatted_result = f"{separator}\n"
        formatted_result += f"{title}\n"
        formatted_result += f"{sub_separator}\n"
        if case.error:
            formatted_result += f"{error}\n"
        else:
            formatted_result += f"{program_output}\n"
            formatted_result += f"\n"
            formatted_result += f"{expected_output}\n"
        formatted_result += f"\n"
        formatted_result += f"{result}\n"
        formatted_result += f"{separator}\n"

        return formatted_result
