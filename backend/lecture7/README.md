# 7-дәріс — теория және іске қосылатын демонстрациялар

15 сұрақтың барлығын жасанды түрде кодқа айналдыру дұрыс емес. Сондықтан
теориялық сұрақтардың жауабы `content.py` ішінде, ал орындалуын шын көрсетуге
болатын 10 сұрақ VS Code ішінде іске қосылатын Python файлдары ретінде берілген.

## VS Code арқылы көрсету

1. `examples` каталогынан қажетті `topic_*.py` файлын ашыңыз.
2. Код түсіндірмесінде белгіленген жолға breakpoint қойыңыз (`F9`).
3. `F5` басып **Python Debugger: Current File** таңдаңыз.
4. Variables, Watch, Call Stack, Step Over (`F10`) және Step Into (`F11`)
   құралдарын қолданыңыз.
5. Debugger қолданбай орындау үшін VS Code ішіндегі **Run Python File**
   батырмасын басыңыз.

## Кодпен көрсетілетін 10 сұрақ

| № | Файл | Не көрсетеді |
|---:|---|---|
| 2 | `topic_02_error_types.py` | Syntax, runtime және logical error |
| 6 | `topic_06_breakpoint.py` | Breakpoint кезіндегі бағдарлама күйі |
| 7 | `topic_07_step_over_into.py` | Step Over, Step Into және Step Out |
| 8 | `topic_08_variables_watch.py` | Variables және Watch өрнектері |
| 9 | `topic_09_call_stack.py` | Функциялар шақыруының Call Stack тізбегі |
| 10 | `topic_10_python_breakpoint.py` | Python `breakpoint()` функциясы |
| 11 | `topic_11_try_except_logging.py` | Exception өңдеу және logging |
| 12 | `topic_12_unit_test.py` | Assertion арқылы unit test |
| 13 | `topic_13_regression_testing.py` | Regression test жинағы |
| 14 | `topic_14_debug_security.py` | Құпия деректерді қауіпсіз логтау |

## Теория түрінде қалатын сұрақтар

- 1 — Debugging анықтамасы және мақсаты;
- 3 — Testing пен Debugging процестерінің жалпы айырмашылығы;
- 4 — түпкі себепті анықтаудың маңызы;
- 5 — Five Whys әдісінің түсіндірмесі;
- 15 — CI/CD pipeline ішіндегі debugging процесі.

Олардың толық жауабы `content.py` файлында сақталған. 3, 4 және 5-сұрақтардың
практикалық қолданылуы `lab7` ішіндегі қате және түзетілген кодтарда көрінеді.

## Терминалдан іске қосу

Бір мысал:

```bash
cd backend
python lecture7/examples/topic_07_step_over_into.py
```

Кодпен көрсетілетін барлық мысал:

```bash
cd backend
python lecture7/run_all.py
```

Немесе жоба түбірінен:

```bash
npm run lecture7
```

10-мысалда нақты `pdb` debugger-ін қосу қажет болса:

```bash
cd backend/lecture7/examples
USE_PDB=1 python topic_10_python_breakpoint.py
```

Қалыпты іске қосқанда бұл файл интерактивті режимге кірмейді, сондықтан барлық
демонстрацияны `run_all.py` арқылы қауіпсіз орындауға болады.
