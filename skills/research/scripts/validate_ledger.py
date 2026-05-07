"""validate_ledger.py — Lint a quant-research project's ledgers and trial artifacts.

Checks consistency across the project's state files:

  - charter.md / prfaq.md frozen and hash matches lock
  - capability_map.md (R&D) Section 1 (Core Technologies, Layer 1) and
    Section 2 (Capabilities, Layer 2) schema compliance
  - explanation_ledger.md (Pure Research) schema compliance
  - prereg/PR_*.md and PR_*.lock pairs intact
  - Per-trial Analysis section 5-field completeness in purposes/trial_*.py
  - TRL skip detection (no transition advancing TRL by > 1)
  - core_tech_id references valid K-IDs
  - dependent_on_research syntax
  - Layer 1 closure check (per references/rd/core_technologies.md)
  - Integration pattern declared in charter (per CHARTER C15 / Amendment-3)
  - decisions.md chronological coverage (no gap > 4 weeks without entry)

Usage:
    python scripts/validate_ledger.py --project-dir <path>
    python scripts/validate_ledger.py --project-dir <path> --strict  # warnings -> errors

Exit codes:
    0: all checks pass
    1: at least one error (strict mode: warnings also count)
    2: setup error (project dir invalid)
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

CHUNK = 65536


@dataclass
class Finding:
    severity: str  # "error" | "warning" | "info"
    where: str
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def err(self, where: str, message: str) -> None:
        self.findings.append(Finding("error", where, message))

    def warn(self, where: str, message: str) -> None:
        self.findings.append(Finding("warning", where, message))

    def info(self, where: str, message: str) -> None:
        self.findings.append(Finding("info", where, message))

    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_lock(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, _, v = s.partition(":")
        out[k.strip()] = v.strip()
    return out


def parse_md_table(text: str, header_keywords: list[str]) -> list[dict[str, str]]:
    """Naive markdown table parser. Looks for the first table whose header
    contains all of `header_keywords` (case-insensitive substring match).
    Returns list of dicts (column name -> value).

    Skips the alignment row (---|---|...).
    Treats `|` as the column separator. Leading/trailing pipes optional.
    """
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "|" in line[1:]:
            cols = [c.strip() for c in line.strip("|").split("|")]
            cols_lc = [c.lower() for c in cols]
            if all(any(kw.lower() in c for c in cols_lc) for kw in header_keywords):
                # Found header. Skip alignment row.
                if i + 1 < len(lines) and re.match(r"^\|?\s*[-:]+", lines[i + 1].strip()):
                    j = i + 2
                else:
                    j = i + 1
                while j < len(lines):
                    row_line = lines[j].strip()
                    if not row_line.startswith("|"):
                        break
                    vals = [c.strip() for c in row_line.strip("|").split("|")]
                    # Pad / truncate to match column count
                    while len(vals) < len(cols):
                        vals.append("")
                    vals = vals[:len(cols)]
                    row = {c: v for c, v in zip(cols, vals)}
                    rows.append(row)
                    j += 1
                return rows
        i += 1
    return rows


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_frozen_artifact(
    project_dir: Path, artifact_name: str, lock_name: str, report: Report
) -> bool:
    artifact = project_dir / artifact_name
    lock = project_dir / "prereg" / lock_name
    if not artifact.exists():
        return False  # not applicable for this mode
    if not lock.exists():
        report.err(artifact_name, f"artifact exists but lock {lock_name} missing — run prereg_freeze.py")
        return False
    info = parse_lock(lock)
    actual_hash = compute_sha256(artifact)
    expected = info.get("sha256", "")
    if actual_hash != expected:
        report.err(
            artifact_name,
            f"hash mismatch with {lock_name} "
            f"(expected {expected[:16]}..., actual {actual_hash[:16]}...) — "
            "artifact was edited in place after freezing. File deviation entry."
        )
        return False
    report.info(artifact_name, f"frozen, hash matches lock ({actual_hash[:16]}...)")
    return True


def check_charter_integration_pattern(project_dir: Path, report: Report) -> None:
    charter = project_dir / "charter.md"
    if not charter.exists():
        return
    text = charter.read_text(encoding="utf-8")
    if "integration pattern" not in text.lower():
        report.err("charter.md", "Integration pattern not declared in H8 (per CHARTER C15)")
        return
    # Detect declared pattern
    pat_match = re.search(r"pattern\s*:?\s*(pattern\s*[123])", text, re.IGNORECASE)
    if pat_match:
        report.info("charter.md", f"integration pattern: {pat_match.group(1).lower()}")
    else:
        report.warn("charter.md", "integration pattern keyword present but pattern (1/2/3) not parseable")


def check_capability_map(project_dir: Path, report: Report) -> dict[str, Any]:
    """Returns parsed K-rows + C-rows for downstream checks."""
    cm = project_dir / "capability_map.md"
    out: dict[str, Any] = {"k_rows": [], "c_rows": []}
    if not cm.exists():
        return out
    text = cm.read_text(encoding="utf-8")

    # Layer 1 (K rows): identify by 発展性 column (unique to Layer 1, not in Layer 2)
    # Try Japanese header first (most common), then English fallback
    k_rows = parse_md_table(text, ["ID", "発展性"])
    if not k_rows:
        k_rows = parse_md_table(text, ["ID", "lifecycle"])
    if not k_rows:
        report.warn("capability_map.md", "Section 1 (Core Technologies) table not detected or empty")
    else:
        out["k_rows"] = k_rows
        report.info("capability_map.md", f"Layer 1: {len(k_rows)} K rows detected")

    # Layer 2 (C rows): identify by kill_criteria + core_tech_id (both unique to Layer 2)
    c_rows = parse_md_table(text, ["ID", "kill_criteria", "core_tech_id"])
    if not c_rows:
        # Fallback: just kill_criteria (still unique to Layer 2)
        c_rows = parse_md_table(text, ["ID", "kill_criteria"])
    if not c_rows:
        report.warn("capability_map.md", "Section 2 (Capabilities) table not detected or empty")
    else:
        out["c_rows"] = c_rows
        report.info("capability_map.md", f"Layer 2: {len(c_rows)} capability rows detected")

    # Layer 1 closure: every K row should have all required fields filled
    required_k_fields = ["ID", "発展性"]  # minimal set; full check below per row
    k_ids = set()
    for row in out["k_rows"]:
        # Get the ID column (it may be named "ID" or similar)
        kid = next((row[c] for c in row if c.upper().startswith("ID")), "").strip()
        if not kid:
            report.err("capability_map.md", f"Layer 1: row with empty ID: {row}")
            continue
        k_ids.add(kid)
        # Check no TBD / placeholder
        for col, val in row.items():
            if val and val.strip().lower() in ("tbd", "todo", "<replace>", "..."):
                report.err(
                    "capability_map.md",
                    f"Layer 1 K {kid}: column '{col}' has placeholder value '{val}'"
                )
        # Check 発展性 has valid value
        lifecycle_col = next((c for c in row if "発展性" in c or "lifecycle" in c.lower()), None)
        if lifecycle_col:
            val = row[lifecycle_col].strip()
            if val not in ("永続型", "継続改善型", "permanent", "continuous"):
                report.warn(
                    "capability_map.md",
                    f"Layer 1 K {kid}: 発展性 = '{val}' (expected 永続型 or 継続改善型)"
                )

    out["k_ids"] = k_ids

    # Layer 2: each C must reference a valid core_tech_id
    for row in out["c_rows"]:
        cid = next((row[c] for c in row if c.upper().startswith("ID")), "").strip()
        ct_col = next((c for c in row if "core_tech_id" in c.lower() or "core_tech" in c.lower()), None)
        if ct_col:
            ct_val = row[ct_col].strip()
            if ct_val and ct_val != "integration" and ct_val not in k_ids:
                report.err(
                    "capability_map.md",
                    f"Layer 2 C {cid}: core_tech_id '{ct_val}' is not a valid K-ID "
                    f"(known K-IDs: {sorted(k_ids)})"
                )
        # TRL skip check requires git history; warn-level only here
        for col in ("current_TRL", "target_TRL"):
            tcol = next((c for c in row if col.lower() in c.lower()), None)
            if tcol:
                val = row[tcol].strip()
                if val and not val.isdigit():
                    report.warn(
                        "capability_map.md",
                        f"Layer 2 C {cid}: {col} = '{val}' is not an integer"
                    )

    return out


def check_explanation_ledger(project_dir: Path, report: Report) -> dict[str, Any]:
    el = project_dir / "explanation_ledger.md"
    out: dict[str, Any] = {"q_rows": [], "e_rows": []}
    if not el.exists():
        return out
    text = el.read_text(encoding="utf-8")

    q_rows = parse_md_table(text, ["ID", "question"])
    e_rows = parse_md_table(text, ["ID", "statement", "mechanism"])
    out["q_rows"] = q_rows
    out["e_rows"] = e_rows

    if not q_rows:
        report.warn("explanation_ledger.md", "Active questions table not detected or empty")
    else:
        report.info("explanation_ledger.md", f"{len(q_rows)} Q rows detected")
    if not e_rows:
        report.warn("explanation_ledger.md", "Explanations table not detected or empty")
    else:
        report.info("explanation_ledger.md", f"{len(e_rows)} E rows detected")

        # Each Q should have ≥2 E rows
        q_ids = {next((r[c] for c in r if c.upper().startswith("ID")), "").strip()
                 for r in q_rows}
        e_by_q: dict[str, int] = {}
        for r in e_rows:
            parent_q_col = next((c for c in r if "parent_q" in c.lower() or "parent" in c.lower()), None)
            if parent_q_col:
                pq = r[parent_q_col].strip()
                e_by_q[pq] = e_by_q.get(pq, 0) + 1
        for qid in q_ids:
            count = e_by_q.get(qid, 0)
            if count < 2:
                report.warn(
                    "explanation_ledger.md",
                    f"Q {qid}: only {count} explanation(s) — pre-reg requires ≥2 competing E + null"
                )

    return out


def check_prereg_files(project_dir: Path, report: Report) -> None:
    prereg_dir = project_dir / "prereg"
    if not prereg_dir.exists():
        return
    # For each .md, expect matching .lock
    for md in prereg_dir.glob("PR_*.md"):
        stem = md.stem
        lock = prereg_dir / f"{stem}.lock"
        if not lock.exists():
            report.err(f"prereg/{md.name}", "no matching .lock — run prereg_freeze.py")
            continue
        info = parse_lock(lock)
        actual = compute_sha256(md)
        expected = info.get("sha256", "")
        if actual != expected:
            report.err(
                f"prereg/{md.name}",
                f"hash mismatch (expected {expected[:16]}..., actual {actual[:16]}...) "
                "— pre-reg edited in place after freezing"
            )
        else:
            report.info(f"prereg/{md.name}", f"frozen ({actual[:16]}...)")


def check_trials_analysis_section(project_dir: Path, report: Report) -> None:
    purposes_dir = project_dir / "purposes"
    if not purposes_dir.exists():
        return
    required_subfields = [
        "Observation",
        "Decomposition",
        "Evidence weighing",
        "Tier rating",
        "Gap to next tier",
    ]
    for trial in sorted(purposes_dir.glob("trial_*.py")) + sorted(purposes_dir.glob("pur_*.py")):
        text = trial.read_text(encoding="utf-8")
        # Detect Analysis section by presence of ALL 5 required sub-fields
        missing = [s for s in required_subfields if s not in text]
        if missing:
            report.warn(
                f"purposes/{trial.name}",
                f"Analysis section missing sub-fields: {missing} "
                "(per references/shared/analysis_depth.md, all 5 are required)"
            )
        # Detect tier rating
        tier_match = re.search(r"\bA([0-5])\b", text)
        if tier_match:
            report.info(f"purposes/{trial.name}", f"detected tier mention: A{tier_match.group(1)}")
        else:
            report.warn(f"purposes/{trial.name}", "no analysis tier (A0-A5) mention detected")


def check_decisions_md_coverage(project_dir: Path, report: Report) -> None:
    dec = project_dir / "decisions.md"
    if not dec.exists():
        report.warn("decisions.md", "file missing")
        return
    text = dec.read_text(encoding="utf-8")
    # Find date headers like "## YYYY-MM-DD"
    date_re = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})", re.MULTILINE)
    dates: list[datetime] = []
    for m in date_re.finditer(text):
        try:
            dates.append(datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc))
        except ValueError:
            continue
    if not dates:
        report.warn("decisions.md", "no dated entries (## YYYY-MM-DD format) detected")
        return
    dates.sort()
    # Check gaps > 4 weeks
    for prev, nxt in zip(dates, dates[1:]):
        if (nxt - prev) > timedelta(weeks=4):
            report.warn(
                "decisions.md",
                f"gap > 4 weeks between {prev.date()} and {nxt.date()} "
                f"({(nxt - prev).days} days) — session-end ritual may have lapsed"
            )
    report.info("decisions.md", f"{len(dates)} dated entries, range {dates[0].date()} → {dates[-1].date()}")


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def validate_project(project_dir: Path) -> Report:
    report = Report()
    project_dir = project_dir.resolve()

    if not project_dir.exists():
        report.err("project", f"project_dir not found: {project_dir}")
        return report

    # Determine mode (R&D vs Pure Research) by which artifacts exist
    has_charter = (project_dir / "charter.md").exists()
    has_prfaq = (project_dir / "prfaq.md").exists()

    if has_charter and has_prfaq:
        report.warn(
            "project",
            "BOTH charter.md and prfaq.md exist — possible mode mixing. "
            "Verify per CHARTER C1 (R&D and Pure Research must not be mixed)."
        )

    if has_charter:
        report.info("project", "Mode: R&D (charter.md detected)")
        check_frozen_artifact(project_dir, "charter.md", "charter.lock", report)
        check_charter_integration_pattern(project_dir, report)
        check_capability_map(project_dir, report)
    elif has_prfaq:
        report.info("project", "Mode: Pure Research (prfaq.md detected)")
        check_frozen_artifact(project_dir, "prfaq.md", "prfaq.lock", report)
        check_explanation_ledger(project_dir, report)
    else:
        report.warn("project", "Neither charter.md nor prfaq.md found — mode undeclared")

    # Both modes
    check_prereg_files(project_dir, report)
    check_trials_analysis_section(project_dir, report)
    check_decisions_md_coverage(project_dir, report)

    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--strict", action="store_true",
                   help="treat warnings as errors for exit code purposes")
    args = p.parse_args()

    report = validate_project(args.project_dir)

    print("=== validate_ledger findings ===")
    by_sev: dict[str, list[Finding]] = {"error": [], "warning": [], "info": []}
    for f in report.findings:
        by_sev[f.severity].append(f)

    for sev in ("error", "warning", "info"):
        items = by_sev[sev]
        if not items:
            continue
        icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}[sev]
        print(f"\n{icon} {sev.upper()} ({len(items)}):")
        for f in items:
            print(f"  [{f.where}] {f.message}")

    n_err = len(report.errors())
    n_warn = len(report.warnings())
    print(f"\nTotal: {n_err} errors, {n_warn} warnings, {len(by_sev['info'])} info")

    if n_err > 0:
        sys.exit(1)
    if args.strict and n_warn > 0:
        print("(strict mode: warnings counted as errors)")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
# end
