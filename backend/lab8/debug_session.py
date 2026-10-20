"""8-зертханаға арналған қайта өндірілетін debugging сценарийі."""

from __future__ import annotations

import logging
import os
import traceback
from decimal import Decimal
from pathlib import Path
from typing import TypedDict

from lab8.before.refund_service import refund_total
from lab8.order_service import OrderItem
from lab8.refund_service import calculate_refund

LOGGER = logging.getLogger(__name__)
ARTIFACT_DIR = Path(__file__).with_name("artifacts")
BUGGY_ITEMS = [{"name": "Mouse", "price": 7500, "quantity": 2}]
FIXED_ITEMS = [OrderItem("Mouse", Decimal("7500"), 2)]
PAID_TOTAL = 12_000


class FailureEvidence(TypedDict):
    """Қате іске қосылғаннан кейін сақталатын дәлелдер."""

    error_message: str
    stack_trace: str
    buggy_result: str
    expected_result: str


def verify_refund_limit() -> float:
    """Бастапқы функцияның бизнес-инвариантын тексереді."""
    refund_amount = refund_total(BUGGY_ITEMS)
    assert refund_amount <= PAID_TOTAL, (  # noqa: S101 - assertion зертханаға қажет
        f"Қайтарым сомасы {refund_amount:.2f} ₸ төленген "
        f"{PAID_TOTAL:.2f} ₸ сомадан аспауы керек."
    )
    return refund_amount


def run_buggy_scenario() -> float:
    """Қате нұсқаны debugger-де ашуға ыңғайлы call stack арқылы іске қосады."""
    if os.getenv("LAB8_BREAKPOINT") == "1":
        breakpoint()  # F5-тен кейін Step Into арқылы verify_refund_limit-ке кіріңіз.
    return verify_refund_limit()


def capture_failure() -> FailureEvidence:
    """AssertionError мәтіні мен толық stack trace-ті қайтарады."""
    try:
        run_buggy_scenario()
    except AssertionError as error:
        return {
            "error_message": f"AssertionError: {error}",
            "stack_trace": traceback.format_exc(),
            "buggy_result": "15000.00 ₸",
            "expected_result": "12000.00 ₸",
        }
    raise RuntimeError("Қате сценарий күтілген AssertionError қатесін бермеді.")


def main() -> int:
    """Қате дәлелдерін файлдарға жазып, түзетілген нәтижені де журналдайды."""
    ARTIFACT_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=ARTIFACT_DIR / "debug.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )

    LOGGER.info("Buggy refund сценарийі басталды: paid_total=%s", PAID_TOTAL)
    evidence = capture_failure()
    LOGGER.error(evidence["error_message"])
    (ARTIFACT_DIR / "error_message.txt").write_text(
        evidence["error_message"] + "\n", encoding="utf-8"
    )
    (ARTIFACT_DIR / "stack_trace.txt").write_text(
        evidence["stack_trace"], encoding="utf-8"
    )

    fixed_result = calculate_refund(FIXED_ITEMS, Decimal(PAID_TOTAL))
    LOGGER.info("Fixed refund нәтижесі: %s ₸", fixed_result)
    print(evidence["error_message"])
    print(evidence["stack_trace"], end="")
    print(f"Түзетілген нәтиже: {fixed_result} ₸")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
