import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from ResultFormatter import ResultFormatter
from Case import Case


def test_pass_gives_green_check():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "", None)
    assert "✅ PASSED" in ResultFormatter().format_case(case)


def test_fail_gives_red_x():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(False, "", None)
    assert "❌ FAILED" in ResultFormatter().format_case(case)


def test_bonus_gives_star():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=True)
    case.set_result(True, "", None)
    assert "⭐ BONUS: " in ResultFormatter().format_case(case)


def test_not_bonus_gives_game_icon():
    case = Case(title="",
                inputs=[],
                expected_output="",
                comparison_type="contains",
                is_bonus=False)
    case.set_result(True, "", None)
    assert "🎮 " in ResultFormatter().format_case(case)


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
    output = ResultFormatter([case1, case2]).format_cases()
    assert "✅ PASSED" in output
    assert "❌ FAILED" in output
