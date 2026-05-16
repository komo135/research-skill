#!/usr/bin/env python3
"""Create a new R&D plan from a mode-specific template.

Usage:
    python new_plan.py <project_root> \
        --id <id> --slug <slug> \
        --category basic_research|applied_research|experimental_development \
        --mode exploratory|confirmatory|milestone|theoretical

Creates:
    plans/<id>_<slug>.md           (from template, with metadata filled in)
    experiments/<id>_<slug>/{code,configs,runs,notebooks}/

The plan is NOT auto-committed. Commit it yourself once the Question / Objective,
Idea portfolio when ideating, Prior-work grounding, Divergence checkpoint, and
Plan sections are filled in. For ideation plans, run check_idea_portfolio.py
before promotion. That commit is the time-anchor for the plan. After execution,
fill the Research review section before writing Claims, a state-changing
Decision, or a report.
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


def main():
    parser = argparse.ArgumentParser(description="Create an R&D plan.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--id", required=True, help="Plan ID, e.g., 01")
    parser.add_argument("--slug", required=True, help="Slug, kebab-case (e.g., phase-transition)")
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
    parser.add_argument("--title", default=None, help="Plan title (defaults to slug)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not project.exists():
        print(f"Error: project root does not exist: {project}", file=sys.stderr)
        sys.exit(1)

    plan_id = args.id
    slug = args.slug
    plan_name = f"{plan_id}_{slug}"
    title = args.title or slug.replace("-", " ").title()

    tpl_path = ASSETS / "plan" / f"rd_plan_{args.mode}.md.template"
    if not tpl_path.exists():
        print(f"Error: template not found: {tpl_path}", file=sys.stderr)
        sys.exit(1)

    tpl = tpl_path.read_text(encoding="utf-8")
    sha = get_git_sha(project)

    content = (
        tpl.replace("<id>", plan_id)
        .replace("<slug>", slug)
        .replace("<category>", args.category)
        .replace("YYYY-MM-DD", str(date.today()))
        .replace("<git sha — auto-filled by new_plan.py>", sha)
        .replace("<Plan title>", title)
        .replace("<plan_id>_<slug>", plan_name)
    )

    plan_path = project / "plans" / f"{plan_name}.md"
    if plan_path.exists():
        print(f"Error: plan already exists: {plan_path}", file=sys.stderr)
        sys.exit(1)
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(content, encoding="utf-8")

    # experiments/<plan_name>/ skeleton.
    exp_dir = project / "experiments" / plan_name
    for sub in ["code", "configs", "runs", "notebooks"]:
        (exp_dir / sub).mkdir(parents=True, exist_ok=True)
    (exp_dir / "code" / ".gitkeep").touch()
    (exp_dir / "configs" / ".gitkeep").touch()
    (exp_dir / "runs" / ".gitkeep").touch()
    (exp_dir / "notebooks" / ".gitkeep").touch()
    (exp_dir / "README.md").write_text(
        f"# Experiments for plan {plan_name}\n\n"
        f"This directory is owned by one plan. Other plans must not import from `code/`.\n"
        f"Promote shared code to project-level `lib/` (record promotion in `decisions.md`).\n",
        encoding="utf-8",
    )

    print(f"Created plan:           {plan_path.relative_to(project)}")
    print(f"Created experiments:    {exp_dir.relative_to(project)}/")
    print()
    print("Next steps:")
    print(
        f"  1. Fill in the Question / Objective, Idea portfolio when ideating, Prior-work grounding, Divergence checkpoint, and Plan sections of "
        f"{plan_path.relative_to(project)}"
    )
    print("  2. If ideating, run scripts/check_idea_portfolio.py before promoting a candidate")
    print(f"  3. git add plans/{plan_name}.md experiments/{plan_name}/")
    print(f"  4. git commit -m 'Plan {plan_id}: {slug}'")
    print("  5. After execution, fill Research review before Claims, state-changing Decision, or report")
    print()
    print("The commit time-anchors the plan. Execution comes after.")


if __name__ == "__main__":
    main()
