"""Render the report as JSON (not implemented yet)."""

from __future__ import annotations

from csvstat.errors import CsvStatError
from csvstat.model import ColumnStats


def render_json(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as a single valid JSON document."""
    raise CsvStatError("render_json is not implemented yet")
