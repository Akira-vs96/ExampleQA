"""Record three independent regression runs to look for observed intermittent failures."""

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    destination = ROOT / "backend/lab13/results"
    destination.mkdir(exist_ok=True)
    result = {"recorded_at": datetime.now(UTC).isoformat(), "runs": []}
    for number in range(1, 4):
        command = [sys.executable, "-m", "pytest", "-q", "backend/lab13/tests"]
        run = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "QA_VARIANT": "after"},
            timeout=60,
        )
        (destination / f"repeat-{number}.txt").write_text(run.stdout + run.stderr, encoding="utf-8")
        result["runs"].append({"run": number, "exit_code": run.returncode})
    result["all_passed"] = all(run["exit_code"] == 0 for run in result["runs"])
    result["interpretation"] = (
        "No intermittent failure observed in these runs"
        if result["all_passed"]
        else "Investigate failures; no retries used"
    )
    (destination / "stability.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return int(not result["all_passed"])


if __name__ == "__main__":
    raise SystemExit(main())
