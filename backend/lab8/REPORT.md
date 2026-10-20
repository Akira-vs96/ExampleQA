# 8-зертханалық жұмыс есебі

**Тақырып:** Static analysis және code review арқылы код сапасын жақсарту  
**Тексеру күні:** 20.10.2026  
**Жоба:** Python тапсырыс және қайтарым сомасын есептеу модулі

## 1. Код жобасын таңдау

Талдауға `lab8/before/order_service.py` және `lab8/before/refund_service.py`
шағын жобасы таңдалды. Ол тауарларды қалыпқа келтіреді, сатып алушы санатына
қарай жеңілдік есептейді және қайтарым сомасын анықтайды. Бастапқы нұсқа
зертханалық жұмыстағы before/after салыстыруын қайталау үшін сақталды.

## 2. Coding Standards

Жобаға мына талаптар қабылданды:

- PEP 8, импорттарды сұрыптау және жол ұзындығы — ең көбі 100 таңба;
- функциялар мен модельдерде type hint және docstring болуы;
- ақшаға binary `float` емес, `Decimal` қолдану;
- кіріс деректерін есептеуге дейін тексеру және нақты exception шығару;
- функцияның cyclomatic complexity мәні 10-нан аспауы;
- DRY қағидасы: есептеу логикасын көшірмеу;
- `eval`, `shell=True`, hardcoded secret қолданбау;
- түзетілген бизнес-логика regression тесттерімен қорғалуы.

Бұл ережелер `backend/pyproject.toml` ішінде Ruff және Pylint үшін бекітілді.

## 3. Pylint/Ruff орнату

Қолданылған нұсқалар:

| Құрал | Нұсқа | Мақсаты |
|---|---:|---|
| Ruff | 0.17.1 | style, error, bugbear, complexity және security rules |
| Pylint | 4.1.3 | code smell, error және duplicate code |
| Radon | 6.0.1 | cyclomatic complexity метрикасы |

Орнату командасы:

```bash
cd backend
.venv/bin/python -m pip install -r requirements-dev.txt
```

## 4–6. Static Analysis, Warning және Error тізімі

Бастапқы анализ:

```bash
cd backend
.venv/bin/ruff check --config pyproject.toml lab8/before
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/before
```

Ruff барлық табылған диагностиканы “error” деп атайды. Осы есепте орындалуды
тікелей бұзатын `F821` **Error**, қалғандары **Warning/Issue** деп бөлінді.

### Warning/Issue тізімі

| Код | Саны | Мәселе |
|---|---:|---|
| F401 / W0611 | 1 | қолданылмаған `os` импорты |
| S105 | 1 | код ішіне жазылған құпиясөз |
| C901 | 1 | `calculate_order` complexity = 11 |
| B006 / W0102 | 1 | mutable default argument (`cache={}`) |
| E711 / C0121 | 1 | `None` мәнімен `==` арқылы салыстыру |
| S307 / W0123 | 1 | қауіпті `eval()` қолдану |
| PLR1730 / R1730 | 1 | артық `if` блогы, `min()` қолдануға болады |
| PLR2004 | 1 | `50` magic value |
| S602 | 1 | пайдаланушы мәні бар `shell=True` шақыруы |
| E722 / W0702 | 1 | exception түрі көрсетілмеген bare `except` |
| C0116 | 2 | public функциялардың docstring-і жоқ |
| R0801 | 1 | екі файлдағы қайталанған код |

### Error тізімі

| Код | Саны | Мәселе | Әсері |
|---|---:|---|---|
| F821 / E0602 | 1 | `customer_name` анықталмаған | жол орындалса `NameError` болады |

Нәтиже: Ruff — **11 issue**, Pylint — **10 message**, Pylint бағасы —
**7.41/10**.

## 7. Code Smell

Қолмен және құралдармен мына иістер анықталды:

- **Long Method / God Function:** `calculate_order` validation, discount,
  command execution, cache және output міндеттерін бір жерде атқарады;
- **Primitive Obsession:** ақша үшін `float`, customer type үшін еркін `str`;
- **Magic Numbers:** 0.8, 0.9, 0.85, 0.75, 0.95, 50 және 100;
- **Mutable Default Argument:** шақырулар арасында ортақ `cache` күйі қалады;
- **Exception Swallowing:** bare `except` нақты қатені жасырады;
- **Dead Code:** қолданылмайтын `os` импорты.

## 8. Duplicate Code

Pylint `R0801` ережесі `order_service.py` және `refund_service.py` ішіндегі
`normalize_items` блоктарының көшірілгенін тапты (кемінде 4 ұқсас жол).
Түзетілген нұсқада ортақ validation және subtotal есебі
`calculate_subtotal()` функциясына шығарылып, refund модулі оны импорттайды.

## 9. Complexity талдауы

Команда:

```bash
.venv/bin/radon cc -s -a lab8/before
.venv/bin/radon cc -s -a lab8/order_service.py lab8/refund_service.py
```

| Кезең | Ең күрделі блок | Max CC | Орташа CC | Radon rank |
|---|---|---:|---:|---|
| Бастапқы | `calculate_order` | 11 | 4.25 | C (блок), A (орташа) |
| Түзетілген | `_validate_item`, `calculate_subtotal` | 4 | 2.00 | A |

## 10. Security issue

- **Critical — S307:** `eval(discount_expression)` arbitrary code execution
  жасауға мүмкіндік береді;
- **Critical — S602:** input-пен жиналған command және `shell=True` command
  injection қаупін тудырады;
- **High — S105:** `ADMIN_PASSWORD = "admin123"` құпия мәнді source code-та
  жариялайды.

Түзетуде discount тек `Decimal` ретінде қабылданады, қажетсіз subprocess толық
алынып тасталды, құпиясөз кодтан жойылды. Қорытынды Ruff security issue саны — 0.

## 11. Code Review Checklist

- [x] Код PEP 8 және import-order талаптарына сай.
- [x] Public API-де type hint пен docstring бар.
- [x] Input validation шекаралық мәндерді қамтиды.
- [x] Ақша `Decimal` арқылы есептеледі.
- [x] Secret, `eval` және shell command жоқ.
- [x] Exception нақты және мағыналы.
- [x] Бір функцияның міндеті шектелген.
- [x] Duplicate code жоқ.
- [x] Cyclomatic complexity threshold-тан аспайды.
- [x] Positive, negative және boundary regression тесттері бар.
- [x] Ruff, Pylint және барлық тест Quality Gate-тен өтеді.

## 12–14. Қолмен тексеру, 10 кемшілік және Severity

| № | Кемшілік | Severity | Табу тәсілі | Түзету |
|---:|---|---|---|---|
| 1 | Сенімсіз мәтінді `eval()` орындауы | Critical | Ruff S307, review | сандық `Decimal` параметрі |
| 2 | Input-пен `shell=True` шақыруы | Critical | Ruff S602, review | қажетсіз subprocess жойылды |
| 3 | Hardcoded admin password | High | Ruff S105 | secret source code-тан жойылды |
| 4 | Анықталмаған `customer_name` | High | Ruff F821, Pylint E0602 | жанама output жойылды |
| 5 | `cache={}` шақырулар арасында күй сақтайды | High | B006/W0102 | cache міндеті жойылды |
| 6 | Теріс баға тек басылып, есепке қосылады | High | қолмен review | validation exception қосылды |
| 7 | Bare `except` барлық қатені жасырады | Medium | E722/W0702 | себепсіз catch жойылды |
| 8 | Бір функцияның CC=11 және міндеті көп | Medium | C901, Radon | шағын функциялар мен model |
| 9 | `normalize_items` екі рет көшірілген | Medium | Pylint R0801 | ортақ `calculate_subtotal` |
| 10 | Қолданылмайтын `os` импорты | Low | F401/W0611 | импорт жойылды |

Жіктеу қорытындысы: **Critical — 2, High — 4, Medium — 3, Low — 1**.

## 15. Кодты түзету

Түзетілген кодта:

- `OrderItem` және `OrderSummary` immutable dataclass модельдері енгізілді;
- customer type еркін мәтіннің орнына `CustomerType` enum болды;
- ақша мен пайыз `Decimal` арқылы есептеледі;
- бос тапсырыс, бос атау, теріс баға, қате quantity және 0–100-ден тыс
  discount үшін `OrderValidationError` беріледі;
- discount кестесі бір жерде сақталды;
- subtotal/validation ортақ функцияға шығарылды;
- қауіпсіздікке қатысы жоқ shell және cache side effect-тері жойылды.

## 16–17. Қайта анализ және салыстыру

Қайта анализ командалары:

```bash
.venv/bin/ruff check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
.venv/bin/radon cc -s -a lab8/order_service.py lab8/refund_service.py
.venv/bin/python -m pytest -q lab8/tests
```

| Көрсеткіш | Бастапқы | Түзетілген | Өзгеріс |
|---|---:|---:|---:|
| Ruff issue | 11 | 0 | −11 |
| Pylint message | 10 | 0 | −10 |
| Pylint score | 7.41/10 | 10.00/10 | +2.59 |
| Pylint Error | 1 | 0 | −1 |
| Security issue (S-код) | 3 | 0 | −3 |
| Duplicate block | 1 | 0 | −1 |
| Max cyclomatic complexity | 11 (C) | 4 (A) | −7 |
| Average complexity | 4.25 | 2.00 | −2.25 |
| Source SLOC | 54 | 72 | +18 |
| Regression tests | жоқ | 11/11 өтті | +11 |

SLOC өсуі жаман нәтиже емес: жасырын side effect орнына explicit models,
validation және бөлек жауапкершіліктер қосылды.

## 18. Quality Gate нәтижесі

| Шарт | Threshold | Нәтиже | Status |
|---|---:|---:|---|
| Ruff | 0 issue | 0 | PASS |
| Pylint | ≥ 9.0/10 | 10.00 | PASS |
| Security | 0 issue | 0 | PASS |
| Duplicate code | 0 block | 0 | PASS |
| Max complexity | ≤ 10 | 4 | PASS |
| Tests | 100% pass | 11/11 | PASS |

**Quality Gate: PASSED.**

## 19. Код сапасының метрикалары

16–18 бөлімдердегі кестелерде static analysis, complexity, duplication,
security, SLOC және test нәтижелері бірдей before/after scope үшін берілді.
Метрикалар `run_analysis.sh` сценарийімен қайта өндіріледі.

## 20. Қорытынды

Static analysis runtime-ға дейін 11 Ruff issue және 10 Pylint message тапты,
ал қолмен review құрал анықтай алмайтын теріс бағаны есепке қосу бизнес қатесін
көрсетті. Refactoring-тен кейін қауіпсіздік ақаулары мен duplicate code жойылды,
max complexity 11-ден 4-ке түсті, Pylint бағасы 10.00/10 болды және 11 regression
test өтті. Қабылданған Quality Gate толық орындалды.
