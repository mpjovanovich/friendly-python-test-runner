from src.test_runner.case import Case


class ResultFormatter:

    @staticmethod
    def format_cases(cases: list[Case]) -> str:
        return "\n" + "\n\n".join([
            ResultFormatter.format_case(case, test_number + 1)
            for test_number, case in enumerate(cases)
        ]) + "\n" + ResultFormatter._get_summary(cases)

    @staticmethod
    def format_case(case: Case, test_number: int) -> str:
        separator = "=" * 60
        sub_separator = "-" * 55

        title = f"{'⭐ BONUS: ' if case.is_bonus else '🎮 '}{test_number}.) {case.title}"

        program_input = "PROGRAM INPUT:\n"
        program_input += "\n".join([f'"{input}"' for input in case.inputs])
        program_input += "\n"

        error = "ERROR:\n"
        error += "┌─────────────────────────────────────────────────────┐\n"
        error += f"{case.error}\n"
        error += "└─────────────────────────────────────────────────────┘"

        program_output = "PROGRAM OUTPUT:\n"
        program_output += "┌─────────────────────────────────────────────────────┐\n"
        program_output += f"{case.output}\n"
        program_output += "└─────────────────────────────────────────────────────┘"

        expected_output = f'CHECKING FOR OUTPUT ({"contains" if case.comparison_type == "contains" else "equals"}):\n'
        expected_output += f'"{case.expected_output}"'

        result = f'RESULT: {"✅ PASSED" if case.passed else "❌ FAILED"}'

        formatted_result = f"{separator}\n"
        formatted_result += f"{title}\n"
        formatted_result += f"{sub_separator}\n"
        formatted_result += f"{program_input}\n"
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

    @staticmethod
    def _get_num_passed(cases: list[Case]) -> int:
        return sum(1 for case in cases if case.passed and not case.is_bonus)

    @staticmethod
    def _get_num_non_bonus(cases: list[Case]) -> int:
        return sum(1 for case in cases if not case.is_bonus)

    @staticmethod
    def _get_num_bonus_passed(cases: list[Case]) -> int:
        return sum(1 for case in cases if case.passed and case.is_bonus)

    @staticmethod
    def _get_num_bonus(cases: list[Case]) -> int:
        return sum(1 for case in cases if case.is_bonus)

    @staticmethod
    def _get_summary(cases: list[Case]) -> str:
        num_passed = ResultFormatter._get_num_passed(cases)
        num_bonus_passed = ResultFormatter._get_num_bonus_passed(cases)
        num_non_bonus = ResultFormatter._get_num_non_bonus(cases)
        num_bonus = ResultFormatter._get_num_bonus(cases)

        return f"SUMMARY: {num_passed}/{num_non_bonus} passed, {num_bonus_passed}/{num_bonus} bonus"
