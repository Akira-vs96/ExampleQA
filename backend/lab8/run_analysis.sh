#!/usr/bin/env bash
set -euo pipefail

LAB8_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$LAB8_DIR/.." && pwd)"
cd "$BACKEND_DIR"

PYTHON=".venv/bin/python"
RUFF=".venv/bin/ruff"
PYLINT=".venv/bin/pylint"
RADON=".venv/bin/radon"

if [[ ! -x "$RUFF" || ! -x "$PYLINT" || ! -x "$RADON" ]]; then
    echo "Алдымен: .venv/bin/python -m pip install -r requirements-dev.txt" >&2
    exit 2
fi

echo "1) Бастапқы нұсқа (ақаулар күтіледі)"
"$RUFF" check --config pyproject.toml lab8/before || true
PYTHONPATH=. "$PYLINT" --rcfile=pyproject.toml lab8/before || true
"$RADON" cc -s -a lab8/before
"$RADON" raw -s lab8/before/order_service.py lab8/before/refund_service.py

echo
echo "2) Түзетілген нұсқа (Quality Gate)"
"$RUFF" check --config pyproject.toml lab8/order_service.py lab8/refund_service.py
PYTHONPATH=. "$PYLINT" --rcfile=pyproject.toml lab8/order_service.py lab8/refund_service.py
"$RADON" cc -s -a lab8/order_service.py lab8/refund_service.py
"$RADON" raw -s lab8/order_service.py lab8/refund_service.py
"$PYTHON" -m pytest -q lab8/tests

echo
echo "QUALITY GATE: PASSED"
