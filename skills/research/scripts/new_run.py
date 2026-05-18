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
import sys
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a run directory for a derived hypothesis.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory, e.g. P001_slug")
    parser.add_argument("--hypothesis", required=True, help="Hypothesis directory, e.g. H001_slug")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for this run")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    hyp_dir = project / "propositions" / args.proposition / "hypotheses" / args.hypothesis
    runs_dir = hyp_dir / "experiments" / "runs"
    if not hyp_dir.exists():
        print(f"Error: hypothesis directory does not exist: {hyp_dir}", file=sys.stderr)
        print("Run new_hypothesis.py first to create the derived hypothesis.", file=sys.stderr)
        sys.exit(1)
    runs_dir.mkdir(parents=True, exist_ok=True)

    existing = [d for d in runs_dir.iterdir() if d.is_dir()]
    n = len(existing) + 1
    hyp_id = args.hypothesis.split("_", 1)[0]

    run_name = f"{hyp_id}__{n:03d}__seed{args.seed}"
    run_dir = runs_dir / run_name
    if run_dir.exists():
        print(f"Error: run directory already exists: {run_dir}", file=sys.stderr)
        sys.exit(1)
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
        f"- tables/ and figures/ — report-ready evidence snapshots when applicable\n\n"
        f"Before promoting observations, run:\n\n"
        f"```bash\n"
        f"python {checker} {run_dir}\n"
        f"```\n",
        encoding="utf-8",
    )

    print(f"Created run: {run_dir.relative_to(project)}/")


if __name__ == "__main__":
    main()
