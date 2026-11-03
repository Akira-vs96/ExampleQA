# 2 зертханалық жұмыс Test Plan және STLC

QA Shop үшін тестілеу жоспары. Негізгі мақсат — ақша есептеу, authentication және жеткізу ережелерінің дұрыстығын әр деңгейде тексеру.

## 1 Қосымшаны таңдау

Нысан: [QA Shop](../qa_shop/), Python 3.13 + FastAPI + SQLite + HTML/JS. Талаптар базасы: [24 талап](../lab1/requirements.csv).

## 2 Тестілеу мақсаты

Бес бастапқы pricing ақауын қайталау, түзету нәтижесін дәлелдеу, рұқсатсыз профиль мен quote-ты бұғаттау. Critical функциялардағы күтпеген failure саны нөл болуы тиіс.

## 3 STLC кезеңдері

Requirement Analysis → Test Planning → Test Design → Environment Setup → Test Execution → Test Closure. Әр өзгеріс regression цикліне қайта кіреді.

## 4 Кезеңдердің мақсаттары

| Кезең | Кіріс | Іс-әрекет | Шығыс |
|---|---|---|---|
| Analysis | PDF, код | Талап пен тәуекелді нақтылау | Requirements, RTM |
| Planning | RTM | Scope, resources, exit criteria | Осы Test Plan |
| Design | Критерийлер | Positive, negative, BVA, states | 20 test case, suites |
| Environment | Dependencies | venv, Chromium, isolated DB | Қайталанатын орта |
| Execution | Build және data | Test, retest, scan, load | JUnit, JSON, CSV, screenshots |
| Closure | Нақты нәтиже | Metrics, residual risk | QA Report және release decision |

## 5 Test Planning

Алдымен Critical authentication және ақша ережелері, одан кейін API/UI, соңында performance/security. Жауапты — жұмысты орындаушы студент; оқытушы қабылдау критерийлерін бағалайды. Әр тексерудің command, exit code және нәтижесі сақталады.

## 6 Requirement Analysis

FR01–FR12 және NFR01–NFR12 тексеріледі. Delivery threshold жеңілдіктен кейін қолданылады; 100% discount жеткізуді автоматты тегін етпейді. Күй ауысуы домендік деңгейде, төлем провайдері scope-тан тыс. Бес түсініксіз талап өлшенетін критерийге айналдырылды.

## 7 Test Design

[5 жұмыстың cases.json](../lab5/cases.json) — 10 positive және 10 negative case. 4 жұмыс: 5 equivalence class, 10 boundary, 4 decision rule және барлық 36 state pair. 3 жұмыс: unit, integration, system және acceptance. 13 жұмыс бұрынғы бес ақаудың regression қорғанысын береді.

## 8 Environment Setup

Linux; Python 3.13; Node 22; SQLite Python standard library; Chromium Playwright; Java ≥ 17 және ZAP. Python dependencies [requirements-dev.txt](../../requirements-dev.txt), Node dependencies [package-lock.json](../../package-lock.json). Әр API test жеке `tmp_path` SQLite пайдаланады. Load/ZAP серверлері бос loopback порт пен уақытша дерекқор алады.

## 9 Test Execution

`npm run demo` бастапқы FAIL мен түзетілген PASS-ты сақтайды. `npm run check` build, analysis, test, coverage, cases және debugging орындайды. `npm run lab10`, `npm run lab11` және ZAP runner арнайы тексерулерді іске қосады. Күтпеген failure түзетіліп, дәл сол test қайта орындалады.

## 10 Test Closure

JUnit test count, failure/error, coverage, UI status, load percentiles, ZAP alerts және unresolved defects біріктіріледі. [15 жұмыс](../lab15/REPORT.md) оқу release-і мен production readiness-ті бөлек бағалайды. Бастапқы нұсқада күтілген failure түзетілген нұсқаның FAIL статистикасына қосылмайды.

## 11 Scope In

Тіркелу, кіру, профиль, logout, catalogue, search, line total, discount, delivery, quote, state graph, reports, input validation, cookies, headers, local workload және CI gate.

## 12 Scope Out

Банк транзакциясы, нақты жеткізу, SMTP/SMS, production deploy, multi-region, ұзақ мерзімді uptime, Safari/Firefox матрицасы, penetration certification. DummyJSON — бөлек external API exercise; жергілікті pytest оған тәуелді емес.

## 13 Entry Criteria

Талаптар ID және acceptance criterion алды; қате/түзетілген нұсқалар бар; dependencies орнатылған; `/api/health` 200; тест деректері synthetic; мақсат loopback. Browser алдында Chromium, scan алдында ZAP орнатылған болуы тиіс.

## 14 Exit Criteria

Corrected pytest және Chromium tests — 100% PASS; errors/skips жоқ; `qa_shop` combined statement/branch coverage ≥ 85%; Ruff нөл error; lab8 quality gate PASS; 50 VU errors ≤ 1%, p95 ≤ 200 ms; passive scan-да High alert жоқ. Production release үшін қосымша rate limiting, HTTPS termination және ұзақ endurance тексеруі қажет.

## 15 Тестілеу түрлері

Functional, negative, boundary, state transition, unit, integration, system, acceptance, smoke, regression, UI, load, stress, spike, passive security және static analysis. Endurance — [11 жұмыстағы](../lab11/REPORT.md) бөлек ұзақ мерзімді жоспар.

## 16 Құралдар және ресурстар

| Құрал | Мақсат | Ресурс |
|---|---|---|
| pytest, HTTPX | Unit/API және isolated DB | Бір CPU process |
| pytest-cov | Statement/branch evidence | Coverage JSON/XML/HTML |
| Playwright | Chromium UI | Бір browser worker |
| Locust | 1/10/25/50/100 VU, spike | Бөлек client/server process |
| ZAP | Passive scan | Java heap және localhost proxy |
| Ruff, Pylint, Radon | Style, smells, complexity | CLI |
| GitHub Actions | Repeatable CI | Ubuntu runner |

## 17 Тестілеу тәуекелдері

Жүктеме генераторы мен сервер бір хостта CPU үшін бәсекелеседі; қысқа профильді production capacity деп түсіндіруге болмайды. Сыртқы API желіге тәуелді. UI деректері бірегей username алады. Уақытқа тәуелді sleep орнына browser auto-wait және readiness polling қолданылады. ZAP scope-ы loopback URL-мен шектеледі.

## 18 Тестілеу кестесі

| Рет | Жұмыс | Жоспарлы уақыт | Тәуелділік |
|---|---|---|---|
| 1 | Талаптар және RTM | 45 min | PDF |
| 2 | Test Plan және case design | 45 min | 1 |
| 3 | Unit, BVA, state, API | 90 min | 2 |
| 4 | Debug және code review | 45 min | 3 |
| 5 | UI, screenshots | 45 min | Орта дайын |
| 6 | Load және security | 60 min | Сервер дайын |
| 7 | Regression, CI, closure | 45 min | 3–6 |

Бұл оқу жұмысына арналған жоспарлы еңбек бағасы; нақты CLI ұзақтығы results файлдарында сақталады.

## 19 Test Deliverables

Requirements CSV, risk matrix, RTM, Test Plan, cases JSON/CSV, pytest suites, before/after logs, pdb transcript, Postman collection/environment, Playwright tests/screenshots, Locust CSV/graph, ZAP JSON, workflow, coverage және final QA report.

## 20 Қорытынды Test Plan

Осы жоспар барлық 15 зертхананың ортақ scope-ын, ортасын, құралдарын және қабылдау шарттарын белгілейді. Тестілеу стратегиясы тәуекелге негізделген: алдымен рұқсаттар мен ақша, кейін интерфейс пен сапа сипаттамалары. Әр release gate нақты сақталған нәтижемен бағаланады; соңғы дәлел [SUMMARY.md](../lab15/results/SUMMARY.md) ішінде.
