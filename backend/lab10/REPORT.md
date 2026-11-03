# 10 зертханалық жұмыс Web қосымшаны тестілеу

Нысан — [QA Shop](../../frontend/shop.html). Тесттер нақты Chromium мен localhost FastAPI серверін қолданады; API response mock қолданылмайды. Орындалатын жинақ: [shop.spec.mjs](tests/shop.spec.mjs).

## 1 Web қосымшаны таңдау

QA Shop тіркелу, login, search, quote және logout функцияларын біріктіреді. Іске қосу `npm run dev`, мекенжай терминалда шығады. Статикалық GitHub Pages тек есептерді көрсетеді; дүкен API-і жергілікті серверді қажет етеді.

## 2 UI элементтері

| № | Элемент | Locator |
|---|---|---|
| 1 | Логин | getByLabel('Логин', exact) |
| 2 | Пароль | getByLabel('Пароль', exact) |
| 3 | Тіркелу | getByRole('button', name='Тіркелу') |
| 4 | Кіру | getByRole('button', name='Кіру') |
| 5 | Шығу | getByRole('button', name='Шығу') |
| 6 | Іздеу өрісі | getByLabel('Тауарды іздеу') |
| 7 | Іздеу батырмасы | getByRole('button', name='Іздеу') |
| 8 | Тауар тізімі | #products li |
| 9 | Quantity | #quantity |
| 10 | Discount | #percent |
| 11 | Есептеу | getByRole('button', name='Есептеу') |
| 12 | Нәтиже | #quote-result |
| 13 | Хабар | #status |

## 3 Login тесті

Бірегей synthetic user тіркеледі, дұрыс парольмен кіреді; status-та «Қош келдіңіз» көрінеді. Қате пароль 401 хабарын көрсетеді. Cookie-ді JavaScript оқымайды.

## 4 Registration тесті

Username әр test үшін бірегей suffix алады. Тіркелу сәтті хабармен расталады; кейін login жасалады. Duplicate behavior API security suite-де 409 ретінде тексеріледі.

## 5 Form Validation

Пароль ұзындығы 8-ден аз болса HTML constraint validation submit-ті тоқтатады. Quantity 1–100, discount 0–100 және step=1. Server schema да осы шектерді тәуелсіз тексереді.

## 6 Search

`KEYBOARD` үлкен әріппен енгізілгенде бір Keyboard қалады. Бос search барлық үш тауарды көрсетеді. Іздеу query параметрі encodeURIComponent арқылы беріледі.

## 7 Navigation

«← Зертханалар» сілтемесі порталға қайтарады; title тексеріледі. Portal test 15 report card жүктелуін, сүзгіні және report dialog ашылуын тексереді.

## 8 Logout

Кіру → шығу → «Жүйеден шықтыңыз» → quote қайта жіберу → «Алдымен жүйеге кіріңіз». Cookie server storage-тан да өшіріледі; replay test [12 жұмыста](../lab12/tests/test_security.py) бар.

## 9 Invalid Input

`<img src=x onerror=alert(1)>` search ретінде берілгенде бос нәтиже мәтіні шығады; DOM-да `img` жоқ. Бұл XSS payload executable HTML-ге айналмағанын тексереді.

## 10 Responsive

375, 768 және 1440 px viewport тексеріледі. Criterion: document.scrollWidth ≤ innerWidth. [before/layout.css](before/layout.css) әдейі min-width:1000px қосады; сол test 375/768-де FAIL болады. Corrected stylesheet fluid width және media query қолданады.

## 11 Playwright орнату

`npm ci --no-audit --no-fund`; `npx playwright install chromium`. CI Linux-те `npx playwright install --with-deps chromium`. Нұсқа [package-lock.json](../../package-lock.json) арқылы бекітілген.

## 12 Locator

Accessible label/role бірінші қолданылады. Нәтиже/status үшін тұрақты id бар. Екі элементтің implicit status role-і бірдей болғандықтан status locator `#status` арқылы нақтыланды; бұл тесттің екіұштылығын жойды.

## 13 Automated Login

`registerAndLogin(page)` form-ды толтырады, тіркелуді күтеді, login жібереді, success мәтінін тексереді. Fixed sleep жоқ; Playwright assertion auto-wait пайдаланады.

## 14 Automated Search

`search is case insensitive` test search өрісіне KEYBOARD жазады, button басады, list count=1 және мәтін Keyboard екенін тексереді. Server response шынымен қолданылғандықтан бұл толық browser/API интеграциясы.

## 15 Screenshot

[375 px](results/after-375.png), [768 px](results/after-768.png), [1440 px](results/after-1440.png) screenshot сақталады. Before режимінде де screenshot assertion алдында жазылады, сондықтан overflow дәлелі жоғалмайды.

## 16 Нәтижелерді тіркеу

`npm run lab10` JSON және HTML report жасайды. [after.json](results/after.json) corrected run-ды, [before.json](results/before.json) layout ақауы бар run-ды сақтайды. Нақты passed/failed/skipped саны final [SUMMARY.md](../lab15/results/SUMMARY.md) ішінде.

## 17 Failed test талдауы

UI_VARIANT=before кезінде mobile/tablet responsive tests `overflow == true` анықтайды. Root cause fixed body min-width 1000px; viewport одан тар. 1440px desktop test өтеді, сондықтан тек desktop қарау ақауды жасырған болар еді.

## 18 Түзету

Corrected stylesheet fixed min-width қолданбайды. `.container` экраннан 32/48px padding алып fluid width есептейді; шағын экранда form columns бір баған болады. Қате CSS тек explicit before experiment кезінде browser route арқылы қосылады.

## 19 Regression

Түзетуден кейін сол responsive tests және registration/login/search/quote/logout suite толық қайта орындалады. Before expected condition өзгермейді. Browser retries=0; flaky failure retry арқылы жасырылмайды.

## 20 Web Testing есебі

UI элементтері, positive/negative, validation, search, navigation, logout және responsive қамтылды. Initial CSS ақауы нақты failure берді, corrected нұсқа regression-нен өтті. Synthetic users және isolated browser contexts тесттерді бір-бірінен тәуелсіз етеді.
