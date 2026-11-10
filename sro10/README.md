# СРО №10 — веб-қосымшаны тестілеу

Тапсырманың барлық бес кезеңі жергілікті **QA Shop** қолданбасында орындалды.
Толық есеп: [REPORT.md](REPORT.md); тапсыруға арналған
[Word құжаты](../word_reports/Абинсериков%20Нурасыл%20АЖ-41%20QA%20СРО-10.docx).

- [20 тест-кейс](TEST_CASES.md): алғышарттар, қадамдар, деректер, күтілетін/нақты нәтижелер.
- [CSV кестесі](test_cases.csv): Excel-де ашуға болады.
- [Playwright + pytest](test_web.py): параметрленген жағдайлармен 30 автотест.
- [Екі Bug Report](BUG_REPORTS.md): қайталау қадамдары және ашық ақаулар.
- [Нақты нәтиже](results/summary.json), [JUnit](results/pytest.xml), [журнал](results/pytest.log).
- [Интерактивті тексеру](results/manual_checks.json), [скриншоттар](results/screenshots/).

## Орнату және орындау

Жоба түбіріндегі virtual environment ішінде:

```bash
python -m pip install -r sro10/requirements.txt
python -m playwright install chromium
npm run report:sro10
```

Соңғы команда браузерде тесттерді іске қосады, журнал мен JUnit сақтайды,
Markdown/CSV және Word есебін нақты нәтижемен қайта жасайды.
Тесттер өз серверін бос localhost портында және уақытша SQLite базасында іске қосады.
Әр тестке жаңа браузер контексті беріледі; қолданушының дүкен базасына жазбайды.

Тек тесттер: `npm run test:sro10`.
Сақталған нәтижелерден есепті қайта жасау: `python -m sro10.build_report`.
Қолмен тексеру: `npm run dev` → `http://127.0.0.1:8000/shop.html`.
Linux CI-де Chromium жүйелік тәуелділіктері үшін
`python -m playwright install --with-deps chromium` қолданылады.

## Нәтижені түсіндіру

WEB-13 және WEB-18 — расталған **ашық ақаулар**, `strict xfail` ретінде белгіленген.
Олар PASSED санына қосылмайды. Қалған 28 тексеріс қалыпты өткенде, suite:
**28 passed, 2 xfailed** деп аяқталады. XFAIL тек assertion қатесіне рұқсат береді;
браузер/сервер ақауы FAILED немесе ERROR болып қалады.

Ақаудың белгісінсіз нақты сәтсіз тексерісті көрсету:

```bash
npm run test:sro10 -- --runxfail -k 'web13 or web18'
```

Бұл команда екі белгілі ақау бар кезде 1 exit code қайтарады.
Ол demonstration болғандықтан, кейін толық `npm run report:sro10` арқылы
есептерді қалыпты толық нәтижемен жаңарту керек.
Интерактивті тексеру жазбалары тарихи evidence ретінде сақталады;
қайта іске қосу оларды жаңадан қолмен тексерілді деп өзгертпейді.
