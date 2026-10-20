"""13. Regression test ескі мүмкіндіктердің бұзылмағанын тексереді."""


def find_max(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("Тізім бос болмауы керек")
    current = numbers[0]
    for number in numbers[1:]:
        if number > current:
            current = number
    return current


def regression_suite() -> None:
    assert find_max([4, 9, 2]) == 9       # Бастапқы bug сценарийі
    assert find_max([-3, -1, -7]) == -1   # Бұрынғы мүмкіндік
    assert find_max([5]) == 5              # Шекаралық жағдай


def main() -> None:
    print("13-сұрақ: Regression testing")
    regression_suite()
    print("PASS: bug қайта пайда болмады, барлық сценарий жұмыс істейді")


if __name__ == "__main__":
    main()
