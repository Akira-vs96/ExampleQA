"""The documented catalogue is also an executable pytest suite."""

import pytest

from lab5.run_cases import CASES, execute


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_documented_case(case, pricing):
    result = execute(case, pricing)
    assert result["status"] == "PASS", result
