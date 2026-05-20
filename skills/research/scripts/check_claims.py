#!/usr/bin/env python3
"""Verify claim records in a plan or paper file.

Parses load-bearing claim records under a "## Claims" section. Verifies:
- All five required fields are present per claim (claim, evidence,
  alternatives_not_excluded, conditions_tested, conditions_not_tested).
- Empty list `[]` is allowed for the two list fields; a missing field is not.
- Claim text passes a vagueness heuristic (presence of a metric, magnitude,
  or specific condition reference).

Exit code 0 if all claims pass, 1 if any issue is reported.

Usage:
    python check_claims.py <path_to_plan_or_paper.md>
"""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "claim",
    "evidence",
    "alternatives_not_excluded",
    "conditions_tested",
    "conditions_not_tested",
]

VAGUE_PATTERNS = [
    r"\bour method works\b",
    r"\bis better\b",
    r"\bis good\b",
    r"\bis useful\b",
    r"\bworks well\b",
    r"\bperforms well\b",
    r"\bsignificantly better\b",  # without numbers
]

NUMERIC_HINT = re.compile(r"[0-9]|%|×|x[0-9]|p<|n=")


def parse_claims(text: str):
    """Extract YAML-like claim records under a Claims heading.

    Each claim begins with a line matching '- claim:'. Field lines that follow
    are indented and start with one of the required field names.
    """
    claims = []
    in_claims = False
    current = None

    for line in text.splitlines():
        header_match = re.match(r"^#+\s+(.+?)\s*$", line)
        if header_match:
            heading = header_match.group(1).strip().lower()
            if heading == "claims":
                in_claims = True
                if current is not None:
                    claims.append(current)
                    current = None
                continue
            # Any other heading ends the Claims section.
            if in_claims:
                in_claims = False
                if current is not None:
                    claims.append(current)
                    current = None
            continue

        if not in_claims:
            continue

        # New claim record.
        m = re.match(r"^\s*-\s*claim\s*:\s*(.+?)\s*$", line)
        if m:
            if current is not None:
                claims.append(current)
            current = {"claim": m.group(1).strip()}
            continue

        if current is None:
            continue

        # Subsequent field on its own line.
        for field in REQUIRED_FIELDS[1:]:
            fm = re.match(rf"^\s*{field}\s*:\s*(.*)$", line)
            if fm:
                value = fm.group(1).strip()
                # For list fields, treat empty `[]` or empty mapping as empty list.
                if field in ("alternatives_not_excluded", "conditions_not_tested"):
                    if value in ("[]", "", "None"):
                        current[field] = []
                    elif value.startswith("[") and value.endswith("]"):
                        # Inline list — split on commas roughly.
                        inner = value[1:-1].strip()
                        current[field] = [s.strip().strip("'\"") for s in inner.split(",")] if inner else []
                    else:
                        # Multi-line list follows; capture marker for further lines.
                        current[field] = value if value else []
                else:
                    current[field] = value
                break
        else:
            # Continuation line for multi-line list (lines starting with "    - ").
            list_item = re.match(r"^\s{2,}-\s+(.+?)\s*$", line)
            if list_item and current is not None:
                # Append to the most recently seen list field, if any.
                for field in ("conditions_not_tested", "alternatives_not_excluded"):
                    if field in current and isinstance(current[field], list):
                        current[field].append(list_item.group(1).strip().strip("'\""))
                        break

    if current is not None:
        claims.append(current)

    return claims


def check_claim(idx: int, c: dict) -> list:
    """Return a list of issue strings for one claim. Empty list = passes."""
    issues = []
    for field in REQUIRED_FIELDS:
        if field not in c:
            issues.append(f"  Claim {idx + 1}: missing field '{field}'")

    if "claim" in c:
        claim_text = c["claim"].lower()
        for pattern in VAGUE_PATTERNS:
            if re.search(pattern, claim_text):
                if not NUMERIC_HINT.search(claim_text):
                    issues.append(
                        f"  Claim {idx + 1}: vague claim text — no metric, magnitude, or specific condition: "
                        f"{c['claim'][:80]}"
                    )
                    break

    if "evidence" in c:
        ev = c["evidence"].lower()
        if ev in ("see the experiments", "the data", "the results", "as discussed"):
            issues.append(f"  Claim {idx + 1}: vague evidence pointer: '{c['evidence']}'")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Verify claim record structure.")
    parser.add_argument("path", help="Plan or paper markdown file to check")
    args = parser.parse_args()

    p = Path(args.path)
    if not p.exists():
        print(f"Error: file not found: {p}", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")
    claims = parse_claims(text)

    print(f"Found {len(claims)} claim record(s) in {p}")

    all_issues = []
    for i, c in enumerate(claims):
        all_issues.extend(check_claim(i, c))

    if all_issues:
        print(f"\n{len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
        sys.exit(1)

    if claims:
        print("All claims have required fields and pass basic vagueness checks.")
    else:
        print("(No claims found under a '## Claims' section. This may be fine for early-stage plans.)")


if __name__ == "__main__":
    main()
