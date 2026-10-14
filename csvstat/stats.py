"""Compute per-column statistics for every :class:`ColumnData`."""

from __future__ import annotations

import math
import statistics

from csvstat.model import ColumnData, ColumnStats


def _is_missing(value: str | None) -> bool:
    """Return ``True`` for a missing value.

    A value is missing when it is ``None`` or a string that is empty or
    whitespace only.
    """
    return value is None or value.strip() == ""


def _to_number(value: str) -> float | int | None:
    """Return the numeric value of ``value``, or ``None`` if it is not a number.

    Leading and trailing whitespace is ignored. Both integers and floats using
    a decimal point ``.`` are accepted; non-finite values such as ``nan`` or
    ``inf`` are rejected, as they are not usable statistics.
    """
    text = value.strip()
    try:
        number = int(text)
    except ValueError:
        try:
            number = float(text)
        except ValueError:
            return None
    if isinstance(number, float) and not math.isfinite(number):
        return None
    return number


def _build_numeric(name: str, numbers: list[float | int], missing: int) -> ColumnStats:
    """Build the statistics for a numeric column with the given values."""
    if not numbers:
        return ColumnStats(
            name=name,
            kind="numeric",
            count=0,
            missing=missing,
            minimum=None,
            maximum=None,
            mean=None,
            unique=None,
        )
    return ColumnStats(
        name=name,
        kind="numeric",
        count=len(numbers),
        missing=missing,
        minimum=min(numbers),
        maximum=max(numbers),
        mean=statistics.mean(numbers),
        unique=None,
    )


def _build_text(name: str, values: list[str], missing: int) -> ColumnStats:
    """Build the statistics for a text column with the given values."""
    return ColumnStats(
        name=name,
        kind="text",
        count=len(values),
        missing=missing,
        minimum=None,
        maximum=None,
        mean=None,
        unique=len(set(values)),
    )


def compute_stats(columns: list[ColumnData]) -> list[ColumnStats]:
    """Compute the statistics for every column, in the order given."""
    result: list[ColumnStats] = []
    for column in columns:
        present: list[str] = []
        missing = 0
        for value in column.values:
            if _is_missing(value):
                missing += 1
            else:
                present.append(value if value is not None else "")

        numbers: list[float | int] = []
        numeric = True
        for value in present:
            number = _to_number(value)
            if number is None:
                numeric = False
                break
            numbers.append(number)

        if numeric:
            result.append(_build_numeric(column.name, numbers, missing))
        else:
            result.append(_build_text(column.name, present, missing))
    return result
