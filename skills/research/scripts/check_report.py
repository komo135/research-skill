#!/usr/bin/env python3
"""Verify a report.md against the skill's v2.4 report contract.

Checks:
- Paper-grade required sections are present: Summary, Background, Related Work,
  Theory / Formulation, Ablation / Sensitivity, Discussion, Limitations,
  Next action, and References.
- At least one evidence-bearing outcome section is present: Results,
  Observations, or Performance.
- At least one methods, system, or derivation-context section is present.
- v2.4 paper-grade sections are allowed, including Theory / Formulation and
  Derivation context.
- Outcome sections include a figure, table, or explicit `No figure/table:` reason.
- Figure references (![...](figures/X) or relative paths) resolve to actual files.
- Limitations section is non-empty (not just placeholder text).
- Next action section is non-empty and ideally references an iteration decision.
- Numeric outcome sections include a statistical reporting minimum: sample size,
  variance/dispersion, CI, effect size, significance, or an explicit non-applicability reason.

Exit code 0 if all pass, 1 if any issue.

Usage:
    python check_report.py <path_to_report.md>
"""
import argparse
import re
import sys
from pathlib import Path


COMMON_REQUIRED = [
    "Summary",
    "Background",
    "Related Work",
    "Theory / Formulation",
    "Ablation / Sensitivity",
    "Discussion",
    "Limitations",
    "Next action",
    "References",
]
CONTEXT_SECTION_OPTIONS = [
    "Methods & Conditions",
    "Methods",
    "Method / Procedure",
    "System description",
    "Derivation context",
]
OUTCOME_SECTION_OPTIONS = ["Results", "Observations", "Performance"]
NONEMPTY_IF_PRESENT = [
    "Summary",
    "Background",
    "Related Work",
    "Methods & Conditions",
    "Methods",
    "Method / Procedure",
    "System description",
    "Theory / Formulation",
    "Derivation context",
    "Results",
    "Observations",
    "Performance",
    "Ablation / Sensitivity",
    "Discussion",
    "Limitations",
    "Next action",
    "References",
]

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


def normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def section_key(sections: dict, expected: str) -> str | None:
    expected_normalized = normalize_heading(expected)
    for key in sections:
        if normalize_heading(key) == expected_normalized:
            return key
    return None


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
    for required in expected:
        if section_key(sections, required) is None:
            issues.append(f"  Missing required section: '{required}'")
    return issues


def check_any_section_present(sections: dict, options: list, label: str) -> list:
    for option in options:
        if section_key(sections, option) is not None:
            return []
    return [f"  Missing required {label}: one of {options}"]


def check_section_nonempty(sections: dict, name: str) -> list:
    issues = []
    actual_key = section_key(sections, name)
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
    key = section_key(sections, "Next action")
    if key is None:
        return issues
    body = sections[key].upper()
    if any(d in body for d in ["NEXT_STEP", "REFINE", "ADJACENT", "PARK", "CLOSE"]):
        return []
    # Not an iteration decision — must contain a clear request or directive.
    if len(body.strip()) > 50:
        # Long enough to plausibly be a meaningful request.
        return []
    issues.append(f"  'Next action' section does not reference an iteration decision (NEXT_STEP/REFINE/ADJACENT/PARK/CLOSE) and is too short to be a clear request")
    return issues


def has_explicit_statistical_nonapplicability(body: str) -> bool:
    lowered = body.lower()
    return bool(re.search(r"(statistical reporting minimum|sample size|variance|ci|confidence interval|effect size|significance).{0,80}(does not apply|not applicable|n/a)", lowered))


def has_sample_size_value(body: str) -> bool:
    return bool(re.search(r"\b(?:n|sample size|sample count)\s*(?:=|:|is|was)?\s*\d+\b", body, flags=re.IGNORECASE))


def has_variability_or_inference_value(body: str) -> bool:
    patterns = [
        r"\b(?:variance|dispersion|standard deviation|std|sd)\s*(?:=|:|is|was)?\s*\d",
        r"\b(?:\d{2,3}%\s*)?ci\b\s*(?:=|:|is|was)?\s*[\[(]?\s*-?\d",
        r"\bconfidence interval\s*(?:=|:|is|was)?\s*[\[(]?\s*-?\d",
        r"\beffect size\s*(?:=|:|is|was)?\s*-?\d",
        r"\bp[- ]?value\s*(?:=|:|is|was)?\s*[<=>]?\s*\d",
        r"\bp\s*=\s*[<=>]?\s*\d",
        r"\bsignificance\s*(?:=|:|is|was)?\s*[<=>]?\s*\d",
    ]
    return any(re.search(pattern, body, flags=re.IGNORECASE) for pattern in patterns)


def is_numeric_evidence_context(section_name: str, body: str) -> bool:
    if not re.search(r"\d", body):
        return False
    if normalize_heading(section_name) in {"results", "performance"}:
        return True
    lowered = body.lower()
    evidence_terms = [
        "metric",
        "accuracy",
        "precision",
        "recall",
        "performance",
        "score",
        "rate",
        "loss",
        "baseline",
        "%",
    ]
    return any(term in lowered for term in evidence_terms) or has_markdown_table(body)


def check_numeric_outcome_reporting(sections: dict) -> list:
    issues = []
    for key, body in sections.items():
        if normalize_heading(key) not in {normalize_heading(option) for option in OUTCOME_SECTION_OPTIONS}:
            continue
        if not is_numeric_evidence_context(key, body):
            continue
        if has_explicit_statistical_nonapplicability(body):
            continue
        if has_sample_size_value(body) and has_variability_or_inference_value(body):
            continue
        issues.append(
            f"  Section '{key}' has numeric Results but numeric Results must report sample size, variance/dispersion, CI, effect size, significance, or a non-applicability reason"
        )
    return issues


def has_markdown_table(body: str) -> bool:
    lines = [line.strip() for line in body.splitlines()]
    for i in range(len(lines) - 1):
        if "|" in lines[i] and re.search(r"\|\s*:?-{3,}:?\s*(\||$)", lines[i + 1]):
            return True
    return False


def has_markdown_image(body: str) -> bool:
    return bool(re.search(r"!\[[^\]]*\]\(([^)]+)\)", body))


def has_no_figure_table_reason(body: str) -> bool:
    return bool(re.search(r"(?im)^no figure/table:\s+\S.{20,}$", body))


def check_outcome_evidence_carrier(sections: dict) -> list:
    issues = []
    for key, body in sections.items():
        if normalize_heading(key) not in {normalize_heading(option) for option in OUTCOME_SECTION_OPTIONS}:
            continue
        if has_markdown_image(body) or has_markdown_table(body) or has_no_figure_table_reason(body):
            continue
        issues.append(f"  Section '{key}' must include a figure, table, or 'No figure/table:' reason")
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

    # Common sections required regardless of category. Category- and
    # mode-specific sections are intentionally conditional in v2.4.
    all_issues.extend(check_section_present(sections, COMMON_REQUIRED))
    all_issues.extend(check_any_section_present(sections, CONTEXT_SECTION_OPTIONS, "method/system/theory section"))
    all_issues.extend(check_any_section_present(sections, OUTCOME_SECTION_OPTIONS, "outcome section"))

    # Non-empty checks for common and recognized paper-grade sections.
    for sec in NONEMPTY_IF_PRESENT:
        all_issues.extend(check_section_nonempty(sections, sec))

    # Next action discipline.
    all_issues.extend(check_next_action_decision(sections))

    # Statistical reporting minimum for numeric evidence.
    all_issues.extend(check_numeric_outcome_reporting(sections))

    # Evidence carrier for outcome sections.
    all_issues.extend(check_outcome_evidence_carrier(sections))

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
