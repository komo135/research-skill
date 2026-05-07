"""render_explanation_dag.py — Render the Pure Research explanation hierarchy as Mermaid.

Reads `<project>/explanation_ledger.md` (Pure Research mode), parses Q rows
and E rows, and emits a Mermaid DAG showing question → competing
explanations with color-coding by E status (active / weakened / rejected /
supported / merged / parked).

Per `references/pure_research/explanation_ledger_schema.md`.

Usage:
    python scripts/render_explanation_dag.py --project-dir <path> > diagram.mmd
    python scripts/render_explanation_dag.py --project-dir <path> --output diagram.mmd

Exit codes:
    0: rendered successfully
    1: explanation_ledger.md not found
    2: parse error (no Q or E rows detected)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class QRow:
    id: str
    question: str
    status: str


@dataclass
class ERow:
    id: str
    parent_q: str
    statement: str
    mechanism: str
    status: str


def parse_md_table(text: str, header_keywords: list[str]) -> list[dict[str, str]]:
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "|" in line[1:]:
            cols = [c.strip() for c in line.strip("|").split("|")]
            cols_lc = [c.lower() for c in cols]
            if all(any(kw.lower() in c for c in cols_lc) for kw in header_keywords):
                if i + 1 < len(lines) and re.match(r"^\|?\s*[-:]+", lines[i + 1].strip()):
                    j = i + 2
                else:
                    j = i + 1
                rows: list[dict[str, str]] = []
                while j < len(lines):
                    row_line = lines[j].strip()
                    if not row_line.startswith("|"):
                        break
                    vals = [c.strip() for c in row_line.strip("|").split("|")]
                    while len(vals) < len(cols):
                        vals.append("")
                    vals = vals[: len(cols)]
                    rows.append({c: v for c, v in zip(cols, vals)})
                    j += 1
                return rows
        i += 1
    return []


def get_col(row: dict[str, str], *candidates: str) -> str:
    for cand in candidates:
        for col, val in row.items():
            if cand.lower() in col.lower():
                return val.strip()
    return ""


def parse_ledger(text: str) -> tuple[list[QRow], list[ERow]]:
    q_raw = parse_md_table(text, ["ID", "question"])
    q_rows = []
    for r in q_raw:
        qid = get_col(r, "ID")
        if not qid or not qid.startswith("Q"):
            continue
        q_rows.append(QRow(
            id=qid,
            question=get_col(r, "question") or qid,
            status=get_col(r, "Status") or "active",
        ))

    e_raw = parse_md_table(text, ["ID", "statement", "mechanism"])
    e_rows = []
    for r in e_raw:
        eid = get_col(r, "ID")
        if not eid or not eid.startswith("E"):
            continue
        e_rows.append(ERow(
            id=eid,
            parent_q=get_col(r, "parent_q", "parent"),
            statement=get_col(r, "statement"),
            mechanism=get_col(r, "mechanism"),
            status=get_col(r, "Status") or "active",
        ))

    return q_rows, e_rows


def status_class(status: str) -> str:
    s = status.lower()
    if "supported" in s:
        return "eSupported"
    if "rejected" in s:
        return "eRejected"
    if "weakened" in s:
        return "eWeakened"
    if "merged" in s or "stale" in s:
        return "eStale"
    if "parked" in s:
        return "eParked"
    return "eActive"


def q_status_class(status: str) -> str:
    s = status.lower()
    if "answered" in s:
        return "qAnswered"
    if "stale" in s or "merged" in s:
        return "qStale"
    if "parked" in s:
        return "qParked"
    return "qActive"


def escape(s: str) -> str:
    return s.replace('"', '#quot;').replace("\n", " ")[:80]


def render(q_rows: list[QRow], e_rows: list[ERow]) -> str:
    lines = []
    lines.append("```mermaid")
    lines.append("flowchart TB")
    lines.append("  %% Class definitions")
    lines.append("  classDef qActive fill:#e3f2fd,stroke:#1565c0,color:#000,stroke-width:2px")
    lines.append("  classDef qAnswered fill:#bbdefb,stroke:#0d47a1,color:#000,stroke-width:3px")
    lines.append("  classDef qStale fill:#f5f5f5,stroke:#9e9e9e,color:#666,stroke-dasharray: 3 3")
    lines.append("  classDef qParked fill:#d1c4e9,stroke:#4527a0,color:#000")
    lines.append("  classDef eActive fill:#e8f5e9,stroke:#2e7d32,color:#000")
    lines.append("  classDef eSupported fill:#a5d6a7,stroke:#1b5e20,color:#000,stroke-width:3px")
    lines.append("  classDef eWeakened fill:#fff3cd,stroke:#cc8800,color:#000")
    lines.append("  classDef eRejected fill:#ffcdd2,stroke:#c62828,color:#000,stroke-dasharray: 5 5")
    lines.append("  classDef eStale fill:#f5f5f5,stroke:#9e9e9e,color:#666,stroke-dasharray: 3 3")
    lines.append("  classDef eParked fill:#d1c4e9,stroke:#4527a0,color:#000")
    lines.append("")

    # Group E by parent Q
    e_by_q: dict[str, list[ERow]] = {}
    for e in e_rows:
        e_by_q.setdefault(e.parent_q, []).append(e)

    for q in q_rows:
        # Question node
        q_label = f"{q.id}: {escape(q.question)}"
        if q.status and q.status != "active":
            q_label += f"<br/>[{q.status}]"
        lines.append(f"  {q.id}[\"{q_label}\"]:::{ q_status_class(q.status)}")

        # Children E nodes
        for e in e_by_q.get(q.id, []):
            e_label = f"{e.id}: {escape(e.statement)}"
            if e.mechanism:
                e_label += f"<br/><i>{escape(e.mechanism)}</i>"
            if e.status and e.status != "active":
                e_label += f"<br/>[{e.status}]"
            lines.append(f"  {e.id}[\"{e_label}\"]:::{ status_class(e.status)}")
            lines.append(f"  {q.id} --> {e.id}")
        lines.append("")

    # Orphan E's (parent_Q references a missing Q)
    q_ids = {q.id for q in q_rows}
    orphans = [e for e in e_rows if e.parent_q not in q_ids]
    if orphans:
        lines.append("  %% Orphan E rows (parent Q not in ledger)")
        for e in orphans:
            e_label = f"{e.id}: {escape(e.statement)} (orphan: parent_Q={e.parent_q})"
            lines.append(f"  {e.id}[\"{e_label}\"]:::{ status_class(e.status)}")

    lines.append("```")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()

    el = args.project_dir / "explanation_ledger.md"
    if not el.exists():
        print(f"ERROR: explanation_ledger.md not found at {el}", file=sys.stderr)
        sys.exit(1)

    text = el.read_text(encoding="utf-8")
    q_rows, e_rows = parse_ledger(text)

    if not q_rows and not e_rows:
        print("ERROR: no Q or E rows parsed from explanation_ledger.md", file=sys.stderr)
        sys.exit(2)

    diagram = render(q_rows, e_rows)
    if args.output:
        args.output.write_text(diagram + "\n", encoding="utf-8")
        print(f"Wrote {len(diagram.splitlines())} lines to {args.output}", file=sys.stderr)
    else:
        print(diagram)


if __name__ == "__main__":
    main()
