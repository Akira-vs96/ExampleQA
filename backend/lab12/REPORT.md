# 12 зертханалық жұмыс Security Testing және OWASP

Тек репозиторийдің өз жергілікті оқу қосымшасы тексерілді. Unit/API security suite және нақты ZAP passive scanner нәтижелері бір-бірін толықтырады.

## 1 Оқу қосымшасы

QA Shop: register, login, profile, logout, product search, quote. Vulnerable мысалдар [before](before/) ішінде және негізгі серверге қосылмайды. Scanner екі уақытша 127.0.0.1 серверімен ғана жұмыс істейді.

## 2 Security Requirements

SR01: профиль authentication талап етеді; SR02: пароль PBKDF2 SHA256 + random salt; SR03: SQL параметрлермен; SR04: HTML input текст ретінде; SR05: session expiry/revocation; SR06: HttpOnly/SameSite; SR07: HTTPS кезінде Secure; SR08: CSP/nosniff/DENY; SR09: secrets response-қа шықпайды; SR10: input bounds.

[OWASP Top 10:2025](https://top10.owasp.org/2025/) сәйкестігі: A01 access control, A02 misconfiguration, A04 crypto, A05 injection, A07 authentication, A09 logging, A10 exceptional conditions. Passive scan осының бәрін толық сертификаттамайды.

## 3 Authentication

Wrong password, unknown user және forged token 401 береді. Username жоқ кезде де PBKDF2 есептеледі. Valid login HttpOnly session cookie береді. Password hash constant-time compare арқылы салыстырылады.

## 4 Authorization

`/me` және `/quote` `get_user` dependency арқылы қорғалады. Token user_id-мен SQLite-де байланысты; response current user-ді ғана береді. Store query public request-тан arbitrary user_id қабылдамайды.

## 5 Input Validation

Логин: 3–40 ASCII alphanumeric/underscore; пароль 8–128; quantity strict integer 1–100; discount 0–100; query ≤80; quote items 1–50 және duplicate product жоқ. Қате schema 422, жоқ product 404.

## 6 Session Management

32 random byte urlsafe token; SQLite-де SHA256 digest қана сақталады; TTL 3600s; logout digest жолын өшіреді; expired/replayed token қабылданбайды. Екі login жеке token алады, біреуінің logout-ы екіншісіне әсер етпейді.

## 7 Security Headers

X-Content-Type-Options: nosniff; X-Frame-Options: DENY; Referrer-Policy: no-referrer; CSP default-src self, frame-ancestors none, base-uri self, form-action self. Shop HTML inline script қолданбайды. Authentication response Cache-Control:no-store. Swagger/ReDoc жеке CDN policy алады.

## 8 Injection тәуекелі

[before/security.py](before/security.py) f-string SQL арқылы `"' OR 1=1 --"` username-мен authentication bypass береді. [demonstrate_security.py](demonstrate_security.py) оны нақты in-memory SQLite-де қайталайды. Corrected repository сол payload-ты `?` binding арқылы string ретінде қарастырады; login нәтиже бермейді.

## 9 XSS тәуекелі

Before HTML query-ді interpolation арқылы `<script>` түрінде қайтарады. Corrected UI `textContent` және JSON қолданады. Playwright `<img onerror>` енгізгенде executable DOM жоқтығын тексереді. CSP қосымша қорғаныс болады.

## 10 Access Control

Anonymous profile, forged session, expired session, logout replay және quote authorization тексеріледі. API body-де price жіберуге болмайды: extra fields forbidden, есеп server catalogue price-ынан алынады.

## 11 OWASP ZAP іске қосу

ZAP 2.17.0 official Linux package, Java 21. Archive SHA256 `efe799aaa3627db683b43f00c9c210aea0b75c00cc8f0a0f0434d12bb3ddde5a` [official release checksum](https://github.com/zaproxy/zaproxy/releases/tag/v2.17.0) мәнімен салыстырылды. `ZAP_HOME` орнатылып, `node scripts/python.mjs backend/lab12/run_zap.py` орындалады. Орнату қадамдары [README](../../README.md) ішінде.

## 12 Passive Scan

[run_zap.py](run_zap.py) loopback proxy ашады, нақты pages/assets/API-ді accessUrl арқылы өткізеді және passive queue біткенін күтеді. Before: 2 URL; after: HTML, JS, CSS және product/search API. Spider, active attack және сыртқы target қолданылмайды.

## 13 Scan нәтижелері

[zap-before.json](results/zap-before.json), [zap-after.json](results/zap-after.json), [zap-summary.json](results/zap-summary.json). Әр alert-та risk, confidence, URL және solution бар. Random scanner API key логтардан жасырылады.

## 14 Vulnerability тізімі

| ID | Finding | Source | Status |
|---|---|---|---|
| SEC01 | SQL injection authentication bypass | Local before reproduction | Fixed by binding |
| SEC02 | Reflected executable HTML | Before HTML + browser retest | Fixed by textContent |
| SEC03 | Missing Anti-clickjacking Header | ZAP before HTML | Fixed by DENY/CSP |
| SEC04 | CSP Header Not Set | ZAP before HTML | Fixed |
| SEC05 | X-Content-Type-Options Header Missing | ZAP before HTML/API | Fixed |

## 15 Severity

SEC01 High, SEC02 High — оқу vulnerability reproductions. ZAP SEC03 Medium, SEC04 Medium, SEC05 Low. Scanner-де before 4 instances: 2 Medium және 2 Low. Corrected scoped run: 0 alerts. Scanner confidence severity-ге тең емес.

## 16 False Positive тексеру

Әр ZAP finding raw response header-мен салыстырылды. Before шынымен CSP/DENY/nosniff бермейді, сондықтан бұл findings false positive емес. Loopback HTTP-де Secure=false күтіледі; HTTPS test Secure=true тексереді — HTTP cookie-де Secure жоқтығын автоматты production vulnerability деп санау қате болар еді. Бұл scanner-ден түскен alert емес, контекст бойынша қолмен талдау.

## 17 Екі осалдықты түзету

SQL injection: raw query interpolation орнына parameterized query. XSS: raw HTML interpolation орнына DOM textContent; CSP қорғанысы қосылды. Бұл түзетулер input blacklisting-ке тәуелді емес, қауіпті interpreter boundary-ін жояды.

## 18 Retest

Security pytest suite corrected repository/API-ді тексереді; Playwright browser DOM-ды тексереді; ZAP corrected local responses-ты қайта сканерлейді. SQLite connection leak coverage кезінде анықталып, `finally:close()` және closed-connection regression test арқылы түзетілді.

## 19 Before After

| Тексеру | Before | After |
|---|---|---|
| SQL bypass | User returned | None / login blocked |
| XSS HTML | Raw script | JSON + safe DOM |
| ZAP Medium | 2 | 0 |
| ZAP Low | 2 | 0 |
| Replay after logout | Рұқсат берілмеуі тиіс | 401 test PASS |

## 20 Security Report

Reproduced injection және HTML ақаулары түзетілді, auth/session/header tests өтеді, scoped passive scan таза. Қалдық production тәуекелдері: login rate limiting, HTTPS termination, long-term audit retention және dependency vulnerability monitoring. Осы оқу release-і localhost үшін; бұл production penetration-test қорытындысы емес.
