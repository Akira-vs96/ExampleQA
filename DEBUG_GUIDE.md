# Python мысалдарын debugger арқылы зерттеу

## 1. Қате нұсқаны іске қосу

```bash
cd backend
python lab7/examples/buggy_division.py
```

Нәтижеде `ZeroDivisionError` және stack trace шығады. Логикалық қате
мысалдары exception шығармайды, бірақ қате нәтиже береді:

```bash
python lab7/examples/buggy_discount.py  # -19000, күтілетіні: 800
python lab7/examples/buggy_maximum.py   # 2, күтілетіні: 9
```

## 2. Breakpoint орнату

VS Code немесе PyCharm ішінде күдікті жол нөмірінің жанына breakpoint
қойыңыз:

- `buggy_division.py`: `return total / count`;
- `buggy_discount.py`: `discount = price * percent`;
- `buggy_maximum.py`: `if number < current`.

Debug режимін іске қосқанда мына құралдарды қолданыңыз:

| Құрал | Мақсаты |
|---|---|
| Variables | Ағымдағы айнымалылар мен олардың мәндерін көру |
| Watch | Таңдалған өрнекті әр қадамда бақылау |
| Call Stack | Функциялар шақырылған ретті көру |
| Step Over | Келесі жолға функцияның ішіне кірмей өту |
| Step Into | Шақырылған функцияның ішіне кіру |
| Step Out | Ағымдағы функциядан шақырушыға қайту |

## 3. Түпкі себепті анықтау

Нақты мәнді күтілетін мәнмен салыстырыңыз. Мысалы, жеңілдік тапсырмасында:

```text
price = 1000
percent = 20
discount = 20000  # қате
```

`20%` мәні есептеуде `20 / 100` болуы керек. Сондықтан түпкі себеп — пайызды
бөлшекке айналдырудың ұмытылуы.

## 4. Дұрыс нұсқа мен тесттер

```bash
cd backend
python lab7/examples/fixed_discount.py
python -m pytest -q lab7/tests
python -m pytest -q
```

Түзетілген функциялар тест файлында импортталады. Сол себепті мысалдардағы
`print(...)` тек `if __name__ == "__main__":` блогының ішінде орналасқан.

## 5. Қауіпсіз debugging

- логқа құпия сөз, token және жеке дерек жазбаңыз;
- production ортада debug режимін қоспаңыз;
- уақытша `breakpoint()` пен `print()` жолдарын commit алдында алып тастаңыз;
- exception-ды бос `except` блогымен жасырмаңыз;
- әр bug түзетілген соң regression test қалдырыңыз.
