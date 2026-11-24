"""Save real failed and corrected runs without changing production files."""

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_suite(destination: Path, targets: list[str]) -> dict:
    destination.mkdir(parents=True, exist_ok=True)
    evidence = {"started_at": datetime.now(UTC).isoformat(), "runs": []}
    for variant in ("before", "after"):
        command = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            *targets,
            f"--junitxml={destination / (variant + '.xml')}",
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "QA_VARIANT": variant},
            timeout=90,
        )
        (destination / f"{variant}.txt").write_text(result.stdout + result.stderr, encoding="utf-8")
        evidence["runs"].append(
            {
                "variant": variant,
                "exit_code": result.returncode,
                "command": command,
                "expected": "failure" if variant == "before" else "success",
            }
        )
        print(f"\n=== {destination.relative_to(ROOT)} · {variant} ===", flush=True)
        print(result.stdout + result.stderr, end="", flush=True)
        print(f"=== {variant} exit code: {result.returncode} ===", flush=True)
    evidence["demonstration_passed"] = (
        evidence["runs"][0]["exit_code"] == 1 and evidence["runs"][1]["exit_code"] == 0
    )
    (destination / "comparison.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", action="store_true")
    parser.add_argument(
        "--lab13", action="store_true", help="run only the Lab 13 before/after suite"
    )
    options = parser.parse_args()
    if options.lab13:
        runs = [run_suite(ROOT / "backend/lab13/results", ["backend/lab13/tests"])]
    elif options.pipeline:
        runs = [run_suite(ROOT / "backend/lab14/results", ["backend/lab13/tests"])]
    else:
        runs = [
            run_suite(ROOT / f"backend/lab{lab}/results", [f"backend/lab{lab}/tests"])
            for lab in (4, 6, 13)
        ]
    return int(not all(item["demonstration_passed"] for item in runs))


if __name__ == "__main__":
    raise SystemExit(main())
