#!/usr/bin/env python3
"""Create a run directory for a derived hypothesis execution.

Naming: <hypothesis_id>__<n>__seed<N>, where n is auto-incremented.

Every research run needs a manifest, captured logs, and durable artifact
locations so print-only execution does not become unreviewable evidence.

Usage:
    python new_run.py <project_root> \
        --proposition P001_slug --hypothesis H001_slug [--seed <N>]
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


PROP_DIR_RE = re.compile(r"^P\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")
HYP_DIR_RE = re.compile(r"^H\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def ensure_inside(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes expected root: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a run directory for a derived hypothesis.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory, e.g. P001_slug")
    parser.add_argument("--hypothesis", required=True, help="Hypothesis directory, e.g. H001_slug")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for this run")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not PROP_DIR_RE.fullmatch(args.proposition):
        fail("proposition must match P###_kebab-case-slug")
    if not HYP_DIR_RE.fullmatch(args.hypothesis):
        fail("hypothesis must match H###_kebab-case-slug")
    propositions_root = project / "propositions"
    hyp_root = propositions_root / args.proposition / "hypotheses"
    hyp_dir = hyp_root / args.hypothesis
    ensure_inside(hyp_dir, hyp_root, "hypothesis path")
    runs_dir = hyp_dir / "experiments" / "runs"
    if not hyp_dir.exists():
        fail(f"hypothesis directory does not exist: {hyp_dir}. Run new_hypothesis.py first.")
    if not (hyp_dir / "plan.md").exists():
        fail(f"hypothesis plan does not exist: {hyp_dir / 'plan.md'}")
    runs_dir.mkdir(parents=True, exist_ok=True)

    existing = [d for d in runs_dir.iterdir() if d.is_dir()]
    n = len(existing) + 1
    hyp_id = args.hypothesis.split("_", 1)[0]

    run_name = f"{hyp_id}__{n:03d}__seed{args.seed}"
    run_dir = runs_dir / run_name
    if run_dir.exists():
        fail(f"run directory already exists: {run_dir}")
    run_dir.mkdir()
    for directory in ["logs", "intermediate", "outputs", "tables", "figures"]:
        (run_dir / directory).mkdir()

    (run_dir / "logs" / "stdout.log").write_text("", encoding="utf-8")
    (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")

    created_at = datetime.now().isoformat(timespec="seconds")
    manifest = {
        "run_id": run_name,
        "proposition": args.proposition,
        "hypothesis": args.hypothesis,
        "plan_path": f"propositions/{args.proposition}/hypotheses/{args.hypothesis}/plan.md",
        "seed": args.seed,
        "created_at": created_at,
        "status": "initialized",
        "command": None,
        "artifacts": [],
        "notes": (
            "Fill command, status, and artifacts after executing research scripts. "
            "stdout is not evidence; every completed run needs at least one durable artifact."
        ),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    checker = Path(__file__).resolve().parent / "check_run_artifacts.py"

    (run_dir / "README.md").write_text(
        f"# Run {run_name}\n\n"
        f"Created: {created_at}\n"
        f"Proposition: {args.proposition}\n"
        f"Hypothesis: {args.hypothesis}\n"
        f"Seed: {args.seed}\n\n"
        f"Print-only execution is not a completed research run: stdout is not evidence.\n"
        f"Use stdout for progress display, then persist the values, tables, figures, diagnostics, or intermediate data that support later analysis.\n\n"
        f"Required scaffold:\n"
        f"- run_manifest.json — update command, status, and artifacts after execution\n"
        f"- logs/stdout.log and logs/stderr.log — captured console output\n"
        f"- intermediate/ — intermediate outputs needed to audit EDA or result analysis\n"
        f"- outputs/ — metrics, predictions, serialized results, diagnostics, or other durable artifact files\n"
        f"- tables/ and figures/ — paper-ready evidence snapshots when applicable\n\n"
        f"Before promoting observations, run:\n\n"
        f"```bash\n"
        f"python {checker} {run_dir}\n"
        f"```\n",
        encoding="utf-8",
    )

    print(f"Created run: {run_dir.relative_to(project)}/")


if __name__ == "__main__":
    main()
