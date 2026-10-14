"""The shared data contract flowing between the csvstat pipeline steps."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ColumnData:
    """One column read from the CSV file, in file order.

    ``values`` holds one entry per data row; ``None`` marks a missing value
    (an empty field or a field that is whitespace only).
    """

    name: str
    values: list[str | None]


@dataclass
class ColumnStats:
    """The computed statistics for a single column."""

    name: str
    kind: str  # "numeric" | "text"
    count: int
    missing: int
    minimum: float | int | None
    maximum: float | int | None
    mean: float | None
    unique: int | None  # numeric column: None
