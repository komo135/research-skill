#!/usr/bin/env python3
"""Initialize a report directory from a hypothesis plan.

Creates:
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/report.md
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/figures/
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/tables/

Usage:
    python draft_report.py <project_root> \
        --proposition P001_slug --hypothesis H001_slug \
        --id R01 --slug <report-slug> \
        --category basic_research|applied_research|experimental_development
"""
import argparse
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a report from a hypothesis plan.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory, e.g. P001_slug")
    parser.add_argument("--hypothesis", required=True, help="Hypothesis directory, e.g. H001_slug")
    parser.add_argument("--id", required=True, help="Report ID, e.g. R01")
    parser.add_argument("--slug", required=True, help="Report slug")
    parser.add_argument(
        "--category",
        required=True,
        choices=["basic_research", "applied_research", "experimental_development"],
    )
    parser.add_argument("--title", default=None, help="Report title (defaults to slug)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    hyp_dir = project / "propositions" / args.proposition / "hypotheses" / args.hypothesis
    if not hyp_dir.exists():
        print(f"Error: hypothesis directory does not exist: {hyp_dir}", file=sys.stderr)
        sys.exit(1)

    report_dir = hyp_dir / "reports" / f"{args.id}_{args.slug}"
    if report_dir.exists():
        print(f"Error: report directory already exists: {report_dir}", file=sys.stderr)
        sys.exit(1)
    report_dir.mkdir(parents=True)
    (report_dir / "figures").mkdir()
    (report_dir / "tables").mkdir()

    tpl_path = ASSETS / "report" / f"{args.category}_report.md.template"
    if not tpl_path.exists():
        print(f"Error: template not found: {tpl_path}", file=sys.stderr)
        sys.exit(1)

    title = args.title or args.slug.replace("-", " ").title()
    plan_path = f"propositions/{args.proposition}/hypotheses/{args.hypothesis}/plan.md"
    run_path = f"propositions/{args.proposition}/hypotheses/{args.hypothesis}/experiments/runs/"
    content = (
        tpl_path.read_text(encoding="utf-8")
        .replace("YYYY-MM-DD", str(date.today()))
        .replace("<report-id>", args.id)
        .replace("<plan-id>", args.hypothesis.split("_", 1)[0])
        .replace("<slug>", args.hypothesis.split("_", 1)[1] if "_" in args.hypothesis else args.hypothesis)
        .replace("<Report Title>", title)
        .replace("propositions/<Pxxx_slug>/hypotheses/<Hxxx_slug>/plan.md", plan_path)
        .replace("propositions/<Pxxx_slug>/hypotheses/<Hxxx_slug>/experiments/runs/", run_path)
    )

    (report_dir / "report.md").write_text(content, encoding="utf-8")
    (report_dir / "figures" / ".gitkeep").touch()
    (report_dir / "tables" / ".gitkeep").touch()

    print(f"Created report directory: {report_dir.relative_to(project)}/")
    print()
    print("Reminders:")
    print(f"  - Fill in {report_dir.relative_to(project)}/report.md")
    print(f"  - Generate real figures into {report_dir.relative_to(project)}/figures/")
    print("    (placeholder figure references fail the report contract)")
    print("  - Run check_claims.py against report.md before sharing")


if __name__ == "__main__":
    main()
