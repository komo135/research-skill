"""draft_imrad.py — Generate IMRAD draft from project artifacts.

Reads the Pure Research project's artifacts (PR/FAQ, pre-registrations,
explanation_ledger, decisions, results) and produces a starting-point
IMRAD-shaped draft per `references/pure_research/imrad_draft.md`.

The output is a STARTING POINT, not a final manuscript. The agent or user
must:
- Add narrative paragraphs the script cannot generate from structured data
- Reconcile any inconsistencies between artifacts
- Write the limitations and future-work sections
- Verify the prereg hash references and reproducibility stamp

Usage:
    python scripts/draft_imrad.py --project-dir <path>
    python scripts/draft_imrad.py --project-dir <path> --output imrad_draft.md
    python scripts/draft_imrad.py --project-dir <path> --supported-e E2

Inputs scanned:
    <project>/prfaq.md
    <project>/prereg/prfaq.lock
    <project>/prereg/PR_*.md
    <project>/prereg/PR_*.lock
    <project>/explanation_ledger.md
    <project>/decisions.md
    <project>/literature/papers.md
    <project>/results/results.parquet (optional, requires polars or pandas)

Exit codes:
    0: draft written
    1: required input missing (e.g., prfaq.md or explanation_ledger.md)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers (parsing markdown sections + tables)
# ---------------------------------------------------------------------------


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


def parse_lock(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, _, v = s.partition(":")
        out[k.strip()] = v.strip()
    return out


def extract_section(text: str, header_pattern: str) -> str:
    """Extract a section from markdown by matching its header. Returns empty
    string if not found."""
    pat = re.compile(rf"^##\s*{header_pattern}.*?$", re.MULTILINE | re.IGNORECASE)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    # Find next ## header or end of file
    next_pat = re.compile(r"^##\s+", re.MULTILINE)
    nxt = next_pat.search(text, start)
    end = nxt.start() if nxt else len(text)
    return text[start:end].strip()


# ---------------------------------------------------------------------------
# Artifact loaders
# ---------------------------------------------------------------------------


@dataclass
class ProjectArtifacts:
    project_dir: Path
    prfaq_text: str = ""
    prfaq_hash: str = ""
    prereg_files: list[Path] = None
    prereg_hashes: dict[str, str] = None
    ledger_q: list[dict] = None
    ledger_e: list[dict] = None
    ledger_claims: list[dict] = None
    decisions_text: str = ""
    papers_text: str = ""

    def __post_init__(self):
        self.prereg_files = self.prereg_files or []
        self.prereg_hashes = self.prereg_hashes or {}
        self.ledger_q = self.ledger_q or []
        self.ledger_e = self.ledger_e or []
        self.ledger_claims = self.ledger_claims or []


def load_artifacts(project_dir: Path) -> ProjectArtifacts:
    art = ProjectArtifacts(project_dir=project_dir)

    prfaq = project_dir / "prfaq.md"
    if prfaq.exists():
        art.prfaq_text = prfaq.read_text(encoding="utf-8")

    prfaq_lock = project_dir / "prereg" / "prfaq.lock"
    info = parse_lock(prfaq_lock)
    art.prfaq_hash = info.get("sha256", "")

    prereg_dir = project_dir / "prereg"
    if prereg_dir.exists():
        for md in sorted(prereg_dir.glob("PR_*.md")):
            art.prereg_files.append(md)
            lock = prereg_dir / f"{md.stem}.lock"
            info = parse_lock(lock)
            art.prereg_hashes[md.stem] = info.get("sha256", "")

    ledger = project_dir / "explanation_ledger.md"
    if ledger.exists():
        text = ledger.read_text(encoding="utf-8")
        art.ledger_q = parse_md_table(text, ["ID", "question"])
        art.ledger_e = parse_md_table(text, ["ID", "statement", "mechanism"])
        art.ledger_claims = parse_md_table(text, ["Q-ID", "E-ID", "claim"])

    decisions = project_dir / "decisions.md"
    if decisions.exists():
        art.decisions_text = decisions.read_text(encoding="utf-8")

    papers = project_dir / "literature" / "papers.md"
    if papers.exists():
        art.papers_text = papers.read_text(encoding="utf-8")

    return art


# ---------------------------------------------------------------------------
# IMRAD section generators
# ---------------------------------------------------------------------------


def section_introduction(art: ProjectArtifacts, supported_e: str) -> str:
    """Generate Section 1: Introduction from PR/FAQ Part 1."""
    pr_part = extract_section(art.prfaq_text, r"Part\s*1") or extract_section(art.prfaq_text, r"Press\s*Release")
    if not pr_part:
        pr_part = "<REPLACE: extract Press Release content from prfaq.md Part 1>"

    intro = [
        "## 1. Introduction",
        "",
        "### 1.1 Phenomenon",
        "<REPLACE: state the phenomenon under study, in concrete terms. The PR/FAQ Part 1 below contains the post-success summary; rewrite as introduction.>",
        "",
        "### 1.2 Prior work and its limits",
        "<REPLACE: cite ≥3 prior works from literature/papers.md. State what they established and what gap remains.>",
        "",
        "### 1.3 This study's contribution",
        "Per the PR/FAQ:",
        "",
        "> " + pr_part.replace("\n", "\n> "),
        "",
        f"This study was pre-registered. PR/FAQ hash: `{art.prfaq_hash[:16]}...`. " +
        f"Pre-registration hash(es): " + ", ".join(f"{stem} `{h[:16]}...`" for stem, h in art.prereg_hashes.items()) + ".",
        "",
    ]
    return "\n".join(intro)


def section_methods(art: ProjectArtifacts, supported_e: str) -> str:
    """Section 2: Methods from pre-registration files."""
    methods = [
        "## 2. Methods",
        "",
        "### 2.1 Pre-registration",
    ]

    for stem in sorted(art.prereg_hashes):
        h = art.prereg_hashes[stem]
        prereg_path = art.project_dir / "prereg" / f"{stem}.md"
        text = prereg_path.read_text(encoding="utf-8") if prereg_path.exists() else ""
        question = extract_section(text, r"1\.\s*Question") or "<REPLACE>"
        explanations = extract_section(text, r"2\.\s*Competing\s*explanations") or "<REPLACE>"
        test_design = extract_section(text, r"3\.\s*Test\s*design") or "<REPLACE>"

        methods.extend([
            f"#### Pre-reg `{stem}`",
            f"- Hash: `{h[:16]}...`",
            f"- Frozen: see `prereg/{stem}.lock`",
            "- Question:",
            f"  > {question[:300]}{'...' if len(question) > 300 else ''}",
            "- Competing explanations (≥2 + null):",
            f"  > {explanations[:500]}{'...' if len(explanations) > 500 else ''}",
            "",
        ])

    methods.extend([
        "",
        "### 2.2 Data",
        "<REPLACE: source, period, frequency, hash from `reproducibility/data_hashes.txt`>",
        "",
        "### 2.3 Sample / split",
        "<REPLACE: split methodology, N per split>",
        "",
        "### 2.4 Test design",
        "<REPLACE: copy test_design from pre-reg above; primary metric, threshold, multiple-testing correction>",
        "",
        "### 2.5 Deviations from pre-registration",
    ])

    # Try to find deviation entries in decisions.md
    devs = re.findall(r"##\s+\d{4}-\d{2}-\d{2}.*?[Dd]eviation.*?(?=\n##\s+|\Z)", art.decisions_text, re.DOTALL)
    if devs:
        methods.append(f"From `decisions.md`: {len(devs)} deviation entries detected.")
        for d in devs[:5]:
            first_line = d.splitlines()[0] if d.splitlines() else ""
            methods.append(f"- {first_line}")
    else:
        methods.append("No deviations recorded in decisions.md (or none detected). <REPLACE if any minor deviations exist>")

    methods.extend([
        "",
        "### 2.6 Reproducibility",
        "<REPLACE: data hash, git commit, env lock hash from `reproducibility/`. Random seed(s).>",
        "",
    ])
    return "\n".join(methods)


def section_results(art: ProjectArtifacts, supported_e: str) -> str:
    """Section 3: Results from explanation_ledger E rows."""
    results = [
        "## 3. Results",
        "",
        "### 3.1 Headline finding",
        "<REPLACE: single number with uncertainty band — primary metric value + bootstrap CI>",
        "",
        "### 3.2 Per-explanation observations",
        "",
    ]

    if art.ledger_e:
        for e in art.ledger_e:
            eid = get_col(e, "ID")
            statement = get_col(e, "statement")
            status = get_col(e, "Status")
            evidence = get_col(e, "current_evidence_summary")
            results.extend([
                f"- **{eid}** ({status}): {statement}",
                f"  - Evidence summary: {evidence or '<REPLACE: extract from explanation_ledger>'}",
            ])
        results.append("")
    else:
        results.append("<REPLACE: per-E observations from explanation_ledger.md>")
        results.append("")

    results.extend([
        "### 3.3 Robustness",
        "<REPLACE: sub-period / sub-universe / parameter sensitivity numbers>",
        "",
        "### 3.4 Verification checks",
        "<REPLACE: pass/fail status for each relevant generic verification or domain-adapter implementation check>",
        "",
    ])
    return "\n".join(results)


def section_discussion(art: ProjectArtifacts, supported_e: str) -> str:
    """Section 4: Discussion. Requires A4+ analysis per CHARTER C13."""
    supported_e_row = next((e for e in art.ledger_e if get_col(e, "ID") == supported_e), {})
    rejected_es = [e for e in art.ledger_e if "rejected" in get_col(e, "Status").lower()]
    weakened_es = [e for e in art.ledger_e if "weakened" in get_col(e, "Status").lower()]

    discussion = [
        "## 4. Discussion",
        "",
        "**Required: this section must reach analysis tier A4 minimum (per",
        "`references/shared/analysis_depth.md`). Mechanism named, alternatives",
        "excluded with discriminating evidence, scope precise, multiple sources",
        "of supporting evidence.**",
        "",
        "### 4.1 Interpretation",
    ]

    if supported_e_row:
        statement = get_col(supported_e_row, "statement")
        mechanism = get_col(supported_e_row, "mechanism")
        discussion.extend([
            f"The evidence supports **{supported_e}**: {statement}",
            "",
            f"Mechanism: {mechanism or '<REPLACE: causal chain>'}",
            "",
            "<REPLACE: walk the causal chain explicitly. Cite Section 3 observations.>",
            "<REPLACE: state scope conditions precisely (universe, period, regime, market structure preconditions).>",
        ])
    else:
        discussion.extend([
            f"<REPLACE: state which E reaches `supported` status, the mechanism, and scope.>",
            f"<Note: --supported-e {supported_e} not found in ledger E rows — fill manually.>",
        ])

    discussion.extend(["", "### 4.2 Alternatives weighed", ""])
    if weakened_es:
        for e in weakened_es:
            eid = get_col(e, "ID")
            statement = get_col(e, "statement")
            discussion.append(f"- **{eid} (weakened)**: {statement}")
            discussion.append("  - <REPLACE: cite the Methods § 2.4 expected pattern + Results § 3.2 observed pattern + reasoning that weakens E.>")
    else:
        discussion.append("<REPLACE: list weakened explanations and discriminating evidence>")

    discussion.extend(["", "### 4.3 Negative claims", ""])
    if rejected_es:
        for e in rejected_es:
            eid = get_col(e, "ID")
            statement = get_col(e, "statement")
            mechanism = get_col(e, "mechanism")
            discussion.append(f"- **{eid} (rejected)**: {statement}")
            if mechanism:
                discussion.append(f"  - Mechanism that was tested: {mechanism}")
            discussion.append("  - <REPLACE: discriminating evidence + scope of rejection. Same A4 rigor as positive claims.>")
    else:
        discussion.append("No rejected explanations recorded. <REPLACE if any rejections exist>")

    discussion.extend([
        "",
        "### 4.4 Limitations",
        "",
        "(Honest list. Identify ≥3 specific limitations.)",
        "",
        "1. **<REPLACE: limitation>**: <implication>",
        "2. **<REPLACE: limitation>**: <implication>",
        "3. **<REPLACE: limitation>**: <implication>",
        "",
        "### 4.5 Future work",
        "",
        "<REPLACE: next discriminating questions; sub-questions to spawn or sibling projects>",
        "",
    ])
    return "\n".join(discussion)


def appendix_prereg_log(art: ProjectArtifacts) -> str:
    lines = [
        "## Appendix B: Pre-registration log",
        "",
        "| PR ID | Hash (truncated) | Source file |",
        "|---|---|---|",
    ]
    for stem in sorted(art.prereg_hashes):
        h = art.prereg_hashes[stem]
        lines.append(f"| {stem} | `{h[:16]}...` | `prereg/{stem}.md` |")
    return "\n".join(lines)


def render_imrad(art: ProjectArtifacts, supported_e: str) -> str:
    title_line = f"# IMRAD draft — {art.project_dir.name}"
    parts = [
        title_line,
        "",
        "Auto-generated by `scripts/draft_imrad.py` from project artifacts.",
        "**This is a starting point — narrative paragraphs and limitations require",
        "agent / user revision.**",
        "",
        f"Status: <REPLACE: draft | revising | promotion-ready | promoted>",
        "",
        f"Pre-registration references:",
        f"- PR/FAQ hash: `{art.prfaq_hash[:16] if art.prfaq_hash else '(missing)'}...`",
        f"- Pre-reg files: " + ", ".join(art.prereg_hashes) if art.prereg_hashes else "(none)",
        "",
        "---",
        "",
        section_introduction(art, supported_e),
        section_methods(art, supported_e),
        section_results(art, supported_e),
        section_discussion(art, supported_e),
        "",
        "---",
        "",
        "## Appendix A: Cited literature",
        "",
        "<REPLACE: extract bibliography from literature/papers.md, filtered to references actually cited in Sections 1-4>",
        "",
        appendix_prereg_log(art),
    ]
    return "\n".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--supported-e", default="E1",
                   help="ID of the explanation being promoted to supported (e.g., E2)")
    p.add_argument("--output", type=Path, default=None,
                   help="output path (default: <project>/imrad_draft.md)")
    args = p.parse_args()

    art = load_artifacts(args.project_dir)
    if not art.prfaq_text:
        print(f"ERROR: prfaq.md not found at {args.project_dir}/prfaq.md", file=sys.stderr)
        sys.exit(1)
    if not art.ledger_e:
        print(f"WARN: explanation_ledger.md missing or empty — draft will have many <REPLACE> markers", file=sys.stderr)

    draft = render_imrad(art, args.supported_e)
    out = args.output or (args.project_dir / "imrad_draft.md")
    out.write_text(draft, encoding="utf-8")
    print(f"Wrote {len(draft.splitlines())} lines to {out}")
    n_replace = draft.count("<REPLACE")
    print(f"  {n_replace} <REPLACE> markers — agent / user must fill these")
    print()
    print("Next: revise the draft, then run promotion review per references/pure_research/pr_promotion_gate.md")


if __name__ == "__main__":
    main()
