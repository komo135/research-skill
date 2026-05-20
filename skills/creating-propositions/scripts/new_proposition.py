#!/usr/bin/env python3
"""Create a proposition-first research state directory.

Usage:
    python new_proposition.py <project_root> \
        --id P001 --slug <slug> --title "<title>" \
        --proposition "<proposition>" --expected "<expected consequence>"

Creates:
    propositions/P001_slug/proposition.md
    propositions/P001_slug/observations.md
    propositions/P001_slug/analyses.md
    propositions/P001_slug/decisions.md
    propositions/P001_slug/hypotheses/

Also appends an OPEN_PROPOSITION project decision to top-level decisions.md.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = SKILL_ROOT.parent
RESEARCH_SKILL_ROOT = SKILLS_ROOT / "research"
ASSETS = SKILL_ROOT / "assets"
PROP_ID_RE = re.compile(r"^P\d{3}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def validate_id_and_slug(prop_id: str, slug: str) -> None:
    if not PROP_ID_RE.fullmatch(prop_id):
        fail("proposition id must match P###, for example P001")
    if not SLUG_RE.fullmatch(slug):
        fail("slug must be kebab-case using lowercase letters, numbers, and hyphens")


def ensure_inside(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes expected root: {path}")


def render_template(path: Path, replacements: dict[str, str]) -> str:
    content = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def append_project_decision(project: Path, prop_name: str, proposition: str) -> None:
    decisions_path = project / "decisions.md"
    if not decisions_path.exists():
        return
    entry = (
        f"\n## {date.today()} - OPEN_PROPOSITION: {prop_name}\n\n"
        "- Scope: project\n"
        "- Previous status: no proposition directory\n"
        f"- New status: propositions/{prop_name}/ opened\n"
        f"- Evidence or analysis pointer: propositions/{prop_name}/proposition.md\n"
        f"- Rationale: {proposition}\n"
        "- Follow-up state change: fill observations.md and analyses.md before deriving hypotheses\n"
    )
    existing = decisions_path.read_text(encoding="utf-8")
    marker = "<!-- Entries below this line, newest first. -->"
    if marker in existing:
        existing = existing.replace(marker, marker + "\n" + entry, 1)
    else:
        existing = existing.rstrip() + "\n" + entry + "\n"
    decisions_path.write_text(existing, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a proposition state directory.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--id", required=True, help="Proposition ID, e.g. P001")
    parser.add_argument("--slug", required=True, help="Slug, kebab-case")
    parser.add_argument("--title", required=True, help="Proposition title")
    parser.add_argument("--proposition", required=True, help="Proposition statement")
    parser.add_argument("--expected", required=True, help="Current expected consequence")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not project.exists():
        fail(f"project root does not exist: {project}")
    if not (project / "decisions.md").exists() or not (project / "propositions").is_dir():
        fail("project root must be initialized by new_project.py before opening propositions")
    validate_id_and_slug(args.id, args.slug)

    prop_name = f"{args.id}_{args.slug}"
    propositions_root = project / "propositions"
    prop_dir = propositions_root / prop_name
    ensure_inside(prop_dir, propositions_root, "proposition path")
    if prop_dir.exists():
        fail(f"proposition already exists: {prop_dir}")

    prop_dir.mkdir(parents=True)
    (prop_dir / "hypotheses").mkdir()

    replacements = {
        "<proposition_id>": args.id,
        "<Proposition title>": args.title,
        "<proposition_statement>": args.proposition,
        "<expected_consequence>": args.expected,
    }

    template_dir = ASSETS / "proposition"
    for name in ["proposition.md", "observations.md", "analyses.md", "decisions.md"]:
        content = render_template(template_dir / f"{name}.template", replacements)
        (prop_dir / name).write_text(content, encoding="utf-8")

    append_project_decision(project, prop_name, args.proposition)

    print(f"Created proposition:     {prop_dir.relative_to(project)}/")
    print(f"Created state ledgers:   {prop_dir.relative_to(project)}/proposition.md, observations.md, analyses.md, decisions.md")
    print()
    print("Next steps:")
    print(f"  1. Fill observations in propositions/{prop_name}/observations.md")
    print(f"  2. Fill analyses in propositions/{prop_name}/analyses.md with generated doubt, working proposition, expected consequence, and proposition status")
    print(f"  3. Create a derived hypothesis only after proposition status warrants it:")
    print(
        f"     python \"{RESEARCH_SKILL_ROOT / 'scripts' / 'new_hypothesis.py'}\" \"{project}\" "
        f"--proposition \"{prop_name}\" --id H001 --slug slug --title \"Title\" "
        "--category applied_research --mode confirmatory --hypothesis \"Hypothesis\" "
        "--source-analysis A001 --status supported"
    )


if __name__ == "__main__":
    main()
