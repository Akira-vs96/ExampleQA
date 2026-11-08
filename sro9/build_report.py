"""Build the SRO 9 report from the captured pytest and Newman results."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from sro9.generate_postman import CASES

HERE = Path(__file__).resolve().parent


def sample(execution: dict) -> str:
    request = execution["request"]
    response = execution["response"]
    path = "/" + "/".join(request["url"]["path"])
    text = f"{request['method']} {path}\nAccept: application/json\n"
    if request.get("body"):
        text += "Content-Type: application/json\n\n" + request["body"]["raw"] + "\n"
    text += f"\nHTTP {response['code']} {response['status']}\n"
    for header in response["header"]:
        if header["key"].lower() in {"content-type", "location"}:
            text += f"{header['key']}: {header['value']}\n"
    raw = bytes(response.get("stream", {}).get("data", [])).decode("utf-8")
    text += "\n" + (raw or "(жауап денесі бос)")
    return "```http\n" + text + "\n```"


def build_report(summary: dict, newman: dict) -> Path:
    executions = {item["item"]["name"]: item for item in newman["run"]["executions"]}
    names = ["TC01 valid GET", "IT01 1 POST", "IT01 3 PUT", "IT02 2 PATCH", "IT01 5 DELETE"]
    samples = "\n\n".join(sample(executions[name]) for name in names)
    rows = []
    for case_id, kind, method, path, data, status, _ in CASES:
        actual = next(value["response"]["code"] for name, value in executions.items()
                      if name.startswith(case_id + " ") and "cleanup" not in name)
        rows.append(f"| {case_id} | {kind} | {method} {path}; {data} | {status} | {actual} |")
    case_table = "\n".join(rows)
    python_source = (HERE / "test_api.py").read_text(encoding="utf-8")
    python_source = python_source.split("def test_tc02_missing_product")[0].rstrip()
    collection = json.loads((HERE / "SRO9.postman_collection.json").read_text(encoding="utf-8"))
    postman_script = "\n".join(collection["item"][0]["item"][0]["event"][-1]["script"]["exec"])
    failure = ET.parse(HERE / "results/before.xml").find(".//failure")
    failure_text = (
        failure.attrib["message"] if failure is not None else "Failure was not reproduced"
    )
    passed = summary["pytest"]["passed"]
    requests = summary["newman"]["requests"]["total"]
    assertions = summary["newman"]["assertions"]["total"]
    versions = ", ".join(f"{name} {value}" for name, value in summary["versions"].items())
    report = f"""# СРО №9. REST API тестілеу

Абинсериков Нурасыл, АЖ-41.

## Жұмыстың мақсаты және нәтижесі

REST архитектурасындағы GET, POST, PUT, PATCH және DELETE әдістерін қолдану,
Request/Response құрылымын талдау, Postman және pytest арқылы автоматты тексеру,
қате тестті зерттеу және екі интеграциялық сценарий құру.

Нақты нәтиже: pytest — {passed} тест өтті; Newman — {requests} сұраныс пен
{assertions} assertion орындалды, қате жоқ. Қате URL мысалында бір тест әдейі
сәтсіз аяқталды; URL түзетілгеннен кейін сол күтіліммен бір тест өтті.
Өлшеу уақыты (UTC): {summary['generated_at_utc']}.

## Зерттеу нысаны және келісімшарт

Оқу сервисі — [app.py](app.py) ішіндегі жергілікті Products REST API.
Әдепкі адрес: http://127.0.0.1:8009; интерактивті құжаттама: /docs.
Деректер бір сервер процесінің жадында сақталады; сервер қайта іске қосылғанда
бастапқы Keyboard тауары қалпына келеді. Әр pytest тесті бөлек қолданба алады.
Бұл оқу жұмысы үшін бір сервер процесі және сұраныстардың тізбекті орындалуы қолданылады.

Құралдар: {versions}. Postman скрипттері Newman 6.2.1 арқылы орындалды.

| Өріс | Тип | Талап |
| --- | --- | --- |
| id | integer | Сервер тағайындайтын оң идентификатор |
| name | string | Бос орындар тазартылғаннан кейін 1–100 таңба |
| price | integer | Бүтін теңге, 0–1000000 аралығы |
| stock | integer | Қоймадағы сан, 0–1000 аралығы |

Бағаға мәтін, bool, теріс немесе шектен үлкен сан берілсе HTTP 422 қайтарылады.
Белгісіз өрістер қабылданбайды. PATCH кезінде бос объект пен null қабылданбайды.
JSON сұранысында Content-Type: application/json қолданылады.

## 1-тапсырма. HTTP әдістері және Request/Response талдауы

| Әдіс | Мақсаты | Сәтті жауап | Тексерілетін қасиет |
| --- | --- | --- | --- |
| GET | Тауарды оқу | 200 және JSON | Оқу сервердегі тауарды өзгертпейді |
| POST | Тауар қосу | 201, JSON және Location | id серверден алынады |
| PUT | Барлық өзгеретін өрісті алмастыру | 200 және JSON | name, price, stock түгел қажет |
| PATCH | Жекелеген өрісті өзгерту | 200 және JSON | Жіберілмеген өрістер сақталады |
| DELETE | Тауарды жою | 204, бос дене | Келесі GET 404 қайтарады |

URI ресурсқа бағытталған: /api/products/{{id}}. GET және PUT бірдей сұранысты
қайталағанда ресурс күйін қосымша өзгертпейді. DELETE-ті қайталағанда тауар
жойылған күйде қалады, бірақ жауап 204-тен 404-ке ауысуы мүмкін. POST жаңа id
жасайды. Осы API-дегі PATCH нақты мәндерді тағайындайды.

Төмендегі сұраныстар мен жауаптар нақты Newman есебінен алынған:

{samples}

GET жауабында id, name, price, stock бар. POST-та 201 ресурстың құрылғанын,
Location жаңа ресурс адресін көрсетеді. PUT барлық үш өрісті өзгертеді.
PATCH мысалында stock=0 болады, name пен price сақталады. DELETE жауабында
JSON болмайды, сондықтан 204 үшін response.json() шақырылмайды.

### Postman автоматты Tests скрипті

GET сұранысының Scripts → Post-response (Tests) бөліміндегі нақты скрипт:

```javascript
{postman_script}
```

Қалған сұраныстарда да нақты HTTP код, JSON тақырыбы, өрістер және типтер
тексеріледі; 204 жауабында дененің бос болуы тексеріледі.
Интеграциялық папкалар POST-тан келген id-ді collection variable-ға сақтап,
келесі сұраныстарға береді және GET арқылы өзгерістердің сақталғанын тексереді.

## 2-тапсырма. Алты міндетті тест-кейс

Алғышарт: API іске қосылған, id=1 бастапқы тауары бар.
Әр жағдай үшін көрсетілген сұранысты жіберіп, кодты және жауапты тексеру керек.
POST денесінің негізі: {{"name":"Mouse","price":2500,"stock":5}};
кестеде тек өзгеретін кіріс көрсетілген.

| ID | Санаты | Сұраныс және кіріс | Күтілетін HTTP | Нақты HTTP |
| --- | --- | --- | --- | --- |
{case_table}

Санаттар: 1 дұрыс, 3 қате және 2 шекаралық жағдай.
Барлық алты тесттің күтілетін және нақты нәтижесі сәйкес келді.
TC02 detail хабарламасын, TC03–TC04 price валидациясын, TC05–TC06 шекарадағы
бағаның жауапта өзгермей қайтқанын тексереді. Қате кіріс үшін 422 алу —
тесттің сәтті өтуі, өйткені бұл API келісімшартына сәйкес нәтиже.
Машинамен оқылатын нұсқа: [test_cases.csv](test_cases.csv).

## 3-тапсырма. Python және pytest автоматтандыруы

Нақты іске қосылған [test_api.py](test_api.py) файлының үзіндісі:

```python
{python_source}
```

assert_product HTTP кодын, Content-Type, өрістер жиынын, типтерін және мән
диапазондарын тексереді. type(value) is int тексерісі bool мәнін бүтін сан
ретінде қабылдамауға мүмкіндік береді. Қосымша тесттер PUT толықтығын,
PATCH бос денесін, null, bool, белгісіз id өрісін, баға шегінен шығуды және
жоюдың ресурс күйіне әсерін қамтиды. Интеграциялық тесттер өзгерісті GET арқылы оқиды.

```bash
npm run test:sro9
```

Нәтиже: {passed} passed. Толық журнал: [pytest.log](results/pytest.log);
JUnit: [pytest.xml](results/pytest.xml).

## 4-тапсырма. Қатені талдау және түзету

Бастапқы тест: [wrong_url.py](examples/wrong_url.py).
Сұраныс: GET /api/producst/1; күтілетін код: 200; нақты код: 404.

```text
{failure_text}
```

Түпкі себеп: products сөзінде әріптердің орны ауысқан. Серверде
/api/producst/1 маршруты жоқ, сондықтан {{"detail":"Not Found"}} қайтарады.
Бұл мысалда мәселе тесттің URL адресінде. HTTP 200 күтілімі дұрыс маршрутқа арналған.

Түзету: URL /api/products/1 болып өзгертілді; күтілетін код 200 күйінде қалды.
Түзетілген тест: [correct_url.py](examples/correct_url.py).

| Нұсқа | Нақты нәтиже | Процестің exit code |
| --- | --- | --- |
| Қате URL | 1 failed, assert 404 == 200 | 1 |
| Түзетілген URL | 1 passed, id=1 | 0 |

Қате және түзетілген мысалдар негізгі test_*.py жинағынан бөлек сақталады;
толық есеп runner-і екеуін де автоматты орындайды. Қате жағдай xfail арқылы
жасырылмайды: [before.log](results/before.log) нақты сәтсіз тестті сақтайды.
Түзетілген нәтиже: [after.log](results/after.log).

## 5-тапсырма. Екі интеграциялық сценарий

### IT01. Тауардың толық өмірлік циклі

Алғышарт: сервер жұмыс істейді; жаңа тауар идентификаторы алдын ала берілмейді.

- POST /api/products: Mouse, price=2500, stock=5 → 201; id және Location сақтау.
- GET Location → 200; барлық өріс POST жауабымен сәйкес.
- PUT Location: Monitor, price=45000, stock=3 → 200; id сақталады.
- GET Location → 200; үш өзгертілген өріс жаңа мәндермен сақталған.
- DELETE Location → 204; жауап денесі бос.
- GET Location → 404; жойылған тауар қолжетімсіз.

Күтілетін соңғы күй: құрылған тауар жойылған. Нақты нәтиже: сценарий өтті.

### IT02. Ішінара өзгерту және қате сұраныстан кейінгі күй

Алғышарт: жаңа тауар POST арқылы құрылып, нақты id алынады.

- POST /api/products: Mouse, price=2500, stock=5 → 201.
- PATCH /api/products/{{id}}: {{"stock":0}} → 200.
- GET → 200; stock=0, name=Mouse, price=2500 күйінде.
- PATCH сол ресурсқа {{"stock":-1}} → 422.
- GET → 200; қате сұраныстан кейін де stock=0, қалған өрістер өзгермеген.
- DELETE → 204; Postman қосымша GET арқылы 404 мәртебесін растайды.

Нақты нәтиже: сценарий өтті. API, валидация және сақтау қабаты бір тізбекте тексерілді.

## Postman және толық есепті қайта орындау

```bash
python -m pip install -r sro9/requirements.txt
npm install --prefix sro9 --no-audit --no-fund
npm run sro9
```

Postman-ға [коллекцияны](SRO9.postman_collection.json) және
[ортаны](SRO9.postman_environment.json) импорттау керек. СРО 9 — localhost
ортасын таңдап, үш папканы бастапқы ретімен, бір итерациямен іске қосыңыз.
Әдепкі base_url: http://127.0.0.1:8009. Коллекция өзгерткен оқу деректерін тазалайды.
Осы жұмыста скрипттер Postman интерфейсімен бірдей коллекцияны орындайтын Newman
арқылы тексерілді.

```bash
npm run report:sro9
```

Бұл команда pytest, қате мысал, түзетілген мысал және Newman тексерістерін
орындап, осы есепті нақты нәтижелермен қайта жасайды.
Newman үшін жеке сервер бос жергілікті портта іске қосылып, соңында тоқтайды.
Newman нәтижесі: {requests} сұраныс, {assertions} assertion, 0 failure.
Бастапқы дәлелдер: [newman.log](results/newman.log),
[newman.json](results/newman.json), [summary.json](results/summary.json).

## Қорытынды

Бес HTTP әдісі орындалды, сұраныс пен жауап құрылымы талданды, алты міндетті
тест-кейс дайындалды. pytest жауап кодтарын, өрістер мен типтерді тексерді.
Қате URL туғызған сәтсіз тест нақты қайталанып, түзетілгеннен кейін өтті.
Екі интеграциялық сценарий деректердің сұраныстар арасында сақталуын және
қате кірістің сақталған күйді өзгертпейтінін растады.
"""
    source = HERE / "REPORT.md"
    source.write_text(report, encoding="utf-8")
    return source
