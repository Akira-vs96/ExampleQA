"""Execute identical cases against the faulty and corrected pricing modules."""

import csv
import importlib
import json
from datetime import UTC, datetime
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
CASES = json.loads((DIRECTORY / "cases.json").read_text(encoding="utf-8"))


def execute(case: dict, module) -> dict:
    try:
        actual = str(getattr(module, case["operation"])(*case["args"]))
        passed = "exception" not in case and actual == case.get("expected")
    except Exception as error:  # The lab records unexpected exception types as FAIL.
        actual = type(error).__name__
        passed = actual == case.get("exception")
    return {**case, "actual": actual, "status": "PASS" if passed else "FAIL"}


def main() -> int:
    results = {"started_at": datetime.now(UTC).isoformat()}
    for variant, name in [("before", "lab6.before.pricing"), ("after", "qa_shop.pricing")]:
        module = importlib.import_module(name)
        results[variant] = [execute(case, module) for case in CASES]
    destination = DIRECTORY / "results"
    destination.mkdir(exist_ok=True)
    (destination / "cases.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (destination / "cases.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "Scenario",
                "Requirement",
                "Preconditions",
                "Data",
                "Steps",
                "Expected",
                "Before",
                "After",
                "Status",
                "Priority",
                "Severity",
            ]
        )
        for before, after in zip(results["before"], results["after"], strict=True):
            writer.writerow(
                [
                    after["id"],
                    after["scenario"],
                    after["requirement"],
                    "Таза модуль, сыртқы сервис қажет емес",
                    json.dumps(after["args"]),
                    f"1. Модульді жүктеу; 2. {after['operation']} шақыру; 3. Нәтижені салыстыру",
                    after.get("expected", after.get("exception")),
                    before["actual"],
                    after["actual"],
                    after["status"],
                    after["priority"],
                    after["severity"],
                ]
            )
    for variant in ("before", "after"):
        passed = sum(item["status"] == "PASS" for item in results[variant])
        print(f"{variant}: {passed}/{len(CASES)} PASS")
    return int(any(item["status"] != "PASS" for item in results["after"]))


if __name__ == "__main__":
    raise SystemExit(main())
