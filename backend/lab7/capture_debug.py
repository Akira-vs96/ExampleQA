"""Reproduce an exception and drive a real pdb session with step/next/return commands."""

import io
import json
import logging
import pdb
import traceback
from contextlib import redirect_stdout
from datetime import UTC, datetime
from pathlib import Path

from lab7.examples.buggy_division import average as buggy_average
from lab7.examples.fixed_division import average as fixed_average

DIRECTORY = Path(__file__).resolve().parent


def scenario():
    total, count = 10, 0
    return buggy_average(total, count)


def main() -> int:
    destination = DIRECTORY / "results"
    destination.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=destination / "debug.log",
        filemode="w",
        level=logging.INFO,
        format="%(levelname)s %(message)s",
        force=True,
    )
    try:
        scenario()
    except ZeroDivisionError as error:
        error_text = f"{type(error).__name__}: {error}"
        (destination / "stack_trace.txt").write_text(traceback.format_exc(), encoding="utf-8")
        (destination / "error_message.txt").write_text(error_text + "\n", encoding="utf-8")
        logging.exception("count=0: reproduced the original error")
    else:
        raise RuntimeError("The faulty program did not reproduce the exception.")
    output = io.StringIO()
    debugger = pdb.Pdb(stdin=io.StringIO(), stdout=output)
    # next stops on the call; step enters the function; up/down inspect the call stack.
    commands = [
        "list",
        "next",
        "p total",
        "p count",
        "step",
        "where",
        "p total",
        "p count",
        "up",
        "down",
        "return",
        "continue",
    ]
    debugger.cmdqueue = commands.copy()
    with redirect_stdout(output):
        try:
            debugger.runcall(scenario)
        except ZeroDivisionError:
            pass
    (destination / "pdb_session.txt").write_text(output.getvalue(), encoding="utf-8")
    actual = fixed_average(10, 0)
    logging.info("Corrected result: %s", actual)
    result = {
        "captured_at": datetime.now(UTC).isoformat(),
        "before": error_text,
        "after": actual,
        "passed": actual == 0,
        "commands": commands,
        "debugger": "pdb.Pdb",
    }
    (destination / "comparison.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Before: {error_text}; after: {actual}. Real pdb transcript saved.")
    return int(not result["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
