"""Tests for the csvstat CLI skeleton."""

from __future__ import annotations

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "csvstat", *args],
        capture_output=True,
        text=True,
    )


def test_help_exits_zero_and_lists_all_options() -> None:
    result = run_cli("--help")
    assert result.returncode == 0
    assert "--delimiter" in result.stdout
    assert "--columns" in result.stdout
    assert "--json" in result.stdout


def test_unfilled_step_exits_nonzero_with_one_line_on_stderr() -> None:
    result = run_cli("does-not-exist.csv")
    assert result.returncode != 0
    assert result.stdout == ""
    assert result.stderr.strip() != ""
    assert len(result.stderr.strip().splitlines()) == 1
    assert "Traceback" not in result.stderr
