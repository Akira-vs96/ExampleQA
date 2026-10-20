"""Тексерілген және түзетілген тапсырыс есептеу логикасы."""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Final

MONEY_STEP: Final = Decimal("0.01")
HUNDRED: Final = Decimal(100)
MIN_PERCENT: Final = Decimal(0)
MAX_PERCENT: Final = Decimal(100)


class OrderValidationError(ValueError):
    """Тапсырыс деректері бизнес ережелеріне сай болмағанда көтеріледі."""


class CustomerType(StrEnum):
    """Қолдау көрсетілетін сатып алушы санаттары."""

    REGULAR = "regular"
    NEW = "new"
    STUDENT = "student"
    EMPLOYEE = "employee"
    VIP = "vip"
    PARTNER = "partner"


@dataclass(frozen=True, slots=True)
class OrderItem:
    """Бір тауар позициясы."""

    name: str
    unit_price: Decimal
    quantity: int = 1


@dataclass(frozen=True, slots=True)
class OrderSummary:
    """Тапсырысты есептеу нәтижесі."""

    subtotal: Decimal
    discount_percent: Decimal
    discount_amount: Decimal
    total: Decimal


CUSTOMER_DISCOUNTS: Final[dict[CustomerType, Decimal]] = {
    CustomerType.REGULAR: Decimal(0),
    CustomerType.NEW: Decimal(5),
    CustomerType.STUDENT: Decimal(10),
    CustomerType.EMPLOYEE: Decimal(15),
    CustomerType.VIP: Decimal(20),
    CustomerType.PARTNER: Decimal(25),
}


def _validate_item(item: OrderItem) -> None:
    if not item.name.strip():
        raise OrderValidationError("Тауар атауы бос болмауы керек.")
    if item.unit_price < 0:
        raise OrderValidationError("Тауар бағасы теріс болмауы керек.")
    if item.quantity <= 0:
        raise OrderValidationError("Тауар саны нөлден үлкен болуы керек.")


def calculate_subtotal(items: Iterable[OrderItem]) -> Decimal:
    """Тауарларды тексеріп, жеңілдікке дейінгі соманы қайтарады."""
    item_list = tuple(items)
    if not item_list:
        raise OrderValidationError("Тапсырыс кемінде бір тауардан тұруы керек.")
    for item in item_list:
        _validate_item(item)
    return sum(
        (item.unit_price * item.quantity for item in item_list),
        start=Decimal(0),
    ).quantize(MONEY_STEP)


def calculate_order(
    items: Iterable[OrderItem],
    customer_type: CustomerType = CustomerType.REGULAR,
    promo_percent: Decimal = Decimal(0),
) -> OrderSummary:
    """Санат пен промокодтың ең үлкен жеңілдігін қауіпсіз есептейді."""
    if not MIN_PERCENT <= promo_percent <= MAX_PERCENT:
        raise OrderValidationError("Жеңілдік 0 мен 100 аралығында болуы керек.")

    subtotal = calculate_subtotal(items)
    discount_percent = max(CUSTOMER_DISCOUNTS[customer_type], promo_percent)
    discount_amount = (subtotal * discount_percent / HUNDRED).quantize(MONEY_STEP)
    total = (subtotal - discount_amount).quantize(MONEY_STEP)
    return OrderSummary(subtotal, discount_percent, discount_amount, total)
