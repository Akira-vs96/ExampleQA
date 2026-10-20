"""7. Step Over, Step Into және Step Out командаларын көрсету."""


def apply_tax(amount: float) -> float:
    tax = amount * 0.12
    return amount + tax


def checkout(price: float, quantity: int) -> float:
    subtotal = price * quantity
    return apply_tax(subtotal)  # Step Into функция ішіне кіреді.


def main() -> None:
    print("7-сұрақ: Step Over және Step Into")
    total = checkout(1000, 2)  # Step Over бүкіл checkout-ты бір қадамда орындайды.
    print("Нәтиже:", total)


if __name__ == "__main__":
    main()
