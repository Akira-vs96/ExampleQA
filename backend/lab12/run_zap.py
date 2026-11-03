"""Run the real ZAP passive scanner against two isolated loopback-only applications."""

import json
import os
import secrets
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


def wait_for(client: httpx.Client, url: str, seconds: int = 60) -> None:
    for _ in range(seconds * 5):
        try:
            if client.get(url).status_code == 200:
                return
        except httpx.TransportError:
            pass
        time.sleep(0.2)
    raise RuntimeError(f"Local service did not become ready: {url}")


def stop(process: subprocess.Popen) -> None:
    process.terminate()
    try:
        process.wait(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    zap_home = Path(os.getenv("ZAP_HOME", ROOT / "tools/vendor/ZAP_2.17.0"))
    launcher = zap_home / "zap.sh"
    if not launcher.is_file():
        raise SystemExit("Install ZAP from https://www.zaproxy.org/download/ and set ZAP_HOME.")
    destination = DIRECTORY / "results"
    destination.mkdir(exist_ok=True)
    summary = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "scanner": "ZAP passive scanner",
        "scope": "only two isolated 127.0.0.1 apps; no active scan or external targets",
        "runs": [],
    }
    for variant, entry in [("before", "lab12.before.app:app"), ("after", "app.main:app")]:
        with tempfile.TemporaryDirectory(prefix=f"qa-zap-{variant}-") as temp:
            web_port, proxy_port = free_port(), free_port()
            api_key = secrets.token_hex(24)
            target = f"http://127.0.0.1:{web_port}"
            proxy = f"http://127.0.0.1:{proxy_port}"
            with (
                (destination / f"{variant}-server.log").open("w") as web_log,
                (destination / f"{variant}-zap.log").open("w") as zap_log,
            ):
                web = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "uvicorn",
                        entry,
                        "--app-dir",
                        "backend",
                        "--host",
                        "127.0.0.1",
                        "--port",
                        str(web_port),
                        "--no-server-header",
                    ],
                    cwd=ROOT,
                    env={**os.environ, "QA_DATABASE": str(Path(temp) / "shop.sqlite3")},
                    stdout=web_log,
                    stderr=subprocess.STDOUT,
                )
                zap = subprocess.Popen(
                    [
                        "bash",
                        str(launcher),
                        "-daemon",
                        "-silent",
                        "-host",
                        "127.0.0.1",
                        "-port",
                        str(proxy_port),
                        "-dir",
                        str(Path(temp) / "zap"),
                        "-config",
                        f"api.key={api_key}",
                        "-config",
                        "autoupdate.checkOnStart=false",
                    ],
                    cwd=ROOT,
                    stdout=zap_log,
                    stderr=subprocess.STDOUT,
                )
                try:
                    with httpx.Client(trust_env=False, timeout=10) as client:
                        wait_for(client, target + "/shop.html", 20)
                        wait_for(client, proxy + f"/JSON/core/view/version/?apikey={api_key}")

                        def call(component, kind, action, _proxy=proxy, _key=api_key, **params):
                            response = client.get(
                                f"{_proxy}/JSON/{component}/{kind}/{action}/",
                                params={"apikey": _key, **params},
                            )
                            response.raise_for_status()
                            data = response.json()
                            if "code" in data and "message" in data:
                                raise RuntimeError(f"ZAP {action}: {data['message']}")
                            return data

                        version = call("core", "view", "version")["version"]
                        paths = ["/shop.html", "/api/shop/products"]
                        if variant == "after":
                            paths += ["/shop.js", "/styles.css", "/api/shop/products?q=Keyboard"]
                        for path in paths:
                            call(
                                "core",
                                "action",
                                "accessUrl",
                                url=target + path,
                                followRedirects="false",
                            )
                        for _ in range(100):
                            if int(call("pscan", "view", "recordsToScan")["recordsToScan"]) == 0:
                                break
                            time.sleep(0.2)
                        else:
                            raise RuntimeError("ZAP passive queue did not drain.")
                        alerts = call(
                            "core", "view", "alerts", baseurl=target, start=0, count=1000
                        )["alerts"]
                        urls = call("core", "view", "urls", baseurl=target)["urls"]
                        if not urls:
                            raise RuntimeError("ZAP did not observe the target traffic.")
                        report = {
                            "variant": variant,
                            "version": version,
                            "target": target,
                            "observed_urls": urls,
                            "alerts": alerts,
                            "alert_count": len(alerts),
                            "high": sum(alert["risk"] == "High" for alert in alerts),
                            "medium": sum(alert["risk"] == "Medium" for alert in alerts),
                        }
                        (destination / f"zap-{variant}.json").write_text(
                            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8",
                        )
                        summary["runs"].append(
                            {
                                key: report[key]
                                for key in ("variant", "version", "alert_count", "high", "medium")
                            }
                        )
                        print(json.dumps(summary["runs"][-1]), flush=True)
                finally:
                    stop(zap)
                    stop(web)
            # Keep the randomly generated ZAP API key out of persisted console logs.
            for path in destination.glob(f"{variant}-*.log"):
                path.write_text(path.read_text(errors="replace").replace(api_key, "[REDACTED]"))
    (destination / "zap-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return int(summary["runs"][-1]["high"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
