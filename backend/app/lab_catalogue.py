"""Read only the fifteen known laboratory reports for the local learning portal."""

from pathlib import Path


def catalogue(root: Path) -> list[dict]:
    items = []
    for number in range(1, 16):
        report = root / f"backend/lab{number}/REPORT.md"
        text = report.read_text(encoding="utf-8") if report.is_file() else "Есеп дайындалуда."
        title = text.splitlines()[0].lstrip("# ") if text else f"Жұмыс {number}"
        items.append(
            {"id": number, "title": title, "report": text, "source": f"backend/lab{number}"}
        )
    return items
