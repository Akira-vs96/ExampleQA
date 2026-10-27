# Debugger сеансының жазбасы

Breakpoint екі нұсқада да қойылады: алдымен қатені анықтау үшін,
содан кейін түзетілген есептеуді қадамдап тексеріп, нәтижелерді салыстыру үшін.
Breakpoint тұрған жол әлі орындалмаған болады; оның нәтижесін `n` (VS Code: `F10`)
командасынан кейін тексеріңіз.

| Тексеру | Қате нұсқа: тоқтау жолдары | Дұрыс нұсқа: тоқтау жолдары | Бақыланатын мәндер |
| --- | --- | --- | --- |
| Жеңілдік | 13 | 16 | `price`, `percent`, қадамнан кейін `discount`: `20000` → `200.0` |
| Ең үлкен сан | 20, 22 | 25, 27 | Бастапқы `largest`: `0` → `-8`; соңғы нәтиже: `0` → `-3` |
| Орташа мән | 7 | 6 | `numbers`, `len(numbers)`; бос тізімде бөлуге дейін тексеру |

VS Code: алдымен [01_buggy.py](01_buggy.py), кейін [02_fixed.py](02_fixed.py)
файлын ашып, кестедегі жолдардың сол жақ жиегіне басыңыз. Әр файлды бөлек `F5`
арқылы іске қосыңыз. `F10` арқылы қадамдап өтіп, Variables/Watch мәндерін салыстырыңыз.

Нақты `pdb` сеансы. Қате нұсқаны іске қосу:

```bash
python3 -m pdb sro7/01_buggy.py
```

## 1. Қате нұсқаның терминал нәтижесі

```text
> /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(1)<module>()
-> """СӨЖ 7: зерттеуге арналған үш қатесі бар бастапқы нұсқа."""
(Pdb) Breakpoint 1 at /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py:13
(Pdb) Breakpoint 2 at /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py:22
(Pdb) Breakpoint 3 at /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py:7
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(13)final_price()
-> discount = price * percent
(Pdb) (1000, 20)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(14)final_price()
-> return price - discount
(Pdb) 20000
(Pdb) Қате нұсқа: жеңілдіктен кейінгі баға: -19000
> /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(22)maximum()
-> if current > largest:
(Pdb) (-8, 0)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(21)maximum()
-> for current in numbers:
(Pdb) (-8, 0)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(22)maximum()
-> if current > largest:
(Pdb) (-3, 0)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(22)maximum()
-> if current > largest:
(Pdb) (-5, 0)
(Pdb) Қате нұсқа: ең үлкен сан: 0
> /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(7)average()
-> return sum(numbers) / len(numbers)
(Pdb) ([], 0)
(Pdb) ZeroDivisionError: division by zero
> /home/akira/IdeaProjects/ExampleQA/sro7/01_buggy.py(7)average()
-> return sum(numbers) / len(numbers)
(Pdb)
```

## 2. Дұрыс нұсқаны debugger арқылы тексеру

```bash
python3 -m pdb sro7/02_fixed.py
```

Төмендегі командалар нақты орындалды (`b` — breakpoint, `c` — жалғастыру,
`n` — келесі қадам, `p` — мәнді көрсету, `q` — шығу):

```text
b 16
b 25
b 27
b 6
c
p price, percent
n
p discount
c
p numbers
n
p largest
c
p current, largest
n
n
p largest
c
p current, largest
c
p numbers
n
p len(numbers)
c
p numbers, len(numbers)
n
n
c
q
```

Нақты терминал нәтижесі:

```text
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(1)<module>()
-> """СӨЖ 7: үш қатесі түзетілген нұсқа."""
(Pdb) Breakpoint 1 at /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py:16
(Pdb) Breakpoint 2 at /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py:25
(Pdb) Breakpoint 3 at /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py:27
(Pdb) Breakpoint 4 at /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py:6
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(16)final_price()
-> discount = price * percent / 100
(Pdb) (1000, 20)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(17)final_price()
-> return price - discount
(Pdb) 200.0
(Pdb) Дұрыс нұсқа: жеңілдіктен кейінгі баға: 800.0
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(25)maximum()
-> largest = numbers[0]
(Pdb) [-8, -3, -5]
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(26)maximum()
-> for current in numbers[1:]:
(Pdb) -8
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(27)maximum()
-> if current > largest:
(Pdb) (-3, -8)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(28)maximum()
-> largest = current
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(26)maximum()
-> for current in numbers[1:]:
(Pdb) -3
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(27)maximum()
-> if current > largest:
(Pdb) (-5, -3)
(Pdb) Дұрыс нұсқа: ең үлкен сан: -3
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(6)average()
-> if not numbers:
(Pdb) [10, 20, 30]
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(8)average()
-> return sum(numbers) / len(numbers)
(Pdb) 3
(Pdb) Дұрыс нұсқа: орташа мән: 20.0
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(6)average()
-> if not numbers:
(Pdb) ([], 0)
(Pdb) > /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(7)average()
-> raise ValueError("Орташа мән үшін кемінде бір сан қажет.")
(Pdb) ValueError: Орташа мән үшін кемінде бір сан қажет.
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(7)average()
-> raise ValueError("Орташа мән үшін кемінде бір сан қажет.")
(Pdb) Бос тізім тексерісі: Орташа мән үшін кемінде бір сан қажет.
The program finished and will be restarted
> /home/akira/IdeaProjects/ExampleQA/sro7/02_fixed.py(1)<module>()
-> """СӨЖ 7: үш қатесі түзетілген нұсқа."""
(Pdb)
```

Жеңілдік `200.0`, соңғы баға `800.0` болды. `largest` бастапқыда `-8`,
кейін `-3` болды; `-5` оны өзгертпеді. Бос тізімде `ValueError` әдейі беріліп,
негізгі бағдарламада өңделді: `ZeroDivisionError` қайталанбады.
Debugger `raise` жолында exception көрсеткені түзету сәтсіз дегенді білдірмейді:
`c` арқылы жалғастырғанда `except ValueError` оны өңдеп, қазақша хабарлама шығарады.
