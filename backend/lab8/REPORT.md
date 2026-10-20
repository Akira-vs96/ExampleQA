# 8-зертханалық жұмыс есебі

**Тақырып:** Static Analysis және Code Review арқылы код сапасын жақсарту

**Тексеру күні:** 20.10.2026

**Жоба:** Python тапсырыс және қайтарым сомасын есептеу модулі

## 1. Код жобасын таңдау

Талдауға `lab8/before/order_service.py` және `lab8/before/refund_service.py`
шағын жобасы таңдалды. Ол тауарларды қалыпқа келтіреді, сатып алушы санатына
қарай жеңілдік есептейді және қайтарым сомасын анықтайды. `before/` бастапқы
нұсқаны, ал `order_service.py` және `refund_service.py` түзетілген нұсқаны сақтайды.

## 2. Coding Standards

- PEP 8, сұрыпталған импорттар және жол ұзындығы ең көбі 100 таңба;
- public функциялар мен модельдерге type hint және docstring жазу;
- ақшаға binary `float` емес, `Decimal` қолдану;
- кіріс деректерін есептеуге дейін тексеріп, нақты exception шығару;
- cyclomatic complexity мәнін 10-нан асырмау;
- DRY қағидасын сақтау және есептеу логикасын көшірмеу;
- `eval`, `shell=True` және hardcoded secret қолданбау;
- түзетілген бизнес-логиканы regression тесттерімен қорғау.

Бұл ережелер `backend/pyproject.toml` ішінде Ruff және Pylint үшін бекітілді.

## 3. Pylint/Ruff орнату

| Құрал | Нұсқа | Мақсаты |
|---|---:|---|
| Ruff | 0.17.1 | style, error, bugbear, complexity және security rules |
| Pylint | 4.1.3 | code smell, error және duplicate code |
| Radon | 6.0.1 | cyclomatic complexity және SLOC метрикасы |

```bash
cd backend
.venv/bin/python -m pip install -r requirements-dev.txt
```

### Барлығын жеке іске қосу командалары

Төмендегі командалар жоба түбірінен орындалады:

```bash
cd /home/akira/IdeaProjects/ExampleQA/backend
```

Виртуалды ортаны жасау және тәуелділіктерді орнату:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Ruff арқылы бастапқы кодты тексеру:

```bash
.venv/bin/ruff check --config pyproject.toml lab8/before
```

Ruff арқылы түзетілген кодты тексеру:

```bash
.venv/bin/ruff check --config pyproject.toml \
  lab8/order_service.py lab8/refund_service.py
```

Pylint арқылы бастапқы кодты тексеру:

```bash
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/before
```

Pylint арқылы түзетілген кодты тексеру:

```bash
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml \
  lab8/order_service.py lab8/refund_service.py
```

Warning және Error тізімін Ruff арқылы жеке алу:

```bash
# Барлық warning/error diagnostics
.venv/bin/ruff check --config pyproject.toml \
  --select B,C90,E,F,I,PL,S,UP,W lab8/before

# Орындалуды бұзатын undefined name қатесі
.venv/bin/ruff check --config pyproject.toml --select F821 lab8/before
```

Code Smell және Duplicate Code-ты Pylint арқылы тексеру:

```bash
# Барлық code smell
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/before

# Тек duplicate code
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml \
  --disable=all --enable=duplicate-code \
  lab8/before/order_service.py lab8/before/refund_service.py
```

Cyclomatic Complexity-ді Radon арқылы салыстыру:

```bash
# Before
.venv/bin/radon cc -s -a lab8/before

# After
.venv/bin/radon cc -s -a \
  lab8/order_service.py lab8/refund_service.py
```

Security issue-лерді Ruff арқылы жеке іздеу:

```bash
# Before: S105, S307 және S602 табылады
.venv/bin/ruff check --config pyproject.toml --select S lab8/before

# After: security issue болмауы керек
.venv/bin/ruff check --config pyproject.toml --select S \
  lab8/order_service.py lab8/refund_service.py
```

SLOC метрикасын Radon арқылы алу:

```bash
# Before
.venv/bin/radon raw -s \
  lab8/before/order_service.py lab8/before/refund_service.py

# After
.venv/bin/radon raw -s \
  lab8/order_service.py lab8/refund_service.py
```

Тек Lab 8 тесттерін іске қосу:

```bash
.venv/bin/python -m pytest -q lab8/tests
```

Жеке тест файлын іске қосу:

```bash
.venv/bin/python -m pytest -q lab8/tests/test_order_service.py
.venv/bin/python -m pytest -q lab8/tests/test_refund_service.py
```

Толық before/after анализі мен Quality Gate-ті бір командамен орындау:

```bash
bash lab8/run_analysis.sh
```

Жоба түбірінен дәл осы толық тексеруді іске қосу:

```bash
cd /home/akira/IdeaProjects/ExampleQA
npm run lab8
```

## 4. Static Analysis жүргізу

```bash
.venv/bin/ruff check --config pyproject.toml lab8/before
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/before
.venv/bin/radon cc -s -a lab8/before
.venv/bin/radon raw -s lab8/before/order_service.py lab8/before/refund_service.py
```

Ruff барлық диагностиканы “error” деп атайды. Осы есепте орындалуды тікелей
бұзатын `F821` **Error**, қалғандары **Warning/Issue** ретінде жіктелді.

## 5. Warning тізімі

| Код | Саны | Мәселе |
|---|---:|---|
| F401 / W0611 | 1 | қолданылмаған `os` импорты |
| S105 | 1 | кодқа жазылған құпиясөз |
| C901 | 1 | `calculate_order` complexity = 11 |
| B006 / W0102 | 1 | mutable default argument (`cache={}`) |
| E711 / C0121 | 1 | `None` мәнімен `==` арқылы салыстыру |
| S307 / W0123 | 1 | қауіпті `eval()` қолдану |
| PLR1730 / R1730 | 1 | артық `if`, `min()` қолдануға болады |
| PLR2004 | 1 | `50` magic value |
| S602 | 1 | input мәні бар `shell=True` шақыруы |
| E722 / W0702 | 1 | exception түрі жоқ bare `except` |
| C0116 | 2 | public функциялардың docstring-і жоқ |
| R0801 | 1 | екі файлдағы қайталанған код |

## 6. Error тізімі

| Код | Саны | Мәселе | Әсері |
|---|---:|---|---|
| F821 / E0602 | 1 | `customer_name` анықталмаған | орындалса `NameError` болады |

Бастапқы нәтиже: **Ruff — 11 issue, Pylint — 10 message, 7.41/10**.

## 7. Code Smell

- **Long Method / God Function:** `calculate_order` бірнеше міндетті атқарады;
- **Primitive Obsession:** ақша үшін `float`, customer type үшін еркін `str`;
- **Magic Numbers:** 0.8, 0.9, 0.85, 0.75, 0.95, 50 және 100;
- **Mutable Default Argument:** `cache={}` шақырулар арасында күй сақтайды;
- **Exception Swallowing:** bare `except` нақты қатені жасырады;
- **Dead Code:** қолданылмайтын `os` импорты.

## 8. Duplicate Code

Pylint `R0801` ережесі екі бастапқы файлдағы `normalize_items` блоктарының
көшірілгенін тапты. Түзетілген нұсқада validation және subtotal есебі ортақ
`calculate_subtotal()` функциясына шығарылып, refund модулі оны импорттайды.

## 9. Complexity талдауы

| Кезең | Ең күрделі блок | Max CC | Орташа CC | Radon rank |
|---|---|---:|---:|---|
| Бастапқы | `calculate_order` | 11 | 4.25 | C (блок), A (орташа) |
| Түзетілген | `_validate_item`, `calculate_subtotal` | 4 | 2.00 | A |

## 10. Security issue

- **Critical — S307:** `eval(discount_expression)` arbitrary code execution қаупін тудырады;
- **Critical — S602:** input-пен жиналған `shell=True` command injection қаупін тудырады;
- **High — S105:** `ADMIN_PASSWORD = "admin123"` source code ішінде сақталған.

Түзетуден кейін Ruff security issue саны — **0**.

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
- [x] Positive, negative және boundary тесттері бар.
- [x] Ruff, Pylint және тесттер Quality Gate-тен өтеді.

## 12–14. Қолмен тексеру, 10 кемшілік және Severity

| № | Кемшілік | Severity | Табу тәсілі | Түзету |
|---:|---|---|---|---|
| 1 | Сенімсіз мәтінді `eval()` орындауы | Critical | Ruff S307, review | сандық `Decimal` параметрі |
| 2 | Input-пен `shell=True` шақыруы | Critical | Ruff S602, review | subprocess жойылды |
| 3 | Hardcoded admin password | High | Ruff S105 | secret кодтан жойылды |
| 4 | Анықталмаған `customer_name` | High | Ruff F821, Pylint E0602 | жанама output жойылды |
| 5 | `cache={}` ортақ күй сақтайды | High | B006/W0102 | cache міндеті жойылды |
| 6 | Теріс баға есепке қосылады | High | қолмен review | validation exception қосылды |
| 7 | Bare `except` қатені жасырады | Medium | E722/W0702 | себепсіз catch жойылды |
| 8 | Бір функцияның CC=11, міндеті көп | Medium | C901, Radon | шағын функциялар мен model |
| 9 | `normalize_items` екі рет көшірілген | Medium | Pylint R0801 | ортақ `calculate_subtotal` |
| 10 | Қолданылмайтын `os` импорты | Low | F401/W0611 | импорт жойылды |

Жіктеу: **Critical — 2, High — 4, Medium — 3, Low — 1**.

## 15. Кодты түзету

- immutable `OrderItem` және `OrderSummary` dataclass модельдері енгізілді;
- customer type үшін `CustomerType` enum қолданылды;
- ақша мен пайыз `Decimal` арқылы есептеледі;
- бос тапсырыс, бос атау, теріс баға, қате quantity және 0–100-ден тыс
  discount үшін `OrderValidationError` беріледі;
- discount кестесі бір жерде сақталды;
- subtotal/validation ортақ функцияға шығарылды;
- `eval`, subprocess, hardcoded secret және cache side effect жойылды.

## 16. Анализді қайта жүргізу

```bash
.venv/bin/ruff check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
.venv/bin/radon cc -s -a lab8/order_service.py lab8/refund_service.py
.venv/bin/radon raw -s lab8/order_service.py lab8/refund_service.py
.venv/bin/python -m pytest -q lab8/tests
```

## 17. Нәтижелерді салыстыру

| Көрсеткіш | Бастапқы | Түзетілген | Өзгеріс |
|---|---:|---:|---:|
| Ruff issue | 11 | 0 | −11 |
| Pylint message | 10 | 0 | −10 |
| Pylint score | 7.41/10 | 10.00/10 | +2.59 |
| Pylint Error | 1 | 0 | −1 |
| Security issue | 3 | 0 | −3 |
| Duplicate block | 1 | 0 | −1 |
| Max cyclomatic complexity | 11 (C) | 4 (A) | −7 |
| Average complexity | 4.25 | 2.00 | −2.25 |
| Source SLOC | 54 | 72 | +18 |
| Автоматты тесттер | жоқ | 14/14 өтті | +14 |

SLOC өсуі explicit models, validation және бөлек жауапкершіліктер қосылуымен түсіндіріледі.

## 18. Quality Gate нәтижесі

| Шарт | Threshold | Нәтиже | Status |
|---|---:|---:|---|
| Ruff | 0 issue | 0 | PASS |
| Pylint | ≥ 9.0/10 | 10.00 | PASS |
| Security | 0 issue | 0 | PASS |
| Duplicate code | 0 block | 0 | PASS |
| Max complexity | ≤ 10 | 4 | PASS |
| Tests | 100% pass | 14/14 | PASS |

**Quality Gate: PASSED.**

## 19. Код сапасының метрикалары

17–18 бөлімдеріндегі кестелер static analysis, complexity, duplication,
security, SLOC және тест нәтижелерін бірдей before/after scope үшін көрсетеді.
Барлық метриканы `run_analysis.sh` сценарийімен қайта өндіруге болады.

## 20. Қорытынды есеп

Static analysis runtime-ға дейін 11 Ruff issue және 10 Pylint message тапты,
ал қолмен review теріс бағаның есепке қосылу қатесін көрсетті. Refactoring-тен
кейін security issue мен duplicate code жойылды, max complexity 11-ден 4-ке
түсті, Pylint бағасы 10.00/10 болды және 14 тест өтті. **Quality Gate — PASSED.**
