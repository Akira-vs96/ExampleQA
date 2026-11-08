"""Exercise real child pytest runs, including failures that must not be hidden."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.sro_comparison import compare, render
from scripts.sro_pytest import ComparisonReporter


def assignment(tmp_path: Path, after: str = "assert actual == 4") -> Path:
    directory = tmp_path / "sro99"
    directory.mkdir()
    (directory / "contract.py").write_text(
        "import os\nimport pytest\n"
        "def test_calculation():\n"
        "    actual = 2 if os.environ['QA_SRO_VARIANT'] == 'before' else 4\n"
        "    if os.environ['QA_SRO_VARIANT'] == 'before':\n"
        "        assert actual == 4\n"
        "    else:\n"
        f"        {after}\n",
        encoding="utf-8",
    )
    (directory / "comparison.json").write_text(json.dumps({
        "before": "contract.py", "after": "contract.py",
        "before_label": "buggy", "after_label": "fixed",
        "checks": {"test_calculation": {
            "function": "calculation()", "expected": "4",
            "cause": "Wrong calculation", "fix": "Correct calculation",
        }},
    }), encoding="utf-8")
    return directory


def test_real_before_failure_and_after_pass_ignore_parent_filter(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTEST_ADDOPTS", "-k no_such_test")
    comparison = compare(assignment(tmp_path))
    assert comparison["ok"]
    before, after = comparison["runs"]
    assert before["exit_code"] == 1
    assert before["cases"][0]["status"] == "FAILED"
    assert "2 == 4" in before["cases"][0]["traceback"]
    assert after["exit_code"] == 0
    assert after["cases"][0]["status"] == "PASSED"
    output = "\n".join(render(comparison))
    assert "FAILED test_calculation — calculation()" in output
    assert "PASSED test_calculation — calculation()" in output
    assert "Wrong calculation" in output


@pytest.mark.parametrize("after", ["assert actual == 5", "pytest.skip('not implemented')"])
def test_bad_or_skipped_fix_fails_parent_session(tmp_path, after):
    reporter = ComparisonReporter()
    reporter.assignments.add(assignment(tmp_path, after))
    session = SimpleNamespace(
        exitstatus=0, config=SimpleNamespace(option=SimpleNamespace(collectonly=False))
    )
    reporter.pytest_sessionfinish(session)
    assert session.exitstatus == pytest.ExitCode.TESTS_FAILED
    assert not reporter.comparisons[0]["ok"]


def test_collection_error_does_not_count_as_reproduced_defect(tmp_path):
    directory = assignment(tmp_path)
    (directory / "contract.py").write_text("def invalid syntax\n", encoding="utf-8")
    comparison = compare(directory)
    assert not comparison["ok"]
    assert comparison["runs"][0]["exit_code"] == 2
    assert comparison["runs"][0]["cases"][0]["status"] == "ERROR"
    assert "SyntaxError" in "\n".join(render(comparison))


def test_discovery_does_not_execute_comparisons(tmp_path):
    reporter = ComparisonReporter()
    reporter.assignments.add(tmp_path / "nonexistent")
    session = SimpleNamespace(
        exitstatus=0, config=SimpleNamespace(option=SimpleNamespace(collectonly=True))
    )
    reporter.pytest_sessionfinish(session)
    assert reporter.comparisons == []
    assert session.exitstatus == 0
