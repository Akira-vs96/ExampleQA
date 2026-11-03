"""Build, test and record actual stage outcomes; --full adds local UI/load/ZAP checks."""

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "backend/lab15/results"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    env = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join([str(ROOT / "backend"), str(ROOT)]),
        "QA_PYTHON": sys.executable,
    }
    stages = [
        ("build", ["node", "scripts/build.mjs"]),
        (
            "analysis",
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--config",
                "pyproject.toml",
                "backend/qa_shop",
                "backend/app",
                "backend/lab3",
                "backend/lab4",
                "backend/lab5",
                "backend/lab6",
                "backend/lab7/capture_debug.py",
                "backend/lab10",
                "backend/lab11",
                "backend/lab12",
                "backend/lab13",
                "scripts",
                "conftest.py",
            ],
        ),
        (
            "tests",
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--cov=qa_shop",
                "--cov-branch",
                "--cov-fail-under=85",
                f"--cov-report=json:{RESULTS / 'coverage.json'}",
                f"--cov-report=xml:{RESULTS / 'coverage.xml'}",
                f"--cov-report=html:{RESULTS / 'coverage-html'}",
                f"--junitxml={RESULTS / 'pytest.xml'}",
            ],
        ),
        ("cases", [sys.executable, "backend/lab5/run_cases.py"]),
        ("debugger", [sys.executable, "backend/lab7/capture_debug.py"]),
        ("before-after", [sys.executable, "scripts/demonstrate.py"]),
        ("pipeline-demo", [sys.executable, "scripts/demonstrate.py", "--pipeline"]),
        ("stability", [sys.executable, "scripts/repeat_regression.py"]),
        ("security-demo", [sys.executable, "backend/lab12/demonstrate_security.py"]),
        ("lab8", ["bash", "backend/lab8/run_analysis.sh"]),
    ]
    if args.full:
        stages += [
            ("browser", ["node", "scripts/demo_ui.mjs"]),
            ("load", [sys.executable, "backend/lab11/run_load.py"]),
            ("zap", [sys.executable, "backend/lab12/run_zap.py"]),
        ]
    summary = {"started_at": datetime.now(UTC).isoformat(), "full": args.full, "stages": []}
    for name, command in stages:
        print(f"Running {name}...", flush=True)
        started = datetime.now(UTC)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=240
            )
            output, code = result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired as error:
            output, code = f"Stage timed out: {error}", 124
        (RESULTS / f"{name}.log").write_text(output, encoding="utf-8")
        summary["stages"].append(
            {
                "name": name,
                "command": command,
                "exit_code": code,
                "duration_seconds": (datetime.now(UTC) - started).total_seconds(),
            }
        )
        print(f"{name}: {'PASS' if code == 0 else 'FAIL'}", flush=True)
        if code:
            print(output[-4000:], flush=True)
    summary["completed_at"] = datetime.now(UTC).isoformat()
    summary["passed"] = all(item["exit_code"] == 0 for item in summary["stages"])
    payload = json.dumps(summary, indent=2) + "\n"
    (RESULTS / "checks.json").write_text(payload, encoding="utf-8")
    if args.full:
        (RESULTS / "full-checks.json").write_text(payload, encoding="utf-8")
    subprocess.run([sys.executable, "scripts/summarize_results.py"], cwd=ROOT, env=env, check=True)
    return int(not summary["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
