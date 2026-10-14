"""Tests for csvstat.reader.read_columns."""

from __future__ import annotations

import pathlib

import pytest

from csvstat.errors import CsvStatError
from csvstat.reader import read_columns


def _write(tmp_path: pathlib.Path, name: str, text: str) -> pathlib.Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_reads_comma_separated_file(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "data.csv", "name,age\nAlice,30\nBob,40\n")

    columns = read_columns(path, ",")

    assert [column.name for column in columns] == ["name", "age"]
    assert columns[0].values == ["Alice", "Bob"]
    assert columns[1].values == ["30", "40"]


def test_reads_semicolon_separated_file(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "data.csv", "name;age\nAlice;30\nBob;40\n")

    columns = read_columns(path, ";")

    assert [column.name for column in columns] == ["name", "age"]
    assert columns[0].values == ["Alice", "Bob"]
    assert columns[1].values == ["30", "40"]


def test_blank_and_whitespace_fields_become_none(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "data.csv", "a,b,c\n1,,  \n2,x,\t\n")

    columns = read_columns(path, ",")

    assert columns[0].values == ["1", "2"]
    assert columns[1].values == [None, "x"]
    assert columns[2].values == [None, None]


def test_missing_file_raises_and_names_path(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "does-not-exist.csv"

    with pytest.raises(CsvStatError) as excinfo:
        read_columns(path, ",")

    assert str(path) in excinfo.value.message


def test_zero_byte_file_raises(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "empty.csv", "")

    with pytest.raises(CsvStatError):
        read_columns(path, ",")


def test_header_only_file_raises(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "header.csv", "name,age\n")

    with pytest.raises(CsvStatError):
        read_columns(path, ",")


def test_header_only_error_names_path(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "header.csv", "name,age\n")

    with pytest.raises(CsvStatError) as excinfo:
        read_columns(path, ",")

    assert str(path) in excinfo.value.message


def test_read_does_not_write_or_create_files(tmp_path: pathlib.Path) -> None:
    path = _write(tmp_path, "data.csv", "a,b\n1,2\n")
    before = sorted(entry.name for entry in tmp_path.iterdir())

    read_columns(path, ",")

    after = sorted(entry.name for entry in tmp_path.iterdir())
    assert after == before
