"""Нөлге бөлу қатесі түзетілген нұсқа."""


def average(total: int, count: int) -> float:
    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    print(average(10, 0))
