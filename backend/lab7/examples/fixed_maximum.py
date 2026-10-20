"""Тізім максимумын табу қатесі түзетілген нұсқа."""


def find_max(numbers: list[int]) -> int:
    current = numbers[0]
    for number in numbers:
        if number > current:
            current = number
    return current


if __name__ == "__main__":
    print(find_max([4, 9, 2]))
