"""Tests for the JSON report renderer."""

from __future__ import annotations

import json

from csvstat.model import ColumnStats
from csvstat.render_json import render_json


def numeric_column(
    *,
    name: str = "betrag",
    count: int = 3,
    missing: int = 1,
    minimum: float | int | None = 1.0,
    maximum: float | int | None = 5.0,
    mean: float | None = 3.0,
) -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="numeric",
        count=count,
        missing=missing,
        minimum=minimum,
        maximum=maximum,
        mean=mean,
        unique=None,
    )


def text_column(
    *,
    name: str = "ort",
    count: int = 3,
    missing: int = 1,
    unique: int | None = 2,
) -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="text",
        count=count,
        missing=missing,
        minimum=None,
        maximum=None,
        mean=None,
        unique=unique,
    )


def test_output_is_one_valid_json_document() -> None:
    output = render_json([numeric_column(), text_column()])
    parsed = json.loads(output)
    assert isinstance(parsed, list)
    assert len(parsed) == 2


def test_output_contains_no_text_outside_the_json_document() -> None:
    output = render_json([numeric_column()])
    assert output.strip() == output
    assert output.strip().startswith("[")
    assert output.strip().endswith("]")
    json.loads(output)


def test_numeric_column_has_the_ac07_keys() -> None:
    parsed = json.loads(render_json([numeric_column()]))
    assert set(parsed[0]) == {
        "name",
        "type",
        "count",
        "min",
        "max",
        "mean",
        "missing",
    }
    assert parsed[0]["name"] == "betrag"
    assert parsed[0]["type"] == "numeric"
    assert parsed[0]["count"] == 3
    assert parsed[0]["min"] == 1.0
    assert parsed[0]["max"] == 5.0
    assert parsed[0]["mean"] == 3.0
    assert parsed[0]["missing"] == 1


def test_text_column_has_the_ac07_keys() -> None:
    parsed = json.loads(render_json([text_column()]))
    assert set(parsed[0]) == {"name", "type", "count", "unique"}
    assert parsed[0]["name"] == "ort"
    assert parsed[0]["type"] == "text"
    assert parsed[0]["count"] == 3
    assert parsed[0]["unique"] == 2


def test_all_missing_numeric_column_yields_null_statistics() -> None:
    column = numeric_column(count=0, missing=3, minimum=None, maximum=None, mean=None)
    parsed = json.loads(render_json([column]))
    assert parsed[0]["min"] is None
    assert parsed[0]["max"] is None
    assert parsed[0]["mean"] is None
    assert parsed[0]["count"] == 0
    assert parsed[0]["missing"] == 3


def test_empty_column_list_yields_an_empty_json_array() -> None:
    assert json.loads(render_json([])) == []
