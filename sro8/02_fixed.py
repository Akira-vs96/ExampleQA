"""Түзетілген интернет-дүкен модулі. Ақша бірлігі — бүтін теңге."""


def line_total(price: int, quantity: int) -> int:
    """Теріс емес баға мен оң сан бойынша тауар құнын есептеу."""
    if price < 0:
        raise ValueError("Баға теріс болмауы керек.")
    if quantity <= 0:
        raise ValueError("Тауар саны нөлден үлкен болуы керек.")
    return price * quantity


def discounted_total(subtotal: int, percent: int) -> int:
    """Жеңілдікті есептеу; соңғы соманы төмен қарай бүтін теңгеге дөңгелектеу."""
    if subtotal < 0:
        raise ValueError("Тапсырыс сомасы теріс болмауы керек.")
    if not 0 <= percent <= 100:
        raise ValueError("Жеңілдік 0–100 пайыз аралығында болуы керек.")
    return subtotal * (100 - percent) // 100


def shipping_cost(total: int) -> int:
    """Жеңілдіктен кейінгі сома кемінде 10000 теңге болса, жеткізу тегін."""
    if total < 0:
        raise ValueError("Тапсырыс сомасы теріс болмауы керек.")
    if total >= 10000:
        return 0
    return 1000


if __name__ == "__main__":
    print("Тауар құны:", line_total(2000, 3))
    print("Жеңілдіктен кейін:", discounted_total(10000, 20))
    print("Жеткізу құны:", shipping_cost(10000))
