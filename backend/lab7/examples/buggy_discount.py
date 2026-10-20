"""Әдейі логикалық қате: 20 пайызды 20 есе жеңілдік деп есептейді."""


def final_price(price: int, percent: int) -> int:
    discount = price * percent
    return price - discount


if __name__ == "__main__":
    print(final_price(1000, 20))
