"""СӨЖ 7: үш қатесі түзетілген нұсқа."""


def average(numbers):
    """Орташа мәнді қайтару; бос тізім үшін түсінікті қате беру."""
    if not numbers:  # B3
        raise ValueError("Орташа мән үшін кемінде бір сан қажет.")
    return sum(numbers) / len(numbers)


def final_price(price, percent):
    """Теріс емес бағаға 0–100 аралығындағы жеңілдікті қолдану."""
    if price < 0 or not 0 <= percent <= 100:
        raise ValueError("Баға теріс болмауы, пайыз 0–100 аралығында болуы керек.")
    # Пайызды жүзге бөліп, жеңілдік сомасын есептейміз.
    discount = price * percent / 100  # B1
    return price - discount


def maximum(numbers):
    """Бос емес тізімдегі ең үлкен санды қайтару."""
    if not numbers:
        raise ValueError("Ең үлкен санды табу үшін тізім бос болмауы керек.")
    # Бастапқы мән нақты элементтен алынады, сондықтан теріс сандар да өңделеді.
    largest = numbers[0]  # B2
    for current in numbers[1:]:
        if current > largest:  # B2
            largest = current
    return largest


if __name__ == "__main__":
    print("Дұрыс нұсқа: жеңілдіктен кейінгі баға:", final_price(1000, 20))
    print("Дұрыс нұсқа: ең үлкен сан:", maximum([-8, -3, -5]))
    print("Дұрыс нұсқа: орташа мән:", average([10, 20, 30]))
    try:
        average([])
    except ValueError as error:
        print("Бос тізім тексерісі:", error)
