"""UI мен API қолданатын 7-зертханалық жұмыс каталогы."""

EXAMPLES = {
    "division": {
        "id": "division",
        "title": "Нөлге бөлу қатесі",
        "error_type": "Орындалу қатесі",
        "difficulty": "Бастапқы",
        "summary": "Бөлгіш нөл болғанда бағдарлама ZeroDivisionError қатесін береді.",
        "buggy_code": """def average(total, count):
    return total / count

print(average(10, 0))""",
        "fixed_code": """def average(total, count):
    if count == 0:
        return 0
    return total / count

print(average(10, 0))""",
        "breakpoint_line": 2,
        "variables": {"total": "10", "count": "0", "нәтиже": "ZeroDivisionError"},
        "buggy_result": "ZeroDivisionError: division by zero",
        "fixed_result": "0",
        "tests": [
            {"name": "Нөлдік бөлгіш", "result": "average(10, 0) == 0"},
            {"name": "Қалыпты орташа", "result": "average(10, 2) == 5"},
        ],
        "report": {
            "бастапқы қате": "count нөл болғанда total / count орындалды.",
            "түпкі себеп": "Бөлгіштің нөл болуына қорғаныс шарты болмады.",
            "түзету жолы": "count == 0 жағдайында 0 қайтаратын guard clause қосылды.",
            "тест нәтижесі": "2/2 тест өтті.",
        },
    },
    "discount": {
        "id": "discount",
        "title": "Жеңілдікті қате есептеу",
        "error_type": "Логикалық қате",
        "difficulty": "Орташа",
        "summary": "Жеңілдік пайызы 100-ге бөлінбегендіктен, нәтиже тым үлкен болады.",
        "buggy_code": """def final_price(price, percent):
    discount = price * percent
    return price - discount

print(final_price(1000, 20))""",
        "fixed_code": """def final_price(price, percent):
    discount = price * percent / 100
    return price - discount

print(final_price(1000, 20))""",
        "breakpoint_line": 2,
        "variables": {"price": "1000", "percent": "20", "discount": "20000"},
        "buggy_result": "-19000",
        "fixed_result": "800",
        "tests": [
            {"name": "20 пайыз жеңілдік", "result": "final_price(1000, 20) == 800"},
            {"name": "Жеңілдіксіз баға", "result": "final_price(500, 0) == 500"},
        ],
        "report": {
            "бастапқы қате": "Процент тікелей көбейткіш ретінде қолданылды.",
            "түпкі себеп": "Пайыздық мәнді бөлшекке түрлендіру ұмытылды.",
            "түзету жолы": "percent мәні 100-ге бөлініп, нақты жеңілдік есептелді.",
            "тест нәтижесі": "2/2 тест өтті.",
        },
    },
    "maximum": {
        "id": "maximum",
        "title": "Тізімдегі максимумды табу",
        "error_type": "Логикалық қате",
        "difficulty": "Орташа",
        "summary": "Салыстыру бағыты қате болғандықтан, функция ең кіші мәнді қайтарады.",
        "buggy_code": """def find_max(numbers):
    current = numbers[0]
    for number in numbers:
        if number < current:
            current = number
    return current

print(find_max([4, 9, 2]))""",
        "fixed_code": """def find_max(numbers):
    current = numbers[0]
    for number in numbers:
        if number > current:
            current = number
    return current

print(find_max([4, 9, 2]))""",
        "breakpoint_line": 4,
        "variables": {"current": "4", "number": "9", "күтілетін нәтиже": "9"},
        "buggy_result": "2",
        "fixed_result": "9",
        "tests": [
            {"name": "Оң сандар", "result": "find_max([4, 9, 2]) == 9"},
            {"name": "Теріс сандар", "result": "find_max([-3, -1]) == -1"},
        ],
        "report": {
            "бастапқы қате": "number < current шарты минимумды іздеді.",
            "түпкі себеп": "Максимум үшін салыстыру операторы кері жазылды.",
            "түзету жолы": "Салыстыру белгісі > операторы болып өзгертілді.",
            "тест нәтижесі": "2/2 тест өтті.",
        },
    },
}
