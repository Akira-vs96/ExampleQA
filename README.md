# DebugLab KZ

PDF бойынша **15 зертханалық жұмыс және 300 тапсырма**. Әр жұмысқа есеп, қажет жерде қате/түзетілген код, орындалатын тесттер және нақты evidence қосылған. Толық каталог: [LABS.md](LABS.md); құрылым: [ARCHITECTURE.md](ARCHITECTURE.md); соңғы нәтиже: [QA Summary](backend/lab15/results/SUMMARY.md).

## Орнату

Python 3.13, Node 22 және Java 17+ (тек ZAP үшін).

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
npm ci --no-audit --no-fund
npx playwright install chromium
```

Windows-та virtual environment interpreter жолы `.venv/Scripts/python.exe`. Npm scripts сол interpreter-ді автоматты табады; қажет болса `QA_PYTHON` арқылы таңдаңыз. Existing `backend/.venv` те fallback ретінде қолданылады.

## Жергілікті қосымша

```bash
npm run dev
```

Әдеттегі мекенжайлар: портал `http://127.0.0.1:8000`, оқу дүкені `http://127.0.0.1:8000/shop.html`, Swagger `http://127.0.0.1:8000/docs`. Порт бос болмаса launcher келесі бос портты көрсетеді. `QA_PORT` портты, `QA_DATABASE` SQLite файлын таңдайды. Тоқтату: Ctrl+C.

Frontend — HTML/CSS/JS; бөлек React/Vite server қажет емес. Дүкенде synthetic аккаунтты UI арқылы тіркеңіз; нақты төлем орындалмайды. Static Pages report portal-ы API-сыз жұмыс істейді, ал shop backend қажет етеді.

## Қате код және түзету

```bash
npm run demo       # Lab4/6/13: дәл сол tests before FAIL, after PASS
npm run lab5       # 10 positive + 10 negative case, CSV/JSON
npm run lab7       # ZeroDivisionError, traceback, real pdb, corrected result
npm run lab14      # failed test stage және corrected run
```

Қате нұсқа [lab6/before](backend/lab6/before/), corrected бизнес код [qa_shop](backend/qa_shop/) ішінде. Existing [lab7 examples](backend/lab7/examples/), [lab8 before/after](backend/lab8/), [SRO7](sro7/README.md), [SRO8](sro8/README.md) сақталған.

СРО7–9 тесттері соңында қате және түзетілген файлдың салыстыруы терминалға
автоматты шығады: FAILED/PASSED, функция, нақты қате, себеп және түзету.

```bash
npm run test:sro7
npm run test:sro8
npm run test:sro9
npm run test:sro10
```

[СРО9](sro9/README.md) — REST API, Postman, алты міндетті тест-кейс және екі
интеграциялық сценарий. Ортақ есеп механизмі: [SRO_TESTS.md](scripts/SRO_TESTS.md).

[СРО10](sro10/README.md) — QA Shop веб-қосымшасын функционалдық және интерфейстік
тестілеу: 20 тест-кейс, Playwright/pytest арқылы 30 тексеріс және екі ашық Bug Report.
`npm run report:sro10` нақты тексерістерді орындап, Word есебін де жаңартады.

## СРО 9 и СРО 10 — где находятся ошибочный и исправный код

Ниже приведён полный порядок показа именно для СРО 9 и СРО 10. Все команды
запускаются из корня проекта:

```bash
cd /home/akira/IdeaProjects/ExampleQA
source .venv/bin/activate
```

### СРО 9: неправильный и исправленный URL

В СРО 9 есть два отдельных файла с одним и тем же тестом:

- неправильный код: [sro9/examples/wrong_url.py](sro9/examples/wrong_url.py)
  — используется `/api/producst/1`, где допущена опечатка `producst`;
- исправленный код: [sro9/examples/correct_url.py](sro9/examples/correct_url.py)
  — используется правильный `/api/products/1`.

Запустить неправильный пример и увидеть ожидаемый `1 failed`:

```bash
python -m pytest -c sro9/pyproject.toml \
  sro9/examples/wrong_url.py \
  --junitxml=sro9/results/before.xml
```

Проверить исправленный пример и увидеть `1 passed`:

```bash
python -m pytest -c sro9/pyproject.toml \
  sro9/examples/correct_url.py \
  --junitxml=sro9/results/after.xml
```

Запустить все тесты СРО 9 и Newman/Postman:

```bash
npm run test:sro9
npm run report:sro9
```

Или напрямую:

```bash
python -m sro9.run_all
```

Ожидаемый результат полного запуска:

```text
pytest: 18 passed
Newman: 21 requests
Assertions: 67
Failures: 0
```

Для ручного показа REST API:

```bash
npm run sro9
```

После запуска открыть <http://127.0.0.1:8009/docs>. Postman-файлы находятся здесь:

- коллекция: [sro9/SRO9.postman_collection.json](sro9/SRO9.postman_collection.json);
- окружение: [sro9/SRO9.postman_environment.json](sro9/SRO9.postman_environment.json);
- pytest-код: [sro9/test_api.py](sro9/test_api.py);
- шесть тест-кейсов: [sro9/test_cases.csv](sro9/test_cases.csv);
- описание и результаты: [sro9/REPORT.md](sro9/REPORT.md),
  [sro9/results/summary.json](sro9/results/summary.json).

### СРО 10: ошибочная реализация и исправное ожидаемое поведение

В СРО 10 отдельные файлы `wrong_url.py` и `correct_url.py` не создавались.
Здесь ошибка находится в рабочем коде веб-приложения:

- ошибочная реализация: [frontend/shop.js](frontend/shop.js);
- тесты исправного ожидаемого поведения: [sro10/test_web.py](sro10/test_web.py),
  тест `test_web13_network_error_message` и тест
  `test_web18_latest_search_wins`;
- описание ошибок: [sro10/BUG_REPORTS.md](sro10/BUG_REPORTS.md).

В [frontend/shop.js](frontend/shop.js) находятся две ошибки:

1. сетевое исключение выводит технический текст `Failed to fetch` вместо
   понятного сообщения пользователю;
2. более старый ответ поиска может заменить результат последнего поиска.

Тесты исправного поведения находятся в [sro10/test_web.py](sro10/test_web.py),
но помечены `strict xfail`, поскольку эти ошибки намеренно оставлены
неисправленными для Bug Report. Поэтому отдельного файла с исправленной
реализацией в СРО 10 сейчас нет: исправный вариант представлен требованиями
и автоматическими тестами.

Запустить обычный полный тест СРО 10:

```bash
npm run test:sro10
```

Или обновить полный отчёт, JUnit, журнал и Word-файл:

```bash
npm run report:sro10
```

Ожидаемый результат:

```text
28 passed, 2 xfailed
```

Показать два дефекта как настоящие падения, отключив `xfail`:

```bash
npm run test:sro10 -- --runxfail -k "web13 or web18"
```

Ожидаемый результат этой демонстрационной команды:

```text
2 failed
```

После демонстрации снова выполнить обычный отчёт:

```bash
npm run report:sro10
```

Важно: команда `npm run report:sro10` после демонстрации снова покажет
`28 passed, 2 xfailed`, потому что в учебной версии два дефекта намеренно
оставлены в [frontend/shop.js](frontend/shop.js). Это не демонстрация
исправленного приложения, а подтверждение открытых Bug Report.

Чтобы показать именно исправленный результат СРО 10, сначала исправьте
[frontend/shop.js](frontend/shop.js), затем уберите `@pytest.mark.xfail(...)`
у тестов `test_web13_network_error_message` и
`test_web18_latest_search_wins` в [sro10/test_web.py](sro10/test_web.py).
После этого запустите:

```bash
npm run test:sro10
npm run report:sro10
```

Ожидаемый результат исправленной версии:

```text
30 passed
```

Для исправления `BUG-10-01` в `api()` нужно преобразовать сетевую ошибку
`fetch` в текст:

```javascript
async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(`./api/shop${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    });
  } catch {
    throw new Error(
      'Желіге қосылу мүмкін болмады. Интернет байланысын тексеріп, қайталап көріңіз.',
    );
  }
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    throw new Error(typeof body.detail === 'string' ? body.detail : 'Деректерді тексеріңіз.');
  }
  return body;
}
```

Для исправления `BUG-10-02` нужно не применять ответ старого поиска.
В [frontend/shop.js](frontend/shop.js) добавьте счётчик запросов:

```javascript
let latestSearch = 0;

async function search() {
  const requestId = ++latestSearch;
  const query = document.querySelector('#query').value;
  const products = await api(`/products?q=${encodeURIComponent(query)}`);
  if (requestId !== latestSearch) return;
  // существующий код обновления #products остаётся ниже без изменений
}
```

После изменения `shop.js` удалите только два `@pytest.mark.xfail(...)`,
сохраните файлы и повторите:

```bash
npm run test:sro10
```

Если код менять не нужно и требуется только показать преподавателю
подготовленный исправный сценарий, используйте тесты как спецификацию:

```bash
npm run test:sro10 -- --runxfail -k "web13 or web18"
```

В текущей версии эта команда ожидаемо выдаёт `2 failed`, потому что приложение
ещё не исправлено. После настоящего исправления и удаления `xfail` те же два
теста должны стать обычными `PASSED`.

Файлы, которые нужно показать по СРО 10:

- основной отчёт: [sro10/REPORT.md](sro10/REPORT.md);
- 20 тест-кейсов: [sro10/TEST_CASES.md](sro10/TEST_CASES.md);
- таблица тест-кейсов: [sro10/test_cases.csv](sro10/test_cases.csv);
- автоматизация Playwright: [sro10/test_web.py](sro10/test_web.py);
- Bug Report: [sro10/BUG_REPORTS.md](sro10/BUG_REPORTS.md);
- итог тестов: [sro10/results/summary.json](sro10/results/summary.json);
- скриншоты: [sro10/results/screenshots/](sro10/results/screenshots/);
- Word-отчёт: [word_reports/Абинсериков Нурасыл АЖ-41 QA СРО-10.docx](word_reports/Абинсериков%20Нурасыл%20АЖ-41%20QA%20СРО-10.docx).

Для ручного показа веб-приложения:

```bash
npm run dev
```

Открыть <http://127.0.0.1:8000/shop.html>, затем в DevTools выбрать
`Network → Fetch/XHR` и показать запросы регистрации, входа, поиска,
расчёта заказа и выхода.

### Короткий сценарий общего показа «ошибка → исправление»

#### СРО 9

Одна команда показывает и неправильный, и исправленный тест:

```bash
npm run report:sro9
```

Файлы, которые запускаются внутри runner:

```text
Ошибка:    sro9/examples/wrong_url.py
Исправлен: sro9/examples/correct_url.py
```

Ожидаемый результат:

```text
wrong_url.py:    1 failed  (неправильный /api/producst/1)
correct_url.py: 1 passed  (правильный /api/products/1)
pytest:          18 passed
Newman:          21 requests, 67 assertions, 0 failures
```

#### СРО 10

В текущей версии два дефекта находятся в [frontend/shop.js](frontend/shop.js).
Сначала показать багнутую версию:

```bash
npm run test:sro10 -- --runxfail -k "web13 or web18"
```

Ожидаемый результат:

```text
2 failed
```

Затем исправить [frontend/shop.js](frontend/shop.js), удалить два декоратора
`@pytest.mark.xfail(...)` у `WEB-13` и `WEB-18` в
[sro10/test_web.py](sro10/test_web.py), и запустить исправленную версию:

```bash
npm run test:sro10
npm run report:sro10
```

Ожидаемый результат:

```text
30 passed
```

Итоговая последовательность команд для показа преподавателю:

```bash
# СРО 9: автоматически ошибка и исправление
npm run report:sro9

# СРО 10: два бага
npm run test:sro10 -- --runxfail -k "web13 or web18"

# СРО 10: после исправления shop.js и удаления xfail
npm run test:sro10
npm run report:sro10
```

Если код СРО 10 не изменять, результатом исправленной версии будет не `30
passed`, а `28 passed, 2 xfailed`: это означает, что два дефекта всё ещё
открыты и зафиксированы в [sro10/BUG_REPORTS.md](sro10/BUG_REPORTS.md).

## Тексеру

```bash
npm test           # барлық corrected Python және SRO tests
npm run check      # build, static, coverage, demo, debugger, lab8 gate
npm run lab10      # нақты Chromium UI және screenshots
npm run lab11      # Locust baseline/load/stress/spike CSV және graph
npm run lab12      # authentication, session, injection, headers tests
npm run build      # 15 report бар dist static build
```

Coverage scope — Python `qa_shop` пакеті; міндетті combined statement/branch threshold **85%**. JUnit, coverage JSON/XML/HTML және quality stage logs [lab15/results](backend/lab15/results/) ішіне жазылады. VS Code pytest discovery және debugging configurations дайын.

## ZAP passive scan

[Official ZAP download](https://www.zaproxy.org/download/) арқылы Linux package орнатыңыз. Осы ортада ZAP 2.17.0 checksum тексеріліп қолданылған; binary Git-ке қосылмайды.

```bash
# ZAP package default path: tools/vendor/ZAP_2.17.0
# Басқа каталог болса ZAP_HOME көрсетіңіз.
node scripts/python.mjs backend/lab12/run_zap.py
npm run lab15      # browser, load, ZAP қоса барлық жергілікті quality stages
```

Scanner өзі ашқан 127.0.0.1 before/after серверлеріне ғана request жібереді және passive scan орындайды. ZAP қорытындысы [Security Report](backend/lab12/REPORT.md) ішінде. Endurance PDF бойынша бөлек жоспар; қысқа Locust run ұзақ SLA ретінде есептелмейді.

## Existing Lab9

```bash
npm ci --prefix backend/lab9 --no-audit --no-fund
npm run lab9
```

[Postman/Newman жинағы](backend/lab9/README.md) 34 DummyJSON scenario береді. Бұл сыртқы API run; негізгі offline pytest/CI-ге тәуелділік емес. Runner finding табылса nonzero exit қайтарады; [нақты нәтижелер](backend/lab9/results/RUN_RESULTS.md) мен [ашық finding](backend/lab9/REPORT.md) жасырылмайды.

## CI және есептер

[labs.yml](.github/workflows/labs.yml) build, tests, static analysis, coverage және Chromium орындайды, reports artifact ретінде сақтайды. [Pages workflow](.github/workflows/pages.yml) quality job өткен соң static portal-ды deploy етеді. Remote execution жаңа commit push/dispatch кезінде орындалады; local run evidence бөлек сақталады.

Әр жұмыстың 20 тапсырмасы [LABS.md](LABS.md) арқылы ашылады. Қорытынды [SUMMARY.md](backend/lab15/results/SUMMARY.md) нақты runner файлдарынан автоматты жасалады. Оқу localhost release-і production deployment readiness-тен бөлек бағаланады.
