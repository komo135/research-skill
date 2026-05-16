#!/usr/bin/env python3
"""Initialize a new R&D project directory structure.

Usage:
    python new_project.py <target_dir> --name "<Project Name>"

Creates the canonical project layout. Does NOT create env locks, data versioning,
or any computational-replicability infrastructure — those are the agent's discretion.
"""
import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


POSITIONING_SEED = """# How the work stands on prior work

This is `literature/positioning.md`. Use it to record grounding, inheritance,
control/comparator choice when relevant, known limitations, and claim scope for each relevant prior
approach.

## <Prior approach or source — cite papers.md entry>

- What it establishes: <summary of the result, method, data, metric, or system>
- Inherited assumption: <assumption this project or plan carries forward>
- Baseline / protocol use: <baseline when applicable, control, comparator, metric, split, benchmark, or evaluation setup informed by this work>
- Known limitation: <limitation relevant to current plans or claims>
- Position of this work: <replication / baseline strengthening / extension / new method / system / other>
- Claim scope: <what this grounding supports, narrows, or blocks>
"""


DIRECTORIES = [
    "plans",
    "literature",
    "lib/data",
    "lib/eval",
    "lib/viz",
    "lib/utils",
    "lib/tests",
    "experiments",
    "data/raw",
    "data/processed",
    "reports",
]


def main():
    parser = argparse.ArgumentParser(description="Initialize an R&D project.")
    parser.add_argument("path", help="Target project path")
    parser.add_argument("--name", required=True, help="Project name (free text)")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    # Create directory structure.
    for d in DIRECTORIES:
        (target / d).mkdir(parents=True, exist_ok=True)

    # Copy project templates with name substitution.
    for stem in ["README.md", "project_state.md", "decisions.md"]:
        src = ASSETS / "project" / f"{stem}.template"
        dst = target / stem
        content = src.read_text(encoding="utf-8").replace("<Project Name>", args.name)
        dst.write_text(content, encoding="utf-8")

    # Seed literature/.
    (target / "literature" / "papers.md").write_text(
        "# Prior work\n\nUse the format from `references/literature_review.md`.\n",
        encoding="utf-8",
    )
    (target / "literature" / "positioning.md").write_text(
        POSITIONING_SEED,
        encoding="utf-8",
    )

    # .gitkeep markers for empty directories.
    for d in ["plans", "experiments", "reports", "data/raw", "data/processed"]:
        keep = target / d / ".gitkeep"
        if not any((target / d).iterdir()):
            keep.touch()

    print(f"Initialized R&D project at {target}")
    print()
    print("Next steps:")
    print(f"  cd {target}")
    print("  git init && git add -A && git commit -m 'Initial project structure'")
    print(f"  python {SKILL_ROOT}/scripts/new_plan.py {target} \\")
    print("    --id 01 --slug <slug> --category <basic_research|applied_research|experimental_development> --mode <exploratory|confirmatory|milestone|theoretical>")


if __name__ == "__main__":
    main()
