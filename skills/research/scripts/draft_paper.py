#!/usr/bin/env python3
"""Initialize a proposition-level research paper.

Creates:
    propositions/<P>/paper.md

Usage:
    python draft_paper.py <project_root> \
        --proposition P001_slug \
        --category basic_research|applied_research|experimental_development
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
PROP_DIR_RE = re.compile(r"^P\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def ensure_inside(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes expected root: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a proposition-level research paper.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory, e.g. P001_slug")
    parser.add_argument(
        "--category",
        required=True,
        choices=["basic_research", "applied_research", "experimental_development"],
    )
    parser.add_argument("--title", default=None, help="Paper title")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not PROP_DIR_RE.fullmatch(args.proposition):
        fail("proposition must match P###_kebab-case-slug")

    prop_root = project / "propositions"
    prop_dir = prop_root / args.proposition
    ensure_inside(prop_dir, prop_root, "proposition path")
    if not prop_dir.exists():
        fail(f"proposition directory does not exist: {prop_dir}")

    paper_path = prop_dir / "paper.md"
    if paper_path.exists():
        fail(f"paper already exists: {paper_path}")

    tpl_path = ASSETS / "paper" / f"{args.category}_paper.md.template"
    if not tpl_path.exists():
        fail(f"template not found: {tpl_path}")

    title = args.title or args.proposition.split("_", 1)[1].replace("-", " ").title()
    content = (
        tpl_path.read_text(encoding="utf-8")
        .replace("YYYY-MM-DD", str(date.today()))
        .replace("<proposition-path>", f"propositions/{args.proposition}/")
        .replace("<Paper Title>", title)
    )

    paper_path.write_text(content, encoding="utf-8")

    print(f"Created research paper: {paper_path.relative_to(project)}")
    print()
    print("Reminders:")
    print(f"  - Fill in {paper_path.relative_to(project)} after the proposition reaches supported or contradicted")
    print("  - Synthesize across hypotheses; do not recreate per-hypothesis summaries")
    print("  - Run check_paper.py before using the paper as material for the next cycle")


if __name__ == "__main__":
    main()
