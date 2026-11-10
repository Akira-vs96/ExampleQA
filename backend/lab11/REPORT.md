# 11 зертханалық жұмыс Performance және Load Testing

Нысан — жергілікті `/api/shop/products` және case-insensitive search. [run_load.py](run_load.py) уақытша дерекқормен жеке сервер ашады, Locust іске қосады және серверді міндетті түрде тоқтатады. Қосымша құралдар: Apache JMeter-ге арналған [JMX жоспары](JMeter_Catalogue.jmx), Postman-ға импортталатын [API коллекциясы](Postman_Lab11.postman_collection.json). JMeter load profile-ін орындайды; Postman коллекциясы API контрактын функционалдық тексеруге арналған.

## 1 Performance объектісі

Public catalogue/read path таңдалды: 75% catalogue, 25% search. Login PBKDF2 және quote write path бұл workload-қа кірмейді; оларды өлшеу үшін бөлек профиль қажет.

## 2 Талаптар

50 VU қысқа жергілікті профиль үшін p95 ≤ 200 ms және error rate ≤ 1%. HTTP status-пен бірге JSON нәтижесі тексеріледі: catalogue 3 тауар, search бірінші ID=1. Think time 20–50 ms.

## 3 Baseline Response Time

1 user, 8 seconds. [baseline_stats.csv](results/baseline_stats.csv) average, median, p95 және max береді. Клиент measured HTTP уақытын есептейді; бұл функцияның CPU уақыты емес.

## 4 Throughput

Throughput = completed requests / elapsed test seconds. Locust `Requests/s` мәні алынады, CLI process startup wall time denominator ретінде қолданылмайды. Әр profile row [summary.json](results/summary.json) ішінде.

## 5 Он пайдаланушы

10 VU, spawn rate 10/s, run time 8 s. [load10_stats.csv](results/load10_stats.csv). Baseline-мен p95 және RPS салыстырылады.

## 6 Жиырма бес пайдаланушы

25 VU, spawn rate 25/s. [load25_stats.csv](results/load25_stats.csv). Error/response contract барлық request үшін сақталады.

## 7 Елу пайдаланушы

50 VU, spawn rate 50/s. Бұл NFR01–02 қабылдау профилі. [load50_stats.csv](results/load50_stats.csv) және final summary actual latency/error rate көрсетеді.

## 8 Жүз пайдаланушы жоспары

Қадам: 50-ден кейін 100 VU, spawn 100/s, 8 s, p95/errors/RPS салыстыру. Бұл жоспар `stress100` ретінде де орындалды. Ұзақ capacity бағалауда 2 min warm-up, 10 min steady және 2 min cool-down қажет.

## 9 Load Test

Baseline → 10 → 25 → 50 VU тізбегі. Әр profile бөлек Locust process және жеке CSV prefix алады. `npm run lab11` барлық run-ды қайталайды.

## 10 Stress Test

100 VU қысқа stress profile негізгі 50 VU target-тен екі есе жоғары. [stress100_stats.csv](results/stress100_stats.csv). Күтпеген crash/error ізделеді; осы деңгейде жүйе сынбаса, бұл breaking point табылды деген сөз емес.

## 11 Spike Test

`SpikeShape`: 0–3 s 10 VU → 3–6 s 100 VU → 6–9 s 10 VU. 100/s spawn өсуді жылдамдатады. [spike_stats_history.csv](results/spike_stats_history.csv) уақыт бойынша latency/throughput береді.

## 12 Endurance жоспары

Жеке run: 50 VU, 2 h steady, wait time 20–50 ms; әр 10 s RSS, CPU, open file descriptors, response p95 және SQLite locks тіркеледі. Acceptance: error ≤1%, p95 ≤200ms, RSS өсуі warm-up-тан кейін ≤10%. Команда: `node scripts/python.mjs -m locust -f backend/lab11/locustfile.py --headless -u 50 -r 10 -t 2h --host http://127.0.0.1:8000 --csv backend/lab11/results/endurance`. Екі сағаттық run жоспарланған, қысқа профильдер оның нәтижесі деп көрсетілмейді.

## 13 Locust сценарийі

[locustfile.py](locustfile.py) HttpUser, between wait және weighted tasks қолданады. `catch_response=True` 200 болғанымен қате JSON-ды failure ретінде белгілейді. Spike shape тек LOCUST_SPIKE=1 кезінде белсенді.

## 14 Virtual Users

CLI --users/--spawn-rate: 1/1, 10/10, 25/25, 50/50, 100/100. Қарапайым профильде duration=8s; spike shape=9s. VU — қатар жұмыс істейтін сценарий орындаушысы; ол бір мезгілдегі TCP request санына дәл тең емес.

## 15 Response Time

Average және p95 ms сақталады; percentile бірліктері ауыстырылмайды. Бірінші өлшеуде 50 VU p95 23 ms болған, бірақ қайталанған run-ның authoritative мәндері [summary.json](results/summary.json) мен [SUMMARY.md](../lab15/results/SUMMARY.md) ішінде.

## 16 Error Rate

Error Rate = failed requests / total requests × 100%. Бос workload 100% error ретінде саналады және runner FAIL береді. Initial алты profile-де request error болмады; әр қайта run нақты counts сақтайды.

## 17 Throughput салыстыру

1→10→25→50→100 VU кезінде RPS өсімі және response latency бірге қаралады. Жаңа VU-лар response time-ды қатты өсіріп, RPS аз өсірсе, saturation белгісі. Тек «көп RPS» нәтижесі бизнес дұрыстығын алмастырмайды.

## 18 Bottleneck талдауы

Initial 50→100 VU кезінде throughput шамамен 1015→1298 RPS, average 12.7→36.2ms өсті. Бұл read path-та queueing/CPU шектеуін зерттеуге негіз, бірақ нақты cause CPU profiler-сіз бекітілмейді. Test client пен бір Uvicorn worker бір хостта: client saturation да ықтимал. Келесі диагностика — separate host generator және server CPU/thread-pool profiling.

## 19 Performance графигі

![Locust p95 chart](results/performance.svg)

График сақталған JSON/CSV өлшемдерінен жасалады; әр баған profile p95 ms көрсетеді. Машинамен оқылатын actual мәндер [summary.json](results/summary.json) ішінде.

## 20 Қорытынды

Locust арқылы baseline, 10/25/50 VU load, 100 VU stress және spike орындалды; CSV, history, logs және график сақталды. Apache JMeter-де 10 VU load іске қосылды: 1,812 сұрау, 0 қате, average 2.38 ms, p95 шамамен 4.35 ms, throughput шамамен 229 сұрау/с; [JMeter HTML есебі](results/jmeter-load10-report/index.html) мен [JTL дерегі](results/jmeter-load10.jtl) сақталды. Postman коллекциясының Newman орындалуында 3 request және 10 assertion өтті, қате болмады ([JSON нәтижесі](results/postman-newman.json)). Endurance жеке жоспар ретінде берілді. Бұл localhost read workload нәтижелері production SLA-ға тікелей көшірілмейді.

## Тесттерді жеке іске қосу

Төмендегі командалар әр профильді жеке қайта орындауға арналған. Алдымен жоба түбірінен серверді бірінші терминалда іске қосыңыз:

```bash
node scripts/python.mjs -m uvicorn app.main:app \
  --app-dir backend \
  --host 127.0.0.1 \
  --port 8000
```

Сервер жұмыс істеп тұрған кезде екінші терминалда жоба түбірінен қажетті Locust командасын орындаңыз. Әр тест CSV нәтижелерін бөлек `manual-*` префиксімен сақтайды.

**Baseline (1 пайдаланушы):**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 1 -r 1 -t 8s \
  --csv backend/lab11/results/manual-baseline
```

**Load Test — 10 пайдаланушы:**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 10 -r 10 -t 8s \
  --csv backend/lab11/results/manual-load10
```

**Load Test — 25 пайдаланушы:**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 25 -r 25 -t 8s \
  --csv backend/lab11/results/manual-load25
```

**Load Test — 50 пайдаланушы:**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 50 -r 50 -t 8s \
  --csv backend/lab11/results/manual-load50
```

**Stress Test — 100 пайдаланушы:**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 100 -r 100 -t 8s \
  --csv backend/lab11/results/manual-stress100
```

**Spike Test:**

```bash
LOCUST_SPIKE=1 node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  --csv backend/lab11/results/manual-spike
```

Spike профилі автоматты түрде 0–3 секундта 10 VU, 3–6 секундта 100 VU, 6–9 секундта қайтадан 10 VU қолданады.

**Endurance Test (2 сағат):**

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --headless \
  --host http://127.0.0.1:8000 \
  -u 50 -r 10 -t 2h \
  --csv backend/lab11/results/endurance
```

Екі сағаттық endurance командасы — ұзақ тест жоспарын іске қосу; оның нәтижесі шыққанға дейін endurance орындалды деп есептелмейді. Әр run-нан кейін `*_stats.csv` ішінен response time, p95 және Requests/s, ал `*_failures.csv` ішінен қателерді қараңыз. Серверді тоқтату үшін бірінші терминалда Ctrl+C басыңыз.

## Locust Web UI және сайтты көрсету

Locust-ты браузер интерфейсімен іске қосу үшін сайт/API сервері мен Locust-ты екі бөлек терминалда қалдырыңыз.

**1-терминал — жобаны іске қосу:** жоба түбірінен:

```bash
npm run dev
```

Терминалда көрсетілген `QA Shop` мекенжайын браузерде ашыңыз (әдетте `http://127.0.0.1:8000/shop.html`). Сервердің өзі берген портты пайдаланыңыз; 8000 бос болмаса, `npm run dev` келесі бос портты таңдауы мүмкін.

**2-терминал — Locust Web UI:** жоба түбірінен (төмендегі host мәніндегі `8000`-ді сайт терминалы көрсеткен портқа ауыстырыңыз):

```bash
node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --host http://127.0.0.1:8000 \
  --web-host 127.0.0.1 \
  --web-port 8089
```

Locust UI-ийг `http://127.0.0.1:8089` мекенжайынан ашыңыз. Start бетінде пайдаланушылар санын (Number of users), іске қосу жылдамдығын (Spawn rate) және ұзақтығын енгізіп, **Start** басыңыз. Мысал: 10 пайдаланушыға `10`, spawn rate `10`, ұзақтық `8s`; қалған load/stress профильдеріне 25/25, 50/50 немесе 100/100 мәндерін беріңіз. `Response Time` графигі мен статистиканы UI-де бақылаңыз; тоқтату үшін **Stop** қолданыңыз. UI режимінде `--headless` жалаушасын қоспаңыз.

**Spike Test:** UI процесін тоқтатып, spike пішінін қоршаған орта айнымалысымен қосып қайта іске қосыңыз:

```bash
LOCUST_SPIKE=1 node scripts/python.mjs -m locust \
  -f backend/lab11/locustfile.py \
  --host http://127.0.0.1:8000 \
  --web-host 127.0.0.1 \
  --web-port 8089
```

Бұл профиль UI-де **Start** басқанда 10 → 100 → 10 VU (әр кезең 3 секунд) болып ауысады. Windows PowerShell-де команданың алдына `$env:LOCUST_SPIKE="1";` деп жазыңыз.

Демонстрация кезінде браузерде дүкен бетін және Locust UI-ді бөлек қойындыларда ашуға болады. Locust-ты тоқтатқаннан кейін сайтты жабу үшін бірінші терминалда Ctrl+C басыңыз; Locust терминалын да Ctrl+C арқылы тоқтатуға болады.

## Apache JMeter және Postman пайдалану

### Apache JMeter — load test

Apache JMeter 5.6.3 және Java 17+ орнатылып, `jmeter` командасы PATH ішінде болуы керек. JMeter-ді [Apache ресми жүктеу бетінен](https://jmeter.apache.org/download_jmeter.cgi) алуға болады. Жоба түбірінен жоспарды GUI-де ашуға болады:

```bash
jmeter -t backend/lab11/JMeter_Catalogue.jmx
```

GUI-де жоспарды қарауға және өзгертуге болады, бірақ жүктемені өлшеуді CLI режимінде орындаңыз. Apache JMeter құжаттамасы load test-терді GUI емес, CLI режимінде жүргізуді ұсынады ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html)). 10 VU мысалы (толық жүктелу үшін 2 секундтық ramp-up, 8 секунд өлшеу):

```bash
jmeter -n \
  -t backend/lab11/JMeter_Catalogue.jmx \
  -Jthreads=10 -Jramp=2 -Jduration=8 \
  -Jhost=127.0.0.1 -Jport=8000 \
  -l backend/lab11/results/jmeter-load10.jtl \
  -e -o backend/lab11/results/jmeter-load10-report
```

25, 50 немесе 100 пайдаланушыны тексеру үшін `-Jthreads` мәнін ауыстырыңыз. Әр жаңа іске қосқанда `-l` және `-o` жолдарын бос, жаңа атауларға өзгертіңіз, мысалы `jmeter-load25.jtl` / `jmeter-load25-report`. Сервер алдын ала қосулы болуы керек. HTML есепте average, p95, throughput және error rate бар.

### Postman — API тексеруі

Postman Desktop-та **Import → Files** таңдап, [Postman_Lab11.postman_collection.json](Postman_Lab11.postman_collection.json) файлын импорттаңыз. Collection variable `baseUrl` мәнін сервердің нақты мекенжайына (әдепкі `http://127.0.0.1:8000`) орнатыңыз. Коллекцияда каталог, case-insensitive search және жоқ тауарға 404 берілетіні тексеріледі; **Run** арқылы толық коллекцияны орындап, нәтижесін Postman Runner-де көрсетуге болады. Postman коллекциясы — functional/API тексеруі; виртуалды пайдаланушы жүктемесін JMeter орындайды.

Postman UI орнатылмаған ортада дәл сол Postman collection Newman арқылы іске қосылады:

```bash
backend/lab9/node_modules/.bin/newman run \
  backend/lab11/Postman_Lab11.postman_collection.json \
  --env-var 'baseUrl=http://127.0.0.1:8000' \
  --reporters cli,json \
  --reporter-json-export backend/lab11/results/postman-newman.json
```

Қазіргі Newman run нәтижесі: 3/3 request және 10/10 assertion өтті. Бұл Postman GUI-де орындалған run емес: импорттауға болатын Postman коллекциясы Newman арқылы тексерілді.
