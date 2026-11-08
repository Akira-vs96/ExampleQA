# СРО 9 — REST API тестілеу

Бес тапсырма орындалған: бес HTTP әдісі, алты міндетті тест-кейс,
Python/pytest автоматтандыруы, қате URL талдауы және екі интеграциялық сценарий.
Толық тапсырма есебі: [REPORT.md](REPORT.md).

## Тесттер және терминалдағы автоматты есеп

Жоба түбірінде:

```bash
python -m pip install -r sro9/requirements.txt
npm run test:sro9
```

Қолмен сервер қосудың қажеті жоқ: pytest әр тестке бөлек қолданба жасайды.
Негізгі 18 тесттен кейін **SRO9 BEFORE / AFTER** бөлімі автоматты шығады:

```text
ОШИБОЧНЫЙ — examples/wrong_url.py
FAILED test_product_url — GET /api/products/1 → get_product()
  assert 404 == 200
  Причина: Опечатка в URL: /api/producst/1 не существует.
Итог ОШИБОЧНЫЙ: 0 passed, 1 failed; exit=1

ИСПРАВЛЕННЫЙ — examples/correct_url.py
PASSED test_product_url — GET /api/products/1 → get_product()
Итог ИСПРАВЛЕННЫЙ: 1 passed, 0 failed; exit=0
```

Нәтижелер екі нақты pytest процесінен алынады. Негізгі іске қосу қате нұсқаның
ақауы қайталанып, түзетілген нұсқа өткенде 0 кодымен аяқталады. Түзетілген нұсқа
өтпесе, тексеріс өткізіліп кетсе немесе іске қосу қатесі болса, exit code — 1.
Есеп жай `python -m pytest sro9` командасында және VS Code тесттерінде де қосылған.
Техникалық журналдар [results/](results/) каталогында сақталады.

## Postman

```bash
npm run sro9
```

API: http://127.0.0.1:8009; Swagger: http://127.0.0.1:8009/docs.
Серверді қайта қосқанда бастапқы `id=1` Keyboard тауары қалпына келеді.
Оқу деректері бір процестің жадында сақталады.

Postman-ға [коллекцияны](SRO9.postman_collection.json) және
[ортаны](SRO9.postman_environment.json) импорттаңыз. **СРО 9 — localhost** ортасын
таңдап, үш папканы бастапқы ретімен бір итерацияда орындаңыз.

Коллекцияда 21 сұраныс, 67 assertion бар. Бірінші папка — бір дұрыс, үш қате
және екі шекаралық жағдай; кейінгі екі папка — тәуелді HTTP сұраныстар тізбегі.
GET өзгерістердің сақталғанын тексереді, сценарий соңында құрылған тауарлар жойылады.

## Барлық тапсырманы қайта тексеру

```bash
npm install --prefix sro9 --no-audit --no-fund
npm run report:sro9
```

[run_all.py](run_all.py) pytest нәтижелерін және автоматты BEFORE/AFTER есебін
терминалға шығарады, уақытша жергілікті серверде Newman орындайды, бастапқы
HTTP жауаптарын сақтайды және тапсырма есебін жаңартады. Newman үшін бөлек
сервер ашудың қажеті жоқ. Ортада дайын `backend/lab9` Newman орнатылымы болса,
runner оны да қолдана алады.

- [test_cases.csv](test_cases.csv) — алты міндетті жағдай.
- [test_api.py](test_api.py) — 18 автотест және екі интеграциялық сценарий.
- [comparison.json](comparison.json) — автоматты салыстыру сипаттамасы.
- [results/summary.json](results/summary.json) — нақты сандар.
- [results/newman.json](results/newman.json) — HTTP жауаптары және assertions.

Коллекция мен CSV-ді қайта жасау: `python -m sro9.generate_postman`.
Ортақ терминал есебін қосу тәртібі: [SRO_TESTS.md](../scripts/SRO_TESTS.md).
