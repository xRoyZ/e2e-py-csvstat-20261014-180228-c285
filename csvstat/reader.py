"""Read a CSV file into the column contract (not implemented yet)."""

from __future__ import annotations

import pathlib

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData


def read_columns(path: pathlib.Path, delimiter: str) -> list[ColumnData]:
    """Read ``path`` and return one :class:`ColumnData` per column.

    Raises :class:`CsvStatError` for a missing path or a file without data rows.
    """
    raise CsvStatError("read is not implemented yet")
