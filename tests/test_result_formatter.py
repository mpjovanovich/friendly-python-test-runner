import pytest
from src.test_runner.case import Case
from src.test_runner.result_formatter import ResultFormatter


def test_displays_program_input():
    case = Case(title="",
                inputs=["input1", " input2 "],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    assert "PROGRAM INPUT:\n\"input1\"\n\" input2 \"" in ResultFormatter.format_case(
        case, 1)


def test_displays_error_header_when_error():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(False, "", "Error message")
    assert "ERROR:" in ResultFormatter.format_case(case, 1)


def test_displays_error_message_when_error():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(False, "", "message123")
    assert "message123" in ResultFormatter.format_case(case, 1)


def test_displays_program_output_header_when_no_error():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "output", "")
    assert "PROGRAM OUTPUT:" in ResultFormatter.format_case(case, 1)


def test_displays_program_output_when_no_error():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "output123", "")
    assert "output123" in ResultFormatter.format_case(case, 1)


def test_displays_checking_for_contains_message():
    case = Case(title="",
                inputs=[],
                expected_output="expected",
                comparison_type="contains",
                is_bonus=False)
    assert "CHECKING FOR OUTPUT (contains):\n\"expected\"" in ResultFormatter.format_case(
        case, 1)


def test_displays_checking_for_equals_message():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="equals",
                is_bonus=False)
    assert "CHECKING FOR OUTPUT (equals):" in ResultFormatter.format_case(
        case, 1)


def test_pass_gives_green_check():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "", None)
    assert "✅ PASSED" in ResultFormatter.format_case(case, 1)


def test_fail_gives_red_x():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(False, "", None)
    assert "❌ FAILED" in ResultFormatter.format_case(case, 1)


def test_bonus_gives_star():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=True)
    case.set_result(True, "", None)
    assert "⭐ BONUS: " in ResultFormatter.format_case(case, 1)


def test_title_line_correct():
    case = Case(title="The Title",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "", None)
    assert "🎮 1.) The Title" in ResultFormatter.format_case(case, 1)


def test_runs_multiple_cases():
    case1 = Case(title="",
                 inputs=[],
                 expected_output="",
                 comparison_type="contains",
                 is_bonus=False)
    case1.set_result(True, "output", None)
    case2 = Case(title="",
                 inputs=[],
                 expected_output="",
                 comparison_type="contains",
                 is_bonus=False)
    case2.set_result(False, "output", None)
    output = ResultFormatter.format_cases([case1, case2])
    assert "✅ PASSED" in output
    assert "❌ FAILED" in output


def test_debug_format():
    case = Case(title="Title of the case",
                inputs=["input1", "input2", "input3"],
                expected_output="Expected output",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "line1\nline2\nExpected output", "")
    # case.set_result(False, "line1\nline2\nline3", "Error message")
    print()
    print()
    print(ResultFormatter().format_case(case, 1))
    print()
