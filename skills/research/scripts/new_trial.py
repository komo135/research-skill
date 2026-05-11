"""new_trial.py — Create a numbered trial notebook (workstream-aware).

Replaces the older `new_purpose.py`. Chooses the correct template based on the
selected workstream state object, or on project-root compatibility state
objects.

Per CHARTER C1 and the templates:
- R&D: assets/rd/rd_trial.py.template (protocol-agnostic evidence artifact)
- Pure Research: assets/pure_research/pr_trial.py.template
  (protocol-agnostic evidence artifact)

Trial files are named `trial_NNN_<slug>.py` in `<project>/purposes/`.

Usage:
    # Mixed project workstream
    python scripts/new_trial.py --project-dir <path> --workstream WS002-capability --slug latency_benchmark

    # Project-root compatibility R&D
    python scripts/new_trial.py --project-dir <path> --slug latency_benchmark

    # Project-root compatibility Pure Research
    python scripts/new_trial.py --project-dir <path> --slug vol_carry_decay_test

Exit codes:
    0: trial notebook created
    1: project not found
    2: missing or ambiguous workstream state selection
    3: trial slug collides
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

RD_STATE_FILES = {"charter.md", "capability_map.md"}
PR_STATE_FILES = {"prfaq.md", "explanation_ledger.md", "imrad_draft.md"}


def detect_mode_from_state_dir(state_dir: Path, label: str) -> str:
    """Detect mode from a state directory's primary state object."""
    present_rd = sorted(name for name in RD_STATE_FILES if (state_dir / name).exists())
    present_pr = sorted(name for name in PR_STATE_FILES if (state_dir / name).exists())
    if present_rd and present_pr:
        raise ValueError(
            f"{label} contains mixed workstream artifacts: "
            f"{', '.join(present_rd + present_pr)}. Split them into separate "
            "workstreams or remove the unrelated state files."
        )

    has_capability_map = (state_dir / "capability_map.md").exists()
    has_explanation_ledger = (state_dir / "explanation_ledger.md").exists()
    if has_capability_map and has_explanation_ledger:
        raise ValueError(
            f"{label} contains both capability_map.md and explanation_ledger.md; "
            "select one primary state object for the trial."
        )
    if has_capability_map:
        return "rd"
    if has_explanation_ledger:
        return "pure-research"

    # Compatibility with older or hand-built projects that only have entry
    # documents available when the first trial is created.
    has_charter = (state_dir / "charter.md").exists()
    has_prfaq = (state_dir / "prfaq.md").exists()
    if has_charter and has_prfaq:
        raise ValueError(
            f"{label} contains both charter.md and prfaq.md; add the primary "
            "state object or pass a more specific --workstream."
        )
    if has_charter:
        return "rd"
    if has_prfaq:
        return "pure-research"

    raise FileNotFoundError(
        f"No state object found in {label}; expected capability_map.md or "
        "explanation_ledger.md."
    )


def resolve_workstream_dir(project_dir: Path, workstream: str) -> Path:
    """Return the selected workstream directory, rejecting path traversal."""
    if workstream in {"", ".", ".."} or "/" in workstream or "\\" in workstream:
        raise ValueError("--workstream must be a directory name under workstreams/")
    workstream_path = Path(workstream)
    if workstream_path.name != workstream or workstream_path.is_absolute():
        raise ValueError("--workstream must be a directory name under workstreams/")
    workstreams_dir = (project_dir / "workstreams").resolve()
    workstream_dir = project_dir / "workstreams" / workstream
    if not workstream_dir.exists():
        raise FileNotFoundError(f"workstream not found: {workstream_dir}")
    if not workstream_dir.is_dir():
        raise ValueError(f"workstream is not a directory: {workstream_dir}")
    resolved = workstream_dir.resolve()
    try:
        resolved.relative_to(workstreams_dir)
    except ValueError as exc:
        raise ValueError(
            f"--workstream must resolve under {workstreams_dir}: {resolved}"
        ) from exc
    return resolved


def detect_mode_and_workstream(
    project_dir: Path, workstream: str | None = None
) -> tuple[str, str | None]:
    """Detect trial mode and the selected workstream, if any."""
    if workstream:
        workstream_dir = resolve_workstream_dir(project_dir, workstream)
        return detect_mode_from_state_dir(workstream_dir, f"workstream {workstream}"), workstream

    try:
        return detect_mode_from_state_dir(project_dir, "project root"), None
    except FileNotFoundError as exc:
        workstreams_dir = project_dir / "workstreams"
        if workstreams_dir.exists():
            candidates: list[tuple[str, str]] = []
            for child in sorted(workstreams_dir.iterdir()):
                if not child.is_dir():
                    continue
                try:
                    candidates.append(
                        (child.name, detect_mode_from_state_dir(child, f"workstream {child.name}"))
                    )
                except FileNotFoundError:
                    continue
            if len(candidates) == 1:
                selected_workstream, selected_mode = candidates[0]
                return selected_mode, selected_workstream
            raise FileNotFoundError(
                "No project-root state object found. Pass --workstream <dir-name> "
                "to select the workstream state object."
            ) from exc
        raise


def detect_mode(project_dir: Path, workstream: str | None = None) -> str:
    """Detect trial mode from a workstream or project-root compatibility state object."""
    mode, _ = detect_mode_and_workstream(project_dir, workstream)
    return mode


def next_trial_number(purposes_dir: Path) -> int:
    """Return next sequence number based on trial_NNN_*.py and pur_NNN_*.py files."""
    purposes_dir.mkdir(parents=True, exist_ok=True)
    pattern_trial = re.compile(r"trial_(\d{3})_.*\.py")
    pattern_pur = re.compile(r"pur_(\d{3})_.*\.py")
    existing: list[int] = []
    for f in purposes_dir.glob("*.py"):
        for pat in (pattern_trial, pattern_pur):
            m = pat.match(f.name)
            if m:
                existing.append(int(m.group(1)))
                break
    return max(existing, default=0) + 1


def find_template(mode: str) -> Path:
    if mode == "rd":
        candidates = [
            ASSETS_DIR / "rd" / "rd_trial.py.template",
        ]
    else:
        candidates = [
            ASSETS_DIR / "pure_research" / "pr_trial.py.template",
        ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"trial template not found in any of: {candidates}")


def substitute_rd(content: str, slug: str, nnn: str, project_name: str) -> str:
    """Replace <REPLACE: ...> markers in R&D trial template that we can fill from args."""
    return (
        content
        .replace("<REPLACE: NNN>", nnn)
        .replace("<REPLACE: short title>", slug.replace("_", " "))
        .replace("<REPLACE: artifact path>", f"purposes/trial_{nnn}_{slug}.py")
        .replace("<REPLACE: project name>", project_name)
    )


def substitute_pr(content: str, prereg_id: str | None, question_id: str | None,
                  discriminating: str | None, slug: str, nnn: str, project_name: str,
                  workstream: str | None) -> str:
    """Replace <REPLACE: ...> markers in PR trial template that we can fill from args."""
    content = (
        content
        .replace("<REPLACE: NNN>", nnn)
        .replace("<REPLACE: short title>", slug.replace("_", " "))
        .replace("<REPLACE: artifact path>", f"purposes/trial_{nnn}_{slug}.py")
        .replace("<REPLACE: project name>", project_name)
    )
    if question_id:
        content = content.replace("<REPLACE: optional ledger row / claim>", question_id)
    if prereg_id:
        prereg_path = (
            f"workstreams/{workstream}/prereg/{prereg_id}.md"
            if workstream else f"prereg/{prereg_id}.md"
        )
        content = content.replace("<REPLACE: optional prereg reference>", prereg_path)
        content = content.replace("<REPLACE: optional prereg/PR_<id>.md>", prereg_path)
    if discriminating:
        content = content.replace("<REPLACE: optional discriminating contrast>", discriminating)
    return content


def create_trial(args: argparse.Namespace) -> Path:
    project_dir: Path = args.project_dir.resolve()
    if not project_dir.exists():
        raise FileNotFoundError(f"project not found: {project_dir}")

    mode, selected_workstream = detect_mode_and_workstream(project_dir, args.workstream)

    purposes_dir = project_dir / "purposes"
    n = next_trial_number(purposes_dir)
    nnn = f"{n:03d}"
    slug = args.slug
    out_path = purposes_dir / f"trial_{nnn}_{slug}.py"
    if out_path.exists():
        raise FileExistsError(f"already exists: {out_path}")

    template_path = find_template(mode)
    content = template_path.read_text(encoding="utf-8")

    if mode == "rd":
        content = substitute_rd(
            content, slug, nnn, project_dir.name,
        )
    else:
        content = substitute_pr(
            content, args.prereg_id, args.question_id, args.discriminating,
            slug, nnn, project_dir.name, selected_workstream,
        )

    out_path.write_text(content, encoding="utf-8")

    # Append to INDEX.md
    index_path = purposes_dir / "INDEX.md"
    if index_path.exists():
        index = index_path.read_text(encoding="utf-8")
        protocol_link = selected_workstream or "none"
        if mode == "rd":
            new_row = (
                f"| trial_{nnn} | rd | purposes/trial_{nnn}_{slug}.py | {protocol_link} | in-progress | pending |\n"
            )
        else:
            new_row = (
                f"| trial_{nnn} | pure-research | purposes/trial_{nnn}_{slug}.py | "
                f"{protocol_link} | in-progress | pending |\n"
            )
        marker = "\n## Artifact-status legend"
        if marker in index:
            before, after = index.split(marker, 1)
            index_path.write_text(before.rstrip() + "\n" + new_row + marker + after, encoding="utf-8")
        else:
            index_path.write_text(index.rstrip() + "\n" + new_row, encoding="utf-8")

    return out_path


def main() -> None:
    p = argparse.ArgumentParser(
        description="Create a numbered research trial evidence artifact.",
    )
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--workstream", help="workstream directory name under <project>/workstreams/")
    p.add_argument("--slug", required=True, help="trial slug (letters, numbers, and _)")
    # R&D trials are protocol-agnostic evidence artifacts; ledger files link
    # them to capability claims during assessment.
    # Optional protocol links. Evidence artifacts do not require them.
    p.add_argument("--prereg-id", help="(optional) pre-registration ID, e.g. PR_001")
    p.add_argument("--question-id", help="(optional) question ID, e.g. Q1")
    p.add_argument("--discriminating", help="(optional) E pair, e.g. 'E1 vs E2'")
    args = p.parse_args()

    try:
        out_path = create_trial(args)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"✅ Created: {out_path}")
    print()
    print("Next steps:")
    print(f"  1. Open {out_path} in marimo: marimo edit {out_path}")
    print("  2. Fill the evidence artifact header (markdown cells) per the template")
    print("  3. Run verification checks BEFORE the main test")
    print("  4. After trial, write a deviation review note or a deviation note if the run drifted")
    print("  5. If used for assessment, cite this artifact from the relevant ledger row")


if __name__ == "__main__":
    main()
