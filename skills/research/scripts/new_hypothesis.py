#!/usr/bin/env python3
"""Create a derived hypothesis directory and hypothesis plan.

Usage:
    python new_hypothesis.py <project_root> \
        --proposition P001_slug \
        --id H001 --slug <slug> --title "<title>" \
        --category basic_research|applied_research|experimental_development \
        --mode exploratory|confirmatory|milestone|theoretical \
        --hypothesis "<hypothesis>" --source-analysis A001 \
        --status supported|contradicted|unrealized-condition|under-specified|split-needed

Creates:
    propositions/P001_slug/hypotheses/H001_slug/hypothesis.md
    propositions/P001_slug/hypotheses/H001_slug/plan.md
    propositions/P001_slug/hypotheses/H001_slug/experiments/
    propositions/P001_slug/hypotheses/H001_slug/reports/
    propositions/P001_slug/hypotheses/H001_slug/decisions.md
"""
import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


def get_git_sha(project_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNCOMMITTED"


def read_title(proposition_md: Path) -> str:
    first = proposition_md.read_text(encoding="utf-8").splitlines()[0].strip()
    if ":" in first:
        return first.split(":", 1)[1].strip()
    return proposition_md.parent.name


def render_template(path: Path, replacements: dict[str, str]) -> str:
    content = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a derived hypothesis and hypothesis plan.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory name, e.g. P001_slug")
    parser.add_argument("--id", required=True, help="Hypothesis ID, e.g. H001")
    parser.add_argument("--slug", required=True, help="Hypothesis slug")
    parser.add_argument("--title", required=True, help="Hypothesis title")
    parser.add_argument(
        "--category",
        required=True,
        choices=["basic_research", "applied_research", "experimental_development"],
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["exploratory", "confirmatory", "milestone", "theoretical"],
    )
    parser.add_argument("--hypothesis", required=True, help="Hypothesis statement")
    parser.add_argument("--source-analysis", required=True, help="Source analysis ID, e.g. A001")
    parser.add_argument(
        "--status",
        required=True,
        choices=["supported", "contradicted", "unrealized-condition", "under-specified", "split-needed"],
        help="Proposition status assessment that produced this hypothesis",
    )
    parser.add_argument("--type", default="predictive / performance", help="Hypothesis type")
    parser.add_argument("--expected", default="<what should be observed if the hypothesis is useful>")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    prop_dir = project / "propositions" / args.proposition
    if not prop_dir.exists():
        print(f"Error: parent proposition does not exist: {prop_dir}", file=sys.stderr)
        sys.exit(1)
    if not (prop_dir / "proposition.md").exists():
        print(f"Error: proposition.md missing under: {prop_dir}", file=sys.stderr)
        sys.exit(1)

    prop_id = args.proposition.split("_", 1)[0]
    hyp_name = f"{args.id}_{args.slug}"
    hyp_dir = prop_dir / "hypotheses" / hyp_name
    if hyp_dir.exists():
        print(f"Error: hypothesis already exists: {hyp_dir}", file=sys.stderr)
        sys.exit(1)

    hyp_dir.mkdir(parents=True)
    (hyp_dir / "experiments").mkdir()
    (hyp_dir / "reports").mkdir()
    for sub in ["code", "configs", "runs", "notebooks"]:
        (hyp_dir / "experiments" / sub).mkdir(parents=True, exist_ok=True)
        (hyp_dir / "experiments" / sub / ".gitkeep").touch()
    (hyp_dir / "reports" / ".gitkeep").touch()

    prop_title = read_title(prop_dir / "proposition.md")
    replacements = {
        "<hypothesis_id>": args.id,
        "<Hypothesis title>": args.title,
        "<proposition_id>": prop_id,
        "<source_analysis>": args.source_analysis,
        "<hypothesis_statement>": args.hypothesis,
        "<working proposition from the source analysis>": "<copy from analyses.md>",
        "<source_status>": args.status,
        "<why this hypothesis preserves, revises, splits, rejects, or realizes a condition of the parent proposition>": "<explain from source analysis>",
        "<what should be observed if the hypothesis is useful>": args.expected,
        "<plausible alternative that could explain the same material>": "<competing hypothesis>",
        "<smallest experiment, analysis, derivation check, or observation that separates this hypothesis from the competitor>": "<minimal discriminator>",
        "<evidence needed before planning or before claiming support>": "<required evidence>",
    }

    hypothesis_md = render_template(ASSETS / "hypothesis" / "hypothesis.md.template", replacements)
    (hyp_dir / "hypothesis.md").write_text(hypothesis_md, encoding="utf-8")
    decisions_md = render_template(ASSETS / "hypothesis" / "decisions.md.template", replacements)
    (hyp_dir / "decisions.md").write_text(decisions_md, encoding="utf-8")

    tpl_path = ASSETS / "plan" / f"rd_plan_{args.mode}.md.template"
    if not tpl_path.exists():
        print(f"Error: template not found: {tpl_path}", file=sys.stderr)
        sys.exit(1)
    plan_name = f"{args.id}_{args.slug}"
    sha = get_git_sha(project)
    plan = (
        tpl_path.read_text(encoding="utf-8")
        .replace("<id>", args.id)
        .replace("<slug>", args.slug)
        .replace("<category>", args.category)
        .replace("YYYY-MM-DD", str(date.today()))
        .replace("<git sha — auto-filled by new_hypothesis.py>", sha)
        .replace("<Plan title>", args.title)
        .replace("<plan_id>_<slug>", plan_name)
        .replace("<parent_proposition_id>", prop_id)
        .replace("<parent_proposition_slug>", args.proposition)
        .replace("<parent_proposition_title>", prop_title)
        .replace("<hypothesis_id>", args.id)
        .replace("<hypothesis_slug>", args.slug)
        .replace("<source_analysis>", args.source_analysis)
        .replace("<source_status>", args.status)
        .replace("<hypothesis_statement>", args.hypothesis)
        .replace("<hypothesis_type>", args.type)
    )
    (hyp_dir / "plan.md").write_text(plan, encoding="utf-8")

    print(f"Created hypothesis:      {hyp_dir.relative_to(project)}/")
    print(f"Created plan:            {hyp_dir.relative_to(project)}/plan.md")
    print()
    print("Next steps:")
    print(f"  1. Fill propositions/{args.proposition}/hypotheses/{hyp_name}/hypothesis.md")
    print(f"  2. Fill propositions/{args.proposition}/hypotheses/{hyp_name}/plan.md from the derived hypothesis")
    print("  3. Dispatch research-plan-review with the plan path only before execution")


if __name__ == "__main__":
    main()
