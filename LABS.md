# Зертханалық жұмыстардың толық жинағы

[Зертханалық жұмыс PDF](./Зертханалық%20жұмыс.pdf) бойынша 15 жұмыс, әрқайсысында 20 тапсырма. Негізгі оқу нысаны — жергілікті QA Shop; бұрынғы Lab7–9 және СӨЖ материалдары сақталған.

| № | Тақырып | Есеп | Орындалатын материал |
|---:|---|---|---|
| 1 | Қосымша сапасы және талаптар | [20 тапсырма](backend/lab1/REPORT.md) | [24 талап CSV](backend/lab1/requirements.csv) |
| 2 | STLC және Test Plan | [20 тапсырма](backend/lab2/REPORT.md) | Scope, resources, schedule, entry/exit |
| 3 | Unit, Integration, System, Acceptance | [20 тапсырма](backend/lab3/REPORT.md) | `npm run lab3` |
| 4 | Black box және White box | [20 тапсырма](backend/lab4/REPORT.md) | `npm run lab4`, CFG, state graph |
| 5 | Test Case және Scenario | [20 тапсырма](backend/lab5/REPORT.md) | `npm run lab5`, [20 case CSV](backend/lab5/results/cases.csv) |
| 6 | Unit Testing | [20 тапсырма](backend/lab6/REPORT.md) | `npm run lab6`, before/after және coverage |
| 7 | Debugging | [20 тапсырма](backend/lab7/REPORT.md) | `npm run lab7`, [real pdb transcript](backend/lab7/results/pdb_session.txt) |
| 8 | Static Analysis және Code Review | [20 тапсырма](backend/lab8/REPORT.md) | `npm run lab8` |
| 9 | REST API | [20 тапсырма](backend/lab9/REPORT.md) | `npm run lab9`, Postman/Newman |
| 10 | Web UI | [20 тапсырма](backend/lab10/REPORT.md) | `npm run lab10`, Chromium, screenshots |
| 11 | Performance, Load, Stress, Spike | [20 тапсырма](backend/lab11/REPORT.md) | `npm run lab11`, Locust CSV/graph |
| 12 | Security және OWASP | [20 тапсырма](backend/lab12/REPORT.md) | `npm run lab12`, [ZAP runner](backend/lab12/run_zap.py) |
| 13 | Regression Automation | [20 тапсырма](backend/lab13/REPORT.md) | `npm run lab13`, before/after/stability |
| 14 | CI CD және Continuous Testing | [20 тапсырма](backend/lab14/REPORT.md) | `npm run lab14`, [workflow](.github/workflows/labs.yml) |
| 15 | Кешенді QA бағалау | [20 тапсырма](backend/lab15/REPORT.md) | `npm run lab15`, [actual summary](backend/lab15/results/SUMMARY.md) |

## Алдымен қате содан кейін түзету

```bash
npm run demo    # бір suite: before FAIL → corrected PASS
npm run lab5    # 20 documented case: before және after
npm run lab7    # exception → pdb → fixed result
npm run lab14   # test stage failure → corrected successful stage
```

Бастапқы нұсқада күтілген FAIL оқу дәлелі ретінде сақталады. Әдеттегі `npm test` corrected implementation-ды тексереді және күтпеген failure-ді жасырмайды.

## Нақты нәтижелер

[SUMMARY.md](backend/lab15/results/SUMMARY.md) — соңғы JUnit, coverage, browser, performance және ZAP evidence-інен автоматты жасалатын есеп. [report.html](backend/lab15/results/report.html) файлмен ашылатын нұсқа. `npm run check` 300 task бөлімінің түгелдігін де тексереді.

Remote GitHub pipeline жаңа commit/push немесе dispatch-тен кейін орындалады. Ұзақ endurance PDF талабы бойынша жоспар түрінде берілген. External DummyJSON finding өз нәтижесінде ашық тіркеледі; local training release production release-тен бөлек бағаланады.
