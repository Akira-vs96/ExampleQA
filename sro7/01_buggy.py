"""СӨЖ 7: зерттеуге арналған үш қатесі бар бастапқы нұсқа."""


def average(numbers):
    """Сандардың орташа мәнін есептеу."""
    # Қате: бос тізімде нөлге бөлу орын алады.
    return sum(numbers) / len(numbers)  # B3
def final_price(price, percent):
    """Жеңілдіктен кейінгі бағаны есептеу."""
    # Қате: пайыз жүздік үлеске айналдырылмаған.
    discount = price * percent  # B1
    return price - discount


def maximum(numbers):
    """Тізімнің ең үлкен санын табу."""
    # Қате: теріс сандар үшін бастапқы мән дұрыс емес.
    largest = 0  # B2
    for current in numbers:
        if current > largest:  # B2
            largest = current
    return largest


if __name__ == "__main__":
    print("Қате нұсқа: жеңілдіктен кейінгі баға:", final_price(1000, 20))
    print("Қате нұсқа: ең үлкен сан:", maximum([-8, -3, -5]))
    # Соңғы шақыру бағдарламаны ZeroDivisionError қатесімен тоқтатады.
    print("Қате нұсқа: бос тізімнің орташа мәні:", average([]))
