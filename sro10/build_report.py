"""Generate Kazakh Markdown, CSV and Word reports from actual test evidence."""

import ast
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from make_word_reports import (
    STUDENT,
    add_table,
    add_text,
    configure_document,
    parse_table,
)
from sro10.cases import CASES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUGS = {"WEB-13": "BUG-10-01", "WEB-18": "BUG-10-02"}


def clean_inline(text):
    text = re.sub(r"!?\[([^]]*)\]\([^)]*\)", r"\1", text)
    return text.replace("**", "").replace("`", "")


def case_result(case_id, summary):
    tests = [test for test in summary["tests"] if test["case"] == case_id]
    if not tests:
        return "ОРЫНДАЛМАҒАН"
    statuses = {test["outcome"] for test in tests}
    if statuses & {"failed", "error", "xpassed"}:
        return "ҚАТЕ: журналды қараңыз"
    if "xfailed" in statuses:
        return f"АҚАУ: {BUGS.get(case_id, 'XFAIL')}"
    if statuses != {"passed"}:
        return "ӨТКІЗІЛГЕН: журналды қараңыз"
    return f"ӨТТІ ({len(tests)} тексеріс)"


def export_cases(summary):
    rows = []
    details = ["# СРО 10 — толық тест-кейстер\n"]
    for case_id, kind, title, preconditions, steps, expected in CASES:
        result = case_result(case_id, summary)
        if "АҚАУ" in result:
            actual = (
                "Failed to fetch; түсінікті қазақша нұсқаулық жоқ."
                if case_id == "WEB-13" else
                "Өрісте Mouse; соңғы нәтижені ескі Keyboard жауабы ауыстырады."
            )
        elif result.startswith("ӨТТІ"):
            actual = "Күтілетін нәтиже автотестпен расталды."
        else:
            actual = "Нәтиже расталмады; бастапқы pytest журналын қараңыз."
        rows.append((case_id, kind, title, preconditions, steps, expected, actual, result))
        details.append(
            f"## {case_id} — {title}\n\n"
            f"Түрі: {kind}.\n\n"
            f"Алғышарт: {preconditions}\n\n"
            f"Қадамдар және деректер: {steps}\n\n"
            f"Күтілетін нәтиже: {expected}\n\n"
            f"Нақты нәтиже: {actual} Мәртебесі: **{result}**.\n"
        )
    (HERE / "TEST_CASES.md").write_text("\n".join(details), encoding="utf-8")
    with (HERE / "test_cases.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([
            "ID", "Түрі", "Сценарий", "Алғышарт", "Қадамдар және деректер",
            "Күтілетін нәтиже", "Нақты нәтиже", "Мәртебесі",
        ])
        writer.writerows(rows)
    return rows


def render_markdown(doc, markdown):
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            code = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            paragraph = doc.add_paragraph("\n".join(code))
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in paragraph.runs:
                run.font.name = "Courier New"
                run.font.size = Pt(9)
        elif line.startswith("|"):
            rows, index = parse_table(lines, index)
            add_table(doc, rows)
            continue
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            add_text(doc, clean_inline(line.lstrip("# ")), bold=True,
                     style="Heading 1" if level == 1 else "Heading 2")
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
            if match:
                path = HERE / match[2]
                if path.exists():
                    paragraph = doc.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    paragraph.paragraph_format.first_line_indent = Cm(0)
                    # Mobile screenshots are tall; limit both page width and height.
                    from docx.image.image import Image

                    picture = Image.from_file(str(path))
                    width = min(15.5, 18 * picture.px_width / picture.px_height)
                    paragraph.add_run().add_picture(str(path), width=Cm(width))
                    add_text(doc, match[1], align=WD_ALIGN_PARAGRAPH.CENTER)
        else:
            paragraph = [line]
            while index + 1 < len(lines):
                following = lines[index + 1].strip()
                if not following or following.startswith(("#", "|", "```", "![", "- ")):
                    break
                if re.match(r"\d+\. ", following):
                    break
                paragraph.append(following)
                index += 1
            add_text(doc, clean_inline(" ".join(paragraph)))
        index += 1


def build_report():
    summary = json.loads((HERE / "results/summary.json").read_text(encoding="utf-8"))
    rows = export_cases(summary)
    counts = summary["counts"]
    versions = summary["versions"]
    total = sum(counts.values())
    table = "\n".join(f"| {row[0]} | {row[2]} | {row[7]} |" for row in rows)
    source = (HERE / "test_web.py").read_text(encoding="utf-8")
    mandatory = {"test_web01_open_page", "test_web01_main_elements_visible",
                 "test_web02_registration_and_login"}
    snippets = "\n\n".join(
        ast.get_source_segment(source, node)
        for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name in mandatory
    )
    quote = {}
    junit = HERE / "results/pytest.xml"
    if junit.exists():
        for case in ET.parse(junit).iter("testcase"):
            if case.get("name") == "test_web14_order_quote":
                prop = case.find("./properties/property[@name='quote_response']")
                if prop is not None:
                    quote = json.loads(prop.get("value"))
    quote_text = json.dumps(quote, ensure_ascii=False, indent=2)
    bugs = (HERE / "BUG_REPORTS.md").read_text(encoding="utf-8")
    # Keep all links relative to the generated report in the same directory.
    bugs = bugs.replace("# СРО 10 — Bug Report", "## 5-кезең. Қателерді тіркеу", 1)
    report = f"""# СРО №10

**Веб-қосымшаны функционалдық, интерфейстік және автоматтандырылған тестілеу**

Орындаған: {STUDENT}
Күні: 08.11.2026. Есеп нақты жергілікті іске қосудан жасалды:
`{summary['generated_at_utc']}`.

## Жұмыстың мақсаты

Веб-қосымшаның негізгі мүмкіндіктерін талдау, дұрыс/қате деректер мен шекаралық
мәндер үшін тест-кейстер дайындау, интерфейс пен HTTP сұраныстарын тексеру,
Playwright және pytest арқылы автоматтандыру, табылған ақауларды тіркеу.

## 1-кезең. Сайтты таңдау және талдау

Таңдалған сайт — осы жобадағы **QA Shop** оқу дүкені.
Интерактивті тексеру мекенжайы: `http://127.0.0.1:8000/shop.html`.
Мысалдағы университет порталының орнына сол талаптарға сай дүкен таңдалды.
Email өрісі болмағандықтан, міндетті өріс тексерісі нақты Логин өрісіне бейімделді.
Автотесттер серверді бос localhost портында өздері қосып, уақытша SQLite базасын қолданады.

Негізгі функциялар:

- Логин және құпиясөз арқылы тіркелу, кіру, сессиядан шығу.
- Үш тауарды көру; атауы бойынша регистрге тәуелсіз іздеу.
- Тауар санын, жеңілдік пен жеткізуді ескеріп тапсырысты есептеу.
- Зертханалар порталына қайту; мобильді экран және пернетақтамен жұмыс.

Нақты қабылдау талаптары: логин 3–40 таңба, тек латын әріптері/цифр/астыңғы сызық;
құпиясөз 8–128 таңба; іздеу ең көбі 80 таңба; саны 1–100 бүтін сан;
жеңілдік 0–100 бүтін пайыз. Keyboard=5000 ₸, Mouse=2500 ₸, Monitor=45000 ₸.
Жеңілдіктен кейінгі сома 10000 ₸-ден бастап жеткізу тегін, одан төменде 1000 ₸.
Жеке дерек пен есептеу үшін сессия қажет. Желі қатесі түсінікті көрсетілуі,
іздеу нәтижесі соңғы сұранысқа сәйкес болуы тиіс.

## 2-кезең. Тест-кейстерді құрастыру

**20 тест-кейс** дайындалды: оң, теріс, шекаралық, интерфейстік және желілік жағдайлар.
Әр жағдайдың алғышарты, қадамдары, енгізілетін деректері, күтілетін және нақты
нәтижелері [TEST_CASES.md](TEST_CASES.md) және [CSV кестесінде](test_cases.csv) берілген.

| ID | Сценарий | Нақты нәтиже |
| --- | --- | --- |
{table}

## 3-кезең. Қолмен және интерактивті тексеру

Нақты браузерде бет, формалар, іздеу, қате хабарламалары және Tab навигациясы
тексерілді. Интерактивті тексерістер [manual_checks.json](results/manual_checks.json)
ішінде жазылған. Тексеру браузер құралдары арқылы орындалды; Network панеліндегі
сұраныстарға балама request/response бақылауы қолданылды.

Формалар: бос логинде native required хабарламасы шығып, valueMissing=true болды.
Қате құпиясөз 401 қайтарды. KEYBOARD сұранысы бір Keyboard тауарын көрсетті.
375, 768, 1440 px экрандарда көлденең жылжу байқалмады.
Tab реті: username → password → login → register → logout → query.
Басқарылатын желі үзілісі мен жауаптардың кері реті екі ақауды қайталады.

DevTools арқылы қайталау: F12 → Network → Fetch/XHR сүзгісі → Preserve log;
форманы жіберіп, Method, Status, Payload, Response өрістерін қарау.
Төмендегі кодтар нақты тексерілді:

| Әрекет | HTTP сұранысы | Нақты мәртебе |
| --- | --- | --- |
| Тіркелу | POST /api/shop/register | 201 Created |
| Дұрыс кіру | POST /api/shop/login | 200 OK |
| Қате құпиясөз | POST /api/shop/login | 401 Unauthorized |
| Тауар іздеу | GET /api/shop/products?q=KEYBOARD | 200 OK |
| Сессиясыз жеке дерек | GET /api/shop/me | 401 Unauthorized |
| Есептеу | POST /api/shop/quote | 200 OK |
| Шығу | DELETE /api/shop/session | 204 No Content |
| Іздеу ұзындығы 81 | GET /api/shop/products?q=… | 422 Unprocessable Entity |

Нақты есептеу сұранысы:

```http
POST /api/shop/quote
Content-Type: application/json

{{"items":[{{"product_id":1,"quantity":2}}],"percent":20}}
```

JUnit-ке сақталған нақты жауап денесі:

```json
{quote_text}
```

Браузердегі fetch сұраныстарының Method/URL/Status/Payload жазбалары
[results/](results/) ішіндегі `*.http.json` файлдарында сақталады;
құпиясөздер журналда жасырылған. API шекаралық тексерістерінің дәлелі — JUnit.
Желі үзілісі HTTP мәртебесімен шатастырылмайды: жауап келмейді, requestfailed пайда болады.

## 4-кезең. Playwright және pytest арқылы автоматтандыру

Орта: Python {versions['python']}; pytest {versions['pytest']};
Playwright {versions['playwright']}; Chromium {versions['chromium']};
FastAPI {versions['fastapi']}; uvicorn {versions['uvicorn']}.

Міндетті үш тексеріс нақты [test_web.py](test_web.py) файлында бар:
бетті ашу, негізгі элементтердің көрінуі және тіркелу/кіру әрекеті.
Төмендегі үзінді тікелей сол файлдан алынған; fixture-лер
[conftest.py](conftest.py) ішінде сервер мен Chromium-ды басқарады.

```python
{snippets}
```

Параметрленген жағдайлармен бірге **{total} автотест орындалды**:
**{counts['passed']} PASSED**, **{counts['xfailed']} XFAIL**,
{counts['failed']} FAILED, {counts.get('error', 0)} ERROR,
{counts['skipped']} SKIPPED, {counts['xpassed']} XPASS. Exit code: {summary['exit_code']}.
XFAIL — расталған ашық ақау; ол сәтті тест санына қосылмайды.
`strict=True, raises=AssertionError` инфрақұрылым қатесін ақау ретінде жасыруға жол бермейді;
түзетуден кейінгі күтпеген XPASS қайта қарауды талап етеді.

Жаңа контекст әр тестке бөлек беріледі, сессиялар араласпайды.
Желілік тесттер localhost сұраныстарына ғана әсер етеді.
Скриншоттар барлық тестке, Playwright trace ақаулы жағдайларға сақталады.

{bugs}

## Орындалу дәлелдері

![Тіркелу, кіру және тапсырысты есептеу](results/screenshots/manual-order.png)

![375 px мобильді экран](results/screenshots/manual-mobile-375.png)

![BUG-10-01: желілік қате хабарламасы](results/screenshots/manual-bug-network.png)

![BUG-10-02: Mouse сұранысына ескі Keyboard нәтижесі](results/screenshots/manual-bug-race.png)

## Қайта іске қосу

Жоба түбірінде:

```bash
python -m pip install -r sro10/requirements.txt
python -m playwright install chromium
npm run report:sro10
```

Linux CI-де жүйелік кітапханалар қажет болса:
`python -m playwright install --with-deps chromium`.
Тек автотесттер: `npm run test:sro10`.
Интерактивті тексеру үшін: `npm run dev`, кейін дүкен мекенжайын ашу.

Нәтижелер: [pytest.log](results/pytest.log), [pytest.xml](results/pytest.xml),
[summary.json](results/summary.json), [скриншоттар](results/screenshots/).
`python -m playwright show-trace sro10/results/test_web18_latest_search_wins.trace.zip`
командасы қате іздеу сценарийінің орындалуын ашады.

## Қорытынды

Тапсырманың бес кезеңі орындалды: сайт талданды, 20 тест-кейс құрастырылды,
интерфейс пен HTTP сұраныстары тексерілді, Playwright/pytest автотесттері орындалды,
екі нақты ақауға Bug Report жасалды. Негізгі сценарийлер мен шекаралық мәндердің
нәтижелері бастапқы журналдарда көрсетілген. Ашық ақаулар: BUG-10-01 және BUG-10-02;
оларды түзету және қайта тексеру бөлек жұмыс ретінде қалады.
"""
    (HERE / "REPORT.md").write_text(report, encoding="utf-8")
    document = Document()
    configure_document(document)
    document.sections[0].page_width = Cm(21)
    document.sections[0].page_height = Cm(29.7)
    render_markdown(document, report)
    for paragraph in document.paragraphs[:2]:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.first_line_indent = Cm(0)
    document.add_page_break()
    add_text(document, "Қосымша А. Толық тест-кейстер", bold=True, style="Heading 1")
    render_markdown(document, (HERE / "TEST_CASES.md").read_text(encoding="utf-8"))
    destination = ROOT / "word_reports" / "Абинсериков Нурасыл АЖ-41 QA СРО-10.docx"
    destination.parent.mkdir(exist_ok=True)
    document.save(destination)
    print(HERE / "REPORT.md")
    print(destination)
    return destination


if __name__ == "__main__":
    build_report()
