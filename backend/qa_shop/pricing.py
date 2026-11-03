"""Money calculations and explicit order transitions, independent of HTTP and storage."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Final

CENT: Final = Decimal("0.01")
FREE_SHIPPING: Final = Decimal("10000.00")
SHIPPING_FEE: Final = Decimal("1000.00")
TRANSITIONS: Final = {
    "new": frozenset({"paid", "cancelled"}),
    "paid": frozenset({"shipped", "refunded"}),
    "shipped": frozenset({"completed"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
    "refunded": frozenset(),
}


def amount(value: Decimal | str | int) -> Decimal:
    """Accept only finite nonnegative amounts; round half up to two decimal places."""
    if isinstance(value, bool):
        raise ValueError("Сома сан болуы керек.")
    try:
        result = Decimal(str(value))
        if not result.is_finite() or result < 0 or result > Decimal("1000000000"):
            raise ValueError("Сома 0 мен 1000000000 аралығында болуы керек.")
        return result.quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError) as error:
        raise ValueError("Соманың пішімі қате.") from error


def line_total(price: Decimal | str | int, quantity: int) -> Decimal:
    """A line contains 1–100 whole units; booleans are not quantities."""
    if type(quantity) is not int or not 1 <= quantity <= 100:
        raise ValueError("Тауар саны 1 мен 100 арасындағы бүтін сан болуы керек.")
    return (amount(price) * quantity).quantize(CENT)


def discounted_total(subtotal: Decimal | str | int, percent: int) -> Decimal:
    """Discount is an integer percentage from zero to one hundred, inclusive."""
    if type(percent) is not int or not 0 <= percent <= 100:
        raise ValueError("Жеңілдік 0 мен 100 арасындағы бүтін сан болуы керек.")
    return (amount(subtotal) * (100 - percent) / 100).quantize(CENT, rounding=ROUND_HALF_UP)


def shipping_cost(total: Decimal | str | int) -> Decimal:
    """Delivery is free starting at 10000 after discount, including the boundary."""
    return Decimal("0.00") if amount(total) >= FREE_SHIPPING else SHIPPING_FEE


def order_total(lines: list[tuple[Decimal | str | int, int]], percent: int = 0) -> Decimal:
    """Calculate a nonempty basket and apply delivery to the discounted amount."""
    if not lines:
        raise ValueError("Себет бос болмауы керек.")
    subtotal = sum((line_total(price, count) for price, count in lines), start=Decimal(0))
    total = discounted_total(subtotal, percent)
    return total + shipping_cost(total)


def transition_order(state: str, target: str) -> str:
    """Reject unknown states and every edge missing from the transition graph."""
    if state not in TRANSITIONS or target not in TRANSITIONS[state]:
        raise ValueError(f"Рұқсат етілмеген ауысу: {state} → {target}.")
    return target
