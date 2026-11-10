"""Run the real browser suite, retain its log, then create submission reports."""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    results = ROOT / "sro10/results"
    results.mkdir(exist_ok=True)
    command = [
        sys.executable, "-m", "pytest", "-c", "sro10/pyproject.toml", "sro10",
        "--junitxml=sro10/results/pytest.xml",
    ]
    started = time.time()
    completed = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=180, check=False
    )
    output = completed.stdout + completed.stderr
    print(output, end="", flush=True)
    (results / "pytest.log").write_text(
        f"Command: {' '.join(command)}\n{output}\nExit code: {completed.returncode}\n",
        encoding="utf-8",
    )
    summary = results / "summary.json"
    if not summary.exists() or summary.stat().st_mtime < started:
        raise RuntimeError("No fresh test results; see sro10/results/pytest.log")
    # Completed test failures also belong in the report.
    from sro10.build_report import build_report

    build_report()
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
