# 1 зертханалық жұмыс Қосымша сапасы және тестілеу талаптары

Нысан — осы репозиторийдегі QA Shop оқу интернет-дүкені. Талаптар кейінгі зертханалардағы кодпен, тесттермен және өлшеулермен байланыстырылған.

## 1 Қосымшаны сипаттау

QA Shop тауар каталогын қарауға және тапсырыс сомасын есептеуге арналған. Сатып алушы логин мен пароль арқылы тіркеледі. Жүйеге кірген пайдаланушы өзінің профилін көреді. Каталогтағы тауарларды атауы бойынша іздеуге болады. Себет сомасына пайыздық жеңілдік және жеткізу ақысы қолданылады. Бөлек домендік модуль тапсырыстың рұқсат етілген күйлерін тексереді. Жоба нақты төлем қабылдамайтын жергілікті оқу қосымшасы ретінде қолданылады.

## 2 Пайдаланушылар

| Пайдаланушы | Рөлі | Мүмкіндігі |
|---|---|---|
| Қонақ | Каталогты зерттеу | Тіркелу, іздеу, зертханалық есеп оқу |
| Сатып алушы | Есептеу | Кіру, профиль, жеңілдікпен тапсырыс есептеу, шығу |
| QA студент | Тексеру | Қате нұсқа, түзету, автоматты тесттер және есеп |
| Оқытушы | Бағалау | 300 тапсырманың дәлелдері мен нәтижелерін салыстыру |

Әкімші панелі және нақты сатушы рөлі осы оқу нұсқасына кірмейді.

## 3 Функционалдық талаптар

| ID | Талап және қабылдау шарты | Басымдық | Тексеру |
|---|---|---|---|
| FR01 | Бірегей логинмен тіркелу 201; қайталау 409 | High | API, SQLite |
| FR02 | Дұрыс парольмен кіру 200; қате пароль 401 | Critical | API, UI |
| FR03 | Сессиямен `/me` профиль береді; сессиясыз 401 | Critical | Security |
| FR04 | Шығу 204; бұрынғы token қайта қолданылса 401 | Critical | Security, UI |
| FR05 | Каталогта 3 анықтамалық тауар бар | High | API, smoke |
| FR06 | `KEYBOARD` сұрауы Keyboard табады; жоқ атау бос тізім береді | High | API, UI |
| FR07 | Баға × бүтін саны; саны 1–100; теріс баға қабылданбайды | Critical | Unit, BVA |
| FR08 | Сома × (100 − пайыз) / 100; пайыз 0–100 | Critical | Unit |
| FR09 | Жеңілдіктен кейінгі сома ≥ 10000 болса жеткізу 0, әйтпесе 1000 | High | Decision table |
| FR10 | Бос емес себет, жеңілдік және жеткізу KZT сомасын береді | Critical | Acceptance |
| FR11 | Тек анықталған күй ауысулары қабылданады | High | State tests |
| FR12 | Порталда 15 жұмыстың толық есебі оқылады және жүктеледі | Medium | Build, UI |

## 4 Функционалдық емес талаптар

| ID | Өлшенетін талап | Басымдық | Әдіс |
|---|---|---|---|
| NFR01 | 50 virtual user кезінде каталог p95 ≤ 200 ms, жергілікті 8 s профиль | High | Locust |
| NFR02 | Сол профильдегі HTTP/application error rate ≤ 1% | High | Locust |
| NFR03 | Пароль PBKDF2 SHA256 және жеке 16 byte salt арқылы сақталады | Critical | SQLite inspection |
| NFR04 | Сессия TTL 3600 s; мерзімі өткен token 401 береді | Critical | Session test |
| NFR05 | Қате JSON құрылымы 422 береді | High | Negative API |
| NFR06 | Ақша Decimal және HALF_UP арқылы 0.01 дәлдігіне дөңгелектенеді | High | Rounding test |
| NFR07 | 375, 768, 1440 px кезінде көлденең overflow жоқ | Medium | Playwright |
| NFR08 | Жауапта nosniff, DENY, CSP және no-referrer бар | High | Headers, ZAP |
| NFR09 | Ортақ `qa_shop` statement және branch жиынтық coverage ≥ 85% | High | pytest-cov |
| NFR10 | Қате тест CI quality gate-ті нөлден өзге кодпен тоқтатады | High | Pipeline demo |
| NFR11 | Профильде пароль, hash, salt және token жоқ | Critical | Response assertions |
| NFR12 | Негізгі pytest suite сыртқы API-сыз, жеке уақытша SQLite-мен орындалады | Medium | Fixtures |

## 5 Талаптарды жіктеу

FR01–FR12 — функционалдық: жүйенің нақты әрекеті. NFR01–NFR12 — функционалдық емес: сол әрекеттердің сапасы, қорғалуы және тексерілуі. Кестелердегі басымдықтар тест кезегін анықтайды. Машинамен оқылатын жиынтық [requirements.csv](requirements.csv) ішінде.

## 6 ISO IEC 25010 сипаттамалары

PDF-тегі сегіз сипаттамаға сәйкес [ISO/IEC 25010:2011](https://www.iso.org/standard/35733.html) үлгісі қолданылады. [2023 редакциясында](https://www.iso.org/standard/78176.html) тоғыз сипаттама бар; редакциялар араластырылмайды.

| Сипаттама | QA Shop үшін өлшем |
|---|---|
| Functional suitability | FR01–FR12 қабылдау шарттары |
| Performance efficiency | NFR01 p95 және NFR02 error rate |
| Compatibility | JSON HTTP API, Chromium және Linux |
| Usability | Form label, validation, responsive өлшемдер |
| Reliability | Қате кірістерде бақыланатын 4xx, тұрақты regression suite |
| Security | Сессия, parameterized SQL, cookie және CSP |
| Maintainability | Pricing → repository → API қабаттары, unit tests |
| Portability | Python 3.13, Node 22, орта айнымалыларымен конфигурация |

## 7 Негізгі пайдаланушы сценарийі

Тіркелу → кіру → Keyboard іздеу → 2 дана таңдау → 20% жеңілдік → есептеу. Күтілетін нәтиже: subtotal 10000.00, discounted 8000.00, shipping 1000.00, total 9000.00 KZT. Шығудан кейін дәл сол есептеу 401 береді. Автоматты дәлел: [system және acceptance tests](../lab3/tests/test_levels.py).

## 8 Use Case

| ID | Actor | Әрекет | Нәтиже | Балама ағын |
|---|---|---|---|---|
| UC01 | Қонақ | Тіркелу | Пайдаланушы сақталды | 409 duplicate |
| UC02 | Қонақ | Кіру | HttpOnly cookie | 401 wrong password |
| UC03 | Қонақ | Іздеу | Сәйкес тауарлар | Бос нәтиже |
| UC04 | Сатып алушы | Тапсырысты есептеу | KZT JSON | 422 invalid quantity |
| UC05 | Сатып алушы | Шығу | Сессия өшірілді | Қайта шығу да 204 |
| UC06 | Студент | Зертхана есебін ашу | Есеп мәтіні және жүктеу | Желі қатесі туралы хабар |

## 9 Талаптардың тексерілуі

3 және 4 бөлімдердегі әр талапта критерий мен тексеру әдісі бар. FR11 тек домендік функция ретінде тексеріледі; тапсырыс күйін сақтайтын HTTP сервисі бұл нұсқаға кірмейді. NFR01–02 қысқа жергілікті экспериментпен шектелген; олар тәуліктік SLA болып саналмайды. NFR07 usability сараптамасын алмастырмайтын өлшемдік тексеру.

## 10 Түсініксіз талаптарды нақтылау

| Бастапқы тұжырым | Өлшенетін нұсқа |
|---|---|
| Жүйе жылдам жұмыс істейді | 50 VU, 8 s каталог профилінде p95 ≤ 200 ms |
| Интерфейс ыңғайлы | Әр input-та label бар; 375 px кезінде overflow жоқ |
| Қосымша сенімді | Regression suite-де күтпеген failure және error жоқ |
| Көп пайдаланушыны қолдайды | 10, 25, 50 VU профильдерінде error rate ≤ 1% |
| Ақпарат тез жүктеледі | Каталогтың end-to-end клиенттік уақыты NFR01 шегінде |

## 11 Қайшылықтар және шешімдер

| Қайшылық | Шешім |
|---|---|
| Жеңілдікке дейін 10000 жеткізу тегін / жеңілдіктен кейін 10000 керек | FR09: тек жеңілдіктен кейінгі сома |
| 100% жеңілдік тегін тапсырыс / жеткізу әрқашан ақылы | Жеңілдік тауарға ғана, total 0 болғанда delivery 1000 |
| Қонақ бағаны қарай алады / есептеу үшін кіру керек | Каталог public, quote protected |

## 12 Талаптардың басымдығы

Critical: FR02, FR03, FR04, FR07, FR08, FR10, NFR03, NFR04, NFR11. High: каталог, іздеу, жеткізу, валидация, coverage және security headers. Medium: есептер порталы, responsive және қайта өндіру. Low: терминал анимациясы мен декоративті көлеңкелер; олар функционалдық release gate емес.

## 13 Тестілеу объектілері

Логин, пароль, registration API, login API, profile API, session storage, SQLite users, catalogue API, search input, price calculation, discount, delivery threshold, quote schema, order states, responsive layout, report catalogue — 16 объект.

## 14 Тәуекелдер

| ID | Тәуекел | Probability | Impact | Score | Деңгей |
|---|---|---:|---:|---:|---|
| R01 | Рұқсатсыз профильге кіру | 4 | 5 | 20 | Critical |
| R02 | Қате жеңілдікпен теріс төлем | 4 | 4 | 16 | High |
| R03 | SQL injection арқылы кіру | 3 | 5 | 15 | High |
| R04 | Жеткізу шегіндегі артық төлем | 3 | 3 | 9 | Medium |
| R05 | Мобильді экранда overflow | 3 | 2 | 6 | Medium |
| R06 | Сыртқы API қолжетімсіздігі | 2 | 3 | 6 | Medium |
| R07 | Қоғамдық серверде brute force | 3 | 4 | 12 | High |

## 15 Тәуекел матрицасы

Risk = Probability × Impact; әр көрсеткіш 1–5. 20–25 Critical, 12–19 High, 6–11 Medium, 1–5 Low.

| P / I | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | — | — | — | — | — |
| 2 | — | — | R06 | — | — |
| 3 | — | R05 | R04 | R07 | R03 |
| 4 | — | — | — | R02 | R01 |
| 5 | — | — | — | — | — |

## 16 Тестілеу кезегі

Алдымен authentication, authorization және ақша есебі; кейін SQL/input/session; одан кейін delivery boundaries мен UI; соңында декоративті тексеру. R07 production алдында rate limiting пен monitoring енгізуді талап етеді. Қазіргі release scope — жергілікті оқу демонстрациясы.

## 17 Бастапқы тест сценарийлері

| ID | Сценарий | Күтілетін нәтиже | Priority |
|---|---|---|---|
| TS01 | Бірегей тіркелу | 201 | High |
| TS02 | Қайталап тіркелу | 409 | High |
| TS03 | Дұрыс пароль | 200 және cookie | Critical |
| TS04 | Қате пароль | 401 | Critical |
| TS05 | Сессиясыз профиль | 401 | Critical |
| TS06 | Дұрыс сессиямен профиль | Тек id, username | Critical |
| TS07 | Шығу және token replay | 204, кейін 401 | Critical |
| TS08 | Каталог | 3 тауар | High |
| TS09 | Үлкен әріппен іздеу | Keyboard | High |
| TS10 | Жоқ тауар | 404 | Medium |
| TS11 | 2500 × 2 | 5000.00 | Critical |
| TS12 | 20% жеңілдік | 8000.00 | Critical |
| TS13 | 10000 delivery шегі | 0.00 | High |
| TS14 | Жеңілдіктен кейінгі жеткізу | total 9000.00 | Critical |
| TS15 | Бос себет | 422 | High |
| TS16 | Тыйым салынған күй | ValueError | High |
| TS17 | 375 px экран | Overflow жоқ | Medium |
| TS18 | 50 VU | p95 ≤ 200 ms, errors ≤ 1% | High |
| TS19 | SQL injection, XSS | Кіру жоқ, executable DOM жоқ | Critical |
| TS20 | 15 есеп | Бәрі оқылады | Medium |

## 18 Requirements Traceability Matrix

| Requirement | Test / дәлел | Күй |
|---|---|---|
| FR01, FR02, FR03, FR04 | TS01–07, lab3, lab10, lab12 | Automated |
| FR05, FR06 | TS08–09, lab13 regression, lab10 | Automated |
| FR07, FR08 | TS11–12, lab4, lab5, lab6 | Automated |
| FR09, FR10 | TS13–15, lab3 acceptance, lab4 decision table | Automated |
| FR11 | TS16, lab4 state pairs | Automated |
| FR12 | TS20, build, portal Playwright | Automated |
| NFR01, NFR02 | TS18, lab11 Locust CSV | Measured |
| NFR03, NFR04, NFR05, NFR08, NFR11 | TS04–07, TS15, TS19, lab12 | Automated |
| NFR06 | lab6 `test_round_half_up` | Automated |
| NFR07 | TS17, lab10 screenshots | Automated |
| NFR09 | lab15 coverage.json | Measured |
| NFR10 | lab14 before/after JUnit | Demonstrated locally |
| NFR12 | conftest fixtures, pytest suite | Automated |

## 19 Тестілеу стратегиясы

Scope In: кестелердегі жергілікті функциялар, API, UI, сессиялар және reports. Scope Out: нақты банк төлемі, SMTP, production HA және нақты тапсырысты жеткізу. Құралдар: pytest, HTTPX/TestClient, coverage, Playwright, Locust, Ruff/Pylint/Radon, ZAP. Critical сценарийлер бірінші орындалады. Exit: барлық corrected tests PASS, core coverage ≥ 85%, security High жоқ, 50 VU error rate ≤ 1%. Сыртқы DummyJSON нәтижесі жеке есептеледі.

## 20 Қорытынды

Бастапқы pricing нұсқасында көбейту, пайыз, жеткізу шегі, есептеу реті және күй ауысуы бойынша бес ақау бар. Ең маңызды тексерулер authentication пен ақша есептеуіне бағытталды. Қабылдау шарттары автоматты unit/API/UI тесттеріне, ал performance пен passive security нақты өлшеуге байланыстырылды. Барлық 24 талап тексерілетін түрде жазылды; соңғы метрикалар [15 жұмыстың нәтижесінде](../lab15/results/SUMMARY.md).
