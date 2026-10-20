"""11. try/except exception-ды өңдейді, logging оқиғаны тіркейді."""

import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def safe_divide(total: int, count: int) -> float | None:
    try:
        return total / count
    except ZeroDivisionError:
        logger.exception("Бөлу орындалмады: count нөлге тең")
        return None


def main() -> None:
    print("11-сұрақ: try/except және logging")
    print("Нәтиже:", safe_divide(10, 0))


if __name__ == "__main__":
    main()
