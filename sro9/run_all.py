"""Run real checks, keep their evidence and export the assignment report."""

import json
import shlex
import socket
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from threading import Thread

import uvicorn

from sro9.app import create_app
from sro9.generate_postman import generate

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "sro9"
RESULTS = HERE / "results"


def run(command: list[str], name: str, expected_exit: int = 0) -> None:
    completed = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=120, check=False
    )
    output = completed.stdout + completed.stderr
    print(output, end="", flush=True)
    (RESULTS / f"{name}.log").write_text(
        f"$ {shlex.join(command)}\n{output}\nExit code: {completed.returncode}\n",
        encoding="utf-8",
    )
    print(f"{name}: exit {completed.returncode}", flush=True)
    if completed.returncode != expected_exit:
        raise RuntimeError(f"{name} failed; see {RESULTS / f'{name}.log'}\n{output}")


def junit(name: str) -> dict:
    suite = ET.parse(RESULTS / f"{name}.xml").getroot().find("testsuite")
    if suite is None:
        raise RuntimeError(f"Missing JUnit suite: {name}")
    stats = {key: int(suite.attrib[key]) for key in ("tests", "failures", "errors", "skipped")}
    stats["passed"] = stats["tests"] - stats["failures"] - stats["errors"] - stats["skipped"]
    return stats


def run_newman() -> dict:
    candidates = [
        HERE / "node_modules/newman/bin/newman.js",
        ROOT / "backend/lab9/node_modules/newman/bin/newman.js",
    ]
    executable = next((path for path in candidates if path.exists()), None)
    if executable is None:
        raise RuntimeError("Install Newman: npm install --prefix sro9 --no-audit --no-fund")

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(128)
        base_url = f"http://127.0.0.1:{listener.getsockname()[1]}"
        server = uvicorn.Server(uvicorn.Config(
            create_app(), host="127.0.0.1", loop="asyncio", log_level="error", access_log=False
        ))
        worker = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        worker.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started:
                if not worker.is_alive() or time.monotonic() > deadline:
                    raise RuntimeError("Local API failed to start")
                time.sleep(0.02)
            run([
                "node", str(executable), "run", str(HERE / "SRO9.postman_collection.json"),
                "-e", str(HERE / "SRO9.postman_environment.json"),
                "--env-var", f"base_url={base_url}", "--reporters", "cli,json",
                "--reporter-json-export", str(RESULTS / "newman.json"),
                "--timeout", "60000", "--timeout-request", "5000",
                "--timeout-script", "5000", "--color", "off",
            ], "newman")
        finally:
            server.should_exit = True
            worker.join(timeout=10)
            if worker.is_alive():
                raise RuntimeError("Local API failed to stop")
    data = json.loads((RESULTS / "newman.json").read_text(encoding="utf-8"))
    if data["run"]["failures"]:
        raise RuntimeError("Newman reported failures")
    return data


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    generate()
    common = [sys.executable, "-m", "pytest", "-c", "sro9/pyproject.toml", "-v"]
    run(common + ["sro9/test_api.py", f"--junitxml={RESULTS / 'pytest.xml'}"], "pytest")
    if junit("before")["failures"] != 1 or junit("before")["errors"]:
        raise RuntimeError("The intentional failure must be one assertion failure")
    data = run_newman()
    packages = ["fastapi", "pydantic", "pytest", "httpx", "uvicorn"]
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "versions": {"python": sys.version.split()[0], **{p: version(p) for p in packages}},
        "pytest": junit("pytest"),
        "wrong_url": junit("before"),
        "correct_url": junit("after"),
        "newman": {
            key: data["run"]["stats"][key] for key in ("requests", "assertions")
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    from sro9.build_report import build_report

    report = build_report(summary, data)
    print(report)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
