"""Select a subset of columns by name."""

from __future__ import annotations

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData


def select_columns(columns: list[ColumnData], names: list[str]) -> list[ColumnData]:
    """Return the columns named in ``names``, in that exact order.

    Raises :class:`CsvStatError` when a requested name does not exist. The
    message names only the unknown column and carries no value from the file.
    """
    by_name = {column.name: column for column in columns}
    selected: list[ColumnData] = []
    for name in names:
        column = by_name.get(name)
        if column is None:
            raise CsvStatError(f"unknown column: {name}")
        selected.append(column)
    return selected
