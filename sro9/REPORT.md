# СРО №9. REST API тестілеу

Абинсериков Нурасыл, АЖ-41.

## Жұмыстың мақсаты және нәтижесі

REST архитектурасындағы GET, POST, PUT, PATCH және DELETE әдістерін қолдану,
Request/Response құрылымын талдау, Postman және pytest арқылы автоматты тексеру,
қате тестті зерттеу және екі интеграциялық сценарий құру.

Нақты нәтиже: pytest — 18 тест өтті; Newman — 21 сұраныс пен
67 assertion орындалды, қате жоқ. Қате URL мысалында бір тест әдейі
сәтсіз аяқталды; URL түзетілгеннен кейін сол күтіліммен бір тест өтті.
Өлшеу уақыты (UTC): 2026-11-11T03:27:11.847049+00:00.

## Зерттеу нысаны және келісімшарт

Оқу сервисі — [app.py](app.py) ішіндегі жергілікті Products REST API.
Әдепкі адрес: http://127.0.0.1:8009; интерактивті құжаттама: /docs.
Деректер бір сервер процесінің жадында сақталады; сервер қайта іске қосылғанда
бастапқы Keyboard тауары қалпына келеді. Әр pytest тесті бөлек қолданба алады.
Бұл оқу жұмысы үшін бір сервер процесі және сұраныстардың тізбекті орындалуы қолданылады.

Құралдар: python 3.13.5, fastapi 0.115.6, pydantic 2.14.1, pytest 8.3.4, httpx 0.28.1, uvicorn 0.34.0. Postman скрипттері Newman 6.2.1 арқылы орындалды.

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

URI ресурсқа бағытталған: /api/products/{id}. GET және PUT бірдей сұранысты
қайталағанда ресурс күйін қосымша өзгертпейді. DELETE-ті қайталағанда тауар
жойылған күйде қалады, бірақ жауап 204-тен 404-ке ауысуы мүмкін. POST жаңа id
жасайды. Осы API-дегі PATCH нақты мәндерді тағайындайды.

Төмендегі сұраныстар мен жауаптар нақты Newman есебінен алынған:

```http
GET /api/products/1
Accept: application/json

HTTP 200 OK
content-type: application/json

{"name":"Keyboard","price":5000,"stock":10,"id":1}
```

```http
POST /api/products
Accept: application/json
Content-Type: application/json

{"name": "Mouse", "price": 2500, "stock": 5}

HTTP 201 Created
content-type: application/json
location: /api/products/4

{"name":"Mouse","price":2500,"stock":5,"id":4}
```

```http
PUT /api/products/4
Accept: application/json
Content-Type: application/json

{"name": "Monitor", "price": 45000, "stock": 3}

HTTP 200 OK
content-type: application/json

{"name":"Monitor","price":45000,"stock":3,"id":4}
```

```http
PATCH /api/products/5
Accept: application/json
Content-Type: application/json

{"stock": 0}

HTTP 200 OK
content-type: application/json

{"name":"Mouse","price":2500,"stock":0,"id":5}
```

```http
DELETE /api/products/4
Accept: application/json

HTTP 204 No Content

(жауап денесі бос)
```

GET жауабында id, name, price, stock бар. POST-та 201 ресурстың құрылғанын,
Location жаңа ресурс адресін көрсетеді. PUT барлық үш өрісті өзгертеді.
PATCH мысалында stock=0 болады, name пен price сақталады. DELETE жауабында
JSON болмайды, сондықтан 204 үшін response.json() шақырылмайды.

### Postman автоматты Tests скрипті

GET сұранысының Scripts → Post-response (Tests) бөліміндегі нақты скрипт:

```javascript
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("JSON Content-Type", () => {
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
pm.test("Product fields and types", function () {
  const body = pm.response.json();
  pm.expect(body).to.have.all.keys("id", "name", "price", "stock");
  pm.expect(Number.isInteger(body.id) && body.id > 0).to.eql(true);
  pm.expect(body.name).to.be.a("string");
  pm.expect(body.name.length).to.be.within(1, 100);
  pm.expect(Number.isInteger(body.price)).to.eql(true);
  pm.expect(body.price).to.be.within(0, 1000000);
  pm.expect(Number.isInteger(body.stock)).to.eql(true);
  pm.expect(body.stock).to.be.within(0, 1000);
});
pm.test("Expected product values", () => {
  pm.expect(pm.response.json()).to.deep.eql({"id": 1, "name": "Keyboard", "price": 5000, "stock": 10});
});
```

Қалған сұраныстарда да нақты HTTP код, JSON тақырыбы, өрістер және типтер
тексеріледі; 204 жауабында дененің бос болуы тексеріледі.
Интеграциялық папкалар POST-тан келген id-ді collection variable-ға сақтап,
келесі сұраныстарға береді және GET арқылы өзгерістердің сақталғанын тексереді.

## 2-тапсырма. Алты міндетті тест-кейс

Алғышарт: API іске қосылған, id=1 бастапқы тауары бар.
Әр жағдай үшін көрсетілген сұранысты жіберіп, кодты және жауапты тексеру керек.
POST денесінің негізі: {"name":"Mouse","price":2500,"stock":5};
кестеде тек өзгеретін кіріс көрсетілген.

| ID | Санаты | Сұраныс және кіріс | Күтілетін HTTP | Нақты HTTP |
| --- | --- | --- | --- | --- |
| TC01 | Дұрыс | GET /api/products/1; — | 200 | 200 |
| TC02 | Қате | GET /api/products/999999; Жоқ ID | 404 | 404 |
| TC03 | Қате | POST /api/products; price=-1 | 422 | 422 |
| TC04 | Қате | POST /api/products; price="2500" | 422 | 422 |
| TC05 | Шекаралық | POST /api/products; price=0 | 201 | 201 |
| TC06 | Шекаралық | POST /api/products; price=1000000 | 201 | 201 |

Санаттар: 1 дұрыс, 3 қате және 2 шекаралық жағдай.
Барлық алты тесттің күтілетін және нақты нәтижесі сәйкес келді.
TC02 detail хабарламасын, TC03–TC04 price валидациясын, TC05–TC06 шекарадағы
бағаның жауапта өзгермей қайтқанын тексереді. Қате кіріс үшін 422 алу —
тесттің сәтті өтуі, өйткені бұл API келісімшартына сәйкес нәтиже.
Машинамен оқылатын нұсқа: [test_cases.csv](test_cases.csv).

## 3-тапсырма. Python және pytest автоматтандыруы

Нақты іске қосылған [test_api.py](test_api.py) файлының үзіндісі:

```python
"""Six required cases, HTTP method checks and two stateful integration scenarios."""

import pytest
from fastapi.testclient import TestClient
from httpx import Response

BASE = "/api/products"
PRODUCT = {"name": "Mouse", "price": 2500, "stock": 5}


def assert_product(response: Response, status: int = 200) -> dict:
    assert response.status_code == status, response.text
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert set(data) == {"id", "name", "price", "stock"}
    assert type(data["id"]) is int and data["id"] >= 1
    assert type(data["name"]) is str and 1 <= len(data["name"]) <= 100
    assert type(data["price"]) is int and 0 <= data["price"] <= 1_000_000
    assert type(data["stock"]) is int and 0 <= data["stock"] <= 1000
    return data


def test_tc01_valid_get(client: TestClient) -> None:
    assert assert_product(client.get(f"{BASE}/1")) == {
        "id": 1, "name": "Keyboard", "price": 5000, "stock": 10
    }
```

assert_product HTTP кодын, Content-Type, өрістер жиынын, типтерін және мән
диапазондарын тексереді. type(value) is int тексерісі bool мәнін бүтін сан
ретінде қабылдамауға мүмкіндік береді. Қосымша тесттер PUT толықтығын,
PATCH бос денесін, null, bool, белгісіз id өрісін, баға шегінен шығуды және
жоюдың ресурс күйіне әсерін қамтиды. Интеграциялық тесттер өзгерісті GET арқылы оқиды.

```bash
npm run test:sro9
```

Нәтиже: 18 passed. Толық журнал: [pytest.log](results/pytest.log);
JUnit: [pytest.xml](results/pytest.xml).

## 4-тапсырма. Қатені талдау және түзету

Бастапқы тест: [wrong_url.py](examples/wrong_url.py).
Сұраныс: GET /api/producst/1; күтілетін код: 200; нақты код: 404.

```text
AssertionError: {"detail":"Not Found"}
assert 404 == 200
 +  where 404 = <Response [404 Not Found]>.status_code
```

Түпкі себеп: products сөзінде әріптердің орны ауысқан. Серверде
/api/producst/1 маршруты жоқ, сондықтан {"detail":"Not Found"} қайтарады.
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
- PATCH /api/products/{id}: {"stock":0} → 200.
- GET → 200; stock=0, name=Mouse, price=2500 күйінде.
- PATCH сол ресурсқа {"stock":-1} → 422.
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
Newman нәтижесі: 21 сұраныс, 67 assertion, 0 failure.
Бастапқы дәлелдер: [newman.log](results/newman.log),
[newman.json](results/newman.json), [summary.json](results/summary.json).

## Қорытынды

Бес HTTP әдісі орындалды, сұраныс пен жауап құрылымы талданды, алты міндетті
тест-кейс дайындалды. pytest жауап кодтарын, өрістер мен типтерді тексерді.
Қате URL туғызған сәтсіз тест нақты қайталанып, түзетілгеннен кейін өтті.
Екі интеграциялық сценарий деректердің сұраныстар арасында сақталуын және
қате кірістің сақталған күйді өзгертпейтінін растады.
