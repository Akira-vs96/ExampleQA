"""Automatically add a before/after console report for every selected SRO."""

import os
from pathlib import Path

import pytest

from scripts.sro_comparison import CHILD_FLAG, ROOT, compare, render


def pytest_configure(config: pytest.Config) -> None:
    if os.environ.get(CHILD_FLAG) != "1" and not config.pluginmanager.hasplugin(
        "sro-comparison-reporter"
    ):
        config.pluginmanager.register(ComparisonReporter(), "sro-comparison-reporter")


class ComparisonReporter:
    def __init__(self) -> None:
        self.assignments: set[Path] = set()
        self.comparisons: list[dict] = []

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        for item in items:
            path = item.path.resolve()
            if not path.name.startswith("test_"):
                continue
            for parent in path.parents:
                if parent.parent == ROOT and (parent / "comparison.json").exists():
                    self.assignments.add(parent)
                    break

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        # Discovery and collect-only must not execute tests or produce reports.
        if session.config.option.collectonly or session.exitstatus not in (0, 1):
            return
        for assignment in sorted(self.assignments):
            comparison = compare(assignment)
            self.comparisons.append(comparison)
            if not comparison["ok"]:
                session.exitstatus = pytest.ExitCode.TESTS_FAILED

    def pytest_terminal_summary(self, terminalreporter) -> None:
        for comparison in self.comparisons:
            terminalreporter.write_sep("=", f"{comparison['assignment'].upper()} BEFORE / AFTER")
            for line in render(comparison):
                terminalreporter.write_line(line)
