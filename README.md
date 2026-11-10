# DebugLab KZ

PDF бойынша **15 зертханалық жұмыс және 300 тапсырма**. Әр жұмысқа есеп, қажет жерде қате/түзетілген код, орындалатын тесттер және нақты evidence қосылған. Толық каталог: [LABS.md](LABS.md); құрылым: [ARCHITECTURE.md](ARCHITECTURE.md); соңғы нәтиже: [QA Summary](backend/lab15/results/SUMMARY.md).

## Орнату

Python 3.13, Node 22 және Java 17+ (тек ZAP үшін).

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
npm ci --no-audit --no-fund
npx playwright install chromium
```

Windows-та virtual environment interpreter жолы `.venv/Scripts/python.exe`. Npm scripts сол interpreter-ді автоматты табады; қажет болса `QA_PYTHON` арқылы таңдаңыз. Existing `backend/.venv` те fallback ретінде қолданылады.

## Жергілікті қосымша

```bash
npm run dev
```

Әдеттегі мекенжайлар: портал `http://127.0.0.1:8000`, оқу дүкені `http://127.0.0.1:8000/shop.html`, Swagger `http://127.0.0.1:8000/docs`. Порт бос болмаса launcher келесі бос портты көрсетеді. `QA_PORT` портты, `QA_DATABASE` SQLite файлын таңдайды. Тоқтату: Ctrl+C.

Frontend — HTML/CSS/JS; бөлек React/Vite server қажет емес. Дүкенде synthetic аккаунтты UI арқылы тіркеңіз; нақты төлем орындалмайды. Static Pages report portal-ы API-сыз жұмыс істейді, ал shop backend қажет етеді.

## Қате код және түзету

```bash
npm run demo       # Lab4/6/13: дәл сол tests before FAIL, after PASS
npm run lab5       # 10 positive + 10 negative case, CSV/JSON
npm run lab7       # ZeroDivisionError, traceback, real pdb, corrected result
npm run lab14      # failed test stage және corrected run
```

Қате нұсқа [lab6/before](backend/lab6/before/), corrected бизнес код [qa_shop](backend/qa_shop/) ішінде. Existing [lab7 examples](backend/lab7/examples/), [lab8 before/after](backend/lab8/), [SRO7](sro7/README.md), [SRO8](sro8/README.md) сақталған.

СРО7–9 тесттері соңында қате және түзетілген файлдың салыстыруы терминалға
автоматты шығады: FAILED/PASSED, функция, нақты қате, себеп және түзету.

```bash
npm run test:sro7
npm run test:sro8
npm run test:sro9
npm run test:sro10
```

[СРО9](sro9/README.md) — REST API, Postman, алты міндетті тест-кейс және екі
интеграциялық сценарий. Ортақ есеп механизмі: [SRO_TESTS.md](scripts/SRO_TESTS.md).

[СРО10](sro10/README.md) — QA Shop веб-қосымшасын функционалдық және интерфейстік
тестілеу: 20 тест-кейс, Playwright/pytest арқылы 30 тексеріс және екі ашық Bug Report.
`npm run report:sro10` нақты тексерістерді орындап, Word есебін де жаңартады.

## Тексеру

```bash
npm test           # барлық corrected Python және SRO tests
npm run check      # build, static, coverage, demo, debugger, lab8 gate
npm run lab10      # нақты Chromium UI және screenshots
npm run lab11      # Locust baseline/load/stress/spike CSV және graph
npm run lab12      # authentication, session, injection, headers tests
npm run build      # 15 report бар dist static build
```

Coverage scope — Python `qa_shop` пакеті; міндетті combined statement/branch threshold **85%**. JUnit, coverage JSON/XML/HTML және quality stage logs [lab15/results](backend/lab15/results/) ішіне жазылады. VS Code pytest discovery және debugging configurations дайын.

## ZAP passive scan

[Official ZAP download](https://www.zaproxy.org/download/) арқылы Linux package орнатыңыз. Осы ортада ZAP 2.17.0 checksum тексеріліп қолданылған; binary Git-ке қосылмайды.

```bash
# ZAP package default path: tools/vendor/ZAP_2.17.0
# Басқа каталог болса ZAP_HOME көрсетіңіз.
node scripts/python.mjs backend/lab12/run_zap.py
npm run lab15      # browser, load, ZAP қоса барлық жергілікті quality stages
```

Scanner өзі ашқан 127.0.0.1 before/after серверлеріне ғана request жібереді және passive scan орындайды. ZAP қорытындысы [Security Report](backend/lab12/REPORT.md) ішінде. Endurance PDF бойынша бөлек жоспар; қысқа Locust run ұзақ SLA ретінде есептелмейді.

## Existing Lab9

```bash
npm ci --prefix backend/lab9 --no-audit --no-fund
npm run lab9
```

[Postman/Newman жинағы](backend/lab9/README.md) 34 DummyJSON scenario береді. Бұл сыртқы API run; негізгі offline pytest/CI-ге тәуелділік емес. Runner finding табылса nonzero exit қайтарады; [нақты нәтижелер](backend/lab9/results/RUN_RESULTS.md) мен [ашық finding](backend/lab9/REPORT.md) жасырылмайды.

## CI және есептер

[labs.yml](.github/workflows/labs.yml) build, tests, static analysis, coverage және Chromium орындайды, reports artifact ретінде сақтайды. [Pages workflow](.github/workflows/pages.yml) quality job өткен соң static portal-ды deploy етеді. Remote execution жаңа commit push/dispatch кезінде орындалады; local run evidence бөлек сақталады.

Әр жұмыстың 20 тапсырмасы [LABS.md](LABS.md) арқылы ашылады. Қорытынды [SUMMARY.md](backend/lab15/results/SUMMARY.md) нақты runner файлдарынан автоматты жасалады. Оқу localhost release-і production deployment readiness-тен бөлек бағаланады.
