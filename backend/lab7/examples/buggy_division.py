"""Әдейі қате мысал: ZeroDivisionError қатесін көрсетеді."""


def average(total: int, count: int) -> float:
    return total / count


if __name__ == "__main__":
    print(average(10, 0))
