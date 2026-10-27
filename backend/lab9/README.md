# 9-зертханалық жұмыс — REST API тестілеу

**Мақсаты:** REST API құжаттамасын зерттеу, бес HTTP әдісін орындау және кемінде
20 сценарийі бар Postman Collection арқылы нәтижелерді тексеру.

Таңдалған сервис — [DummyJSON](https://dummyjson.com/docs). Коллекцияда **34 бөлек
HTTP сценарийі және 180 assertion** бар. 27.10.2026 күнгі нақты Newman іске
қосылуында **33/34 сценарий, 179/180 assertion өтті**. TC33 профиль жауабында
`password` өрісін анықтады; бұл оқу сервисінің шектеуі есепте сипатталған.

## Тапсыратын материалдар

| Файл | Мазмұны |
|---|---|
| [REPORT.md](REPORT.md) | 20 тапсырманың толық есебі және анықталған мәселе |
| [Lab9_DummyJSON.postman_collection.json](Lab9_DummyJSON.postman_collection.json) | Postman Collection v2.1, 34 сценарий және assertions |
| [Lab9_DummyJSON.postman_environment.json](Lab9_DummyJSON.postman_environment.json) | API адресі, ашық демо логин/пароль, уақыт шегі |
| [SCENARIOS.md](SCENARIOS.md) | Барлық сценарийдің method, endpoint және expected status кестесі |
| [results/RUN_RESULTS.md](results/RUN_RESULTS.md) | Әр сұраныстың нақты статусы, уақыты және PASS/FAIL |
| [results/newman-results.json](results/newman-results.json) | Assertions, нақты response body және headers; токендер жасырылған |

## Swagger UI және ReDoc

Жоба түбірінен backend іске қосыңыз:

```bash
cd backend
./.venv/bin/uvicorn main:app --reload --port 8000
```

- [Lab 9 Swagger UI](http://localhost:8000/lab9/docs) — сұраныстарды қолмен орындау.
- [Lab 9 ReDoc](http://localhost:8000/lab9/redoc) — endpoint және schema құжаттамасы.

Екі бет [DummyJSON OpenAPI схемасын](https://dummyjson.com/openapi.json)
қолданады. Swagger-де endpoint ашып, **Try it out → Execute** таңдаңыз.
Мысалы: `GET /products/{id}`, `id=1` → 200 және тауардың JSON жауабы.
Сұраныстар тікелей DummyJSON-ға жіберіледі; интернет қажет.
Жобаның өз API беттері `/docs` және `/redoc` адрестерінде қалады.

## Postman Collection Runner арқылы іске қосу

1. Postman Desktop ашыңыз. Web нұсқасында сұраныстар үшін Desktop Agent таңдаңыз.
2. **Import → Files** арқылы коллекция мен environment JSON файлдарын импорттаңыз.
3. Оң жақтағы environment тізімінен **Lab9 — DummyJSON** таңдаңыз.
4. Коллекцияны ашып, **Run collection** таңдаңыз.
5. Барлық төрт папкадағы **34 сұранысты бастапқы ретімен** қалдырыңыз.
6. **Iterations = 1**, **Delay = 300 ms** орнатыңыз. Data file қажет емес.
7. **Run** басып, нәтижелердегі Requests және Tests/Assertions бөлімдерін қараңыз.

Толық іске қосу маңызды: бастапқы GET сұраныстары шекаралық мәндерді және
бастапқы тауарды сақтайды; TC32 access token алып, TC33–TC34 оны қолданады.
Cookie jar әр сұраныста өшірілген, сондықтан Bearer тексерісіне cookie әсер етпейді.
Коллекция TC01 кезінде уақытша айнымалыларды тазартады.

`password` environment мәні — ресми құжаттамада жарияланған демо пароль.
Егер Postman оны импорттағанда жасырса немесе бос қалдырса, **Lab9 — DummyJSON**
environment ішінде `password` жергілікті мәнін `emilyspass` етіп орнатыңыз.
API key немесе жеке аккаунт қажет емес.

Осы ортада Postman графикалық интерфейсі іске қосылған жоқ. Сақталған нәтиже —
сол коллекцияның **Newman 6.2.1 арқылы нақты орындалуы**.

## Newman арқылы қайталау

Node.js 20 және npm, интернет байланысы қажет. Жоба түбірінде:

```bash
npm ci --prefix backend/lab9 --no-audit --no-fund
npm run lab9
```

Немесе тікелей:

```bash
npm test --prefix backend/lab9
```

Скрипт нәтижелердің екі файлын қайта жазады. Assertion орындалмаса, процесс
**exit code 1** қайтарады. Ағымдағы DummyJSON-де бұл TC33 тексерісіне байланысты
күтілетін анықталған мәселе; тексеріс өшірілмеген және FAIL жасырылмайды.
Сервис өзгергенде жаңа нәтиже өзгеше болуы мүмкін.

Стандартты Newman CLI командасы да сол коллекцияны орындайды:

```bash
backend/lab9/node_modules/.bin/newman run \
  backend/lab9/Lab9_DummyJSON.postman_collection.json \
  --environment backend/lab9/Lab9_DummyJSON.postman_environment.json \
  --iteration-count 1 --delay-request 300 --timeout-request 15000
```

Жоба скрипті қосымша JSON және Markdown есептерін жасайды және токендерді жасырады.
`maxResponseTimeMs=5000` — зертхананың өзгертуге болатын оқу критерийі.
Қайта іске қосуды жиі қайталамаңыз: API жауаптарында rate limit бар;
429 алынса, сервер көрсеткен шектеудің аяқталуын күтіңіз.

## Коллекцияны өзгерту

[generate-collection.mjs](generate-collection.mjs) — коллекция, environment және
сценарий кестесінің бастапқы коды. Өзгерткеннен кейін:

```bash
npm run generate --prefix backend/lab9
```

Бұл команда тек коллекция файлдарын жасайды; API-ге сұраныс жібермейді.
[run.mjs](run.mjs) дайын коллекцияны орындайды және нақты нәтижелерді сақтайды.
DummyJSON POST/PUT/PATCH/DELETE операциялары деректерді тұрақты сақтамайды;
TC17, TC20 және TC22 осы ерекшелікті арнайы тексереді.
