# 8-зертханалық жұмыс — код сапасын талдау

Бұл зертханада Python-дағы тапсырыс және қайтарым сомасын есептеу жобасына
Static Analysis және Code Review жасалады. `before/` — әдейі сапасыз бастапқы
код, ал `order_service.py` және `refund_service.py` — түзетілген нұсқа.

## Құрылым

```text
lab8/
├── before/                 # әдейі ақаулы бастапқы код
├── tests/                  # автоматты және regression тесттері
├── order_service.py        # түзетілген тапсырыс логикасы
├── refund_service.py       # түзетілген қайтарым логикасы
├── run_analysis.sh         # before/after анализі және Quality Gate
└── REPORT.md               # 20 тапсырманың толық есебі
```

## Орнату және іске қосу

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
cd ..
npm run lab8
```

Немесе backend каталогында жеке командаларды орындауға болады:

```bash
.venv/bin/ruff check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
.venv/bin/radon cc -s -a lab8/order_service.py lab8/refund_service.py
.venv/bin/python -m pytest -q lab8/tests
```

Warning/Error тізімдері, code smell, duplicate code, complexity, security,
10 кемшілік, severity, before/after метрикалары және Quality Gate нәтижесі
[REPORT.md](REPORT.md) файлында берілген.
