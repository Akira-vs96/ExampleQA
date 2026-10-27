# 9-зертханалық жұмыс есебі

**Тақырып:** REST API-ді Postman арқылы функционалдық және теріс сценарийлермен тестілеу.

**Мақсаты:** API documentation зерттеу; GET, POST, PUT, PATCH, DELETE сұраныстарын
орындау; жауап кодын, body, headers, authentication және response time тексеру;
кемінде 20 сценарийден тұратын Postman Collection дайындау.

**Тексеру күні:** 27.10.2026. **Орта:** HTTPS, Node.js 20.19.2, Newman 6.2.1.

**Нәтиже:** 34 сценарий орындалды; **33 PASS, 1 FAIL**. 180 assertion ішінен
179 өтті. Жалғыз FAIL — профиль жауабында `password` өрісінің болуы.

## 1. REST API таңдау

[DummyJSON](https://dummyjson.com/) — тестілеуге арналған ашық REST API.
Негізгі URL: `https://dummyjson.com`. Тауарлар мен пайдаланушы профилі таңдалды:
олар қажетті бес HTTP әдісін, пагинацияны және Bearer authentication тексеруді қамтиды.
API key, тіркелу немесе жеке деректер қажет емес.

## 2. API documentation зерттеу

Ресми құжаттама:

- [Introduction](https://dummyjson.com/docs): pagination, `limit=0`, қорғалған ресурстар.
- [Products](https://dummyjson.com/docs/products): тізім, ID, іздеу, select, POST, PUT/PATCH, DELETE.
- [Authentication](https://dummyjson.com/docs/auth): login, accessToken, refreshToken, `/auth/me`.

Request және response форматы — JSON. Query параметрлері: `limit`, `skip`,
`select`, `q`. `limit=0` шектеуді алып тастап, барлық жазбаны қайтарады.
Қорғалған сұраныс `Authorization: Bearer <accessToken>` қолданады.
Login токендерді JSON-да және cookie-де қайтарады.

Құжаттама POST/PUT/PATCH/DELETE өзгерістерінің **имитация** екенін ескертеді:
сервердегі деректер сақталмайды. DummyJSON PUT жіберілген өрістерді жаңартады;
бұл мінез-құлықты барлық REST API-ге ортақ толық ауыстыру шарты деп қабылдамаймыз.

### Swagger UI және ReDoc арқылы көрсету

Backend іске қосылғанда зертхананың екі құжаттама беті қолжетімді:

- [Swagger UI](http://localhost:8000/lab9/docs) — endpoint таңдау,
  **Try it out → Execute** арқылы сұраныс жіберу, status/body/headers қарау.
- [ReDoc](http://localhost:8000/lab9/redoc) — endpoint сипаттамаларын,
  параметрлерін және request/response схемаларын оқу.

Жоба түбірінен backend іске қосу:

```bash
cd backend
./.venv/bin/uvicorn main:app --reload --port 8000
```

Екі бет те [DummyJSON OpenAPI](https://dummyjson.com/openapi.json) схемасын
жүктейді. Swagger сұраныстары тікелей `https://dummyjson.com` адресіне жіберіледі;
бұл беттер жергілікті CRUD серверін жасамайды. Құжаттаманы жүктеу және
API-ге сұраныс жіберу үшін интернет керек. Мысал көрсету үшін Swagger-де
`GET /products/{id}` ашып, `id=1` енгізіңіз және **Execute** басыңыз.

Жобаның өз API құжаттамасы бөлек:
[/docs](http://localhost:8000/docs) және [/redoc](http://localhost:8000/redoc).
Swagger/ReDoc интерфейстері 34 Postman сценарийін автоматты орындамайды;
олардың assertions нәтижесі Newman есебінде берілген.

## 3. Endpoint тізімі

| Method | Endpoint | Мақсаты | Тексерілген status |
|---|---|---|---|
| GET | `/test` | API қолжетімділігі | 200 |
| GET | `/products` | Тізім, pagination, select | 200 |
| GET | `/products/{id}` | Бір тауар | 200 немесе 404 |
| GET | `/products/search?q=...` | Іздеу | 200 |
| POST | `/products/add` | Тауар қосуды имитациялау | 201 немесе 400 |
| PUT | `/products/{id}` | Жіберілген өрістерді жаңарту | 200 немесе 404 |
| PATCH | `/products/{id}` | Ішінара жаңарту | 200 немесе 404 |
| DELETE | `/products/{id}` | Жоюды имитациялау | 200 немесе 404 |
| POST | `/auth/login` | Кіру және токен алу | 200 немесе 400 |
| GET | `/auth/me` | Қорғалған профиль | 200 немесе 401 |
| GET | `/auth/products` | Қорғалған тауарлар | 200 |

Барлық 34 сұраныстың нақты параметрлері мен expected status мәндері
[SCENARIOS.md](SCENARIOS.md) кестесінде берілген.

## 4. GET сұранысын орындау

TC03: `GET {{baseUrl}}/products/1` → **200 OK**.
Нақты жауаптың негізгі өрістері:

```json
{
  "id": 1,
  "title": "Essence Mascara Lash Princess",
  "price": 9.99,
  "stock": 99
}
```

ID, өріс типтері және JSON Schema тексерілді. `title` мен `price` айнымалыларға
сақталып, кейін жаңарту имитациясын тексеруге қолданылды.

## 5. POST сұранысын орындау

TC16: `POST {{baseUrl}}/products/add`, `Content-Type: application/json`.

```json
{"title": "Lab9 Test Product", "price": 29.99, "stock": 10}
```

Нақты status — **201 Created**, body-де `id=195` және барлық жіберілген өріс бар.
Жаңа ID статикалық жазылмай, response-тан алынады. TC17 сол ID үшін GET
орындап, **404** алды: бұл құжаттамадағы сақталмайтын POST имитациясына сәйкес.

## 6. PUT сұранысын орындау

TC18: `PUT {{baseUrl}}/products/1`.

```json
{"title": "Lab9 PUT Product", "price": 49.99}
```

Нәтиже: **200**, `id=1`, `title="Lab9 PUT Product"`, `price=49.99`.
Product schema және өзгерген мәндер тексерілді. Жоқ ресурсқа PUT — TC23, **404**.

## 7. PATCH сұранысын орындау

TC19: `PATCH {{baseUrl}}/products/1`.

```json
{"price": 19.99}
```

Нәтиже: **200**, `price=19.99`; жіберілмеген `title` бастапқы мәнінде қалды.
TC20 тәуелсіз GET орындап, бастапқы `price=9.99` және `title` сақталғанын
растады: PUT/PATCH операциялары деректерді тұрақты өзгертпейді.

## 8. DELETE сұранысын орындау

TC21: `DELETE {{baseUrl}}/products/1` → **200**. Нақты жауапта `id=1`,
`isDeleted=true`, `deletedOn="2026-10-27T12:15:28.234Z"` бар.
Күн мәні алдын ала бекітілмейді, date ретінде оқылуы тексеріледі.
TC22 кейінгі GET арқылы тауардың әлі бар екенін растады. Жоқ ресурсқа
DELETE — TC25, **404**. DummyJSON бұл сұраныста 204 емес, JSON body бар 200 қайтарады.

## 9. Status Code тексеру

Әр сценарийде нақты күтілетін кодқа жеке assertion бар:

```javascript
pm.test("HTTP 201", function () {
  pm.response.to.have.status(201);
});
```

| Код | Осы зертханадағы мәні |
|---:|---|
| 200 | GET, PUT, PATCH, DELETE және дұрыс login сәтті орындалды |
| 201 | POST арқылы имитациялық тауар жасалды |
| 400 | JSON бұзылған, credentials қате немесе міндетті параметр жоқ |
| 401 | Қорғалған endpoint үшін токен жоқ немесе жарамсыз |
| 404 | Тауар жоқ немесе ID жарамсыз |

34 сұраныстың барлығында нақты status күтілетін мәнге сәйкес болды.
Теріс сценарийде күтілетін 400/401/404 алу — PASS.

## 10. Response Body тексеру

Барлық жауап JSON ретінде оқылады. Сценарийге қарай `id`, `title`, `price`,
`stock`, массив ұзындығы, `total`, `limit`, `skip`, error `message`, JWT және
жою белгілері тексеріледі. Product JSON Schema міндетті өрістерді және
сандық/мәтіндік типтерді тексереді; `price` және `stock` теріс болмауы тиіс.

Профильде пароль болмауы туралы **QA-SEC-01** қосымша сапа критерийі TC33-де
тексерілді. Бұл — зертхана енгізген қауіпсіздік талабы; ресми documentation
`password` өрісін міндетті алып тастауға уәде бермейді. Осы тексеріс FAIL берді.

## 11. Header тексеру

Сұраныстарда `Accept: application/json`, JSON body бар сұраныстарда қосымша
`Content-Type: application/json` орнатылды. Нақты жауаптарда
`Content-Type: application/json; charset=utf-8` алынды.

Коллекциядағы ортақ assertion:

```javascript
pm.test("Header: Content-Type = JSON", function () {
  pm.expect(pm.response.headers.get("Content-Type"))
    .to.match(/^application\/json\b/i);
});
```

Параметрі бар Content-Type қабылданады; барлық 34 header тексерісі өтті.
Сақталған JSON нәтижесінде `content-type`, `date`, `etag` және rate-limit
headers бар. Authorization header-дің жұмысы бөлек auth сценарийлерімен тексерілді.

## 12. Authentication тексеру

Ресми құжаттамадағы ашық demo account: `username=emilys`, `password=emilyspass`.
TC32 `POST /auth/login` арқылы `expiresInMins=30` жіберіп, **200**, accessToken
және refreshToken алды. Access token collection variable ретінде автоматты сақталды:

```javascript
pm.collectionVariables.set("accessToken", responseData.accessToken);
```

TC33 және TC34 `Authorization: Bearer {{accessToken}}` қолданды: екеуі де **200**.
TC33 пайдаланушының ID және username мәндерін login жауабымен салыстырды.
TC27 токенсіз — **401**; TC28 жарамсыз токенмен — **401**; TC29 қате парольмен —
**400**, accessToken берілмеді. Бұл кодтар DummyJSON мінез-құлқына сай таңдалды.

Cookie jar барлық сұраныста өшірілген. Нәтиже файлдарында токендер, парольдер
және cookies сақталмайды; сезімтал өрістер `[REDACTED]` болып ауыстырылады.
TC33-де парольдің **мәні емес, өрісінің бар болуы** тіркелді.

## 13. Қате параметр жіберу

TC11: `GET /products/abc` → **404**, body-де бос емес `message` бар.
TC26: `POST /products/add` ішінде аяқталмаған `{"title":` жіберілді → **400**,
`message="Unexpected end of JSON input"`.
TC29 қате password жібергенде **400**, `message="Invalid credentials"` алды.
Бұл сценарийлер ID, JSON синтаксисі және authentication қателерін бөлек қамтиды.

## 14. Бос параметр жіберу

TC12: `q=` бос іздеу жолы → **200** және толық жиыннан 5 тауар.
Бос жол бұл endpoint үшін жарамды; қате кодты жасанды түрде күтпейміз.
TC30: `{"username":"","password":""}` → **400**,
`message="Username and password required"`.
TC31: body-де password мүлде жоқ → **400**, сол message.
Бос query, бос міндетті мән және жоқ параметр бөлек тексерілді.

## 15. Boundary мәндерін жіберу

| Сценарий | Шекара | Нақты нәтиже |
|---|---|---|
| TC05 | `limit=1`, `skip=0` | 200, бірінші бір жазба |
| TC06 | `skip=1` | 200, келесі жазба |
| TC07 | `limit=0` | 200, барлық 194 ID |
| TC08 | Соңғы жарамды ID — 194 | 200 |
| TC09 | ID=0 | 404 |
| TC10 | Жоқ ID — 100194 | 404 |
| TC13 | `skip=total`, осы іске қосуда 194 | 200, бос массив |
| TC14 | `skip=total−1`, осы іске қосуда 193 | 200, соңғы бір жазба |
| TC15 | `skip=total+1`, осы іске қосуда 195 | 200, бос массив |

194 — өлшенген жиын мөлшері, API-дің тұрақты техникалық максимумы емес.
Коллекция `total`, нақты максималды ID және offset мәндерін әр іске қосуда
қайта есептейді. `limit=0` бос page емес, барлық жазбаны алу екенін тексереді.

## 16. Response Time өлшеу

Newman әр жауаптың клиент жағындағы уақытын миллисекундпен өлшеді.
Оқу критерийі: **әр жауап < 5000 ms**; environment арқылы өзгертіледі.

| Метрика | Нақты мән |
|---|---:|
| Сұраныс саны | 34 |
| Minimum | 23 ms |
| Average | 189.68 ms |
| p95, nearest rank | 391 ms |
| Maximum | 503 ms |
| Уақыт шегінен асқан жауап | 0 |

Бұл бір итерациядағы HTTPS уақыты; желі, TLS және кэш әсер етуі мүмкін.
Нәтиже жүктемелік тест немесе сервистің SLA кепілдігі болып саналмайды.

## 17. Postman Collection жасау

[Lab9_DummyJSON.postman_collection.json](Lab9_DummyJSON.postman_collection.json)
Postman Collection v2.1 форматында жасалды. Төрт папкада 34 бөлек request бар:
GET/пагинация, теріс/шекаралық мәндер, жазу әдістері, authentication.

[Environment](Lab9_DummyJSON.postman_environment.json) ішінде `baseUrl`,
`username`, `password`, `maxResponseTimeMs` сақталған. Бос collection variables
runtime кезінде есептеледі: accessToken, userId, total, firstId, lastId,
missingId, lastOffset, beyondOffset, originalTitle, originalPrice, createdId.
Толық коллекция TC01–TC34 ретімен іске қосылады.

## 18. Assertions қосу

Коллекция деңгейінде әр жауапқа үш ортақ тексеріс қосылған: Content-Type,
JSON жарамдылығы және уақыт. Request деңгейінде нақты status және сценарийге
сәйкес body/schema тексерістері қосылған. Нақты орындалғаны — **180 assertion**.

```javascript
pm.test("Response Time < maxResponseTimeMs", function () {
  pm.expect(pm.response.responseTime)
    .to.be.below(Number(pm.environment.get("maxResponseTimeMs")));
});

pm.test("price өзгерді, title сақталды", function () {
  pm.expect(responseData.id).to.eql(1);
  pm.expect(responseData.price).to.eql(19.99);
  pm.expect(responseData.title)
    .to.eql(pm.collectionVariables.get("originalTitle"));
});

pm.test("Пароль жауапта жоқ", function () {
  pm.expect(responseData).not.to.have.property("password");
});
```

Соңғы тексеріс әдейі өшірілген жоқ: анықталған сапа мәселесін көрсетеді.

## 19. Collection Runner арқылы орындау

Нақты автоматты іске қосу **Newman 6.2.1** арқылы орындалды. Бұл Postman
Collection-ды командалық жолдан орындайтын runner; Postman GUI нәтижесі деп
көрсетілмейді. Параметрлер: **1 iteration, delay 300 ms, request timeout 15000 ms**.

Жоба түбіріндегі командалар:

```bash
npm ci --prefix backend/lab9 --no-audit --no-fund
npm run lab9
```

Нақты іске қосу: **2026-10-27 12:15:17–12:15:35 UTC**
(Asia/Almaty: **17:15:17–17:15:35**, UTC+5).
Барлық 34 HTTP сұранысы орындалды; transport және script қателері жоқ.
Жалғыз assertion қатесіне байланысты process exit code — **1**.

Postman GUI-де қайталау: екі JSON файлды Import жасау → environment таңдау →
Run collection → барлық 34 request → Iterations 1, Delay 300 → Run.
Толық қадамдар [README.md](README.md) ішінде. GUI осы ортада іске қосылған жоқ.

## 20. API тестілеу есебі

| Көрсеткіш | Нәтиже |
|---|---:|
| Сценарий жоспарланған / орындалған | 34 / 34 |
| PASS / FAIL | 33 / 1 |
| Assertions орындалған / өткен / өтпеген | 180 / 179 / 1 |
| HTTP status сәйкестігі | 34 / 34 |
| Content-Type тексерісі | 34 / 34 |
| JSON жарамдылығы | 34 / 34 |
| Response Time шегі | 34 / 34 |
| Transport / script errors | 0 / 0 |

Әр сценарийдің нақты status, уақыт және assertion саны
[RUN_RESULTS.md](results/RUN_RESULTS.md) ішінде. Толық body, таңдалған headers
және әрбір assertion нәтижесі [newman-results.json](results/newman-results.json)
файлында сақталған. Қайта іске қосу осы нәтижелерді жаңартады; бұл бөлімнің
сандық мәндері 27.10.2026 күнгі көрсетілген іске қосуға тиесілі.

### LAB9-01 Профиль жауабында password өрісі бар

| Өріс | Мәні |
|---|---|
| Сценарий | TC33 |
| Талап | QA-SEC-01: профиль API жауабында password болмауы тиіс |
| Қадамдар | Дұрыс login → accessToken алу → `GET /auth/me` Bearer токенмен |
| Күтілетін | 200, дұрыс профиль, password өрісінсіз |
| Нақты | 200, дұрыс профиль, `password` өрісі бар |
| Дәлел | JSON есебінде TC33 body: `"password": "[REDACTED]"`; assertion FAIL |
| Баға | Оқу API-інің production үлгісіне жарамсыз шектеуі; нақты жеке аккаунттың құпиясы табылған жоқ |
| Ұсыныс | Response DTO-да рұқсат етілген профиль өрістерін ғана қайтару; password-ты алып тастау |
| Статус | Анықталды; сыртқы API коды бұл жобада түзетілмейді |

DummyJSON пайдаланушылары мен демо парольдері ашық тест деректері.
Сондықтан бұл нәтиже нақты пайдаланушы құпиясының жарияланғанын немесе
documentation шартының бұзылғанын білдірмейді. Ол зертхананың қосымша
қауіпсіздік критерийінен ауытқуды көрсетеді.

## Қорытынды

20 тапсырмаға арналған материалдар дайындалды: API зерттелді, endpoint тізімі
жасалды, бес HTTP әдісі нақты орындалды, status/body/header/authentication,
қате/бос/boundary мәндер және уақыт тексерілді. Ұсынылған Postman Collection
**34 тестілік сценарийден** тұрады. Нақты Newman нәтижесі — **33/34 сценарий,
179/180 assertion PASS**; пароль өрісіне қатысты бір сапа мәселесі тіркелді.
