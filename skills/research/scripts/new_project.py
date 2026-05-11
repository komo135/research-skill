"""new_project.py - Initialize a research project folder, mode-aware.

Per CHARTER C1 / C2 / C3 / D-2 (`.rebuild/CHARTER.md`): R&D and Pure Research
are separate disciplines with different primary state objects. This script
scaffolds the correct artifacts based on --mode.

Usage:
    python new_project.py <name> --mode rd
    python new_project.py <name> --mode pure-research
    python new_project.py <name> --mode rd --root projects/

What gets created:
    Common (both modes):
        README.md                          (mode-specific from assets/<mode>/README.md.template)
        decisions.md                       (from assets/shared/decisions.md.template)
        literature/papers.md               (from assets/shared/papers.md.template)
        literature/differentiation.md      (from assets/shared/differentiation.md.template)
        purposes/INDEX.md                  (from assets/shared/INDEX.md.template)
        configs/                           (project-instance experiment configs)
        src/                               (project-instance implementation)
        tests/                             (project-instance verification)
        prereg/                            (pre-registration drafts live here)
        results/figures/                   (empty)
        results/intermediate/              (empty)
        tracking/                          (optional tracker exports / run notes)
        reproducibility/data_versions.txt  (header-only)
        reproducibility/env_lock_ref.txt   (header-only)
        reproducibility/seed.txt           (default seed 42)

    R&D mode adds:
        charter.md                         (from assets/rd/charter.md.template)
        capability_map.md                  (from assets/rd/capability_map.md.template)

    Pure Research mode adds:
        prfaq.md                           (from assets/pure_research/prfaq.md.template)
        prereg/PR_001.md                   (from assets/pure_research/preregistration.md.template)
        explanation_ledger.md              (from assets/pure_research/explanation_ledger.md.template)
        imrad_draft.md                     (from assets/pure_research/imrad_draft.md.template, started early)

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

RD_FILES = [
    ("charter.md.template", "charter.md"),
    ("capability_map.md.template", "capability_map.md"),
    ("README.md.template", "README.md"),
]

PR_FILES = [
    ("prfaq.md.template", "prfaq.md"),
    ("preregistration.md.template", "prereg/PR_001.md"),
    ("explanation_ledger.md.template", "explanation_ledger.md"),
    ("imrad_draft.md.template", "imrad_draft.md"),
    ("README.md.template", "README.md"),
]


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


def init_project(name: str, root: Path, mode: str) -> Path:
    if mode not in ("rd", "pure-research"):
        raise ValueError(f"unknown mode: {mode}")

    project_dir = root / name
    if project_dir.exists():
        raise FileExistsError(f"project already exists: {project_dir}")

    # Directory layout
    for sub in [
        "configs",
        "literature",
        "purposes",
        "prereg",
        "results/figures",
        "results/intermediate",
        "tracking",
        "reproducibility",
        "src",
        "tests",
    ]:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    # .gitkeep for empty dirs
    for keep in [
        "configs/.gitkeep",
        "prereg/.gitkeep",
        "results/.gitkeep",
        "results/figures/.gitkeep",
        "results/intermediate/.gitkeep",
        "tracking/.gitkeep",
        "src/.gitkeep",
        "tests/.gitkeep",
    ]:
        (project_dir / keep).touch()

    # Common templates (from shared/)
    for tmpl_name, dest_rel in COMMON_FILES:
        src = find_template(tmpl_name, "shared")
        dest = project_dir / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dest)

    # Mode-specific templates
    mode_subdir = "rd" if mode == "rd" else "pure_research"
    mode_files = RD_FILES if mode == "rd" else PR_FILES
    for tmpl_name, dest_rel in mode_files:
        src = find_template(tmpl_name, mode_subdir)
        dest = project_dir / dest_rel
        # Substitute project name in README
        if dest_rel == "README.md":
            content = src.read_text(encoding="utf-8").replace("<REPLACE: project name>", name)
            dest.write_text(content, encoding="utf-8")
        elif dest_rel == "prereg/PR_001.md":
            content = (
                src.read_text(encoding="utf-8")
                .replace("PR_<REPLACE: id, e.g., 001>", "PR_001")
                .replace("PR_<id>", "PR_001")
                .replace("<REPLACE: id>", "001")
            )
            dest.write_text(content, encoding="utf-8")
        else:
            shutil.copy(src, dest)

    # Reproducibility scaffolding
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

    return project_dir


def print_next_steps(project_dir: Path, mode: str) -> None:
    print(f"\n✅ Created: {project_dir} (mode: {mode})")
    print()
    print("Next steps:")
    if mode == "rd":
        print(f"  1. Edit {project_dir}/charter.md — answer Heilmeier 8 questions")
        print(f"     OR run: python scripts/charter_interview.py --output {project_dir}/charter.md")
        print(f"  2. When the charter is ready, change its status to READY")
        print(f"  3. Choose a lightweight tracking path before the first load-bearing claim")
        print(f"     Record the review path and decision note in {project_dir}/decisions.md")
        print(f"  4. Edit {project_dir}/capability_map.md — Layer 1 (Core Technologies)")
        print(f"     Apply operational filter per references/rd/core_technologies.md")
        print(f"  5. Verify Layer 1 closure in review, then add Layer 2 capabilities")
    else:
        print(f"  1. Edit {project_dir}/prfaq.md — write the press release + ≥10 FAQ entries")
        print(f"  2. When PR/FAQ is ready, change its status to READY")
        print(f"  3. Run targeted literature: python scripts/lit_fetch.py --project-dir {project_dir} --query '<your query>'")
        print(f"  4. Choose a lightweight tracking path before the first load-bearing claim")
        print(f"     Record the review path and decision note in {project_dir}/decisions.md")
        print(f"  5. Choose path: exploratory research first, or confirmatory PR_001 if a confirmation target is ready")
        print(f"  6. For confirmatory work, compare PR_001 with current state before execution")
        print(f"  7. Edit {project_dir}/explanation_ledger.md — add Q1 + ≥2 competing E + null candidates")
        print(f"  8. Optional confirmatory run: python scripts/new_trial.py --project-dir {project_dir} --slug <trial_slug> --prereg-id PR_001 --question-id Q1 --discriminating 'E1 vs E2'")
    print()
    print("Reminder: per SKILL.md § Initial-day prohibitions, no claim-bearing")
    print("confirmation trial runs before the required plan is ready. Exploratory")
    print("work must be labeled exploratory / diagnostic.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("name", help="project name (folder name)")
    p.add_argument("--mode", required=True, choices=["rd", "pure-research"])
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

    print_next_steps(project_dir, args.mode)


if __name__ == "__main__":
    main()
