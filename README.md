# DebugLab KZ

Python debugging тақырыбына арналған қазақша оқу жобасы. Жоба теорияны,
қате/дұрыс код жұптарын, debugger симуляциясын және автоматтандырылған
тесттерді бір сценарийге біріктіреді.

## Жоба құрылымы

```text
backend/
├── app/                 # FastAPI қолданбасы, route және schema
├── lab7/
│   ├── examples/        # buggy_*.py және fixed_*.py жұптары
│   └── tests/           # түзетілген кодтың regression тесттері
├── lab8/                # static analysis: before/after, метрикалар және Quality Gate
├── tests/               # API integration тесттері
└── main.py              # uvicorn кіру нүктесі
frontend/
└── src/
    ├── components/      # зертхана және есеп компоненттері
    ├── api.ts           # API клиенті
    ├── types.ts         # TypeScript модельдері
    └── App.tsx          # бет композициясы
```

## Іске қосу

Тәуелділіктерді бірінші рет бір рет орнатыңыз:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../frontend
npm install
```

Одан кейін бүкіл жобаны түбірлік каталогтан бір командамен іске қосыңыз:

```bash
cd /home/akira/IdeaProjects/ExampleQA
npm run dev
```

Команда FastAPI мен React серверлерін бірге іске қосады. Екеуін де тоқтату
үшін `Ctrl+C` басыңыз.

- әдеттегі сайт адресі: `http://localhost:5173`;
- әдеттегі API адресі: `http://localhost:8000`;
- API құжаттамасы: `http://localhost:8000/docs`.

Егер `5173` немесе `8000` бос болмаса, іске қосу скрипті келесі бос порттарды
автоматты түрде таңдап, нақты сілтемелерді терминалда көрсетеді. Vite proxy
таңдалған backend-портқа автоматты түрде бейімделеді.

Vite `/api` сұрауларын автоматты түрде `localhost:8000` серверіне жібереді.
Қажет болса, басқа API адресін `VITE_API_URL` арқылы көрсетуге болады.

## 7-зертханалық жұмыс

Әр тапсырмада алдымен әдейі қате код, содан кейін дұрыс нұсқа беріледі:

```bash
cd backend

# 1. Қатені бақылау
python lab7/examples/buggy_division.py

# 2. Дұрыс нұсқаны тексеру
python lab7/examples/fixed_division.py

# 3. Regression тесттерін орындау
python -m pytest -q lab7/tests
```

Қалған жұптар:

- `buggy_discount.py` → `fixed_discount.py`;
- `buggy_maximum.py` → `fixed_maximum.py`.

Толық debugger нұсқаулығы [DEBUG_GUIDE.md](DEBUG_GUIDE.md) файлында.

## 8-зертханалық жұмыс

Ruff, Pylint, Radon, тесттер және Quality Gate-ті бір командамен іске қосу:

```bash
cd /home/akira/IdeaProjects/ExampleQA
npm run lab8
```

Warning/Error, code smell, duplicate code, complexity, security, 10 кемшілік,
before/after метрикалары және 20 тапсырманың толық есебі
[backend/lab8/REPORT.md](backend/lab8/REPORT.md) файлында берілген.

## 9-зертханалық жұмыс

REST API тестілеу: DummyJSON үшін 34 сценарийі және 180 assertion бар
Postman Collection, environment және нақты Newman нәтижелері.
Орнату және іске қосу:

```bash
npm ci --prefix backend/lab9 --no-audit --no-fund
npm run lab9
```

Толық [нұсқаулық](backend/lab9/README.md), [20 тапсырманың есебі](backend/lab9/REPORT.md)
және [нақты тест нәтижелері](backend/lab9/results/RUN_RESULTS.md).
27.10.2026 нәтижесі: 33/34 сценарий өтті; профильде password өрісін анықтаған
TC33 FAIL берді, сондықтан runner exit code 1 қайтарады.

## Барлық тесттер

```bash
cd backend
python -m pytest -q
```

Frontend production build:

```bash
cd frontend
npm run build
```

## СӨЖ 7

[sro7](sro7/README.md) — алдымен қате, кейін түзетілген Python бағдарламасы,
нақты debugger қадамдары және автоматтандырылған тесттер.

```bash
python3 sro7/01_buggy.py
python3 sro7/02_fixed.py
python3 -m unittest discover -s sro7 -p "test_*.py" -v
```
