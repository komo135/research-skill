"""render_capability_dag.py — Render the R&D capability dependency graph as Mermaid.

Reads `<project>/capability_map.md` (R&D mode), parses Section 1 (K rows)
and Section 2 (C rows), and emits a Mermaid DAG showing the dependency
structure with subgraphs per K and color-coding by lifecycle (K) or
status (C).

Per CHARTER C14 (Amendment-2: two-layer decomposition) and D-23 / F5
(critical path automation), this DAG complements `validate_ledger.py`
visually.

Usage:
    python scripts/render_capability_dag.py --project-dir <path> > diagram.mmd
    python scripts/render_capability_dag.py --project-dir <path> --output diagram.mmd

Output (stdout or --output): a Mermaid `flowchart` block ready to embed
in markdown or render via mermaid CLI.

Exit codes:
    0: rendered successfully
    1: capability_map.md not found
    2: parse error (no K or C rows detected)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class KRow:
    id: str
    name: str
    lifecycle: str  # 永続型 | 継続改善型 | unknown
    status: str


@dataclass
class CRow:
    id: str
    name: str
    core_tech_id: str  # K-id or "integration"
    depends_on: list[str]
    current_trl: int
    target_trl: int
    status: str


def parse_md_table(text: str, header_keywords: list[str]) -> list[dict[str, str]]:
    """Same parser as validate_ledger.py — duplicated here to keep this script standalone."""
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
    """Get first non-empty column matching any candidate (case-insensitive substring)."""
    for cand in candidates:
        for col, val in row.items():
            if cand.lower() in col.lower():
                return val.strip()
    return ""


def parse_int(s: str, default: int = -1) -> int:
    s = s.strip()
    if not s or not s.lstrip("-").isdigit():
        return default
    return int(s)


def parse_capability_map(text: str) -> tuple[list[KRow], list[CRow]]:
    # Layer 1
    k_rows_raw = parse_md_table(text, ["ID", "発展性"])
    if not k_rows_raw:
        k_rows_raw = parse_md_table(text, ["ID", "lifecycle"])
    k_rows: list[KRow] = []
    for r in k_rows_raw:
        kid = get_col(r, "ID")
        if not kid or not kid.startswith("K"):
            continue
        k_rows.append(KRow(
            id=kid,
            name=get_col(r, "コア", "core technology", "name") or kid,
            lifecycle=get_col(r, "発展性", "lifecycle") or "unknown",
            status=get_col(r, "Status") or "active",
        ))

    # Layer 2
    c_rows_raw = parse_md_table(text, ["ID", "kill_criteria", "core_tech_id"])
    if not c_rows_raw:
        c_rows_raw = parse_md_table(text, ["ID", "kill_criteria"])
    c_rows: list[CRow] = []
    for r in c_rows_raw:
        cid = get_col(r, "ID")
        if not cid or not cid.startswith("C"):
            continue
        deps_str = get_col(r, "depends_on")
        deps = [d.strip() for d in re.split(r"[,;\s]+", deps_str) if d.strip()]
        c_rows.append(CRow(
            id=cid,
            name=get_col(r, "capability") or cid,
            core_tech_id=get_col(r, "core_tech_id") or "integration",
            depends_on=deps,
            current_trl=parse_int(get_col(r, "current_TRL")),
            target_trl=parse_int(get_col(r, "target_TRL"), default=6),
            status=get_col(r, "Status") or "active",
        ))

    return k_rows, c_rows


def lifecycle_color(lc: str) -> str:
    """Mermaid class for K lifecycle."""
    if "永続" in lc or "permanent" in lc.lower():
        return "kPermanent"
    if "継続" in lc or "continuous" in lc.lower():
        return "kContinuous"
    return "kUnknown"


def status_color(status: str) -> str:
    """Mermaid class for C status."""
    s = status.lower()
    if "matured" in s or "established" in s or "supported" in s:
        return "cMatured"
    if "killed" in s or "rejected" in s:
        return "cKilled"
    if "blocked" in s:
        return "cBlocked"
    if "stale" in s or "merged" in s:
        return "cStale"
    if "parked" in s:
        return "cParked"
    return "cActive"


def escape(s: str) -> str:
    """Escape characters problematic in Mermaid node labels."""
    return s.replace('"', '#quot;').replace("\n", " ")[:80]


def render(k_rows: list[KRow], c_rows: list[CRow]) -> str:
    """Generate the Mermaid flowchart string."""
    lines: list[str] = []
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("  %% Class definitions")
    lines.append("  classDef kPermanent fill:#cce5ff,stroke:#0066cc,color:#000")
    lines.append("  classDef kContinuous fill:#fff3cd,stroke:#cc8800,color:#000")
    lines.append("  classDef kUnknown fill:#e0e0e0,stroke:#666666,color:#000")
    lines.append("  classDef cActive fill:#e8f5e9,stroke:#2e7d32,color:#000")
    lines.append("  classDef cMatured fill:#a5d6a7,stroke:#1b5e20,color:#000,stroke-width:3px")
    lines.append("  classDef cBlocked fill:#ffe0b2,stroke:#e65100,color:#000")
    lines.append("  classDef cKilled fill:#ffcdd2,stroke:#c62828,color:#000,stroke-dasharray: 5 5")
    lines.append("  classDef cStale fill:#f5f5f5,stroke:#9e9e9e,color:#666,stroke-dasharray: 3 3")
    lines.append("  classDef cParked fill:#d1c4e9,stroke:#4527a0,color:#000")
    lines.append("")

    # Group C's by parent K (or "integration")
    c_by_k: dict[str, list[CRow]] = {}
    for c in c_rows:
        c_by_k.setdefault(c.core_tech_id, []).append(c)

    # K subgraphs
    for k in k_rows:
        lifecycle_label = k.lifecycle if k.lifecycle != "unknown" else ""
        label = f"{k.id}: {escape(k.name)}"
        if lifecycle_label:
            label += f" [{lifecycle_label}]"
        lines.append(f"  subgraph {k.id}_subgraph[\"{label}\"]")
        for c in c_by_k.get(k.id, []):
            trl_label = f"TRL {c.current_trl}/{c.target_trl}" if c.current_trl >= 0 else ""
            c_label = f"{c.id}: {escape(c.name)}"
            if trl_label:
                c_label += f"<br/>{trl_label}"
            if c.status and c.status != "active":
                c_label += f"<br/>({c.status})"
            lines.append(f"    {c.id}[\"{c_label}\"]:::{ status_color(c.status)}")
        lines.append("  end")
        lines.append(f"  class {k.id}_subgraph {lifecycle_color(k.lifecycle)}")
        lines.append("")

    # Integration capabilities (no K parent / core_tech_id == "integration")
    integration_cs = c_by_k.get("integration", [])
    if integration_cs:
        lines.append("  subgraph integration_subgraph[\"integration\"]")
        for c in integration_cs:
            trl_label = f"TRL {c.current_trl}/{c.target_trl}" if c.current_trl >= 0 else ""
            c_label = f"{c.id}: {escape(c.name)}"
            if trl_label:
                c_label += f"<br/>{trl_label}"
            if c.status and c.status != "active":
                c_label += f"<br/>({c.status})"
            lines.append(f"    {c.id}[\"{c_label}\"]:::{status_color(c.status)}")
        lines.append("  end")
        lines.append("")

    # Edges from depends_on
    lines.append("  %% Dependencies")
    for c in c_rows:
        for dep in c.depends_on:
            if dep:  # non-empty
                lines.append(f"  {dep} --> {c.id}")

    lines.append("```")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--output", type=Path, default=None,
                   help="output file (default: stdout)")
    args = p.parse_args()

    cm = args.project_dir / "capability_map.md"
    if not cm.exists():
        print(f"ERROR: capability_map.md not found at {cm}", file=sys.stderr)
        sys.exit(1)

    text = cm.read_text(encoding="utf-8")
    k_rows, c_rows = parse_capability_map(text)

    if not k_rows and not c_rows:
        print("ERROR: no K rows or C rows parsed from capability_map.md", file=sys.stderr)
        sys.exit(2)

    diagram = render(k_rows, c_rows)
    if args.output:
        args.output.write_text(diagram + "\n", encoding="utf-8")
        print(f"Wrote {len(diagram.splitlines())} lines to {args.output}", file=sys.stderr)
    else:
        print(diagram)


if __name__ == "__main__":
    main()
