"""new_purpose.py - retired command.

Use `new_trial.py` for current workstream-aware projects. This command is kept
only to fail fast for older instructions; it must not create files from retired
templates.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


RETIREMENT_MESSAGE = (
    "new_purpose.py is retired and no longer creates purpose notebooks. "
    "Use scripts/new_trial.py with --project-dir, --workstream when needed, "
    "and --slug to create a current evidence artifact."
)


def create_purpose(*_args: object, **_kwargs: object) -> Path:
    """Fail fast for callers that still import the retired helper."""
    raise RuntimeError(RETIREMENT_MESSAGE)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Retired command. Use scripts/new_trial.py instead.",
    )
    p.add_argument("--project", required=True, help="project name")
    p.add_argument("--slug", required=True, help="trial slug (letters, numbers, and _)")
    p.add_argument("--hyp", required=True, help="linked hypothesis ID (e.g. H3)")
    p.add_argument("--title", default=None, help="title (defaults to slug humanized)")
    p.add_argument("--root", default="projects")
    p.parse_args()

    print(f"ERROR: {RETIREMENT_MESSAGE}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
