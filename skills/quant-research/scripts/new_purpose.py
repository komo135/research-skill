"""new_purpose.py — Create a new Purpose notebook (one parent thesis per file) with a sequential number.

A "Purpose notebook" carries the parent research thesis as a declarative
falsifiable statement; each `## H<id>` block inside it is one experiment
that tests a sub-claim of the thesis. The notebook receives a
Purpose-level verdict at closure (in addition to per-H verdicts).

Usage:
    python new_purpose.py --project <project-name> --slug <purpose> --hyp H1
    python new_purpose.py --project <project-name> --slug pca_factor_screening --hyp H1

What it does:
    1. Scans existing notebooks/<project-name>/purposes/pur_NNN_*.py for the next number.
    2. Copies assets/purpose.py.template and substitutes placeholders.
    3. Appends a row to purposes/INDEX.md.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def next_purpose_number(purposes_dir: Path) -> int:
    """Return the next sequence number based on existing pur_NNN_*.py files."""
    if not purposes_dir.exists():
        return 1
    pattern = re.compile(r"pur_(\d{3})_.*\.py")
    existing: list[int] = []
    for f in purposes_dir.glob("pur_*.py"):
        m = pattern.match(f.name)
        if m:
            existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def create_purpose(
    project: str,
    slug: str,
    hyp: str,
    title: str | None = None,
    root: Path = Path("notebooks"),
) -> Path:
    project_dir = root / project
    if not project_dir.exists():
        raise FileNotFoundError(
            f"Project not found: {project_dir}. Run new_project.py first."
        )

    purposes_dir = project_dir / "purposes"
    purposes_dir.mkdir(parents=True, exist_ok=True)

    n = next_purpose_number(purposes_dir)
    nnn = f"{n:03d}"
    out_path = purposes_dir / f"pur_{nnn}_{slug}.py"
    if out_path.exists():
        raise FileExistsError(f"Already exists: {out_path}")

    template = (ASSETS_DIR / "purpose.py.template").read_text(encoding="utf-8")
    content = (
        template
        .replace("{{PROJECT_NAME}}", project)
        .replace("{{NNN}}", nnn)
        .replace("{{SLUG}}", slug)
        .replace("{{TITLE}}", title or slug.replace("_", " "))
        .replace("{{HYP_ID}}", hyp.lstrip("H"))
        .replace("{{NEW_HYP_ID}}", "?")
    )
    out_path.write_text(content, encoding="utf-8")

    index_path = purposes_dir / "INDEX.md"
    if index_path.exists():
        index = index_path.read_text(encoding="utf-8")
        new_row = f"| pur_{nnn} | {title or slug} | {hyp} | planned | (pending) | (pending) |\n"
        index += new_row
        index_path.write_text(index, encoding="utf-8")

    return out_path


def main() -> None:
    p = argparse.ArgumentParser(
        description="Create a new Purpose notebook (one parent thesis per file) with sequential numbering.",
    )
    p.add_argument("--project", required=True, help="project name (notebooks/<name>/)")
    p.add_argument("--slug", required=True, help="Purpose slug (alphanumeric and _)")
    p.add_argument("--hyp", required=True, help="linked hypothesis ID (e.g. H3)")
    p.add_argument("--title", default=None, help="title (defaults to slug humanized)")
    p.add_argument("--root", default="notebooks")
    args = p.parse_args()

    out = create_purpose(
        args.project, args.slug, args.hyp, title=args.title, root=Path(args.root)
    )
    print(f"created: {out}")
    print("next steps:")
    print(f"  1. Edit the Markdown cells in {out} (parent thesis, hypothesis, acceptance).")
    print(f"  2. Update hypotheses.md: mark {args.hyp} as in-progress.")
    print(f"  3. Open the notebook with marimo edit {out}.")


if __name__ == "__main__":
    main()
