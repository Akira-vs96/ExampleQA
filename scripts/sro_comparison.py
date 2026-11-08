"""Execute the same contracts against before/after versions and show real failures."""

import json
import os
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHILD_FLAG = "QA_SRO_COMPARISON_CHILD"


def read_junit(path: Path) -> list[dict]:
    """Keep assertion failures, setup errors and skips distinct."""
    cases = []
    for case in ET.parse(path).iter("testcase"):
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")
        problem = failure if failure is not None else error
        status = "PASSED"
        if failure is not None:
            status = "FAILED"
        elif error is not None:
            status = "ERROR"
        elif skipped is not None:
            status = "SKIPPED"
        cases.append({
            "name": case.attrib["name"],
            "status": status,
            "message": problem.attrib.get("message", "") if problem is not None else "",
            "traceback": (problem.text or "").strip() if problem is not None else "",
        })
    return cases


def compare(assignment: Path) -> dict:
    """Run real pytest processes; expected before failures do not mask after failures."""
    config = json.loads((assignment / "comparison.json").read_text(encoding="utf-8"))
    results = assignment / "results"
    results.mkdir(exist_ok=True)
    comparison = {"assignment": assignment.name, "config": config, "runs": []}
    for phase in ("before", "after"):
        command = [
            sys.executable, "-m", "pytest", "-q", "-c", str(ROOT / "pyproject.toml"),
            "--tb=short", "--color=no", str(assignment / config[phase]),
            f"--junitxml={results / (phase + '.xml')}",
        ]
        environment = os.environ.copy()
        environment.update({CHILD_FLAG: "1", "QA_SRO_VARIANT": phase})
        # Parent options such as -k and --lf must not deselect the comparison contracts.
        environment.pop("PYTEST_ADDOPTS", None)
        try:
            completed = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
                timeout=30, check=False,
            )
            output = completed.stdout + completed.stderr
            cases = read_junit(results / f"{phase}.xml")
            run = {"phase": phase, "exit_code": completed.returncode, "cases": cases}
            if completed.returncode not in (0, 1) or not cases:
                run["error"] = "pytest did not complete the contract tests\n" + output
        except (subprocess.TimeoutExpired, OSError, ET.ParseError) as error:
            output = str(error)
            run = {"phase": phase, "exit_code": -1, "cases": [], "error": output}
        (results / f"{phase}.log").write_text(output, encoding="utf-8")
        comparison["runs"].append(run)
    before, after = comparison["runs"]
    comparison["ok"] = (
        before["exit_code"] == 1
        and bool(before["cases"])
        and any(case["status"] == "FAILED" for case in before["cases"])
        and all(case["status"] in {"FAILED", "PASSED"} for case in before["cases"])
        and after["exit_code"] == 0
        and bool(after["cases"])
        and all(case["status"] == "PASSED" for case in after["cases"])
        and sorted(case["name"] for case in before["cases"])
        == sorted(case["name"] for case in after["cases"])
        and not any(run.get("error") for run in comparison["runs"])
    )
    (results / "comparison.json").write_text(
        json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return comparison


def render(comparison: dict) -> list[str]:
    """Produce a readable console report, using only actual pytest outcomes."""
    config = comparison["config"]
    lines = ["", f"{comparison['assignment'].upper()}: ошибочный и исправленный варианты"]
    lines.append("Одинаковые требования проверяются на обеих версиях.")
    for run in comparison["runs"]:
        phase = run["phase"]
        label = "ОШИБОЧНЫЙ" if phase == "before" else "ИСПРАВЛЕННЫЙ"
        lines.extend(["", f"{label} — {config[phase + '_label']}"])
        for case in run["cases"]:
            details = config.get("checks", {}).get(case["name"], {})
            lines.append(f"{case['status']} {case['name']} — {details.get('function', '')}")
            if details.get("expected"):
                lines.append(f"  Требование: {details['expected']}")
            if case["traceback"]:
                lines.extend("  " + line for line in case["traceback"].splitlines())
            if case["status"] == "FAILED" and phase == "before":
                lines.append("  Причина: " + details.get("cause", case["message"]))
                if details.get("fix"):
                    lines.append("  Исправление: " + details["fix"])
        if run.get("error"):
            lines.extend(["ERROR запуска сравнения", run["error"]])
        counts = {status: sum(case["status"] == status for case in run["cases"])
                  for status in ("PASSED", "FAILED", "ERROR", "SKIPPED")}
        lines.append(
            f"Итог {label}: {counts['PASSED']} passed, {counts['FAILED']} failed, "
            f"{counts['ERROR']} errors, {counts['SKIPPED']} skipped; exit={run['exit_code']}"
        )
    lines.extend(["", "Сравнение: " + (
        "PASS — исходные ошибки воспроизведены, исправленные проверки прошли."
        if comparison["ok"] else "FAIL — результаты сравнения требуют проверки."
    )])
    return lines


class ComparisonSuite(unittest.TestSuite):
    """Also show the comparison for a direct unittest run of SRO 7."""

    def __init__(self, tests: unittest.TestSuite, assignment: Path) -> None:
        super().__init__(tests)
        self.assignment = assignment

    def run(self, result: unittest.TestResult, debug: bool = False) -> unittest.TestResult:
        super().run(result, debug)
        if os.environ.get(CHILD_FLAG) != "1":
            comparison = compare(self.assignment)
            stream = getattr(result, "stream", sys.stderr)
            for line in render(comparison):
                print(line, file=stream)
            if not comparison["ok"]:
                failure = unittest.FunctionTestCase(
                    lambda: None, description="before/after comparison"
                )
                result.startTest(failure)
                try:
                    raise AssertionError("Before/after comparison failed; see the console report")
                except AssertionError:
                    result.addFailure(failure, sys.exc_info())
                result.stopTest(failure)
        return result
