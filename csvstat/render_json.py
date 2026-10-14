"""Render the report as a single JSON document."""

from __future__ import annotations

import json

from csvstat.model import ColumnStats


def _column_to_dict(column: ColumnStats) -> dict[str, object]:
    """Map one column's statistics onto its JSON object.

    Numeric columns carry ``count``, ``min``, ``max``, ``mean`` and ``missing``,
    text columns ``count`` and ``unique`` (AC-07). A statistic that is not
    available stays ``None`` and serialises to JSON ``null``.
    """
    if column.kind == "numeric":
        return {
            "name": column.name,
            "type": column.kind,
            "count": column.count,
            "min": column.minimum,
            "max": column.maximum,
            "mean": column.mean,
            "missing": column.missing,
        }
    return {
        "name": column.name,
        "type": column.kind,
        "count": column.count,
        "unique": column.unique,
    }


def render_json(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as a single valid JSON document."""
    document = [_column_to_dict(column) for column in stats]
    return json.dumps(document)
