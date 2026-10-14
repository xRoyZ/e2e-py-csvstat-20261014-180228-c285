"""Entry point so that ``python -m csvstat`` works like the ``csvstat`` script."""

from csvstat.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
