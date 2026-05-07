"""charter_interview.py — Interactive elicitation of the Heilmeier 8 questions.

Walks the user (or the agent walking the user) through the 8 charter
questions per `references/rd/rd_charter.md`. Validates each answer against
the discipline (concrete kill criteria, one-time vs recurring cost split,
integration pattern declaration). Outputs charter.md.

Does NOT auto-freeze. After the user reviews charter.md, run
`scripts/prereg_freeze.py --type charter --path charter.md`.

Usage:
    python scripts/charter_interview.py --output <path-to-charter.md>
    python scripts/charter_interview.py --output charter.md --non-interactive \\
        --answers-yaml answers.yaml

In non-interactive mode (for agent use), provide all answers in a YAML file.

Exit codes:
    0: charter.md written successfully
    1: validation failed (e.g., kill criteria are not concrete)
    2: setup error (output path invalid, YAML missing)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# Templates and validation per question
QUESTIONS = [
    {
        "id": "H1",
        "title": "What capability should exist?",
        "prompt": (
            "State the target as a single sentence describing what new capability "
            "the project will produce. Use no internal jargon, no library names, no "
            "model names. Imagine explaining to a smart person from a different domain."
        ),
        "validate": lambda s: len(s.strip()) >= 30 or "too short — at least one full sentence required",
    },
    {
        "id": "H2",
        "title": "How is this approximated today, and what are the limits?",
        "prompt": (
            "Describe the current best practice (team's or field's) and what is "
            "specifically unsatisfactory. Quantify the limit if possible."
        ),
        "validate": lambda s: len(s.strip()) >= 50 or "too short — explain current state and the limit",
    },
    {
        "id": "H3",
        "title": "What is new in the proposed approach, and why might it work?",
        "prompt": (
            "Name the specific novelty (algorithm, data, decomposition, validation). "
            "State the prior evidence or mechanism that makes success plausible."
        ),
        "validate": lambda s: len(s.strip()) >= 50 or "too short — name novelty + plausibility",
    },
    {
        "id": "H4",
        "title": "Who cares? Who is the consumer, and what decision does this serve?",
        "prompt": (
            "Name a specific consumer and the decision they are currently blocked on."
        ),
        "validate": lambda s: len(s.strip()) >= 30 or "too short — consumer must be named",
    },
    {
        "id": "H5",
        "title": "If we succeed, what changes downstream?",
        "prompt": "Describe the world after success in concrete terms. Quantify if possible.",
        "validate": lambda s: len(s.strip()) >= 30 or "too short",
    },
    {
        "id": "H6",
        "title": "Dominant risks + kill criteria",
        "prompt": (
            "List 3-5 risks. For each, name SPECIFIC OBSERVABLE EVIDENCE that would "
            "kill the project. These become the project's binding kill criteria. "
            "Format: '<risk>. KILL if <numeric or behavioral threshold>.'"
        ),
        "validate": None,  # bound below to _validate_kill_criteria
    },
    {
        "id": "H7",
        "title": "Cost: one-time vs recurring",
        "prompt": (
            "Provide compute / data / wall-clock cost in two subsections: "
            "ONE-TIME (charter, decomposition, initial setup) and RECURRING "
            "(re-tuning cadence, monitoring, ongoing data feed). "
            "Format your answer as 'one_time: <text>\\nrecurring: <text>'."
        ),
        "validate": None,  # bound below to _validate_cost_split
    },
    {
        "id": "H8",
        "title": "Midterm exam, final exam, and integration pattern",
        "prompt": (
            "Provide three subsections:\n"
            "  midterm: <concrete demonstration of the hardest sub-question>\n"
            "  final: <TRL-6 operational prototype on representative workload>\n"
            "  integration_pattern: <Pattern 1 | Pattern 2 | Pattern 3> + reason\n"
            "Per references/rd/integration_patterns.md, Pattern 3 (skeleton + spike) "
            "is the recommended default."
        ),
        "validate": None,  # bound below to _validate_h8
    },
]


# Validators for the structured questions

def _validate_kill_criteria(s: str) -> str | bool:
    """H6: must contain at least 1 'KILL if' line with numeric/behavioral threshold."""
    if "kill if" not in s.lower():
        return "no 'KILL if' marker found — kill criteria must be concrete"
    # Look for numeric markers or behavioral verbs
    has_numeric = bool(re.search(r"[<>≤≥]\s*\d|\d+\s*(%|bp|ms|s|days?|weeks?|hours?)", s))
    has_behavioral = bool(re.search(r"\b(fails to|cannot|does not|unable|exceeds|drops below|requires)\b", s, re.IGNORECASE))
    if not (has_numeric or has_behavioral):
        return "kill criteria are not concrete (no numeric threshold + no behavioral marker)"
    return True


def _validate_cost_split(s: str) -> str | bool:
    """H7: must have one_time + recurring subsections."""
    has_onetime = bool(re.search(r"one[_-]?time", s, re.IGNORECASE))
    has_recurring = bool(re.search(r"recurring|ongoing|per[_-]?(year|month|cycle)", s, re.IGNORECASE))
    if not has_onetime:
        return "no 'one_time' subsection — H7 requires one-time vs recurring split"
    if not has_recurring:
        # Allow if user explicitly says "all 永続型, no recurring"
        if "永続型" not in s and "no recurring" not in s.lower():
            return "no 'recurring' subsection — H7 requires recurring even if 'no recurring' (with justification)"
    return True


def _validate_h8(s: str) -> str | bool:
    """H8: must mention midterm + final + integration_pattern."""
    s_lower = s.lower()
    if "midterm" not in s_lower:
        return "missing 'midterm' subsection"
    if "final" not in s_lower:
        return "missing 'final' subsection"
    if "integration" not in s_lower or "pattern" not in s_lower:
        return "missing integration pattern declaration (per CHARTER C15 / Amendment-3)"
    if not re.search(r"pattern\s*[123]", s_lower):
        return "integration pattern not specified as Pattern 1 / Pattern 2 / Pattern 3"
    return True


# Wire up validators
QUESTIONS[5]["validate"] = _validate_kill_criteria
QUESTIONS[6]["validate"] = _validate_cost_split
QUESTIONS[7]["validate"] = _validate_h8


@dataclass
class Answer:
    qid: str
    title: str
    text: str


def interactive_collect() -> list[Answer]:
    """Walk the user through the 8 questions interactively."""
    print("\n=== R&D Charter Interview (Heilmeier 8 questions) ===\n")
    print("Answer each question. Type END on its own line to finish a multi-line answer.")
    print("Validation runs after each answer; you may revise.\n")

    answers: list[Answer] = []
    for q in QUESTIONS:
        while True:
            print(f"\n--- {q['id']}: {q['title']} ---")
            print(q["prompt"])
            print("(Enter answer, end with line containing only 'END'):")
            lines: list[str] = []
            try:
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
            except EOFError:
                pass
            text = "\n".join(lines).strip()
            if not text:
                print("(empty answer not accepted)")
                continue
            valid = q["validate"](text)
            if valid is True:
                answers.append(Answer(q["id"], q["title"], text))
                break
            print(f"Validation failed: {valid}")
            print("Retry this question.")
    return answers


def render_charter(answers: list[Answer], project_name: str = "<REPLACE: project name>") -> str:
    """Render a charter.md file from collected answers."""
    parts = [
        f"# Charter — {project_name}",
        "",
        "Status: DRAFT (run `python scripts/prereg_freeze.py --type charter --path charter.md` to freeze)",
        "Hash: <fill after prereg_freeze.py runs>",
        "",
        "---",
        "",
    ]
    for a in answers:
        parts.append(f"## {a.qid}. {a.title}")
        parts.append("")
        parts.append(a.text)
        parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Approval")
    parts.append("- Drafted by: agent (charter_interview.py)")
    parts.append("- Reviewed by: <REPLACE: user>")
    parts.append("- Frozen at: <fill after prereg_freeze.py>")
    parts.append("- Frozen hash: <fill after prereg_freeze.py>")
    parts.append("")
    parts.append("After freezing, proceed to `references/rd/core_technologies.md` to define Layer 1.")
    return "\n".join(parts)


def load_yaml_answers(yaml_path: Path) -> list[Answer]:
    """Load answers from a simple YAML file. Format:
        H1: |
          ...answer text...
        H2: |
          ...
        ...
    """
    text = yaml_path.read_text(encoding="utf-8")
    # Naive parser for the H<n>: | block format
    answers_dict: dict[str, str] = {}
    current_id: str | None = None
    current_lines: list[str] = []
    for raw in text.splitlines():
        m = re.match(r"^(H[1-8])\s*:\s*\|?\s*$", raw)
        if m:
            if current_id is not None:
                answers_dict[current_id] = "\n".join(current_lines).strip()
            current_id = m.group(1)
            current_lines = []
            continue
        if current_id is not None:
            # Strip leading 2-space indent if present
            line = raw[2:] if raw.startswith("  ") else raw
            current_lines.append(line)
    if current_id is not None:
        answers_dict[current_id] = "\n".join(current_lines).strip()

    # Build Answer list in QUESTIONS order
    out: list[Answer] = []
    for q in QUESTIONS:
        if q["id"] not in answers_dict:
            raise ValueError(f"answers YAML missing {q['id']}")
        text_val = answers_dict[q["id"]]
        valid = q["validate"](text_val)
        if valid is not True:
            raise ValueError(f"{q['id']} validation failed: {valid}")
        out.append(Answer(q["id"], q["title"], text_val))
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--project-name", default="<REPLACE: project name>")
    p.add_argument("--non-interactive", action="store_true")
    p.add_argument("--answers-yaml", type=Path, default=None)
    args = p.parse_args()

    try:
        if args.non_interactive:
            if not args.answers_yaml:
                print("ERROR: --non-interactive requires --answers-yaml", file=sys.stderr)
                sys.exit(2)
            if not args.answers_yaml.exists():
                print(f"ERROR: answers YAML not found: {args.answers_yaml}", file=sys.stderr)
                sys.exit(2)
            answers = load_yaml_answers(args.answers_yaml)
        else:
            answers = interactive_collect()
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    charter = render_charter(answers, args.project_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(charter, encoding="utf-8")

    print(f"\n✅ Charter written to {args.output}")
    print(f"   ({len(answers)} questions answered, {len(charter.splitlines())} lines)")
    print()
    print("Next steps:")
    print(f"  1. Review {args.output} — fill any <REPLACE> markers")
    print(f"  2. Run: python scripts/prereg_freeze.py --type charter --path {args.output}")
    print("  3. Append a freeze entry to decisions.md")


if __name__ == "__main__":
    main()
