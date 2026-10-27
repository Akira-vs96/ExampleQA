"""Негізгі функциялардың қалыпты, шекаралық және қате кірістерін тексеру."""

import importlib.util
from pathlib import Path

import pytest


def load_module(filename):
    """Бастапқы және түзетілген файлдарды бөлек жүктеу."""
    spec = importlib.util.spec_from_file_location(filename, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


buggy = load_module("01_buggy.py")
fixed = load_module("02_fixed.py")


def test_original_defects():
    """Бастапқы нұсқаның төрт ақауы нақты қайталанады."""
    assert buggy.line_total(2000, 3) == 2003
    assert buggy.discounted_total(10000, 20) == -190000
    assert buggy.shipping_cost(10000) == 1000
    assert buggy.shipping_cost(10001) == "0"


@pytest.mark.parametrize("price, quantity, expected", [(2000, 3, 6000), (0, 2, 0)])
def test_line_total(price, quantity, expected):
    assert fixed.line_total(price, quantity) == expected


@pytest.mark.parametrize("price, quantity", [(-1, 1), (100, 0), (100, -2)])
def test_invalid_line(price, quantity):
    with pytest.raises(ValueError):
        fixed.line_total(price, quantity)


@pytest.mark.parametrize(
    "subtotal, percent, expected",
    [(10000, 20, 8000), (10000, 0, 10000), (10000, 100, 0), (101, 50, 50)],
)
def test_discount(subtotal, percent, expected):
    assert fixed.discounted_total(subtotal, percent) == expected


@pytest.mark.parametrize("subtotal, percent", [(-1, 20), (100, -1), (100, 101)])
def test_invalid_discount(subtotal, percent):
    with pytest.raises(ValueError):
        fixed.discounted_total(subtotal, percent)


@pytest.mark.parametrize("total, expected", [(0, 1000), (9999, 1000), (10000, 0), (10001, 0)])
def test_shipping_boundary_and_type(total, expected):
    result = fixed.shipping_cost(total)
    assert result == expected
    assert type(result) is int


def test_negative_shipping():
    with pytest.raises(ValueError):
        fixed.shipping_cost(-1)


def test_order_scenario():
    """Жеткізу шегі жеңілдіктен кейінгі сомаға қолданылады."""
    subtotal = fixed.line_total(2000, 6)
    total = fixed.discounted_total(subtotal, 20)
    assert total == 9600
    assert total + fixed.shipping_cost(total) == 10600
