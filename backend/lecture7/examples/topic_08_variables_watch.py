"""8. Variables және Watch панельдерінде мәндерді бақылау."""


def process_order(price: int, quantity: int, percent: int) -> float:
    subtotal = price * quantity
    discount = subtotal * percent / 100
    total = subtotal - discount  # Breakpoint осы жолда.
    return total


def main() -> None:
    print("8-сұрақ: Variables және Watch")
    total = process_order(1500, 3, 10)
    print("Watch өрнектері: subtotal, discount, subtotal - discount")
    print("Нәтиже:", total)


if __name__ == "__main__":
    main()
