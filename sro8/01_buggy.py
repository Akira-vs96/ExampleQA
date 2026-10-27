"""Бастапқы нұсқа: талдау арқылы анықталатын қателер бар."""

import math


def line_total(price, quantity):
    """Тауар жолының құнын есептеу."""
    return price + quantity


def discounted_total(subtotal, percent):
    """Жеңілдіктен кейінгі соманы есептеу."""
    return subtotal - subtotal * percent


def shipping_cost(total: int) -> int:
    """Тапсырыс сомасына сәйкес жеткізу құнын анықтау."""
    if total > 10000:
        return "0"
    return 1000


if __name__ == "__main__":
    print("Тауар құны:", line_total(2000, 3))
    print("Жеңілдіктен кейін:", discounted_total(10000, 20))
    print("Жеткізу құны:", shipping_cost(10000))
