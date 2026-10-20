# DebugLab KZ

Python debugging тақырыбына арналған қазақша оқу жобасы. Жоба теорияны,
қате/дұрыс код жұптарын, debugger симуляциясын және автоматтандырылған
тесттерді бір сценарийге біріктіреді.

## Жоба құрылымы

```text
backend/
├── app/                 # FastAPI қолданбасы, route және schema
├── lecture7/            # 15 бақылау сұрағы және қазақша жауаптар
├── lab7/
│   ├── examples/        # buggy_*.py және fixed_*.py жұптары
│   └── tests/           # түзетілген кодтың regression тесттері
├── lab8/                # static analysis, code review және quality gate
├── tests/               # API integration тесттері
└── main.py              # uvicorn кіру нүктесі
frontend/
└── src/
    ├── components/      # дәріс, зертхана және есеп компоненттері
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

## 7-дәріс

15 сұрақтың кодпен көрсетуге болатын 10 тармағы
[backend/lecture7/examples](backend/lecture7/examples) ішінде жеке Python
файлдары ретінде орындалған. Оларды VS Code ішінде **Run Python File** немесе
`F5` арқылы ашып, breakpoint, Variables, Watch, Call Stack, Step Over және
Step Into көмегімен көрсетуге болады. Қалған теориялық сұрақтар жасанды кодқа
айналдырылмай, `backend/lecture7/content.py` ішінде жауап ретінде сақталған.

Барлық дәріс мысалдарын бірден іске қосу:

```bash
npm run lecture7
```

Жеке файлды іске қосу:

```bash
cd backend
python lecture7/examples/topic_07_step_over_into.py
```

Толық файл тізімі мен debugger нұсқаулығы
[backend/lecture7/README.md](backend/lecture7/README.md) ішінде берілген.

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

Ruff, Pylint және Radon арқылы бастапқы/түзетілген кодты салыстыру:

```bash
cd backend
.venv/bin/python -m pip install -r requirements-dev.txt
cd ..
npm run lab8
```

20 тапсырманың толық есебі мен метрикалар
[backend/lab8/REPORT.md](backend/lab8/REPORT.md) файлында берілген.

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
