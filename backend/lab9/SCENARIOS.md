# Lab 9 — 34 тестілік сценарий

Әр жол — бөлек HTTP сұранысы. Әр сұраныста қосымша Content-Type, JSON және уақыт assertions орындалады.

| ID | Method | Endpoint | Тексеру | Күтілетін HTTP |
|---|---|---|---|---:|
| TC01 | GET | `/test` | API қолжетімділігі | 200 |
| TC02 | GET | `/products?limit=10&skip=0` | Тауарлар тізімі | 200 |
| TC03 | GET | `/products/1` | Бір тауарды алу | 200 |
| TC04 | GET | `/products/search?q=phone&limit=5` | Іздеу | 200 |
| TC05 | GET | `/products?limit=1&skip=0` | Boundary: limit=1, skip=0 | 200 |
| TC06 | GET | `/products?limit=1&skip=1` | Boundary: skip=1 | 200 |
| TC07 | GET | `/products?limit=0&select=id` | Boundary: limit=0 | 200 |
| TC08 | GET | `/products/{{lastId}}` | Boundary: соңғы жарамды ID | 200 |
| TC09 | GET | `/products/0` | Boundary: ID=0 | 404 |
| TC10 | GET | `/products/{{missingId}}` | Жоқ ID | 404 |
| TC11 | GET | `/products/abc` | Қате параметр: мәтіндік ID | 404 |
| TC12 | GET | `/products/search?q=&limit=5` | Бос параметр: q= | 200 |
| TC13 | GET | `/products?limit=1&skip={{total}}` | Boundary: skip=total | 200 |
| TC14 | GET | `/products?limit=1&skip={{lastOffset}}` | Boundary: skip=total−1 | 200 |
| TC15 | GET | `/products?limit=1&skip={{beyondOffset}}` | Boundary: skip=total+1 | 200 |
| TC16 | POST | `/products/add` | POST: тауар қосу | 201 |
| TC17 | GET | `/products/{{createdId}}` | POST нәтижесі серверде сақталмайды | 404 |
| TC18 | PUT | `/products/1` | PUT: title және price өзгерту | 200 |
| TC19 | PATCH | `/products/1` | PATCH: тек price өзгерту | 200 |
| TC20 | GET | `/products/1` | PUT/PATCH өзгерістері сақталмайды | 200 |
| TC21 | DELETE | `/products/1` | DELETE: тауарды жою | 200 |
| TC22 | GET | `/products/1` | DELETE нәтижесі серверде сақталмайды | 200 |
| TC23 | PUT | `/products/{{missingId}}` | PUT: жоқ ресурс | 404 |
| TC24 | PATCH | `/products/{{missingId}}` | PATCH: жоқ ресурс | 404 |
| TC25 | DELETE | `/products/{{missingId}}` | DELETE: жоқ ресурс | 404 |
| TC26 | POST | `/products/add` | POST: бүлінген JSON | 400 |
| TC27 | GET | `/auth/me` | Токен жоқ | 401 |
| TC28 | GET | `/auth/me` | Жарамсыз Bearer токен | 401 |
| TC29 | POST | `/auth/login` | Қате құпиясөз | 400 |
| TC30 | POST | `/auth/login` | Бос логин және пароль | 400 |
| TC31 | POST | `/auth/login` | Міндетті password параметрі жоқ | 400 |
| TC32 | POST | `/auth/login` | Дұрыс логин: токен алу | 200 |
| TC33 | GET | `/auth/me` | Жарамды токенмен профиль алу | 200 |
| TC34 | GET | `/auth/products?limit=1` | Қорғалған тауарлар тізімі | 200 |

Айнымалылар толық коллекцияны ретімен іске қосқанда автоматты есептеледі. `lastId` — нақты максималды ID; `total` — нақты жазбалар саны.
