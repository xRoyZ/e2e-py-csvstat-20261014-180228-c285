"""Error types shared by every step of the csvstat pipeline."""

from __future__ import annotations


class CsvStatError(Exception):
    """A user-facing failure.

    The ``message`` is printed as-is on stderr as exactly one line, followed by
    a non-zero exit code. Callers must never let a traceback escape for it.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
