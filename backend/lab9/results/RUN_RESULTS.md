# Lab 9 — нақты Newman нәтижесі

- API: https://dummyjson.com
- Runner: Newman 6.2.1; iterations: 1; request delay: 300 ms.
- Басталуы (UTC): 2026-10-30T18:45:57.425Z; аяқталуы (UTC): 2026-10-30T18:46:15.570Z.
- Нәтиже: **FAIL**.
- Сценарийлер: **33/34 PASS**, орындалғаны 34, FAIL: 1.
- Assertions: 180; failed: 1; pending: 0.
- Уақыт (ms): min 25; average 183.68; p95 382; max 901.
- Әр жауап үшін шек: < 5000 ms.

| ID | Сценарий | Method | Күтілетін код | Нақты код | Уақыт, ms | Assertions өтті/барлығы | Нәтиже |
|---|---|---|---:|---:|---:|---:|---|
| TC01 | API қолжетімділігі | GET | 200 | 200 | 901 | 5/5 | PASS |
| TC02 | Тауарлар тізімі | GET | 200 | 200 | 229 | 6/6 | PASS |
| TC03 | Бір тауарды алу | GET | 200 | 200 | 53 | 6/6 | PASS |
| TC04 | Іздеу | GET | 200 | 200 | 373 | 6/6 | PASS |
| TC05 | Boundary: limit=1, skip=0 | GET | 200 | 200 | 382 | 5/5 | PASS |
| TC06 | Boundary: skip=1 | GET | 200 | 200 | 132 | 5/5 | PASS |
| TC07 | Boundary: limit=0 | GET | 200 | 200 | 130 | 6/6 | PASS |
| TC08 | Boundary: соңғы жарамды ID | GET | 200 | 200 | 138 | 6/6 | PASS |
| TC09 | Boundary: ID=0 | GET | 404 | 404 | 135 | 5/5 | PASS |
| TC10 | Жоқ ID | GET | 404 | 404 | 321 | 5/5 | PASS |
| TC11 | Қате параметр: мәтіндік ID | GET | 404 | 404 | 183 | 5/5 | PASS |
| TC12 | Бос параметр: q= | GET | 200 | 200 | 168 | 5/5 | PASS |
| TC13 | Boundary: skip=total | GET | 200 | 200 | 130 | 5/5 | PASS |
| TC14 | Boundary: skip=total−1 | GET | 200 | 200 | 344 | 5/5 | PASS |
| TC15 | Boundary: skip=total+1 | GET | 200 | 200 | 268 | 5/5 | PASS |
| TC16 | POST: тауар қосу | POST | 201 | 201 | 187 | 5/5 | PASS |
| TC17 | POST нәтижесі серверде сақталмайды | GET | 404 | 404 | 127 | 5/5 | PASS |
| TC18 | PUT: title және price өзгерту | PUT | 200 | 200 | 126 | 6/6 | PASS |
| TC19 | PATCH: тек price өзгерту | PATCH | 200 | 200 | 124 | 5/5 | PASS |
| TC20 | PUT/PATCH өзгерістері сақталмайды | GET | 200 | 200 | 32 | 5/5 | PASS |
| TC21 | DELETE: тауарды жою | DELETE | 200 | 200 | 131 | 5/5 | PASS |
| TC22 | DELETE нәтижесі серверде сақталмайды | GET | 200 | 200 | 25 | 5/5 | PASS |
| TC23 | PUT: жоқ ресурс | PUT | 404 | 404 | 158 | 5/5 | PASS |
| TC24 | PATCH: жоқ ресурс | PATCH | 404 | 404 | 140 | 5/5 | PASS |
| TC25 | DELETE: жоқ ресурс | DELETE | 404 | 404 | 134 | 5/5 | PASS |
| TC26 | POST: бүлінген JSON | POST | 400 | 400 | 127 | 5/5 | PASS |
| TC27 | Токен жоқ | GET | 401 | 401 | 136 | 6/6 | PASS |
| TC28 | Жарамсыз Bearer токен | GET | 401 | 401 | 124 | 5/5 | PASS |
| TC29 | Қате құпиясөз | POST | 400 | 400 | 131 | 6/6 | PASS |
| TC30 | Бос логин және пароль | POST | 400 | 400 | 125 | 5/5 | PASS |
| TC31 | Міндетті password параметрі жоқ | POST | 400 | 400 | 146 | 5/5 | PASS |
| TC32 | Дұрыс логин: токен алу | POST | 200 | 200 | 131 | 6/6 | PASS |
| TC33 | Жарамды токенмен профиль алу | GET | 200 | 200 | 127 | 5/6 | FAIL |
| TC34 | Қорғалған тауарлар тізімі | GET | 200 | 200 | 127 | 5/5 | PASS |

## Қателер

- TC33 — Жарамды токенмен профиль алу: Пароль жауапта жоқ: expected { id: 1, firstName: 'Emily', …(26) } to not have property 'password'

## Нәтижені түсіндіру

400/401/404 күтілетін теріс сценарийлерде PASS — дұрыс нәтиже. API жазу операцияларын имитациялайды; деректердің сақталмауы TC17/TC20/TC22 арқылы тексерілген.

Бұл нақты Newman іске қосылуы. Postman GUI Collection Runner осы ортада орындалмады; GUI арқылы қайталау қадамдары [README.md](../README.md) ішінде. Бір итерация өнімділік немесе қолжетімділік SLA-ын дәлелдемейді.

Әр assertion, response body және таңдалған response headers [newman-results.json](newman-results.json) ішінде. Токендер мен құпиясөздер жасырылған.
