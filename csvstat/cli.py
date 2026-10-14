"""The csvstat command-line front end."""

from __future__ import annotations

import argparse
import pathlib
import sys

from csvstat import reader, render_json, render_text, selection, stats
from csvstat.errors import CsvStatError


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with the CSV path and all three options."""
    parser = argparse.ArgumentParser(
        prog="csvstat",
        description="Print per-column statistics for a CSV file.",
    )
    parser.add_argument(
        "csv_path",
        help="path to the CSV file to analyse",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="field delimiter used by the CSV file (default: ',')",
    )
    parser.add_argument(
        "--columns",
        default=None,
        help="comma-separated list of column names to report, in the given order",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the report as JSON instead of aligned text",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the full pipeline and return the process exit code.

    The pipeline runs in a fixed order: read -> select (only when ``--columns``
    is given) -> statistics -> render. Any :class:`CsvStatError` is turned into
    exactly one line on stderr and exit code 1, never a traceback.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        columns = reader.read_columns(pathlib.Path(args.csv_path), args.delimiter)
        if args.columns is not None:
            names = [name.strip() for name in args.columns.split(",") if name.strip()]
            columns = selection.select_columns(columns, names)
        column_stats = stats.compute_stats(columns)
        if args.json:
            output = render_json.render_json(column_stats)
        else:
            output = render_text.render_text(column_stats)
    except CsvStatError as exc:
        print(exc.message, file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
