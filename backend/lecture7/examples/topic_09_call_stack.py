"""9. Call Stack функциялардың шақырылу ретін көрсетеді."""

import inspect


def level_three() -> None:
    calls = [frame.function for frame in inspect.stack()[:4]]
    print("Call Stack:", " -> ".join(calls))  # Осы жолға breakpoint қойыңыз.


def level_two() -> None:
    level_three()


def level_one() -> None:
    level_two()


def main() -> None:
    print("9-сұрақ: Call Stack")
    level_one()


if __name__ == "__main__":
    main()
