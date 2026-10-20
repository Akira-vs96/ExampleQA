"""12. Unit test қатені шағын және қайталанатын сценарийде көрсетеді."""


def final_price(price: int, percent: int) -> float:
    return price - price * percent / 100


def test_final_price() -> None:
    assert final_price(1000, 20) == 800
    assert final_price(500, 0) == 500


def main() -> None:
    print("12-сұрақ: Unit test")
    test_final_price()  # Тест сәтсіз болса, debugger осы шақырудан басталады.
    print("PASS: 2 assertion орындалды")


if __name__ == "__main__":
    main()
