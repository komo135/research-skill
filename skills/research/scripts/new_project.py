"""new_project.py - Initialize a research project folder, workstream-aware.

Projects start as mixed containers. Workstreams select one implemented state
object and review path. Passing --mode creates the mixed container plus a first
compatible workstream.

Usage:
    python new_project.py <name>
    python new_project.py <name> --mode rd
    python new_project.py <name> --mode pure-research
    python new_project.py <name> --mode rd --root projects/

What gets created:
    Mixed container (default):
        README.md                          (from assets/shared/README.md.template)
        project_state.md                   (from assets/shared/project_state.md.template)
        decisions.md                       (from assets/shared/decisions.md.template)
        literature/papers.md               (from assets/shared/papers.md.template)
        literature/differentiation.md      (from assets/shared/differentiation.md.template)
        purposes/INDEX.md                  (from assets/shared/INDEX.md.template)
        workstreams/                       (discipline-specific state lives under here)
        configs/                           (project-instance experiment configs)
        src/                               (project-instance implementation)
        tests/                             (project-instance verification)
        results/figures/                   (empty)
        results/reports/                   (empty report package root)
        results/intermediate/              (empty)
        tracking/                          (optional tracker exports / run notes)
        reproducibility/data_versions.txt  (header-only)
        reproducibility/env_lock_ref.txt   (header-only)
        reproducibility/seed.txt           (default seed 42)

    Workstream shortcut (--mode) also creates the first workstream under
    workstreams/ and:

    R&D shortcut adds:
        workstreams/WS001-rd/rd_plan.md
        workstreams/WS001-rd/prereg/PR_001_initial.md

    Phenomenon / Mechanism Research shortcut adds:
        workstreams/WS001-phenomenon/prfaq.md
        workstreams/WS001-phenomenon/prereg/PR_001_initial.md
        workstreams/WS001-phenomenon/explanation_ledger.md
        workstreams/WS001-phenomenon/imrad_draft.md

Exit codes:
    0: project created
    1: project already exists at target path
    2: missing template asset
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


COMMON_FILES = [
    # (source_template_name, dest_relative_path)
    ("decisions.md.template", "decisions.md"),
    ("papers.md.template", "literature/papers.md"),
    ("differentiation.md.template", "literature/differentiation.md"),
    ("INDEX.md.template", "purposes/INDEX.md"),
]

MIXED_FILES = [
    ("README.md.template", "README.md"),
    ("project_state.md.template", "project_state.md"),
]

RD_FILES = [
    ("rd_plan.md.template", "rd_plan.md"),
    ("preregistration.md.template", "prereg/PR_001_initial.md"),
    ("README.md.template", "README.md"),
]

PR_FILES = [
    ("prfaq.md.template", "prfaq.md"),
    ("preregistration.md.template", "prereg/PR_001_initial.md"),
    ("explanation_ledger.md.template", "explanation_ledger.md"),
    ("imrad_draft.md.template", "imrad_draft.md"),
    ("README.md.template", "README.md"),
]

MODE_WORKSTREAMS = {
    "rd": {
        "directory": "WS001-rd",
        "label": "R&D Workstream",
        "state_object": "rd_plan.md",
        "next_decision": "review R&D plan and pre-registration",
    },
    "pure-research": {
        "directory": "WS001-phenomenon",
        "label": "Phenomenon / Mechanism Research",
        "state_object": "explanation_ledger.md",
        "next_decision": "review PR/FAQ and explanation candidates",
    },
}


def find_template(name: str, mode_subdir: str | None) -> Path:
    """Find a template under assets/<mode_subdir>/ or assets/shared/."""
    candidates = []
    if mode_subdir:
        candidates.append(ASSETS_DIR / mode_subdir / name)
    candidates.append(ASSETS_DIR / "shared" / name)
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"template not found in any of: {candidates}")


def keep_only_exploratory_body(content: str) -> str:
    """Render the shortcut preregistration as an exploratory starter file."""
    confirmatory_marker = "## Confirmatory body"
    exploratory_marker = "## Exploratory body"
    if confirmatory_marker not in content or exploratory_marker not in content:
        raise ValueError(
            "pre-registration template is missing required body markers: "
            f"{confirmatory_marker!r} and {exploratory_marker!r}"
        )

    prefix, after_confirmatory = content.split(confirmatory_marker, 1)
    _, exploratory = after_confirmatory.split(exploratory_marker, 1)
    prefix = prefix.replace(
        "Complete these fields for both confirmatory and exploratory preregistrations.\n"
        "Delete the body section that does not match `preregistration_type`.",
        "Complete these fields for this exploratory preregistration. Create a "
        "separate confirmatory pre-registration when a confirmation target is ready.",
    )
    return prefix + exploratory_marker + exploratory


def init_project(name: str, root: Path, mode: str | None = None) -> Path:
    if mode is not None and mode not in ("rd", "pure-research"):
        raise ValueError(f"unknown mode: {mode}")

    project_dir = root / name
    if project_dir.exists():
        raise FileExistsError(f"project already exists: {project_dir}")

    # Directory layout
    common_dirs = [
        "configs",
        "literature",
        "purposes",
        "results/figures",
        "results/intermediate",
        "results/reports",
        "tracking",
        "reproducibility",
        "src",
        "tests",
        "workstreams",
    ]
    for sub in common_dirs:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    # .gitkeep for empty dirs
    common_keeps = [
        "configs/.gitkeep",
        "results/.gitkeep",
        "results/figures/.gitkeep",
        "results/intermediate/.gitkeep",
        "results/reports/.gitkeep",
        "tracking/.gitkeep",
        "src/.gitkeep",
        "tests/.gitkeep",
        "workstreams/.gitkeep",
    ]
    for keep in common_keeps:
        (project_dir / keep).touch()

    # Common templates (from shared/)
    for tmpl_name, dest_rel in COMMON_FILES:
        src = find_template(tmpl_name, "shared")
        dest = project_dir / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dest)

    for tmpl_name, dest_rel in MIXED_FILES:
        src = find_template(tmpl_name, "shared")
        dest = project_dir / dest_rel
        content = src.read_text(encoding="utf-8").replace("<REPLACE: project name>", name)
        dest.write_text(content, encoding="utf-8")

    if mode is None:
        write_reproducibility_scaffold(project_dir)
        return project_dir

    # Shortcut-selected templates go inside the first workstream.
    mode_subdir = "rd" if mode == "rd" else "pure_research"
    mode_files = RD_FILES if mode == "rd" else PR_FILES
    workstream = MODE_WORKSTREAMS[mode]
    workstream_dir = project_dir / "workstreams" / workstream["directory"]
    for tmpl_name, dest_rel in mode_files:
        src = find_template(tmpl_name, mode_subdir)
        dest = workstream_dir / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Substitute project name in README
        if dest_rel == "README.md":
            content = src.read_text(encoding="utf-8").replace("<REPLACE: project name>", name)
            dest.write_text(content, encoding="utf-8")
        elif dest_rel == "prereg/PR_001_initial.md":
            content = (
                src.read_text(encoding="utf-8")
                .replace("PR_<REPLACE: id, e.g., 001>_<REPLACE: slug, e.g., initial>", "PR_001_initial")
                .replace("RPT_<REPLACE: id, e.g., 001>_<REPLACE: slug>", "RPT_001_initial")
                .replace("PR_<REPLACE: id, e.g., 001>", "PR_001")
                .replace("PR_<id>_<slug>", "PR_001_initial")
                .replace("RPT_<id>_<slug>", "RPT_001_initial")
                .replace("preregistration_type: confirmatory | exploratory", "preregistration_type: exploratory")
                .replace("PR_<id>", "PR_001")
                .replace("<REPLACE: id>", "001")
                .replace("<REPLACE: slug>", "initial")
            )
            content = keep_only_exploratory_body(content)
            dest.write_text(content, encoding="utf-8")
        else:
            shutil.copy(src, dest)

    write_initial_workstream_state(project_dir, workstream)
    write_reproducibility_scaffold(project_dir)

    return project_dir


def write_initial_workstream_state(project_dir: Path, workstream: dict[str, str]) -> None:
    """Replace the project-state placeholder row for mode shortcut scaffolds."""
    project_state = project_dir / "project_state.md"
    content = project_state.read_text(encoding="utf-8")
    placeholder = (
        "| <REPLACE: workstream name> | <REPLACE: R&D Workstream; "
        "Phenomenon / Mechanism Research> | <REPLACE: workstreams/<name>/rd_plan.md "
        "or workstreams/<name>/explanation_ledger.md> | <REPLACE> | <REPLACE> |"
    )
    state_path = f"workstreams/{workstream['directory']}/{workstream['state_object']}"
    row = (
        f"| {workstream['directory']} | {workstream['label']} | {state_path} | draft | "
        f"{workstream['next_decision']} |"
    )
    project_state.write_text(content.replace(placeholder, row), encoding="utf-8")


def write_reproducibility_scaffold(project_dir: Path) -> None:
    """Create shared reproducibility marker files."""
    (project_dir / "reproducibility" / "data_versions.txt").write_text(
        "# format: <data source or table> | <version/date/path used>\n",
        encoding="utf-8",
    )
    (project_dir / "reproducibility" / "shared_pins.txt").write_text(
        "# format: <shared module path> | <commit note or revision reference>\n",
        encoding="utf-8",
    )
    (project_dir / "reproducibility" / "env_lock_ref.txt").write_text(
        "# format: <environment pin source> | <version/path used>\n",
        encoding="utf-8",
    )
    (project_dir / "reproducibility" / "seed.txt").write_text(
        f"# format: <component>  <seed>\nproject_default_seed  42\n", encoding="utf-8"
    )


def print_next_steps(project_dir: Path, mode: str | None) -> None:
    if mode is None:
        print(f"\n✅ Created: {project_dir} (mixed project)")
        print()
        print("Next steps:")
        print(f"  1. Map the current research state in {project_dir}/project_state.md")
        print(f"  2. Create the first workstream under {project_dir}/workstreams/<name>/")
        print("  3. Put the workstream state object in that folder:")
        print("     - R&D Workstream: rd_plan.md and optional prereg/PR_<id>_<slug>.md")
        print("     - Phenomenon / Mechanism Research: prfaq.md and explanation_ledger.md")
        print("  4. For report packages, note how presented evidence will be resolved")
        print(f"     Record durable state decisions in {project_dir}/decisions.md")
        print("  5. Create trial evidence with:")
        print(f"     python scripts/new_trial.py --project-dir {project_dir} --workstream <name> --slug <trial_slug>")
        print()
        print("Reminder: the project container can hold multiple workstreams, but each")
        print("workstream must select one state object and gate before claim-bearing work.")
        return

    workstream = MODE_WORKSTREAMS[mode]
    workstream_dir = project_dir / "workstreams" / workstream["directory"]
    print(f"\n✅ Created: {project_dir} (mixed project with {workstream['directory']})")
    print()
    print("Next steps:")
    if mode == "rd":
        print(f"  1. Review the R&D plan in {workstream_dir}/rd_plan.md")
        print(f"  2. Edit {workstream_dir}/prereg/PR_001_initial.md before claim-bearing work")
        print("  3. For report packages, note how presented evidence will be resolved")
        print(f"     Record durable state decisions in {project_dir}/decisions.md")
        print("  4. Execute the planned work and update rd_plan.md with evidence links")
        print("  5. Compare execution and results against the pre-registration")
    else:
        print(f"  1. Edit {workstream_dir}/prfaq.md — write the press release + ≥10 FAQ entries")
        print(f"  2. When PR/FAQ is ready, change its status to READY")
        print(f"  3. Run targeted literature: python scripts/lit_fetch.py --project-dir {project_dir} --query '<your query>'")
        print("  4. For report packages, note how presented evidence will be resolved")
        print(f"     Record durable state decisions in {project_dir}/decisions.md")
        print(f"  5. Choose path: exploratory research first, use PR_001_initial for a scoped exploratory pass. Create a separate confirmatory pre-registration if a confirmation target is ready")
        print(f"  6. Before any run, compare its matching pre-registration with current state before execution")
        print(f"  7. Edit {workstream_dir}/explanation_ledger.md — add Q1 + ≥2 competing E + null candidates")
        print(f"  8. Optional confirmatory run: create a confirmatory PR, then run python scripts/new_trial.py --project-dir {project_dir} --workstream {workstream['directory']} --slug <trial_slug> --prereg-id <confirmatory_pr_id> --question-id Q1 --discriminating 'E1 vs E2'")
    print()
    print("Reminder: no claim-bearing confirmation run should be reported before")
    print("the relevant plan is ready. Exploratory work must be labeled")
    print("exploratory / diagnostic.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("name", help="project name (folder name)")
    p.add_argument("--mode", choices=["rd", "pure-research"])
    p.add_argument("--root", default="projects", type=Path,
                   help="root directory (default: projects/)")
    args = p.parse_args()

    try:
        project_dir = init_project(args.name, args.root, args.mode)
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    print_next_steps(project_dir, args.mode)


if __name__ == "__main__":
    main()
