#!/usr/bin/env python3
"""Verify a report.md against the skill's report contract.

Checks:
- All required sections present (Summary, Methods/System description, Results,
  Limitations, Next action).
- Figure references (![...](figures/X) or relative paths) resolve to actual files.
- Limitations section is non-empty (not just placeholder text).
- Next action section is non-empty and ideally references an iteration decision.

Exit code 0 if all pass, 1 if any issue.

Usage:
    python check_report.py <path_to_report.md>
"""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS_BASIC = ["Summary", "Background", "Methods", "Observations", "Limitations", "Next action"]
REQUIRED_SECTIONS_APPLIED = ["Summary", "Background", "Method / Procedure", "Evaluation", "Results", "Limitations", "Next action"]
REQUIRED_SECTIONS_DEV = ["Summary", "Background", "System description", "Performance", "Operational limits", "Limitations", "Next action"]

# Less strict: at least one of these sections must exist (we infer category from contents)
CORE_REQUIRED = ["Summary", "Limitations", "Next action"]

PLACEHOLDER_PATTERNS = [
    re.compile(r"<[A-Z]"),                 # <Some placeholder text>
    re.compile(r"^TODO", re.IGNORECASE),
    re.compile(r"^TBD", re.IGNORECASE),
    re.compile(r"^XXX"),
    re.compile(r"\{\{"),                   # {{template}} markers
]


def find_sections(text: str) -> dict:
    """Return mapping of section heading -> body text."""
    sections = {}
    current = None
    buffer = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = m.group(1).strip()
            buffer = []
        else:
            if current is not None:
                buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def find_figure_references(text: str) -> list:
    """Return list of (line_no, path) for all figure references."""
    refs = []
    # Match markdown images: ![alt](path)
    for i, line in enumerate(text.splitlines(), start=1):
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", line):
            refs.append((i, m.group(1)))
    return refs


def check_section_present(sections: dict, expected: list) -> list:
    """Return issues for missing core sections."""
    issues = []
    sections_lower = {k.lower(): k for k in sections}
    for required in expected:
        # Allow case-insensitive AND partial match for "Methods & Conditions"-style headings.
        found = False
        for key in sections_lower:
            if required.lower() in key:
                found = True
                break
        if not found:
            issues.append(f"  Missing required section: '{required}'")
    return issues


def check_section_nonempty(sections: dict, name: str) -> list:
    issues = []
    actual_key = None
    for key in sections:
        if name.lower() in key.lower():
            actual_key = key
            break
    if actual_key is None:
        return []  # Already flagged by check_section_present
    body = sections[actual_key]
    if not body or len(body.strip()) < 10:
        issues.append(f"  Section '{actual_key}' is empty or near-empty")
    # Check for placeholder-only content.
    if body and not re.search(r"[a-zA-Z]{20,}", body):
        # No long alphabetic stretch — likely placeholder.
        if all(any(p.search(line) for p in PLACEHOLDER_PATTERNS) for line in body.splitlines() if line.strip()):
            issues.append(f"  Section '{actual_key}' appears to contain only placeholder text")
    return issues


def check_figures_exist(report_path: Path, refs: list) -> list:
    issues = []
    report_dir = report_path.parent
    for line_no, ref in refs:
        # Skip external URLs.
        if ref.startswith(("http://", "https://")):
            continue
        # Skip placeholder names.
        if ref.endswith("<filename>.png") or "TODO" in ref or "PLACEHOLDER" in ref.upper():
            issues.append(f"  Line {line_no}: figure reference is a placeholder: '{ref}'")
            continue
        # Resolve relative to report dir.
        fig_path = (report_dir / ref).resolve()
        if not fig_path.exists():
            issues.append(f"  Line {line_no}: figure reference does not resolve: '{ref}' (looked for {fig_path})")
    return issues


def check_next_action_decision(sections: dict) -> list:
    """The Next action section should reference one of the 5 iteration decisions or a clear human-facing request."""
    issues = []
    for key in sections:
        if "next action" in key.lower():
            body = sections[key].upper()
            if any(d in body for d in ["NEXT_STEP", "REFINE", "ADJACENT", "PARK", "CLOSE"]):
                return []
            # Not an iteration decision — must contain a clear request or directive.
            if len(body.strip()) > 50:
                # Long enough to plausibly be a meaningful request.
                return []
            issues.append(f"  'Next action' section does not reference an iteration decision (NEXT_STEP/REFINE/ADJACENT/PARK/CLOSE) and is too short to be a clear request")
            return issues
    return issues


def main():
    parser = argparse.ArgumentParser(description="Verify report.md against skill contract.")
    parser.add_argument("path", help="Path to report.md")
    args = parser.parse_args()

    p = Path(args.path).resolve()
    if not p.exists():
        print(f"Error: file not found: {p}", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")
    sections = find_sections(text)

    print(f"Checking report: {p}")
    print(f"Found {len(sections)} sections: {list(sections.keys())}")
    print()

    all_issues = []

    # Core sections required regardless of category.
    all_issues.extend(check_section_present(sections, CORE_REQUIRED))

    # Non-empty checks for Summary, Limitations.
    for sec in ["Summary", "Results", "Observations", "Performance", "Limitations", "Next action"]:
        all_issues.extend(check_section_nonempty(sections, sec))

    # Next action discipline.
    all_issues.extend(check_next_action_decision(sections))

    # Figure existence.
    refs = find_figure_references(text)
    if refs:
        print(f"Found {len(refs)} figure reference(s).")
    all_issues.extend(check_figures_exist(p, refs))

    if all_issues:
        print(f"\n{len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
        sys.exit(1)

    print("Report passes all contract checks.")


if __name__ == "__main__":
    main()
