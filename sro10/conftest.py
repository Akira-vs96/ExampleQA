"""Real Chromium, a temporary database, HTTP evidence and reproducible reports."""

import json
import re
import socket
import sys
import time
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from threading import Thread
from uuid import uuid4

import pytest
import uvicorn
from playwright.sync_api import sync_playwright

from app.main import create_app

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RECORDS: list[dict] = []
BROWSER_VERSION = ""


@pytest.fixture(scope="session")
def web_base_url(tmp_path_factory):
    database = tmp_path_factory.mktemp("sro10") / "shop.sqlite3"
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(128)
        server = uvicorn.Server(uvicorn.Config(
            create_app(database), host="127.0.0.1", loop="asyncio",
            log_level="error", access_log=False,
        ))
        worker = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        worker.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started:
                if not worker.is_alive() or time.monotonic() > deadline:
                    raise RuntimeError("SRO10 server did not start")
                time.sleep(0.02)
            yield f"http://127.0.0.1:{listener.getsockname()[1]}"
        finally:
            server.should_exit = True
            worker.join(timeout=10)
            if worker.is_alive():
                raise RuntimeError("SRO10 server did not stop")


@pytest.fixture(scope="session")
def web_browser():
    global BROWSER_VERSION
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        BROWSER_VERSION = browser.version
        yield browser
        browser.close()


@pytest.fixture
def web_page(web_browser, web_base_url, request):
    context = web_browser.new_context(
        base_url=web_base_url, viewport={"width": 1440, "height": 900}, locale="kk-KZ"
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    network = []

    def capture(response):
        if "/api/shop/" not in response.url:
            return
        payload = response.request.post_data_json
        if isinstance(payload, dict) and "password" in payload:
            payload = {**payload, "password": "[test password redacted]"}
        network.append({
            "method": response.request.method,
            "path": response.url.removeprefix(web_base_url),
            "status": response.status,
            "request_json": payload,
            "content_type": response.headers.get("content-type"),
        })

    page.on("response", capture)
    page.goto("/shop.html")
    yield page
    name = re.sub(r"[^A-Za-z0-9_-]", "_", request.node.name)
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "screenshots").mkdir(exist_ok=True)
    (RESULTS / f"{name}.http.json").write_text(
        json.dumps(network, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    page.screenshot(path=str(RESULTS / "screenshots" / f"{name}.png"), full_page=True)
    report = getattr(request.node, "web_report", None)
    if report and (report.failed or hasattr(report, "wasxfail")):
        context.tracing.stop(path=str(RESULTS / f"{name}.trace.zip"))
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture
def web_credentials():
    return {"username": f"sro10_{uuid4().hex[:12]}", "password": "Sro10_Test_2026"}


@pytest.fixture
def web_signed_page(web_page, web_credentials):
    assert web_page.request.post("/api/shop/register", data=web_credentials).status == 201
    assert web_page.request.post("/api/shop/login", data=web_credentials).status == 200
    return web_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    if report.when == "call":
        item.web_report = report


def pytest_runtest_logreport(report):
    if not report.nodeid.replace("\\", "/").startswith(("sro10/", "test_web.py")):
        return
    if report.when != "call" and not report.failed:
        return
    match = re.search(r"test_web(\d+)_", report.nodeid)
    status = report.outcome if report.when == "call" else "error"
    if hasattr(report, "wasxfail"):
        status = "xfailed" if report.skipped else "xpassed"
    RECORDS.append({
        "case": f"WEB-{int(match[1]):02}" if match else "setup/teardown",
        "test": report.nodeid,
        "outcome": status,
        "duration_seconds": round(report.duration, 3),
        "reason": str(getattr(report, "wasxfail", "")),
        "details": str(report.longrepr) if report.failed or hasattr(report, "wasxfail") else "",
    })


def pytest_sessionfinish(session):
    if session.config.option.collectonly or not RECORDS:
        return
    RESULTS.mkdir(exist_ok=True)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "exit_code": int(session.exitstatus),
        "versions": {
            "python": sys.version.split()[0], "chromium": BROWSER_VERSION,
            **{name: version(name) for name in ("pytest", "playwright", "fastapi", "uvicorn")},
        },
        "counts": {
            key: sum(row["outcome"] == key for row in RECORDS)
            for key in ("passed", "failed", "error", "xfailed", "xpassed", "skipped")
        },
        "tests": RECORDS,
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
