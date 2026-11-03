"""Generate readable QA metrics from saved runner evidence, never from guessed counts."""

import html
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "backend/lab15/results"


def read_json(path: str):
    file = ROOT / path
    return json.loads(file.read_text(encoding="utf-8")) if file.is_file() else None


def junit_counts(path: Path) -> dict:
    if not path.is_file():
        return {"status": "NOT RUN"}
    cases = list(ET.parse(path).getroot().iter("testcase"))
    failed = sum(case.find("failure") is not None for case in cases)
    errors = sum(case.find("error") is not None for case in cases)
    skipped = sum(case.find("skipped") is not None for case in cases)
    passed = len(cases) - failed - errors - skipped
    return {
        "total": len(cases),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "pass_rate": round(100 * passed / len(cases), 2) if cases else 0,
        "status": "PASS" if cases and not (failed or errors or skipped) else "FAIL",
    }


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    reports = []
    for number in range(1, 16):
        file = ROOT / f"backend/lab{number}/REPORT.md"
        text = file.read_text(encoding="utf-8") if file.is_file() else ""
        sections = {int(value) for value in re.findall(r"^## (\d+)\b", text, re.MULTILINE)}
        missing = sorted(set(range(1, 21)) - sections)
        reports.append(
            {"lab": number, "task_sections": len(sections & set(range(1, 21))), "missing": missing}
        )
    tests = junit_counts(RESULTS / "pytest.xml")
    coverage = read_json("backend/lab15/results/coverage.json")
    browser = read_json("backend/lab10/results/after.json")
    load = read_json("backend/lab11/results/summary.json")
    zap = read_json("backend/lab12/results/zap-summary.json")
    cases = read_json("backend/lab5/results/cases.json")
    external = read_json("backend/lab9/results/newman-results.json")
    stability = read_json("backend/lab13/results/stability.json")
    full = read_json("backend/lab15/results/full-checks.json")
    runs = [run for run in (full, read_json("backend/lab15/results/checks.json")) if run]
    checks = max(runs, key=lambda run: run["completed_at"]) if runs else None
    totals = coverage["totals"] if coverage else {}
    core_coverage = round(totals.get("percent_covered", 0), 2)
    browser_stats = browser.get("stats", {}) if browser else {}
    load50 = (
        next((row for row in load["profiles"] if row["profile"] == "load50"), None)
        if load
        else None
    )
    zap_after = (
        next((row for row in zap["runs"] if row["variant"] == "after"), None) if zap else None
    )
    readiness = (
        tests["status"] == "PASS"
        and core_coverage >= 85
        and browser_stats.get("expected", 0) > 0
        and not any(browser_stats.get(key, 0) for key in ("unexpected", "flaky", "skipped"))
        and load50 is not None
        and load50["p95_ms"] <= 200
        and load50["error_rate_percent"] <= 1
        and zap_after is not None
        and zap_after["high"] == 0
        and cases is not None
        and all(case["status"] == "PASS" for case in cases["after"])
        and all(not report["missing"] for report in reports)
        and checks is not None
        and checks["passed"]
    )
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "reports": reports,
        "pytest": tests,
        "coverage": totals,
        "browser": browser_stats,
        "load": load,
        "zap": zap,
        "regression_stability": stability,
        "external_lab9": {
            key: external.get(key) for key in ("completedAt", "passed", "scenarios", "failures")
        }
        if external
        else None,
        "local_demo_ready": bool(readiness),
        "production_ready": False,
        "production_limits": [
            "login rate limiting",
            "HTTPS deployment hardening",
            "extended security review",
            "sustained load and endurance",
        ],
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    complexity = subprocess.run(
        [sys.executable, "-m", "radon", "cc", "-j", "backend/qa_shop/pricing.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    (RESULTS / "complexity.json").write_text(complexity, encoding="utf-8")
    decision = "GO" if readiness else "NO GO немесе тексеру толық емес"
    lines = [
        "# QA Shop нақты тексеру нәтижелері",
        "",
        f"Жаңартылғаны UTC: {summary['generated_at']}",
        "",
        f"Localhost оқу демонстрациясы: **{decision}**.",
        "Production: **NO GO**; rate limiting, deployment hardening, "
        "кеңейтілген security және endurance қажет.",
        "",
        "| Тексеру | Нақты нәтиже |",
        "|---|---|",
        f"| PDF есептері | {sum(not r['missing'] for r in reports)}/15; "
        f"тапсырмалар {sum(r['task_sections'] for r in reports)}/300 |",
        f"| Pytest | {tests.get('passed', 0)}/{tests.get('total', 0)} PASS; "
        f"failures {tests.get('failed', 0)}; errors {tests.get('errors', 0)}; "
        f"skipped {tests.get('skipped', 0)} |",
        f"| Pass Rate | {tests.get('pass_rate', 0)}% |",
        f"| Coverage combined statement/branch | {core_coverage}%; minimum 85% |",
        f"| Statements | {totals.get('covered_lines', 0)}/{totals.get('num_statements', 0)} |",
        f"| Branches | {totals.get('covered_branches', 0)}/{totals.get('num_branches', 0)} |",
        f"| Chromium | {browser_stats.get('expected', 0)} expected; "
        f"{browser_stats.get('unexpected', 0)} unexpected; "
        f"{browser_stats.get('skipped', 0)} skipped |",
        f"| 50 VU | p95 {load50['p95_ms'] if load50 else 'NOT RUN'} ms; "
        f"errors {load50['error_rate_percent'] if load50 else 'NOT RUN'}% |",
        f"| ZAP corrected | {zap_after['alert_count'] if zap_after else 'NOT RUN'} alerts |",
        "",
        "## Before және After",
        "",
        "| Suite | Before | After |",
        "|---|---|---|",
    ]
    for number in (4, 6, 13, 14):
        before = junit_counts(ROOT / f"backend/lab{number}/results/before.xml")
        after = junit_counts(ROOT / f"backend/lab{number}/results/after.xml")
        lines.append(
            f"| Lab {number} | {before.get('passed', 0)} passed / "
            f"{before.get('failed', 0)} failed | {after.get('passed', 0)} passed / "
            f"{after.get('failed', 0)} failed |"
        )
    if cases:
        lines.append(
            f"| Lab 5 catalogue | {sum(c['status'] == 'PASS' for c in cases['before'])}/20 PASS | "
            f"{sum(c['status'] == 'PASS' for c in cases['after'])}/20 PASS |"
        )
    lines += [
        "",
        "## Coverage scope",
        "",
        "Python qa_shop package; JavaScript және external API бұл пайызға кірмейді.",
        "",
        "| Source | Statements covered/total | Branches covered/total | Combined |",
        "|---|---|---|---|",
    ]
    for file, data in coverage.get("files", {}).items() if coverage else []:
        row = data["summary"]
        lines.append(
            f"| {file} | {row['covered_lines']}/{row['num_statements']} | "
            f"{row['covered_branches']}/{row['num_branches']} | {row['percent_covered']:.2f}% |"
        )
    lines += [
        "",
        "## Performance",
        "",
        "8-second local read profiles; spike 10→100→10 users. Бір host, production SLA емес.",
        "",
        "| Profile | VU | Requests | Failed | Average ms | p95 ms | RPS |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in load["profiles"] if load else []:
        lines.append(
            f"| {row['profile']} | {row['users']} | {row['requests']} | {row['failures']} | "
            f"{row['average_ms']:.2f} | {row['p95_ms']} | {row['requests_per_second']:.2f} |"
        )
    lines += [
        "",
        "![Performance graph](../../lab11/results/performance.svg)",
        "",
        "## ZAP passive scan",
        "",
        "| Variant | Version | Alerts | High | Medium |",
        "|---|---|---:|---:|---:|",
    ]
    for row in zap["runs"] if zap else []:
        lines.append(
            f"| {row['variant']} | {row['version']} | {row['alert_count']} | "
            f"{row['high']} | {row['medium']} |"
        )
    lines += [
        "",
        "Scope: тек local shop pages/assets және public catalogue/search; "
        "authenticated passive scan немесе толық pentest емес.",
        "",
        "## External Lab 9",
        "",
    ]
    if external:
        lines += [
            f"DummyJSON, recorded {external.get('completedAt')}: {external.get('scenarios')}. "
            "Нақты assertion failures [Lab 9 есебінде](../../lab9/results/RUN_RESULTS.md).",
            "Third-party finding жергілікті corrected pytest нәтижесіне қосылмайды; "
            "профильдің password өрісі бойынша LAB9-01 ашық finding ретінде сақталған.",
        ]
    else:
        lines.append("Newman нәтижесі жоқ; external run орындалмаған.")
    lines += ["", "## Quality stages", "", "| Stage | Exit | Seconds |", "|---|---:|---:|"]
    for stage in checks["stages"] if checks else []:
        lines.append(
            f"| {stage['name']} | {stage['exit_code']} | {stage['duration_seconds']:.2f} |"
        )
    lines += [
        "",
        "## Қабылдау шектері",
        "",
        "Remote GitHub Actions run push/dispatch кейін орындалады. Long endurance — жоспар; "
        "толық production release осы оқу тексерулеріне кірмейді.",
        "",
        "Дәлелдер: [JUnit](pytest.xml), [coverage](coverage.json), [checks](checks.json), "
        "[full checks](full-checks.json), [JSON summary](summary.json).",
        "",
    ]
    (RESULTS / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    content = html.escape("\n".join(lines))
    page = (
        '<!doctype html><html lang="kk"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>QA Shop тексеру нәтижелері</title><style>"
        "body{max-width:1100px;margin:40px auto;padding:20px;background:#f4f7fb;color:#17263d;"
        "font:15px/1.65 system-ui}pre{white-space:pre-wrap;overflow-wrap:anywhere}"
        "</style><h1>QA Shop тексеру нәтижелері</h1><pre>" + content + "</pre></html>"
    )
    (RESULTS / "report.html").write_text(page, encoding="utf-8")
    print(
        f"Reports: {sum(not r['missing'] for r in reports)}/15; "
        f"tests: {tests}; coverage: {core_coverage}%"
    )
    return int(any(report["missing"] for report in reports))


if __name__ == "__main__":
    raise SystemExit(main())
