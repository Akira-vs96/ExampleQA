#!/usr/bin/env bash
set -euo pipefail

LAB8_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$LAB8_DIR/.." && pwd)"
cd "$BACKEND_DIR"
if [[ -n "${QA_PYTHON:-}" ]]; then
    PYTHON="$QA_PYTHON"
elif [[ -x "../.venv/bin/python" ]]; then
    PYTHON="../.venv/bin/python"
else
    PYTHON=".venv/bin/python"
fi

echo "1) Бастапқы нұсқа (ақаулар күтіледі)"
"$PYTHON" -m ruff check --config pyproject.toml lab8/before || true
PYTHONPATH=. "$PYTHON" -m pylint --rcfile=pyproject.toml lab8/before || true
"$PYTHON" -m radon cc -s -a lab8/before
"$PYTHON" -m radon raw -s lab8/before/order_service.py lab8/before/refund_service.py

echo "2) Түзетілген нұсқа (Quality Gate)"
"$PYTHON" -m ruff check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. "$PYTHON" -m pylint --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
"$PYTHON" -m radon cc -s -a lab8/order_service.py lab8/refund_service.py
"$PYTHON" -m radon raw -s lab8/order_service.py lab8/refund_service.py
"$PYTHON" -m pytest -q lab8/tests
echo "QUALITY GATE: PASSED"
