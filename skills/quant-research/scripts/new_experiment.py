"""new_experiment.py — Create a new experiment notebook with a sequential number.

Usage:
    python new_experiment.py --project <project-name> --slug <purpose> --hyp H1
    python new_experiment.py --project <project-name> --slug pca_factor_screening --hyp H1

What it does:
    1. Scans existing notebooks/<project-name>/experiments/exp_NNN_*.py for the next number.
    2. Copies assets/experiment.py.template and substitutes placeholders.
    3. Appends a row to experiments/INDEX.md.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def next_exp_number(experiments_dir: Path) -> int:
    """Return the next sequence number based on existing exp_NNN_*.py files."""
    if not experiments_dir.exists():
        return 1
    pattern = re.compile(r"exp_(\d{3})_.*\.py")
    existing: list[int] = []
    for f in experiments_dir.glob("exp_*.py"):
        m = pattern.match(f.name)
        if m:
            existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def create_experiment(
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

    experiments_dir = project_dir / "experiments"
    experiments_dir.mkdir(parents=True, exist_ok=True)

    n = next_exp_number(experiments_dir)
    nnn = f"{n:03d}"
    out_path = experiments_dir / f"exp_{nnn}_{slug}.py"
    if out_path.exists():
        raise FileExistsError(f"Already exists: {out_path}")

    template = (ASSETS_DIR / "experiment.py.template").read_text(encoding="utf-8")
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

    index_path = experiments_dir / "INDEX.md"
    if index_path.exists():
        index = index_path.read_text(encoding="utf-8")
        new_row = f"| exp_{nnn} | {title or slug} | {hyp} | planned | (pending) |\n"
        index += new_row
        index_path.write_text(index, encoding="utf-8")

    return out_path


def main() -> None:
    p = argparse.ArgumentParser(
        description="Create a new experiment notebook with sequential numbering.",
    )
    p.add_argument("--project", required=True, help="project name (notebooks/<name>/)")
    p.add_argument("--slug", required=True, help="experiment slug (alphanumeric and _)")
    p.add_argument("--hyp", required=True, help="linked hypothesis ID (e.g. H3)")
    p.add_argument("--title", default=None, help="title (defaults to slug humanized)")
    p.add_argument("--root", default="notebooks")
    args = p.parse_args()

    out = create_experiment(
        args.project, args.slug, args.hyp, title=args.title, root=Path(args.root)
    )
    print(f"created: {out}")
    print("next steps:")
    print(f"  1. Edit the Markdown cells in {out} (question, hypothesis, acceptance).")
    print(f"  2. Update hypotheses.md: mark {args.hyp} as in-progress.")
    print(f"  3. Open the notebook with marimo edit {out}.")


if __name__ == "__main__":
    main()
