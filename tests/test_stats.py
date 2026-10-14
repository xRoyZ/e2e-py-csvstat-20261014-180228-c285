"""Tests for :func:`csvstat.stats.compute_stats`."""

from __future__ import annotations

import pytest

from csvstat.model import ColumnData
from csvstat.stats import compute_stats


def test_numeric_column_with_ints_and_floats() -> None:
    column = ColumnData(name="betrag", values=["1", "2.5", "3", "4.5"])

    (stats,) = compute_stats([column])

    assert stats.kind == "numeric"
    assert stats.count == 4
    assert stats.missing == 0
    assert stats.minimum == 1
    assert stats.maximum == 4.5
    assert stats.mean == pytest.approx(2.75)
    assert stats.unique is None


def test_all_missing_numeric_column_returns_none_without_crashing() -> None:
    column = ColumnData(name="betrag", values=[None, None, None])

    (stats,) = compute_stats([column])

    assert stats.kind == "numeric"
    assert stats.count == 0
    assert stats.missing == 3
    assert stats.minimum is None
    assert stats.maximum is None
    assert stats.mean is None
    assert stats.unique is None


def test_numeric_values_tolerate_surrounding_whitespace() -> None:
    column = ColumnData(name="betrag", values=[" 1 ", "\t2.5", "3 \n"])

    (stats,) = compute_stats([column])

    assert stats.kind == "numeric"
    assert stats.count == 3
    assert stats.missing == 0
    assert stats.minimum == 1
    assert stats.maximum == 3
    assert stats.mean == pytest.approx(2.1666, rel=1e-3)


def test_text_column_counts_unique_values_and_ignores_blanks() -> None:
    column = ColumnData(
        name="ort",
        values=["Berlin", "Berlin", "Hamburg", None, "  ", "", "Hamburg"],
    )

    (stats,) = compute_stats([column])

    assert stats.kind == "text"
    assert stats.count == 4
    assert stats.missing == 3
    assert stats.unique == 2
    assert stats.minimum is None
    assert stats.maximum is None
    assert stats.mean is None


def test_mixed_column_is_reported_as_text() -> None:
    column = ColumnData(name="gemischt", values=["1", "2", "abc", "3"])

    (stats,) = compute_stats([column])

    assert stats.kind == "text"
    assert stats.count == 4
    assert stats.missing == 0
    assert stats.unique == 4
    assert stats.minimum is None
    assert stats.maximum is None
    assert stats.mean is None


def test_stats_preserve_column_order() -> None:
    columns = [
        ColumnData(name="a", values=["1", "2"]),
        ColumnData(name="b", values=["x", "y"]),
    ]

    result = compute_stats(columns)

    assert [stats.name for stats in result] == ["a", "b"]
    assert [stats.kind for stats in result] == ["numeric", "text"]
