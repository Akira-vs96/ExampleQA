# Құралдардың нақты тексеру нәтижелері

Бастапқы нұсқадағы Ruff және mypy қатесі күтіледі. Түзетілген код бөлек тексеріледі.

## `ruff --version`

```bash
backend/.venv/bin/python -m ruff --version
```

```text
ruff 0.17.1
```

Шығу коды: `0`.

## `mypy --version`

```bash
backend/.venv/bin/python -m mypy --version
```

```text
mypy 2.4.0 (compiled: yes)
```

Шығу коды: `0`.

## `pytest --version`

```bash
backend/.venv/bin/python -m pytest --version
```

```text
pytest 8.3.4
```

Шығу коды: `0`.

## `ruff check --config sro8/pyproject.toml sro8/01_buggy.py`

```bash
backend/.venv/bin/python -m ruff check --config sro8/pyproject.toml sro8/01_buggy.py
```

```text
F401 [*] `math` imported but unused
 --> sro8/01_buggy.py:3:8
  |
1 | """Бастапқы нұсқа: талдау арқылы анықталатын қателер бар."""
2 |
3 | import math
  |        ^^^^
help: Remove unused import: `math`
  |
2 |
  - import math
3 |
  |

Found 1 error.
[*] 1 fixable with `--fix`.
```

Шығу коды: `1`.

## `mypy --config-file sro8/pyproject.toml sro8/01_buggy.py`

```bash
backend/.venv/bin/python -m mypy --config-file sro8/pyproject.toml sro8/01_buggy.py
```

```text
sro8/01_buggy.py:6: error: Function is missing a type annotation  [no-untyped-def]
sro8/01_buggy.py:11: error: Function is missing a type annotation  [no-untyped-def]
sro8/01_buggy.py:19: error: Incompatible return value type (got "str", expected "int")  [return-value]
sro8/01_buggy.py:24: error: Call to untyped function "line_total" in typed context  [no-untyped-call]
sro8/01_buggy.py:25: error: Call to untyped function "discounted_total" in typed context  [no-untyped-call]
Found 5 errors in 1 file (checked 1 source file)
```

Шығу коды: `1`.

## `ruff check --config sro8/pyproject.toml sro8/02_fixed.py sro8/test_shop.py sro8/__init__.py`

```bash
backend/.venv/bin/python -m ruff check --config sro8/pyproject.toml sro8/02_fixed.py sro8/test_shop.py sro8/__init__.py
```

```text
All checks passed!
```

Шығу коды: `0`.

## `mypy --config-file sro8/pyproject.toml sro8/02_fixed.py`

```bash
backend/.venv/bin/python -m mypy --config-file sro8/pyproject.toml sro8/02_fixed.py
```

```text
Success: no issues found in 1 source file
```

Шығу коды: `0`.

## `pytest -q -c sro8/pyproject.toml sro8`

```bash
backend/.venv/bin/python -m pytest -q -c sro8/pyproject.toml sro8
```

```text
...................                                                      [100%]
19 passed in 0.01s
```

Шығу коды: `0`.

## `sro8/01_buggy.py`

```bash
backend/.venv/bin/python sro8/01_buggy.py
```

```text
Тауар құны: 2003
Жеңілдіктен кейін: -190000
Жеткізу құны: 1000
```

Шығу коды: `0`.

## `sro8/02_fixed.py`

```bash
backend/.venv/bin/python sro8/02_fixed.py
```

```text
Тауар құны: 6000
Жеңілдіктен кейін: 8000
Жеткізу құны: 0
```

Шығу коды: `0`.
