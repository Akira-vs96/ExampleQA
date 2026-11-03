# 5 зертханалық жұмыс Test Case және Test Scenario

Орындалатын 20 test case [cases.json](cases.json) ішінде. Толық preconditions, data, steps, expected, actual, status, priority және severity бар кесте [results/cases.csv](results/cases.csv) ішінде.

## 1 Тестілейтін функция

Тапсырыс бағасын есептеудің бес ережесі: line, discount, shipping, basket және state transition. Ортақ corrected модуль [pricing.py](../qa_shop/pricing.py), бастапқы faulty модуль [before/pricing.py](../lab6/before/pricing.py).

## 2 Бес Test Scenario

| ID | Сценарий | Cases |
|---|---|---|
| SC1 | Тауар жолын есептеу және quantity validation | TC01–03, TC11–14, TC20 |
| SC2 | Пайыздық жеңілдік | TC04–06, TC15–16 |
| SC3 | Жеткізу шегі және жарамсыз сома | TC07–08, TC17 |
| SC4 | Толық себет және бос себет | TC09, TC18 |
| SC5 | Заңды және тыйым салынған күй | TC10, TC19 |

## 3 Он Positive Test Case

| ID | Action және data | Expected |
|---|---|---|
| TC01 | line_total(2500,2) | 5000.00 |
| TC02 | line_total(0,1) | 0.00 |
| TC03 | line_total(100,100) | 10000.00 |
| TC04 | discounted_total(10000,20) | 8000.00 |
| TC05 | discounted_total(10000,0) | 10000.00 |
| TC06 | discounted_total(10000,100) | 0.00 |
| TC07 | shipping_cost(9999.99) | 1000.00 |
| TC08 | shipping_cost(10000) | 0.00 |
| TC09 | order_total([(2000,6)],20) | 10600.00 |
| TC10 | transition_order(paid,shipped) | shipped |

## 4 Он Negative Test Case

| ID | Action және invalid data | Expected |
|---|---|---|
| TC11 | line_total(-1,1) | ValueError |
| TC12 | line_total(100,0) | ValueError |
| TC13 | line_total(100,101) | ValueError |
| TC14 | line_total(100,1.5) | ValueError |
| TC15 | discounted_total(100,-1) | ValueError |
| TC16 | discounted_total(100,101) | ValueError |
| TC17 | shipping_cost(NaN) | ValueError |
| TC18 | order_total([]) | ValueError |
| TC19 | transition_order(shipped,cancelled) | ValueError |
| TC20 | line_total(100,true) | ValueError |

## 5 Preconditions

Python dependencies орнатылған; түбір каталог; таза модуль жүктелген; network немесе DB қажет емес. Before және after бөлек модуль ретінде импортталады. Екі run бірдей cases.json пайдаланады.

## 6 Test Data

Деректер [cases.json](cases.json) арқылы беріледі. Ақша string/int ретінде Decimal-ге түрленеді. JSON `true` Python bool екенін ескеретін жеке negative test бар; NaN JSON number ретінде емес, string ретінде беріледі.

## 7 Test Steps

1. Нұсқаны жүктеу. 2. Case.operation функциясын Case.args арқылы шақыру. 3. Нәтижені expected string немесе exact exception class-пен салыстыру. 4. Actual мен status сақтау. Қадамдар әр CSV жолына да жазылады.

## 8 Expected Result

Ақша нәтижесі екі таңбалы Decimal мәтінімен салыстырылады. Negative case тек `ValueError` күтеді: кездейсоқ `TypeError`/`InvalidOperation` PASS болып есептелмейді. Осылайша exception-ның бақыланатын contract-ы да тексеріледі.

## 9 Priority

Critical: TC01, TC04, TC09, TC19; High: негізгі boundary және validation; Medium: zero price, fraction/bool/NaN. Priority — орындау кезегі.

## 10 Severity

High — ақшалай есеп пен тыйым салынған ауысу бұзылуы; Medium — delivery boundary немесе қате input handling. Case-тегі severity — сол талап бұзылғандағы әсер; барлық passing case-де defect бар деген сөз емес.

## 11 Positive және Negative салыстыру

Positive жарамды әрекетке нақты нәтиже береді. Negative жарамсыз әрекеттің қауіпсіз тоқтауын тексереді. Тек positive suite қолданылса, zero quantity мен arbitrary state сияқты ақаулар жасырын қалар еді.

## 12 Boundary тесттері

Quantity 0/1/100/101; percent -1/0/100/101; shipping 9999.99/10000.00. Қосымша 10000.01 және rounding 1.005 [6 жұмыста](../lab6/tests/test_units.py) бар.

## 13 Тестілерді орындау

`npm run lab5`. Runner [run_cases.py](run_cases.py) before/after нәтижелерін JSON және CSV-ге жазады. Pytest бейімдемесі [test_cases.py](tests/test_cases.py) барлық 20 case-ті final suite-ке қосады.

## 14 Actual Result

Бастапқы нұсқа: 1/20 PASS; түзетілген нұсқа: 20/20 PASS. Мысал TC01 before 2502, after 5000.00; TC04 before -190000, after 8000.00; TC08 before 1000, after 0.00. Барлық actual [results/cases.json](results/cases.json) ішінде.

## 15 Status

PASS — actual expected-пен дәл сәйкес немесе күтілген exact exception шықты. FAIL — нәтиже/exception түрі сәйкес емес. Not Run осы runner-ге кірмейді: барлық case орындалуы міндетті.

## 16 Failed Test Case

TC08: Input 10000, Expected 0.00, Actual before 1000. Себеп: inclusive threshold `>` арқылы жазылған. Бұл test delivery boundary ақауын анықтайды.

## 17 Defect Report

ID D03; title «10000 KZT кезінде жеткізу артық есептеледі»; environment Python 3.13; precondition before module; steps `shipping_cost(10000)`; expected 0; actual 1000; severity Medium; priority High; root cause strict comparison; fix `>=`; retest TC08 PASS; status Closed.

## 18 Retest

Дәл сол cases.json corrected модульге қайта жіберілді. Expected өзгермеді. TC08 және қалған 19 case PASS; бастапқы before модуль оқу дәлелі ретінде сақталды.

## 19 Requirements Traceability Matrix

FR07 → TC01–03/11–14/20; FR08 → TC04–06/15–16; FR09 → TC07–08/17; FR10 → TC09/18; FR11 → TC10/19. Әр JSON case-де requirement ID бар. Талап пен case арасындағы байланыс runner CSV-де де сақталады.

## 20 Test Case жинағы

20 case, 5 scenario, нақты күтілетін нәтижелер, қадамдар және before/after evidence дайын. Қате нұсқаның failure-лары түзетуге дейінгі эксперимент ретінде сақталады; final corrected suite-те олар expected-failure ретінде жасырылмайды.
