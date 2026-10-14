"""Read a CSV file into the column contract.

The file is opened strictly read-only: nothing is written, no temporary file or
cache is created, and no field value is ever logged. CSV content is treated as
data only -- it is never passed to ``eval``, ``exec`` or a subprocess.
"""

from __future__ import annotations

import csv
import pathlib

from csvstat.errors import CsvStatError
from csvstat.model import ColumnData


def _to_value(field: str | None) -> str | None:
    """Return the field as a value, or ``None`` when it is missing.

    A field that is empty or consists only of whitespace counts as missing.
    """
    if field is None:
        return None
    if field.strip() == "":
        return None
    return field


def read_columns(path: pathlib.Path, delimiter: str) -> list[ColumnData]:
    """Read ``path`` and return one :class:`ColumnData` per column.

    The first row is the header and every following row is a data row. Each
    column's ``values`` list holds one entry per data row in file order, with
    ``None`` for a missing value.

    Raises :class:`CsvStatError` for a missing path or a file without data rows.
    """
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = csv.reader(handle, delimiter=delimiter)
            try:
                header = next(rows)
            except StopIteration:
                raise CsvStatError(f"no data rows found in file: {path}") from None
            data_rows = list(rows)
    except FileNotFoundError:
        raise CsvStatError(f"file not found: {path}") from None
    except IsADirectoryError:
        raise CsvStatError(f"not a regular file: {path}") from None
    except OSError:
        raise CsvStatError(f"cannot read file: {path}") from None

    if not data_rows:
        raise CsvStatError(f"no data rows found in file: {path}")

    columns = [ColumnData(name=name, values=[]) for name in header]
    for row in data_rows:
        for index, column in enumerate(columns):
            field = row[index] if index < len(row) else None
            column.values.append(_to_value(field))

    return columns
