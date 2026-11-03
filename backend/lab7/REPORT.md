# 7 зертханалық жұмыс Debugging

Нысан — `average(10,0)` шақыруындағы ZeroDivisionError. Үш қосымша мысал [examples](examples/) ішінде. Төмендегі қадамдар нақты Python debugger арқылы орындалған.

## 1 Қате бағдарламаны таңдау

[buggy_division.py](examples/buggy_division.py): `return total / count`. Нөлдік count үшін guard жоқ. Түзетілген жұп: [fixed_division.py](examples/fixed_division.py).

## 2 Қатені іске қосу

`node scripts/python.mjs backend/lab7/examples/buggy_division.py` ZeroDivisionError береді. Толық capture және debugger сеансы: `npm run lab7`.

## 3 Error Message

`ZeroDivisionError: division by zero`. Нақты exception мәтіні [error_message.txt](results/error_message.txt) ішінде сақталады.

## 4 Stack Trace

[stack_trace.txt](results/stack_trace.txt) main → scenario → buggy_average call chain және exception жолын сақтайды. Бұл қолдан жазылған stack үлгісі емес, `traceback.format_exc()` нәтижесі.

## 5 Қате жолы

`buggy_division.py` файлының 5-жолындағы `return total / count`. Exception алдында total=10 және count=0. Divisor нөл екені негізгі себепті растайды.

## 6 Breakpoint

VS Code-де 5-жолға breakpoint қойып, Python Debugger Current File іске қосылады. Автоматты [capture_debug.py](capture_debug.py) `pdb.Pdb.runcall(scenario)` арқылы function-entry тоқтауын жасайды; бұл бастапқы breakpoint рөлін атқарады.

## 7 Debug режимі

`npm run lab7` нақты `pdb.Pdb` іске қосады. Интерактивті балама: `node scripts/python.mjs -m pdb backend/lab7/examples/buggy_division.py`. VS Code configuration [launch.json](../../.vscode/launch.json) ішінде.

## 8 Variable мәндері

Debugger `p total` → 10, `p count` → 0 көрсетеді. Output [pdb_session.txt](results/pdb_session.txt) ішінде. Variable мәндері API каталогындағы демонстрациялық snapshot-тан бөлек runtime-да алынады.

## 9 Step Over

`next` жергілікті total,count тағайындауын орындап, function call жолында тоқтайды. Сыртқы функцияға кірмей келесі жолға өтеді.

## 10 Step Into

`step` `buggy_average` функциясына кіреді. Одан кейін total/count қайта қаралады. Бұл caller мен callee арасындағы нақты аргументтерді салыстыруға мүмкіндік береді.

## 11 Step Out

`return` ағымдағы frame-нің қайтуына дейін жалғастырады; қате нұсқада exception арқылы unwinding болады. `continue` сеансты аяқтайды. Интерактивті debugger-де исправленный функция үшін осы command қалыпты return-ды көрсетеді.

## 12 Call Stack

`where` main/debugger → scenario → average frame-дерін көрсетеді. `up` caller-ге, `down` callee-ге ауысады. Нақты paths пен line numbers transcript-те сақталған.

## 13 Logging

[debug.log](results/debug.log) бастапқы exception және corrected result-ты тіркейді. `logging.exception` traceback-ты қосады, ал түзетілген нәтиже INFO ретінде жазылады.

## 14 Root Cause

Сырттан count=0 келгенде функция validation жасамай бөледі. Runtime evidence divisor нөл екенін көрсетті. Fix caller-де input ауыстыру емес, producer функциясына zero guard енгізу арқылы жасалды.

## 15 Түзету

Осы тапсырманың бизнес келісімі: count=0 болса 0 қайтару. `if count == 0: return 0` қосылды. Қалыпты count үшін total/count сақталды.

## 16 Unit Test

[test_fixed_examples.py](tests/test_fixed_examples.py) average(10,0)=0 және average(10,2)=5 тексереді. Басқа ереже қажет жобада zero divisor үшін exception таңдауға болады; бұл зертханада existing contract сақталды.

## 17 Regression Test

Сол suite discount және maximum мысалдарын да тексереді. `node scripts/python.mjs -m pytest -q backend/lab7/tests` және толық `npm test` қолданылады.

## 18 Before After

| Input | Before | After |
|---|---|---|
| average(10,0) | ZeroDivisionError | 0 |
| average(10,2) | 5 | 5 |
| final_price(1000,20) | -19000 | 800 |
| find_max([4,9,2]) | 2 | 9 |

## 19 Debugging журналы

Рет: exception қайта өндіру → traceback → entry stop → next → variable print → step → where/up/down → return → root cause → guard → retest. Уақыты мен before/after [comparison.json](results/comparison.json) ішінде; толық transcript жеке сақталған.

## 20 Қорытынды

Exception, stack, variables және call path арқылы нөлдік divisor дәлелденді. Түзету бастапқы функцияда жасалды және unit/regression test арқылы тексерілді. Алғашқы қате код оқу үшін сақталған, түзетілген код негізгі бағдарламаға арналған.
