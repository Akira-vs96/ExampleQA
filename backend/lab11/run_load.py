"""Start an isolated local server, run six Locust profiles and save a comparison chart."""

import csv
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
DIRECTORY = Path(__file__).resolve().parent


def free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def main() -> int:
    result_dir = DIRECTORY / "results"
    result_dir.mkdir(exist_ok=True)
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    records = []
    with tempfile.TemporaryDirectory(prefix="qa-load-") as temp:
        with (result_dir / "server.log").open("w", encoding="utf-8") as server_log:
            server = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--app-dir",
                    "backend",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(port),
                    "--no-access-log",
                    "--no-server-header",
                ],
                cwd=ROOT,
                env={**os.environ, "QA_DATABASE": str(Path(temp) / "shop.sqlite3")},
                stdout=server_log,
                stderr=subprocess.STDOUT,
            )
            try:
                with httpx.Client(trust_env=False, timeout=1) as client:
                    for _ in range(100):
                        try:
                            if client.get(base + "/api/health").status_code == 200:
                                break
                        except httpx.TransportError:
                            pass
                        time.sleep(0.1)
                    else:
                        raise RuntimeError("Local load-test server did not start.")
                for label, users in [
                    ("baseline", 1),
                    ("load10", 10),
                    ("load25", 25),
                    ("load50", 50),
                    ("stress100", 100),
                    ("spike", 100),
                ]:
                    prefix = result_dir / label
                    command = [
                        sys.executable,
                        "-m",
                        "locust",
                        "-f",
                        str(DIRECTORY / "locustfile.py"),
                        "--host",
                        base,
                        "--headless",
                        "--csv",
                        str(prefix),
                        "--csv-full-history",
                        "--only-summary",
                        "--exit-code-on-error",
                        "1",
                    ]
                    env = {**os.environ, "LOCUST_SPIKE": "1" if label == "spike" else "0"}
                    if label != "spike":
                        command += [
                            "--users",
                            str(users),
                            "--spawn-rate",
                            str(users),
                            "--run-time",
                            "8s",
                        ]
                    started = time.perf_counter()
                    result = subprocess.run(
                        command, cwd=ROOT, capture_output=True, text=True, env=env, timeout=45
                    )
                    (result_dir / f"{label}.log").write_text(
                        result.stdout + result.stderr, encoding="utf-8"
                    )
                    if not Path(str(prefix) + "_stats.csv").exists():
                        raise RuntimeError(f"Locust did not produce CSV: {label}")
                    with Path(str(prefix) + "_stats.csv").open(encoding="utf-8") as file:
                        row = next(
                            row for row in csv.DictReader(file) if row["Name"] == "Aggregated"
                        )
                    count = int(row["Request Count"])
                    failures = int(row["Failure Count"])
                    records.append(
                        {
                            "profile": label,
                            "users": users,
                            "requests": count,
                            "failures": failures,
                            "error_rate_percent": round(100 * failures / count, 3)
                            if count
                            else 100,
                            "average_ms": float(row["Average Response Time"]),
                            "p95_ms": float(row["95%"]),
                            "requests_per_second": float(row["Requests/s"]),
                            "wall_seconds": round(time.perf_counter() - started, 3),
                            "exit_code": result.returncode,
                        }
                    )
                    print(json.dumps(records[-1]), flush=True)
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)
    summary = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "target": "isolated localhost",
        "workload": "75% catalogue, 25% case-insensitive search; think time 20–50 ms",
        "limits": "8-second profiles measure this host only; endurance is a separate plan",
        "profiles": records,
    }
    (result_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    bars = []
    maximum = max(row["p95_ms"] for row in records) or 1
    for index, row in enumerate(records):
        y = 55 + index * 45
        width = 450 * row["p95_ms"] / maximum
        bars.append(
            f'<text x="20" y="{y + 18}">{row["profile"]}</text>'
            f'<rect x="140" y="{y}" width="{width:.1f}" height="25" fill="#5586b6"/>'
            f'<text x="{150 + width:.1f}" y="{y + 18}">{row["p95_ms"]} ms</text>'
        )
    chart = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="360" '
        'viewBox="0 0 760 360"><rect width="760" height="360" fill="#f4f7fb"/>'
        '<g font-family="sans-serif" font-size="14" fill="#17263d">'
        '<text x="20" y="28" font-size="20">Locust: p95 response time by workload</text>'
        + "".join(bars)
        + "</g></svg>"
    )
    (result_dir / "performance.svg").write_text(chart, encoding="utf-8")
    return int(any(row["exit_code"] != 0 or row["requests"] == 0 for row in records))


if __name__ == "__main__":
    raise SystemExit(main())
