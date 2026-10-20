"""6. Breakpoint кезінде бағдарлама күйін зерттеу."""


def calculate_total(price: int, quantity: int) -> int:
    subtotal = price * quantity
    discount = 250
    total = subtotal - discount  # Осы жолға IDE breakpoint қойыңыз.
    return total


def main() -> None:
    print("6-сұрақ: Breakpoint")
    result = calculate_total(1200, 2)
    print("Breakpoint кезінде price, quantity, subtotal, discount мәндерін қараңыз")
    print("Нәтиже:", result)


if __name__ == "__main__":
    main()
