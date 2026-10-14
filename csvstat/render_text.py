"""Render the report as aligned plain text (not implemented yet)."""

from __future__ import annotations

from csvstat.errors import CsvStatError
from csvstat.model import ColumnStats


def render_text(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as a human-readable text report."""
    raise CsvStatError("render_text is not implemented yet")
