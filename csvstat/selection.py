"""Select a subset of columns by name (not implemented yet)."""

from __future__ import annotations

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData


def select_columns(columns: list[ColumnData], names: list[str]) -> list[ColumnData]:
    """Return the columns named in ``names``, in that exact order.

    Raises :class:`CsvStatError` when a requested name does not exist.
    """
    raise CsvStatError("select is not implemented yet")
