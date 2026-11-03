# 6 зертханалық жұмыс Unit Testing

Бес бизнес функциясы және validation helper үшін unit suite дайындалды. Алдымен [қате нұсқа](before/pricing.py), кейін [түзетілген нұсқа](../qa_shop/pricing.py) тексеріледі.

## 1 Python жобасы

Python 3.13 virtual environment, root pytest configuration және dependencies қолданылды. Орнату: `python -m pip install -r requirements-dev.txt`; іске қосу: `npm run lab6`.

## 2 Тестілейтін модуль

[qa_shop/pricing.py](../qa_shop/pricing.py) HTTP, DB және browser-ден тәуелсіз. Барлық calculation функциялары берілген кірістен return value немесе ValueError шығарады.

## 3 Бес функция

| Функция | Кіріс | Шығыс |
|---|---|---|
| line_total | price, quantity 1–100 | Decimal |
| discounted_total | subtotal, integer percent 0–100 | Decimal |
| shipping_cost | discounted total | Decimal 0/1000 |
| order_total | Nonempty lines, percent | Decimal total |
| transition_order | source, target | target немесе ValueError |

## 4 Әр функцияға Unit Test

[test_units.py](tests/test_units.py) бес функцияның қалыпты және қате нәтижелерін тексереді. Жеке ақша parser-інде NaN, infinity, bool және malformed мәндері тексеріледі.

## 5 Positive Test

`line_total(2500,2) == Decimal('5000.00')`; `discounted_total(100,20) == 80.00`; valid state new→paid. Expected business arithmetic арқылы алдын ала анықталды.

## 6 Negative Test

Negative price, quantity 0/−1/101, бөлшек және string quantity; percent −1/101; NaN/infinity; белгісіз күй. Бәрі бақыланатын ValueError беруі тиіс.

## 7 Edge Case

Zero price valid; 100% discount valid; quantity 1 және 100 valid; `10000.00` delivery шегіне кіреді. Decimal('1.005') бірлік бағасы HALF_UP арқылы 1.01 болады; екі бірлік 2.02 береді.

## 8 Exception Test

`test_empty_cart` бос order-ді қабылдамайды. `test_transition` shipped→cancelled ауысуын тоқтатады. `test_invalid_amount` қате саннан decimal exception leak болмауын тексереді.

## 9 Assert

Күтілетін Decimal нақты теңдікпен салыстырылады; binary float tolerance қажет емес. State target string-пен салыстырылады. Әр test бір бизнес ережені түсінікті атпен белгілейді.

## 10 pytest raises

`with pytest.raises(ValueError): ...` қай input қабылданбауға тиіс екенін тексереді. Exception болмауы да, басқа class болуы да FAIL болады.

## 11 Parametrized Test

`@pytest.mark.parametrize` quantity, percent, shipping boundary және malformed amount комбинацияларын жеке test ретінде тіркейді. Failure атауында нақты параметр көрінеді; тест body қайталанбайды.

## 12 Fixture

Root [conftest.py](../../conftest.py) `pricing` fixture береді. `QA_VARIANT=before` кезінде faulty module, әдетте corrected module таңдалады. Suite және expected өзгермейді.

## 13 Test Suite

`backend/lab6/tests` — unit suite. 4 жұмыс boundary/state, 5 жұмыс documented cases, 13 жұмыс regression арқылы толықтырылады. Default pytest faulty implementation-ды автоматты іске қоспайды.

## 14 Тестілерді орындау

Corrected: `npm run lab6`. Толық before/after: `npm run demo`. Нақты output [results/after.txt](results/after.txt) және [results/before.txt](results/before.txt) ішінде.

## 15 Failed тесті

Бастапқы `line_total(2500,2)` 2502 береді; test 5000 күтеді. Бастапқы discount(100,20) −1900 береді, test 80 күтеді. Бірдей suite нақты формула ақауын қайталайды.

## 16 Қате кодты түзету

Қосу көбейтуге ауыстырылды; пайыз /100 түрлендіріледі; shipping boundary inclusive; order discount-тан кейін жеткізуді есептейді; state graph тексеріледі. Сонымен бірге finite nonnegative money және strict integer guard қосылды.

## 17 Retest

`scripts/demonstrate.py` әр variant-ты бөлек pytest subprocess-те орындайды. Before exit 1, after exit 0. [comparison.json](results/comparison.json) command пен exit code-ты сақтайды.

## 18 pytest cov

`npm run check` командасы `--cov=qa_shop --cov-branch --cov-fail-under=85` пайдаланады. JSON, XML және HTML coverage есептері [15 жұмыс нәтижелеріне](../lab15/results/) жазылады.

## 19 Coverage талдауы

Coverage scope — ортақ `qa_shop` Python пакеті. Statement және branch бөлек саналады; нақты мәндер [SUMMARY.md](../lab15/results/SUMMARY.md) ішінде. Before кодтың төмен coverage-ы corrected quality gate-ке қосылмайды. Барлық жолдың орындалуы бизнес талаптардың толықтығын өздігінен дәлелдемейді.

## 20 Unit Testing есебі

Бес функцияға positive, negative, edge, exception және parametrized tests жасалды. Алдымен faulty нұсқа fail болды, түзетілген нұсқа сол күтілетін нәтижелермен retest-тен өтті. Suite external network-сыз орындалады және CI coverage шегіне қосылған.
