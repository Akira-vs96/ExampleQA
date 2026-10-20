# 8-зертханалық жұмыс — код сапасын талдау

Бұл зертханада Python-дағы тапсырыс сомасын есептеу шағын жобасы таңдалды.
`before/` — талдау нәтижесін қайта көрсету үшін әдейі өзгертілмей сақталған
бастапқы нұсқа. `order_service.py` және `refund_service.py` — түзетілген нұсқа.

## Құрылым

```text
lab8/
├── before/                 # әдейі ақаулы бастапқы код
├── tests/                  # regression тесттері
├── order_service.py        # түзетілген тапсырыс логикасы
├── refund_service.py       # түзетілген қайтарым логикасы
├── run_analysis.sh         # before/after анализі және Quality Gate
└── REPORT.md               # 20 тапсырманың толық есебі
```

## Орнату және іске қосу

Жоба түбірінен:

```bash
cd backend
python -m venv .venv                 # орта әлі жоқ болса
.venv/bin/python -m pip install -r requirements-dev.txt
cd ..
npm run lab8
```

Немесе `backend` каталогында жеке командаларды орындауға болады:

```bash
.venv/bin/ruff check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. .venv/bin/pylint --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
.venv/bin/radon cc -s -a lab8/order_service.py lab8/refund_service.py
.venv/bin/python -m pytest -q lab8/tests
```

Толық нәтиже мен қорытынды [REPORT.md](REPORT.md) файлында берілген.
