"""Identical requirements for the buggy and fixed program, selected by the runner."""

import importlib.util
import os
from pathlib import Path

import pytest

FILENAME = "01_buggy.py" if os.environ.get("QA_SRO_VARIANT") == "before" else "02_fixed.py"
SPEC = importlib.util.spec_from_file_location("sro7_contract", Path(__file__).parents[1] / FILENAME)
assert SPEC is not None and SPEC.loader is not None
program = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(program)


def test_final_price() -> None:
    assert program.final_price(1000, 20) == 800


def test_maximum() -> None:
    assert program.maximum([-8, -3, -5]) == -3


def test_average_empty() -> None:
    with pytest.raises(ValueError, match="кемінде бір сан"):
        program.average([])
