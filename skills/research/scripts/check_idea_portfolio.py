#!/usr/bin/env python3
"""Verify an Idea portfolio against the research ideation contract.

Checks:
- If an Idea portfolio is present and applicable, it contains the generation
  substrate, generation operators, assumption audit, anti-vacuity gate,
  blind-spot catalog, evaluator feedback, pruning, scoring, divergence review,
  and promotion record.
- The substrate contains at least two named substrate ids.
- Generation operators and the anti-vacuity gate contain the fields that keep
  candidates from being accepted as post-hoc prose.
- Evaluator feedback records either real evaluator evidence or a named skip
  reason plus the effect on promotion.
- Every surviving candidate has a blind-spot record that states a possible
  mechanism failure path, claim-scope effect, and required repair.

Exit code 0 if all checks pass, 1 if any issue is reported.

Usage:
    python check_idea_portfolio.py <path_to_plan.md>
"""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_SUBSECTIONS = [
    "Idea substrate",
    "Generation operators",
    "De-anchored candidates",
    "Assumption audit",
    "Anti-vacuity gate",
    "Blind-spot catalog",
    "Hypothesis synthesis",
    "Evaluator feedback",
    "Grounded pruning",
    "Information-gain scoring",
    "Pre-execution divergence review",
    "Promotion decision",
]

GENERATION_FIELDS = [
    "Substrate ids",
    "Operator",
    "Changed premise",
]

ANTI_VACUITY_FIELDS = [
    "Substrate ids",
    "Changed premise",
    "Mechanism conjecture",
    "Predicted measurable effect",
    "Counter-hypothesis",
    "Minimal disconfirming test",
    "Verdict",
]

BLIND_SPOT_FIELDS = [
    "Blind-spot area",
    "How it could break the mechanism",
    "Claim-scope effect",
    "Required repair",
]

CLAIM_SCOPE_EFFECT_PREFIXES = [
    "conditions_not_tested",
    "narrowed_claim",
    "park",
    "adjacent",
    "no_change",
]

REQUIRED_REPAIR_PREFIXES = [
    "retrieval",
    "evaluator construction",
    "evaluator_construction",
    "user_input",
    "narrow_conditions",
    "none_with_reason",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"<[^>]+>"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\{\{"),
]


def extract_idea_portfolio(text: str) -> str | None:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Idea portfolio\s*$", line, flags=re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None

    end = len(lines)
    for i in range(start, len(lines)):
        if re.match(r"^##\s+\S", lines[i]):
            end = i
            break
    return "\n".join(lines[start:end]).strip()


def extract_subsections(portfolio: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []

    for line in portfolio.splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = m.group(1).strip()
            buffer = []
        elif current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def section_key(sections: dict[str, str], expected: str) -> str | None:
    for key in sections:
        if expected.lower() == key.lower():
            return key
    return None


def has_placeholder_only(body: str) -> bool:
    content_lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not content_lines:
        return True
    return all(any(pattern.search(line) for pattern in PLACEHOLDER_PATTERNS) for line in content_lines)


def is_bare_none_or_missing_reason(value: str) -> bool:
    normalized = value.strip().lower()
    stripped = normalized.strip(" .;:-")
    if stripped in {"none", "n/a", "na", "not applicable"}:
        return True

    match = re.match(r"^none\s+with\s+reason\b(.*)$", normalized)
    if match:
        return not bool(match.group(1).strip(" .;:-"))
    return False


def is_meaningful_contract_value(value: str) -> bool:
    return (
        bool(value.strip())
        and not has_placeholder_only(value)
        and not is_bare_none_or_missing_reason(value)
    )


def has_allowed_prefixed_value(value: str, prefixes: list[str]) -> bool:
    lowered = value.strip().lower()
    for prefix in prefixes:
        match = re.match(rf"^{re.escape(prefix.lower())}\s*:\s*(.+)$", lowered)
        if match and is_meaningful_contract_value(match.group(1)):
            return True
    return False


def check_required_subsections(sections: dict[str, str]) -> list[str]:
    issues = []
    for expected in REQUIRED_SUBSECTIONS:
        key = section_key(sections, expected)
        if key is None:
            issues.append(f"  Missing required Idea portfolio subsection: '{expected}'")
            continue
        body = sections[key]
        if len(body.strip()) < 20 or has_placeholder_only(body):
            issues.append(f"  Idea portfolio subsection '{key}' is empty or placeholder-only")
    return issues


def check_substrate(sections: dict[str, str]) -> list[str]:
    key = section_key(sections, "Idea substrate")
    if key is None:
        return []

    body = sections[key]
    ids = re.findall(r"^\s*-\s*([A-Z][A-Z0-9_-]*\d*)\s*:", body, flags=re.MULTILINE)
    if len(set(ids)) < 2:
        return ["  Idea substrate must define at least two named substrate ids such as S1: and S2:"]
    return []


def check_fields(sections: dict[str, str], section: str, fields: list[str]) -> list[str]:
    key = section_key(sections, section)
    if key is None:
        return []
    body = sections[key].lower()
    issues = []
    for field in fields:
        if field.lower() not in body:
            issues.append(f"  Section '{key}' missing required field: '{field}'")
    return issues


def parse_candidate_blocks(body: str) -> dict[str, dict[str, str]]:
    """Parse top-level markdown candidate blocks and their indented fields."""
    candidates: dict[str, dict[str, str]] = {}
    current = None

    for line in body.splitlines():
        candidate = re.match(r"^-\s*([^:]+?)\s*:\s*(.*)$", line)
        if candidate:
            current = candidate.group(1).strip()
            candidates.setdefault(current, {})
            rest = candidate.group(2).strip()
            if rest:
                candidates[current]["_summary"] = rest
            continue

        field = re.match(r"^\s{2,}-\s*([^:]+?)\s*:\s*(.*?)\s*$", line)
        if field and current is not None:
            candidates[current][field.group(1).strip().lower()] = field.group(2).strip()

    return candidates


def substrate_ids_from_section(sections: dict[str, str]) -> set[str]:
    key = section_key(sections, "Idea substrate")
    if key is None:
        return set()
    body = sections[key]
    return set(re.findall(r"^\s*-\s*([A-Z][A-Z0-9_-]*\d*)\s*:", body, flags=re.MULTILINE))


def candidate_refs(value: str) -> set[str]:
    return set(re.findall(r"\b[A-Z][A-Z0-9_-]*\d+\b", value))


def has_named_missing_constraint(value: str) -> bool:
    lowered = value.lower()
    return "constraint" in lowered or "missing" in lowered or "not available" in lowered


def normalize_verdict(value: str) -> str | None:
    normalized = value.strip().lower().strip(" .;")
    if normalized in {"survives", "killed"}:
        return normalized
    return None


def check_candidate_refs(candidate: str, value: str, defined_ids: set[str]) -> list[str]:
    issues = []
    refs = candidate_refs(value)
    if not refs and not has_named_missing_constraint(value):
        issues.append(f"  Candidate '{candidate}' must cite substrate ids or a named missing-substrate constraint")
        return issues
    if refs and len(refs) < 2 and not has_named_missing_constraint(value):
        issues.append(f"  Candidate '{candidate}' must cite at least two substrate ids or a named missing-substrate constraint")
    for ref in sorted(refs - defined_ids):
        issues.append(f"  Candidate '{candidate}' references undefined substrate id '{ref}'")
    return issues


def check_blind_spot_fields(candidate: str, fields: dict[str, str]) -> list[str]:
    issues: list[str] = []

    for field in BLIND_SPOT_FIELDS:
        key = field.lower()
        if key not in fields:
            issues.append(f"  Candidate '{candidate}' blind-spot block missing '{field}'")
            continue
        if not is_meaningful_contract_value(fields[key]):
            issues.append(
                f"  Candidate '{candidate}' blind-spot field '{field}' is empty, placeholder-only, or bare None"
            )

    claim_scope = fields.get("claim-scope effect", "")
    if is_meaningful_contract_value(claim_scope) and not has_allowed_prefixed_value(claim_scope, CLAIM_SCOPE_EFFECT_PREFIXES):
        issues.append(
            f"  Candidate '{candidate}' blind-spot Claim-scope effect must start with conditions_not_tested:, narrowed_claim:, PARK:, ADJACENT:, or no_change:"
        )

    repair = fields.get("required repair", "")
    if is_meaningful_contract_value(repair) and not has_allowed_prefixed_value(repair, REQUIRED_REPAIR_PREFIXES):
        issues.append(
            f"  Candidate '{candidate}' blind-spot Required repair must start with retrieval:, user_input:, evaluator_construction:, narrow_conditions:, or none_with_reason:"
        )

    return issues


def check_candidate_contract(sections: dict[str, str]) -> list[str]:
    issues: list[str] = []
    defined_ids = substrate_ids_from_section(sections)

    generation_key = section_key(sections, "Generation operators")
    anti_key = section_key(sections, "Anti-vacuity gate")
    synthesis_key = section_key(sections, "Hypothesis synthesis")
    blind_spot_key = section_key(sections, "Blind-spot catalog")
    pruning_key = section_key(sections, "Grounded pruning")
    promotion_key = section_key(sections, "Promotion decision")

    generation = parse_candidate_blocks(sections.get(generation_key or "", ""))
    anti = parse_candidate_blocks(sections.get(anti_key or "", ""))
    synthesis = parse_candidate_blocks(sections.get(synthesis_key or "", ""))
    blind_spots = parse_candidate_blocks(sections.get(blind_spot_key or "", ""))

    if not generation:
        issues.append("  Generation operators must define at least one candidate block")

    for candidate, fields in generation.items():
        for field in GENERATION_FIELDS:
            if field.lower() not in fields:
                issues.append(f"  Candidate '{candidate}' generation block missing '{field}'")
        if "substrate ids" in fields:
            issues.extend(check_candidate_refs(candidate, fields["substrate ids"], defined_ids))

    for candidate, fields in anti.items():
        if candidate not in generation:
            issues.append(f"  Anti-vacuity candidate '{candidate}' has no generation-operator block")
        for field in ANTI_VACUITY_FIELDS:
            if field.lower() not in fields:
                issues.append(f"  Candidate '{candidate}' anti-vacuity block missing '{field}'")
        if "substrate ids" in fields:
            issues.extend(check_candidate_refs(candidate, fields["substrate ids"], defined_ids))
        verdict_value = fields.get("verdict", "")
        if verdict_value and normalize_verdict(verdict_value) is None:
            issues.append(f"  Candidate '{candidate}' anti-vacuity verdict must be exactly 'survives' or 'killed'")

    for candidate in synthesis:
        if candidate not in anti:
            issues.append(f"  Hypothesis synthesis candidate '{candidate}' did not pass through anti-vacuity")
        elif normalize_verdict(anti[candidate].get("verdict", "")) != "survives":
            issues.append(f"  Hypothesis synthesis candidate '{candidate}' did not survive anti-vacuity")

    survived = {name for name, fields in anti.items() if normalize_verdict(fields.get("verdict", "")) == "survives"}
    known_candidates = set(generation) | set(anti) | set(synthesis)

    for candidate, fields in blind_spots.items():
        if candidate not in known_candidates:
            issues.append(f"  Blind-spot candidate '{candidate}' has no candidate contract block")
        issues.extend(check_blind_spot_fields(candidate, fields))

    def mentioned_candidates(text: str) -> set[str]:
        return {candidate for candidate in known_candidates if re.search(rf"\b{re.escape(candidate)}\b", text)}

    advanced_candidates: set[str] = set()
    if pruning_key is not None:
        pruning = sections[pruning_key]
        for line in pruning.splitlines():
            if re.match(r"^\s*-\s*Advance\s*:", line, flags=re.IGNORECASE):
                advanced = mentioned_candidates(line)
                advanced_candidates.update(advanced)
                for candidate in advanced:
                    if candidate not in survived:
                        issues.append(f"  Advanced candidate '{candidate}' did not survive anti-vacuity")

    if promotion_key is not None:
        promotion = sections[promotion_key]
        promoted_lines = [
            line for line in promotion.splitlines()
            if re.match(r"^\s*-\s*Promoted idea\s*:", line, flags=re.IGNORECASE)
        ]
        for line in promoted_lines:
            promoted = mentioned_candidates(line)
            if not promoted and "none" not in line.lower():
                issues.append("  Promotion decision names no known candidate")
            for candidate in promoted:
                if candidate not in survived:
                    issues.append(f"  promoted candidate '{candidate}' did not survive anti-vacuity")
                if pruning_key is not None and candidate not in advanced_candidates:
                    issues.append(f"  promoted candidate '{candidate}' was not advanced by grounded pruning")

    for candidate in sorted(survived):
        if candidate not in blind_spots:
            issues.append(f"  survived candidate '{candidate}' missing blind-spot catalog block")

    return issues


def check_anti_vacuity_verdict(sections: dict[str, str]) -> list[str]:
    key = section_key(sections, "Anti-vacuity gate")
    if key is None:
        return []
    body = sections[key].lower()
    if "verdict:" not in body:
        return ["  Anti-vacuity gate must record a candidate verdict"]
    return []


def check_evaluator_feedback(sections: dict[str, str]) -> list[str]:
    key = section_key(sections, "Evaluator feedback")
    if key is None:
        return []

    body = sections[key].lower()
    issues = []
    if "status:" not in body:
        issues.append("  Evaluator feedback must include 'Status:'")
        return issues

    if "skipped:" in body:
        for required in ["required evaluator", "effect on promotion"]:
            if required not in body:
                issues.append(f"  Skipped evaluator feedback missing '{required}'")
        return issues

    if "ran:" in body:
        for required in ["executable signature", "artifact", "fitness vector"]:
            if required not in body:
                issues.append(f"  Ran evaluator feedback missing '{required}'")
        return issues

    issues.append("  Evaluator feedback status must be 'Ran:' or 'Skipped:'")
    return issues


def check_portfolio(text: str) -> list[str]:
    portfolio = extract_idea_portfolio(text)
    if portfolio is None:
        return []

    if "not applicable: objective already chosen" in portfolio.lower() and "###" not in portfolio:
        return []

    sections = extract_subsections(portfolio)
    issues: list[str] = []
    issues.extend(check_required_subsections(sections))
    issues.extend(check_substrate(sections))
    issues.extend(check_fields(sections, "Generation operators", GENERATION_FIELDS))
    issues.extend(check_fields(sections, "Anti-vacuity gate", ANTI_VACUITY_FIELDS))
    issues.extend(check_candidate_contract(sections))
    issues.extend(check_anti_vacuity_verdict(sections))
    issues.extend(check_evaluator_feedback(sections))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Verify an Idea portfolio against the research ideation contract.")
    parser.add_argument("path", help="Path to plan markdown file")
    args = parser.parse_args()

    p = Path(args.path).resolve()
    if not p.exists():
        print(f"Error: file not found: {p}", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")
    issues = check_portfolio(text)

    print(f"Checking Idea portfolio: {p}")
    if issues:
        print(f"\n{len(issues)} issue(s):")
        for issue in issues:
            print(issue)
        sys.exit(1)

    print("Idea portfolio passes contract checks.")


if __name__ == "__main__":
    main()
