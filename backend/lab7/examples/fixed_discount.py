"""Жеңілдікті есептеу қатесі түзетілген нұсқа."""


def final_price(price: int, percent: int) -> float:
    discount = price * percent / 100
    return price - discount


if __name__ == "__main__":
    print(final_price(1000, 20))
