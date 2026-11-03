# 13 зертханалық жұмыс Regression Testing

Regression suite мақсаты — бұрын анықталған бес pricing ақауын және негізгі HTTP contract-ты әр өзгерістен кейін қайта тексеру. Бірдей expected values faulty және corrected implementation-ға қолданылады.

## 1 Бастапқы қосымша

QA Shop corrected application және [before/pricing.py](../lab6/before/pricing.py) бастапқы бес ақауды көрсетеді. Live API тек corrected модульге тәуелді.

## 2 Жиырма негізгі функция

| № | Функционал | Дәлел |
|---|---|---|
| 1 | Бірегей тіркелу | lab3 integration |
| 2 | Duplicate registration | lab12 |
| 3 | Valid login | lab10 |
| 4 | Invalid login | lab12 |
| 5 | Authenticated profile | lab12 |
| 6 | Anonymous profile denial | lab12 |
| 7 | Logout | lab10 |
| 8 | Revoked token rejection | lab12 |
| 9 | Каталог | regression smoke |
| 10 | Case-insensitive search | regression |
| 11 | Бос search | lab10 |
| 12 | Unknown product | regression |
| 13 | Line total | regression |
| 14 | Discount | regression |
| 15 | Inclusive delivery boundary | regression |
| 16 | Discounted basket | regression |
| 17 | Quantity validation | lab4/lab6 |
| 18 | Empty quote validation | regression |
| 19 | Allowed order state | lab4/regression |
| 20 | Report catalogue | portal browser test |

## 3 Smoke Test

Health 200, catalogue count 3 және multiplication result дұрыс. `node scripts/python.mjs -m pytest -q -m smoke` ең маңызды launch checks орындайды.

## 4 Regression Test Case

RG01 multiplication, RG02 percent conversion, RG03 inclusive free delivery, RG04 delivery after discount, RG05 illegal cancellation, RG06 health, RG07 catalogue, RG08 upper-case search, RG09 unknown product, RG10 empty quote.

## 5 Test Suite

[test_regression.py](tests/test_regression.py) — 10 арнайы check; `pytest.mark.regression` фильтрі бар. Кеңейтілген full suite unit/API/security/SRO тесттерін де қамтиды.

## 6 Автоматтандыру таңдауы

Детерминистік arithmetic, states, HTTP statuses және catalogue нәтижелері автоматтандырылды. Эстетикалық баға және ұзақ endurance бақылауы осы suite-ке кірмейді. Synthetic user, tmp_path DB және exact expectations қолданылады.

## 7 Он автоматты тест

RG01–RG10 әрқайсысы жеке pytest function ретінде іске қосылады. Fixture domain implementation-ды таңдайды; API өз dependency-сымен corrected болып қалады. Сондықтан before экспериментінде бес formula/state test fail болады, бес API check өтеді.

## 8 Test Data

2000×3=6000; 10000−20%=8000; delivery(10000)=0; 12000−20%+delivery=10600; shipped→cancelled forbidden. HTTP IDs: known 1 және unknown 999; quote үшін empty list.

## 9 Тестілерді орындау

`npm run lab13` corrected suite орындайды. `npm run demo` before/after pytest subprocess-терін іске қосып, output және JUnit сақтайды.

## 10 Нәтижелер

[results/before.txt](results/before.txt): regression пайда болатын нұсқа. [results/after.txt](results/after.txt): corrected result. [comparison.json](results/comparison.json) exact commands және exit codes сақтайды.

## 11 Failed Test

RG03 бастапқы `shipping_cost(10000)` үшін 1000 алады; expected=0. RG05 shipped order-ді cancel жасауға рұқсат берілгенін анықтайды. Қалған үш fail есептеу ережелеріне тиесілі.

## 12 Бағдарламаға өзгеріс

Regression experiment before модуліндегі бес ақауды corrected pricing implementation-мен ауыстырады. Тест expected values өзгермейді. Live кодты уақытша бүлдірудің орнына fixture explicit variant таңдайды.

## 13 Қайта орындау

After сол test targets-пен қайта орындалады; exit code 0. Бұл retest жаңа fix-ті және бұрынғы API тексерулердің сақталғанын көрсетеді.

## 14 Before After салыстыру

Before: 5 failed, 5 passed. After: 10 passed. Бір run-ның failed/expected-failure саны after pass rate denominator-ына қосылмайды. JUnit файлдары екі нұсқа үшін бөлек.

## 15 Broken Function

line_total, discounted_total, shipping_cost, order_total және transition_order — broken functions. Әрқайсысына нақты regression case бар; симптомды UI-де жасыру арқылы түзету жасалған жоқ.

## 16 Flaky Test іздеу

[repeat_regression.py](../../scripts/repeat_regression.py) corrected suite-ті үш тәуелсіз process-те қайталайды. Нәтиже [stability.json](results/stability.json) ішінде. Үш тұрақты run осы экспериментте flaky failure байқалмағанын көрсетеді; бұл болашақта мүлде болмайтынының дәлелі емес.

## 17 Suite оңтайландыру

Таза calculation checks unit-де, тек негізгі workflow browser-де қалдырылды. Fixed sleep және external API dependence жоқ. Usernames бірегей, DB уақытша, retry=0. Smoke marker жылдам launch feedback береді.

## 18 Test Coverage

Full suite coverage scope — `qa_shop`. [coverage.json](../lab15/results/coverage.json) және final [SUMMARY.md](../lab15/results/SUMMARY.md) statement/branch мәндерін береді. Dedicated regression 10 checks толық Python code coverage claim жасамайды.

## 19 Automation Rate

Таңдалған regression suite: automated 10 / planned 10 ×100 = 100%. Documented case catalogue: automated 20 / planned 20 = 100%. Бұл пайыз exploratory UI немесе production endurance қамтылғанын білдірмейді.

## 20 Қорытынды

Бес ақау regression checks-пен қайталанды, түзетуден кейін 10/10 dedicated checks өтті. Үш repeat run stability evidence береді. Full test suite мен CI осы regression қорғанысын үнемі орындайды.
