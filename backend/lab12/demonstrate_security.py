"""Reproduce SQL injection in the isolated before module; verify corrected storage."""

import json
import sqlite3
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from lab12.before.security import login, search_html
from qa_shop.store import Store


def main() -> int:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users(username TEXT, password TEXT)")
    connection.execute("INSERT INTO users VALUES ('student', 'secret')")
    injected = login(connection, "' OR 1=1 --", "wrong")
    assert injected is not None
    payload = "<script>alert(1)</script>"
    assert payload in search_html(payload)
    connection.close()
    with tempfile.TemporaryDirectory() as temp:
        store = Store(Path(temp) / "users.sqlite3")
        store.register("student", "Test_password_2026")
        blocked = store.login("' OR 1=1 --", "wrong") is None
    result = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "sql_injection_before": "authentication bypass reproduced",
        "sql_injection_after": "blocked" if blocked else "FAILED",
        "xss_before": "raw script tag in HTML reproduced",
        "xss_after": "DOM textContent; see Playwright invalid input is rendered safely",
        "passed": blocked,
    }
    destination = Path(__file__).with_name("results")
    destination.mkdir(exist_ok=True)
    (destination / "before_after.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return int(not blocked)


if __name__ == "__main__":
    raise SystemExit(main())
