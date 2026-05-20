#!/usr/bin/env python3
"""Initialize a proposition-first R&D project directory structure.

Usage:
    python new_project.py <target_dir> --name "<Project Name>"

Creates the canonical proposition-first project layout. Does NOT create env locks,
data versioning, or any computational-replicability infrastructure — those are the
agent's discretion.
"""
import argparse
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


POSITIONING_SEED = """# How the work stands on prior work

This is `literature/positioning.md`. Use it to record grounding, inheritance,
control/comparator choice when relevant, known limitations, and claim scope for each relevant prior
approach.

## <Prior approach or source — cite papers.md entry>

- What it establishes: <summary of the result, method, data, metric, or system>
- Used in plan as: <question framing / mechanism prior / baseline / comparator / metric / data / evaluation protocol / theoretical foundation / limitation / contradictory evidence / claim-scope boundary>
- Inherited assumption: <assumption this project or plan carries forward>
- Baseline / protocol use: <baseline when applicable, control, comparator, metric, split, benchmark, or evaluation setup informed by this work>
- Known limitation: <limitation relevant to current plans or claims>
- Position of this work: <replication / baseline strengthening / extension / new method / system / other>
- Claim scope: <what this grounding supports, narrows, or blocks>
"""


DIRECTORIES = [
    "propositions",
    "literature",
    "lib/data",
    "lib/eval",
    "lib/viz",
    "lib/utils",
    "lib/tests",
    "data/raw",
    "data/processed",
    "data/eda",
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
    (target / "intake.md").write_text(
        (
            "# Intake\n\n"
            "## Intent\n\n"
            "<What the user wants to understand, decide, or build.>\n\n"
            "## Uncertain in outcome gate\n\n"
            "- Is the outcome uncertain? <yes/no>\n"
            "- If no, route as implementation rather than R&D.\n"
            "- If yes, name the uncertainty that makes this R&D.\n\n"
            "## Initial material needs\n\n"
            "- Observations needed:\n"
            "- Comparators or expected references:\n"
            "- Data, traces, or prior-work facts to acquire:\n"
        ),
        encoding="utf-8",
    )
    (target / "observations.md").write_text(
        (
            "# Project Observations\n\n"
            "Project-level observation backlog from scoping, literature, EDA, and prior proposition papers.\n"
            "Move proposition-specific observations into `propositions/Pxxx_slug/observations.md` when opening a proposition.\n"
        ),
        encoding="utf-8",
    )
    (target / "status_brief.md").write_text(
        (
            "# Status Brief\n\n"
            "Project-level dated stakeholder brief for interim status before proposition resolution.\n"
            "This is not `paper.md`, does not mark a proposition supported or contradicted, and does not trigger the next proposition cycle.\n\n"
            "## Entries\n\n"
            "<YYYY-MM-DD>: <route, current artifact, unresolved material, next action>\n"
        ),
        encoding="utf-8",
    )
    (target / "literature" / "papers.md").write_text(
        "# Prior work\n\nUse the format from `references/literature_review.md`.\n",
        encoding="utf-8",
    )
    (target / "literature" / "scoping.md").write_text(
        (
            "# Scoping Literature Scan\n\n"
            "Use this before proposition creation to locate existing work, comparators, known failures, datasets, and gaps.\n"
            "This does not replace hypothesis-specific prior-work grounding in a plan.\n"
        ),
        encoding="utf-8",
    )
    (target / "literature" / "positioning.md").write_text(
        POSITIONING_SEED,
        encoding="utf-8",
    )

    # .gitkeep markers for empty directories.
    for d in ["propositions", "data/raw", "data/processed", "data/eda"]:
        keep = target / d / ".gitkeep"
        if not any((target / d).iterdir()):
            keep.touch()

    print(f"Initialized proposition-first R&D project at {target}")
    print()
    print("Next steps:")
    print(f"  cd {target}")
    print("  git init && git add -A && git commit -m 'Initial project structure'")
    print(
        f"  python \"{SKILL_ROOT.parent / 'creating-propositions' / 'scripts' / 'new_proposition.py'}\" \"{target}\" "
        "--id P001 --slug slug --title \"Title\" --proposition \"Proposition\" --expected \"Expected consequence\""
    )


if __name__ == "__main__":
    main()
