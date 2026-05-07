"""standup.py — Summarize recent decisions.md transitions for session continuity.

Reads `<project>/decisions.md` and produces a chronological summary of the
last N hours of state transitions, deviations, and "no progress" entries.

Per `references/rd/rd_workflow.md` § Session-end ritual: every session
either moves a ledger row or records "no progress: <reason>". This script
surfaces what happened recently to help an agent re-orient at session start.

Usage:
    python scripts/standup.py --project-dir <path>
    python scripts/standup.py --project-dir <path> --hours 24

Output:
    Pretty-printed summary listing each entry from the window, classified by
    type (state transition / deviation / no-progress / freeze / promotion).

Exit codes:
    0: summary printed successfully
    1: setup error (project_dir or decisions.md not found)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


# Patterns for classifying entries by their first line
ENTRY_PATTERNS = [
    (re.compile(r"deviation", re.IGNORECASE), "deviation"),
    (re.compile(r"no progress", re.IGNORECASE), "no-progress"),
    (re.compile(r"frozen|freeze|freezing", re.IGNORECASE), "freeze"),
    (re.compile(r"promot", re.IGNORECASE), "promotion"),
    (re.compile(r"kill", re.IGNORECASE), "kill"),
    (re.compile(r"matured|established|supported|rejected|merged|stale|parked|active", re.IGNORECASE),
     "state transition"),
    (re.compile(r"layer 1 closure", re.IGNORECASE), "layer 1 closure"),
    (re.compile(r"stage gate", re.IGNORECASE), "stage gate"),
    (re.compile(r"trial complete|trial run", re.IGNORECASE), "trial"),
]


@dataclass
class Entry:
    date: datetime
    title: str
    body: str
    kind: str


def parse_decisions(path: Path) -> list[Entry]:
    """Parse decisions.md into a list of dated entries.

    Expected format: each entry starts with `## YYYY-MM-DD <title>` (date
    optionally followed by HH:MM time). Entries continue until the next `## `
    header.
    """
    text = path.read_text(encoding="utf-8")
    entries: list[Entry] = []
    # Match "## YYYY-MM-DD" optionally followed by " HH:MM" then anything (the title)
    header_re = re.compile(
        r"^##\s+(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?\s*(.*?)$",
        re.MULTILINE,
    )
    matches = list(header_re.finditer(text))
    for i, m in enumerate(matches):
        date_str = m.group(1)
        time_str = m.group(2) or "00:00"
        title = m.group(3).strip()
        try:
            ts = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        kind = classify(title, body)
        entries.append(Entry(date=ts, title=title, body=body, kind=kind))
    return entries


def classify(title: str, body: str) -> str:
    haystack = f"{title}\n{body}"
    for pat, label in ENTRY_PATTERNS:
        if pat.search(haystack):
            return label
    return "other"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--hours", type=int, default=24, help="lookback window in hours (default 24)")
    p.add_argument("--all", action="store_true", help="show all entries, ignore --hours")
    args = p.parse_args()

    decisions = args.project_dir / "decisions.md"
    if not decisions.exists():
        print(f"ERROR: decisions.md not found at {decisions}", file=sys.stderr)
        sys.exit(1)

    entries = parse_decisions(decisions)
    if not entries:
        print("(no dated entries in decisions.md)")
        sys.exit(0)

    if args.all:
        window_entries = entries
        title_window = "all entries"
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
        window_entries = [e for e in entries if e.date >= cutoff]
        title_window = f"last {args.hours} hours"

    # Sort newest first
    window_entries.sort(key=lambda e: e.date, reverse=True)

    print(f"=== Standup: {args.project_dir.name} ({title_window}) ===")
    print(f"Total entries in decisions.md: {len(entries)}; in window: {len(window_entries)}")
    print()

    if not window_entries:
        print(f"(no entries within {title_window})")
        # Show last entry for context
        last = max(entries, key=lambda e: e.date)
        print(f"Most recent entry: {last.date.date()} — {last.title}")
        sys.exit(0)

    # Group by kind
    by_kind: dict[str, list[Entry]] = {}
    for e in window_entries:
        by_kind.setdefault(e.kind, []).append(e)

    # Print summary by kind
    print("Summary by kind:")
    for kind in ("promotion", "freeze", "state transition", "stage gate", "trial",
                 "layer 1 closure", "kill", "deviation", "no-progress", "other"):
        if kind in by_kind:
            print(f"  {kind}: {len(by_kind[kind])}")
    print()

    # Print individual entries
    print("Entries (newest first):")
    for e in window_entries:
        ts = e.date.strftime("%Y-%m-%d %H:%M UTC")
        print(f"\n  [{ts}] [{e.kind}] {e.title}")
        # First few lines of body for context
        body_lines = [ln for ln in e.body.splitlines() if ln.strip()][:5]
        for ln in body_lines:
            print(f"    {ln}")
        if len(e.body.splitlines()) > 5:
            print(f"    ... ({len(e.body.splitlines()) - 5} more lines in decisions.md)")

    # Suggest next-session focus
    print()
    print("Session-start suggestions:")
    if "no-progress" in by_kind:
        print(f"  • {len(by_kind['no-progress'])} 'no progress' entry/entries — investigate blockers first")
    if "deviation" in by_kind:
        print(f"  • {len(by_kind['deviation'])} deviation(s) — verify whether downstream artifacts need re-evaluation")
    if "kill" in by_kind:
        print(f"  • {len(by_kind['kill'])} kill event(s) — confirm A4 decomposition is on file")
    if "promotion" in by_kind:
        print(f"  • {len(by_kind['promotion'])} promotion(s) — ensure post-promotion artifacts (IMRAD draft, maintenance plan) are stable")


if __name__ == "__main__":
    main()
