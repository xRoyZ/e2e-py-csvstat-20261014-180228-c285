"""Tests for column selection by name."""

from __future__ import annotations

import pytest

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData
from csvstat.selection import select_columns


def make_columns() -> list[ColumnData]:
    return [
        ColumnData(name="ort", values=["Berlin", "Hamburg"]),
        ColumnData(name="betrag", values=["1.5", "2.5"]),
        ColumnData(name="note", values=["a", "b"]),
    ]


def test_subset_keeps_given_order_regardless_of_file_order() -> None:
    columns = make_columns()
    result = select_columns(columns, ["betrag", "ort"])
    assert [column.name for column in result] == ["betrag", "ort"]


def test_single_column_works() -> None:
    columns = make_columns()
    result = select_columns(columns, ["note"])
    assert len(result) == 1
    assert result[0].name == "note"
    assert result[0].values == ["a", "b"]


def test_only_requested_columns_are_returned() -> None:
    columns = make_columns()
    result = select_columns(columns, ["ort"])
    assert all(column.name == "ort" for column in result)
    assert not any(column.name == "betrag" for column in result)


def test_unknown_name_raises_and_names_only_that_column() -> None:
    columns = make_columns()
    with pytest.raises(CsvStatError) as excinfo:
        select_columns(columns, ["unbekannt"])

    message = excinfo.value.message
    assert "unbekannt" in message
    assert "1.5" not in message
    assert "Berlin" not in message
    assert "betrag" not in message
    assert "ort" not in message
    assert "\n" not in message
