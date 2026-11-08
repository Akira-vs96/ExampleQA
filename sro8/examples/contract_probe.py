"""The same four assertions must fail before the fix and pass after it."""

import importlib.util
import os
from pathlib import Path

FILENAME = "01_buggy.py" if os.environ.get("QA_SRO_VARIANT") == "before" else "02_fixed.py"
SPEC = importlib.util.spec_from_file_location("sro8_contract", Path(__file__).parents[1] / FILENAME)
assert SPEC is not None and SPEC.loader is not None
shop = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shop)


def test_line_total() -> None:
    assert shop.line_total(2000, 3) == 6000


def test_discounted_total() -> None:
    assert shop.discounted_total(10000, 20) == 8000


def test_shipping_cost_boundary() -> None:
    assert shop.shipping_cost(10000) == 0


def test_shipping_cost_type() -> None:
    result = shop.shipping_cost(10001)
    assert type(result) is int, f"expected int, actual {type(result).__name__}: {result!r}"
