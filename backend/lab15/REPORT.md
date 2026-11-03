# 15 зертханалық жұмыс Кешенді Quality Assurance Report

Нысан — жергілікті QA Shop және зертханалық портал. Функционалдық, интеграциялық, UI, regression, performance, security және static analysis нәтижелері біріктірілген. Нақты сандық нәтиже [SUMMARY.md](results/SUMMARY.md) және [summary.json](results/summary.json) арқылы автоматты түрде жасалады.

## 1 Қосымшаны таңдау

Python/FastAPI/SQLite + browser UI; public products, authenticated quote, safe session management. Бөлек buggy modules оқу үшін сақталған. External DummyJSON Lab9 деректері жергілікті қосымшаның release scope-ынан бөлек бағаланады.

## 2 Функционалдық талаптар

FR01–FR12 және NFR01–NFR12 [requirements.csv](../lab1/requirements.csv) ішінде. Critical: authentication, profile isolation, revocation, money correctness, quote contract және sensitive data protection.

## 3 Test Plan

[2 жұмыстағы жоспар](../lab2/REPORT.md): risk-based order, isolated DB, deterministic cases, exact criteria. Entry dependencies/health, exit passing corrected suites, coverage≥85%, zero High passive alerts және 50 VU NFR01–02.

## 4 Жиырма Test Case

[cases.json](../lab5/cases.json) 10 positive +10 negative case береді; [cases.csv](../lab5/results/cases.csv) толық steps/expected/actual/priority/severity сақтайды. Catalogue after 20/20 PASS болып тексеріледі.

## 5 Unit Testing

5 негізгі pricing функциясы, validation, rounding, exceptions, boundary және state graph тексерілді. [6 жұмыс](../lab6/REPORT.md). Before actual failing cases сақталған, corrected suite қалыпты PASS болуы тиіс.

## 6 Integration Testing

Registration route→SQLite және login cookie→persistent session repository. Нақты DB queries, жеке tmp_path және HTTP response contract қолданылады. [3 жұмыс](../lab3/tests/test_levels.py).

## 7 System Testing

Register→login→search→quote→logout→401 workflow. Бұл in-process HTTP system test; нақты browser/network test келесі бөлімде бөлек. Екі acceptance test discounted delivery мен anonymous denial-ды тексереді.

## 8 API Testing

Local API status, body, headers, schema, authentication және negative inputs pytest арқылы тексеріледі. [9 жұмыста](../lab9/REPORT.md) external DummyJSON үшін GET/POST/PUT/PATCH/DELETE бар Postman/Newman collection сақталған. Оның белгілі third-party finding-і final summary-де бөлек көрсетіледі.

## 9 UI Testing

Chromium register/login, invalid password, HTML validation, search, safe DOM, navigation, quote, logout, үш responsive size және report portal. [after.json](../lab10/results/after.json), screenshots және HTML report нақты browser run-нан алынған.

## 10 Regression Testing

10 dedicated check, before→after салыстыру және corrected suite-тің үш stability run-ы. [13 жұмыс](../lab13/REPORT.md). Expected values regression fix кезінде өзгермейді.

## 11 Performance Testing

Baseline,10,25,50,100 VU және spike; actual request counts, error rate, mean/p95/RPS [summary.json](../lab11/results/summary.json) ішінде. Read workload және қысқа duration шегі сақталады. Endurance екі сағаттық бөлек жоспар.

## 12 Security Testing

Authentication/authorization, SQL injection, XSS, input bounds, session TTL/revocation, cookie flags және headers. Real ZAP passive before/after scan: [zap-summary.json](../lab12/results/zap-summary.json). Scoped zero alert production security толықтығына тең емес.

## 13 Static Code Analysis

Ruff жаңа maintained source-ты тексереді. Lab8 Pylint, Ruff, Radon және 14 regression tests сапа gate-ін береді. Pricing complexity [complexity.json](results/complexity.json) ішінде.

## 14 Defect тізімі

| ID | Defect | Дәлел | Түзету мәртебесі |
|---|---|---|---|
| D01 | Price addition | Unit before | Fixed |
| D02 | Percent conversion | Unit before | Fixed |
| D03 | Exclusive shipping boundary | BVA before | Fixed |
| D04 | Shipping before discount | Acceptance/regression | Fixed |
| D05 | Arbitrary state transition | State tests | Fixed |
| D06 | SQLite connection left open | Coverage ResourceWarning | Fixed, regression added |
| UI01 | Fixed desktop width on mobile | Browser before screenshot | Fixed |
| SEC01 | Raw SQL authentication bypass | Before local SQLite | Fixed |
| SEC02 | Executable reflected HTML | Before HTML, browser retest | Fixed |
| SEC03–05 | Missing response headers | ZAP before | Fixed |
| LAB9-01 | Third-party profile password field | Newman TC33 | External open finding |

Lab8-дің 10 static/review defect-і өз есебінде толық берілген; бір root cause бірнеше test failure бере алатындықтан failures defect count ретінде қосылмайды.

## 15 Severity

Local pricing D01/D02/D04/D05 High; D03/D06 Medium; UI01 Medium; SEC01/SEC02 High; ZAP header findings Medium/Low. Lab8 before-да 2 Critical бар, corrected нұсқада олар жойылған. External LAB9-01 High болып бөлек қалады. Exact defect classification [lab8](../lab8/REPORT.md), [lab9](../lab9/REPORT.md), [lab12](../lab12/REPORT.md) есептерінде.

## 16 Test Coverage

Тексерілетін scope `qa_shop` пакетінің Python statement/branch coverage-ы. `npm run check` JSON/XML/HTML report және 85% minimum gate береді. Бұл UI JavaScript, external API немесе барлық ықтимал business path coverage-ы емес.

## 17 Pass Fail Rate

Pass Rate = passed/executed×100; Fail Rate = failed/executed×100. pytest failure/error және Playwright unexpected/skipped бөлек жазылады. Documented cases after — 20/20. Before intentional failures corrected release metric-іне қосылмайды. Барлық actual counts [SUMMARY.md](results/SUMMARY.md) ішінде есептеледі.

## 18 Қалдық тәуекелдер

Production login rate limiting жоқ; HTTPS termination deployment environment-ке тәуелді; multi-browser, long endurance және real payment scope-тан тыс; load generator/server бір хостта; passive security only selected URLs. External API password exposure жергілікті кодпен түзетілмейді. Бұлар production release қабылдауын шектейді.

## 19 Release Readiness

GO тек localhost оқу демонстрациясы үшін, егер current full quality run gate-тері өтсе. Production NO GO: rate limiting, hardened deployment, sustained load және кеңейтілген security review керек. CI workflow remote run-ы push/dispatch кейін ғана пайда болады; local stage evidence дайын.

## 20 Қорытынды Quality Assurance Report

Барлық 15 жұмыстың 300 task тармағы жеке есеппен қамтылған. Негізгі ақаулар before версияда қайталанып, corrected code және автоматты tests арқылы жабылды. `npm run lab15` build, static, unit/API, cases, debugging, regression, browser, load және ZAP evidence-ін қайта жасайды. Соңғы gate нәтижелері, counts және метрикалар [автоматты жиынтықта](results/SUMMARY.md).
