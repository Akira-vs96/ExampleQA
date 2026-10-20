# 7-зертханалық жұмыс — Қатені табу және түзету

Әр мысал екі файлдан тұрады:

| Қате нұсқа | Дұрыс нұсқа | Тақырып |
|---|---|---|
| `examples/buggy_division.py` | `examples/fixed_division.py` | `ZeroDivisionError` |
| `examples/buggy_discount.py` | `examples/fixed_discount.py` | Пайызды есептеу |
| `examples/buggy_maximum.py` | `examples/fixed_maximum.py` | Салыстыру шарты |

Жұмыс реті: алдымен `buggy_*.py` файлын іске қосып қатені бақылаңыз, кейін
debugger арқылы себебін табыңыз. Соңында `fixed_*.py` нұсқасын және тесттерді
орындаңыз.

```bash
cd backend
python lab7/examples/buggy_division.py
python lab7/examples/fixed_division.py
python -m pytest -q lab7/tests
```
