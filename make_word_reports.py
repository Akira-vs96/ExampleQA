from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt


ROOT = Path(__file__).parent
OUT = ROOT / "word_reports"
STUDENT = "Абинсериков Нурасыл АЖ-41."

LAB10_TEST_TITLES = {
    "registration and login": "Тіркелу және жүйеге кіру",
    "invalid password does not authenticate": "Қате құпиясөзбен жүйеге кіруге болмайды",
    "form validation blocks short passwords": "Форма тексерісі қысқа құпиясөзді қабылдамайды",
    "search is case insensitive": "Іздеу үлкен және кіші әріпке тәуелсіз орындалады",
    "empty search returns the catalogue": "Бос іздеу каталогты қайтарады",
    "invalid input is rendered safely": "Жарамсыз енгізу қауіпсіз көрсетіледі",
    "navigation returns to laboratory portal": "Навигация зертханалар порталына қайтарады",
    "portal opens all fifteen reports and filters works": "Портал он бес есепті ашады және сүзгі жұмыс істейді",
    "quote uses discount before delivery": "Есептеу кезінде жеткізу алдында жеңілдік қолданылады",
    "logout revokes access": "Жүйеден шығу рұқсатты жояды",
    "responsive layout at 375px": "375 px өлшеміндегі бейімделгіш орналасу",
    "responsive layout at 768px": "768 px өлшеміндегі бейімделгіш орналасу",
    "responsive layout at 1440px": "1440 px өлшеміндегі бейімделгіш орналасу",
}


def set_cell_border(cell):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "000000")


def configure_document(doc: Document):
    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(14)
    normal.paragraph_format.first_line_indent = Cm(1.25)
    normal.paragraph_format.line_spacing = 1.0
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    heading = doc.styles["Heading 1"]
    heading.font.name = "Times New Roman"
    heading._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    heading.font.size = Pt(14)
    heading.font.bold = True
    heading.paragraph_format.first_line_indent = Cm(1.25)
    heading.paragraph_format.line_spacing = 1.0
    heading.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for style_name in ("Heading 2", "Heading 3"):
        style = doc.styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(14)
        style.font.bold = True
        style.paragraph_format.first_line_indent = Cm(1.25)
        style.paragraph_format.line_spacing = 1.0
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def add_text(doc, text, *, bold=False, italic=False, align=None, style=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(14)
    return p


def add_table(doc, rows):
    if not rows:
        return
    cols = max(len(row) for row in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for ri, row in enumerate(rows):
        for ci in range(cols):
            cell = table.cell(ri, ci)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_border(cell)
            cell.text = row[ci] if ci < len(row) else ""
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ri == 0 else WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.line_spacing = 1.0
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
                    run.font.size = Pt(12)
                    run.bold = ri == 0
    doc.add_paragraph()


def parse_table(lines, start):
    rows = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw = lines[i].strip().strip("|")
        if not re.fullmatch(r"\s*:?-+:?\s*(\|\s*:?-+:?\s*)*", raw):
            rows.append([re.sub(r"[`*_]", "", x.strip()) for x in raw.split("|")])
        i += 1
    return rows, i


def clean_inline(text):
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def convert_report(lab: int):
    report = ROOT / "backend" / f"lab{lab}" / "REPORT.md"
    lines = report.read_text(encoding="utf-8").splitlines()
    doc = Document()
    configure_document(doc)
    add_text(doc, STUDENT, bold=True, style="Heading 1")
    add_text(doc, f"https://github.com/Akira-vs96/ExampleQA/tree/main/backend/lab{lab}", bold=True)
    doc.add_paragraph()
    title_seen = False
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            p = add_text(doc, "\n".join(code), align=WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.first_line_indent = Cm(0)
            for r in p.runs:
                r.font.name = "Courier New"
                r._element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
                r.font.size = Pt(10)
            i += 1
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = clean_inline(line[level:].strip())
            if level == 1 and not title_seen:
                text = text.replace(" зертханалық жұмыс", "-зертханалық жұмыс", 1)
                title_seen = True
            add_text(doc, text, bold=True, style="Heading 1" if level == 1 else "Heading 2")
            i += 1
            continue
        if line.startswith("|"):
            rows, i = parse_table(lines, i)
            add_table(doc, rows)
            continue
        if line.startswith("- ") or line.startswith("* "):
            p = add_text(doc, "• " + clean_inline(line[2:]))
            p.paragraph_format.left_indent = Cm(1.25)
            p.paragraph_format.first_line_indent = Cm(0)
            i += 1
            continue
        if line.startswith("---"):
            i += 1
            continue
        text = clean_inline(line)
        if text.startswith("mermaid"):
            i += 1
            continue
        add_text(doc, text)
        i += 1
    if lab == 10:
        add_lab10_evidence(doc)
    out = OUT / f"Абинсериков Нурасыл АЖ-41 QA Lab-{lab}.docx"
    doc.save(out)
    return out


def add_lab10_evidence(doc: Document):
    """Append the actual Playwright result and the before/after UI evidence."""
    add_text(doc, "Нақты UI тексеруінің дәлелдері", bold=True, style="Heading 1")
    result = json.loads((ROOT / "backend" / "lab10" / "results" / "after.json").read_text(encoding="utf-8"))
    stats = result["stats"]
    add_text(
        doc,
        f"Playwright Chromium нәтижесі: {stats['expected']} тест сәтті өтті, "
        f"{stats['unexpected']} күтпеген қате, {stats['skipped']} өткізіліп кеткен тест. "
        f"Жалпы орындау уақыты: {stats['duration'] / 1000:.1f} секунд.",
    )
    rows = [["№", "Тексеру", "Мәртебесі", "Уақыт, мс"]]
    number = 1
    for suite in result.get("suites", []):
        for spec in suite.get("specs", []):
            test_result = spec.get("tests", [{}])[0].get("results", [{}])[0]
            title = LAB10_TEST_TITLES.get(spec["title"], spec["title"])
            rows.append([
                str(number),
                title,
                "ӨТТІ" if spec.get("ok") else "ҚАТЕ",
                str(test_result.get("duration", "—")),
            ])
            number += 1
    add_table(doc, rows)
    add_text(doc, "UI тапсырмаларының орындалу нәтижелері", bold=True)
    number = 1
    for suite in result.get("suites", []):
        for spec in suite.get("specs", []):
            safe_title = re.sub(r"[^a-z0-9]+", "-", spec["title"], flags=re.IGNORECASE).strip("-").lower()
            image = ROOT / "backend" / "lab10" / "results" / "task-screens" / f"after-{safe_title}.png"
            if not image.exists():
                continue
            title = LAB10_TEST_TITLES.get(spec["title"], spec["title"])
            add_text(doc, f"Тапсырма {number}. {title}", bold=True)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.add_run().add_picture(str(image), width=Cm(14))
            add_text(doc, f"Сурет – {number}. {title} тапсырмасының орындалу нәтижесі", align=WD_ALIGN_PARAGRAPH.CENTER)
            number += 1
    add_text(doc, "Салыстыру нәтижесі", bold=True)
    comparison = json.loads((ROOT / "backend" / "lab10" / "results" / "comparison.json").read_text(encoding="utf-8"))
    add_text(
        doc,
        f"Бастапқы нұсқа exit code: {comparison['runs'][0]['exit_code']}; "
        f"түзетілген нұсқа exit code: {comparison['runs'][1]['exit_code']}. "
        "Демонстрация қатені анықтап, түзетілген нұсқада сәтті аяқталды.",
    )
    figure = number
    for variant, label in (("before", "Бастапқы нұсқа"), ("after", "Түзетілген нұсқа")):
        for width in (375, 768, 1440):
            image = ROOT / "backend" / "lab10" / "results" / f"{variant}-{width}.png"
            if not image.exists():
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.add_run().add_picture(str(image), width=Cm(14))
            add_text(
                doc,
                f"Сурет – {figure}. {label}: бейімделгіш UI, экран ені {width} px",
                align=WD_ALIGN_PARAGRAPH.CENTER,
            )
            figure += 1


def main():
    OUT.mkdir(exist_ok=True)
    for lab in range(1, 16):
        print(convert_report(lab))


if __name__ == "__main__":
    main()
