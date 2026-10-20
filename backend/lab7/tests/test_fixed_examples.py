from lab7.examples.fixed_discount import final_price
from lab7.examples.fixed_division import average
from lab7.examples.fixed_maximum import find_max


def test_average_handles_zero_count() -> None:
    assert average(10, 0) == 0


def test_average_calculates_normal_value() -> None:
    assert average(10, 2) == 5


def test_discount_is_calculated_as_percent() -> None:
    assert final_price(1000, 20) == 800


def test_maximum_is_found_correctly() -> None:
    assert find_max([4, 9, 2]) == 9
