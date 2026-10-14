"""Compute per-column statistics (not implemented yet)."""

from __future__ import annotations

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData, ColumnStats


def compute_stats(columns: list[ColumnData]) -> list[ColumnStats]:
    """Compute the statistics for every column, in the order given."""
    raise CsvStatError("statistics is not implemented yet")
