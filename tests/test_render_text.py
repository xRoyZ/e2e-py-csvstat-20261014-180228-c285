"""Tests for the aligned plain-text report renderer."""

from __future__ import annotations

import re

from csvstat.model import ColumnStats
from csvstat.render_text import render_text


def numeric_column() -> ColumnStats:
    return ColumnStats(
        name="amount",
        kind="numeric",
        count=3,
        missing=1,
        minimum=1.5,
        maximum=9.0,
        mean=5.0,
        unique=None,
    )


def text_column() -> ColumnStats:
    return ColumnStats(
        name="city",
        kind="text",
        count=4,
        missing=0,
        minimum=None,
        maximum=None,
        mean=None,
        unique=3,
    )


def test_numeric_column_reports_all_statistics() -> None:
    report = render_text([numeric_column()])
    assert "amount" in report
    assert "numeric" in report
    for label in ("count", "min", "max", "mean", "missing"):
        assert label in report
    assert "1.5" in report
    assert "9" in report
    assert "5" in report
    assert "-" in report  # unique is not applicable to a numeric column


def test_text_column_reports_count_and_unique() -> None:
    report = render_text([text_column()])
    assert "city" in report
    assert "text" in report
    assert "unique" in report
    assert "3" in report


def test_all_missing_numeric_column_uses_placeholder() -> None:
    column = ColumnStats(
        name="amount",
        kind="numeric",
        count=0,
        missing=5,
        minimum=None,
        maximum=None,
        mean=None,
        unique=None,
    )
    report = render_text([column])
    assert "amount" in report
    assert "missing" in report
    assert "5" in report
    assert "-" in report


def test_report_is_column_aligned() -> None:
    report = render_text([numeric_column(), text_column()])
    lines = report.splitlines()
    assert len(lines) >= 3
    starts = {re.search(r"\s{2,}", line).end() for line in lines}
    assert len(starts) == 1
    assert "amount" in report
    assert "city" in report


def test_control_characters_and_ansi_are_neutralised() -> None:
    column = ColumnStats(
        name="\x1b[31mevil\x1b[0m\nname\twith\rcontrols",
        kind="numeric",
        count=1,
        missing=0,
        minimum=1.0,
        maximum=1.0,
        mean=1.0,
        unique=None,
    )
    report = render_text([column])
    assert "\x1b" not in report
    assert "31m" not in report
    assert "evil name with controls" in report


def test_empty_report_does_not_crash() -> None:
    assert render_text([]) != ""
