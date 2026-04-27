"""new_project.py — Initialize a new research project folder.

Usage:
    python new_project.py <project-name> [--root notebooks/] [--start YYYY-MM-DD] [--end YYYY-MM-DD]

Creates the standard project layout under notebooks/<project-name>/:

    README.md
    hypotheses.md
    decisions.md
    literature/
        papers.md
        differentiation.md
    experiments/
        INDEX.md
    results/
        figures/
        intermediate/
    reproducibility/
        env.lock
        data_hashes.txt
        seed.txt

Templates are copied from the plugin's assets/ directory.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def init_project(
    name: str,
    root: Path = Path("notebooks"),
    start: str | None = None,
    end: str | None = None,
) -> Path:
    """Create a new research project folder with the standard layout."""
    project_dir = root / name
    if project_dir.exists():
        raise FileExistsError(f"Project already exists: {project_dir}")

    for sub in [
        "literature",
        "experiments",
        "results/figures",
        "results/intermediate",
        "reproducibility",
    ]:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    # Render README from template
    readme_template = (ASSETS_DIR / "README.md.template").read_text(encoding="utf-8")
    readme = (
        readme_template
        .replace("{{PROJECT_NAME}}", name)
        .replace("{{START}}", start or "TBD")
        .replace("{{END}}", end or "TBD")
    )
    (project_dir / "README.md").write_text(readme, encoding="utf-8")

    shutil.copy(ASSETS_DIR / "hypotheses.md.template", project_dir / "hypotheses.md")
    shutil.copy(ASSETS_DIR / "decisions.md.template", project_dir / "decisions.md")
    shutil.copy(ASSETS_DIR / "papers.md.template", project_dir / "literature" / "papers.md")
    shutil.copy(
        ASSETS_DIR / "differentiation.md.template",
        project_dir / "literature" / "differentiation.md",
    )
    shutil.copy(ASSETS_DIR / "INDEX.md.template", project_dir / "experiments" / "INDEX.md")

    # Reproducibility files
    (project_dir / "reproducibility" / "env.lock").write_text(
        "# dependency lock content here\n", encoding="utf-8"
    )
    (project_dir / "reproducibility" / "data_hashes.txt").write_text(
        "# format: <relative path>  <sha256>\n", encoding="utf-8"
    )
    (project_dir / "reproducibility" / "seed.txt").write_text("42\n", encoding="utf-8")

    for keep in [
        "results/.gitkeep",
        "results/figures/.gitkeep",
        "results/intermediate/.gitkeep",
    ]:
        (project_dir / keep).touch()

    return project_dir


def main() -> None:
    p = argparse.ArgumentParser(
        description="Initialize a new quant-research project folder.",
    )
    p.add_argument("name", help="project name (used directly as the folder name)")
    p.add_argument("--root", default="notebooks", help="root directory (default: notebooks/)")
    p.add_argument("--start", default=None, help="data range start (YYYY-MM-DD)")
    p.add_argument("--end", default=str(date.today()), help="data range end (default: today)")
    args = p.parse_args()

    project_dir = init_project(args.name, root=Path(args.root), start=args.start, end=args.end)
    print(f"created: {project_dir}")
    print("next steps:")
    print(f"  1. Edit {project_dir}/README.md and fill in question, hypotheses, acceptance.")
    print(f"  2. Add 5-10 prior papers to {project_dir}/literature/papers.md.")
    print(
        f"  3. State differentiation against prior work in "
        f"{project_dir}/literature/differentiation.md."
    )
    print(f"  4. List H1, H2, ... in {project_dir}/hypotheses.md.")
    print(
        f"  5. python new_experiment.py --project {args.name} --slug <purpose> --hyp H1"
    )


if __name__ == "__main__":
    main()
