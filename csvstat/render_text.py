"""Render the per-column statistics as an aligned plain-text report.

Only formatting lives here; the statistics themselves are computed in
:mod:`csvstat.stats`. Every string that originates from the CSV (a column
name) is sanitized before it reaches the report so a prepared header cannot
manipulate the terminal (AC-15).
"""

from __future__ import annotations

import re

from csvstat.model import ColumnStats

# ANSI escape sequences: CSI (colours, cursor), OSC (window title/links) and
# the two-character escapes. Removed before anything is written to stdout.
_ANSI_ESCAPE = re.compile(
    r"\x1b(?:\[[0-?]*[ -/]*[@-~]"  # CSI ... final byte
    r"|\][^\x07\x1b]*(?:\x07|\x1b\\)"  # OSC ... BEL or ST
    r"|[@-Z\\-_])"  # other two-character escapes
)

# Any remaining control character (newlines, carriage returns, tabs, C1 codes).
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f]")

_WHITESPACE = re.compile(r"\s+")

_PLACEHOLDER = "-"
_LABEL_HEADER = "column"
_KIND_HEADER = "type"


def _sanitize(value: str) -> str:
    """Neutralise control characters and ANSI escapes in a CSV-sourced string."""
    cleaned = _ANSI_ESCAPE.sub("", value)
    cleaned = _CONTROL_CHARS.sub(" ", cleaned)
    return _WHITESPACE.sub(" ", cleaned).strip()


def _format_stat(value: float | int | None) -> str:
    """Format one statistic, using a readable placeholder for a missing value."""
    if value is None:
        return _PLACEHOLDER
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    return f"{value:g}"


def render_text(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as a human-readable, column-aligned text report.

    Each reported column is labelled with its (sanitized) CSV column name and
    its kind, so it is recognisable as numeric or text. Numeric columns expose
    count, min, max, mean and missing; text columns expose count and unique.
    Statistics that are not available print as ``-`` instead of crashing.
    """
    if not stats:
        return "No columns to report."

    headers = [_sanitize(column.name) for column in stats]
    kinds = [column.kind for column in stats]

    rows: list[tuple[str, list[str]]] = [
        ("count", [str(column.count) for column in stats]),
        ("min", [_format_stat(column.minimum) for column in stats]),
        ("max", [_format_stat(column.maximum) for column in stats]),
        ("mean", [_format_stat(column.mean) for column in stats]),
        ("missing", [str(column.missing) for column in stats]),
        ("unique", [_format_stat(column.unique) for column in stats]),
    ]

    label_width = max([len(_LABEL_HEADER), len(_KIND_HEADER)] + [len(label) for label, _ in rows])
    column_widths = [
        max([len(headers[index]), len(kinds[index])] + [len(cells[index]) for _, cells in rows])
        for index in range(len(stats))
    ]

    def format_row(label: str, cells: list[str]) -> str:
        parts = [label.ljust(label_width)]
        parts += [cells[index].ljust(column_widths[index]) for index in range(len(stats))]
        return "  ".join(parts).rstrip()

    lines = [format_row(_LABEL_HEADER, headers), format_row(_KIND_HEADER, kinds)]
    lines += [format_row(label, cells) for label, cells in rows]
    return "\n".join(lines)
