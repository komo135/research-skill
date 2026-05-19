#!/usr/bin/env python3
"""Create a derived hypothesis directory and hypothesis plan.

Usage:
    python new_hypothesis.py <project_root> \
        --proposition P001_slug \
        --id H001 --slug <slug> --title "<title>" \
        --category basic_research|applied_research|experimental_development \
        --mode exploratory|confirmatory|milestone|theoretical \
        --hypothesis "<hypothesis>" --source-analysis A001 \
        --status supported|unrealized-condition

Creates:
    propositions/P001_slug/hypotheses/H001_slug/hypothesis.md
    propositions/P001_slug/hypotheses/H001_slug/plan.md
    propositions/P001_slug/hypotheses/H001_slug/experiments/
    propositions/P001_slug/hypotheses/H001_slug/reports/
    propositions/P001_slug/hypotheses/H001_slug/decisions.md
"""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
PROP_DIR_RE = re.compile(r"^P\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")
HYP_ID_RE = re.compile(r"^H\d{3}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ANALYSIS_ID_RE = re.compile(r"^A\d{3}$")
PLANNABLE_STATUSES = {"supported", "unrealized-condition"}
PARENT_PLANNABLE_STATUSES = {"open", "supported", "unrealized-condition"}


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def ensure_inside(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes expected root: {path}")


def validate_components(proposition: str, hyp_id: str, slug: str, source_analysis: str) -> None:
    if not PROP_DIR_RE.fullmatch(proposition):
        fail("proposition must match P###_kebab-case-slug")
    if not HYP_ID_RE.fullmatch(hyp_id):
        fail("hypothesis id must match H###, for example H001")
    if not SLUG_RE.fullmatch(slug):
        fail("slug must be kebab-case using lowercase letters, numbers, and hyphens")
    if not ANALYSIS_ID_RE.fullmatch(source_analysis):
        fail("source-analysis must match A###, for example A001")


def parse_analysis_entry(analyses_md: Path, analysis_id: str) -> dict[str, str]:
    lines = analyses_md.read_text(encoding="utf-8").splitlines()
    heading_re = re.compile(rf"^##\s+{re.escape(analysis_id)}\b.*$")
    start = None
    for index, line in enumerate(lines):
        if heading_re.match(line.strip()):
            start = index + 1
            break
    if start is None:
        fail(f"source analysis not found in analyses.md: {analysis_id}")

    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^##\s+\S", lines[index]):
            end = index
            break
    block = lines[start:end]

    fields: dict[str, str] = {}
    for line in block:
        match = re.match(r"^-\s+([^:]+):\s*(.*)$", line.strip())
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def is_placeholder(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    lowered = stripped.lower()
    none_like = {
        "none",
        "none.",
        "n/a",
        "na",
        "not applicable",
        "no material",
        "no material yet",
        "no hypothesis",
        "no hypothesis yet",
    }
    return (
        "<" in stripped
        or ">" in stripped
        or lowered in none_like
        or lowered.startswith("none:")
        or lowered.startswith("n/a:")
        or lowered.startswith("not applicable:")
        or lowered.startswith("no material")
        or lowered.startswith("no hypothesis")
        or lowered.startswith("todo")
        or lowered.startswith("tbd")
        or lowered.startswith("none yet")
    )


def require_analysis_field(fields: dict[str, str], name: str) -> str:
    value = fields.get(name, "")
    if is_placeholder(value):
        fail(f"source analysis is still placeholder-only: {name}")
    return value


def load_source_analysis(prop_dir: Path, analysis_id: str, requested_status: str) -> dict[str, str]:
    analyses_md = prop_dir / "analyses.md"
    if not analyses_md.exists():
        fail(f"analyses.md missing under: {prop_dir}")
    fields = parse_analysis_entry(analyses_md, analysis_id)
    required_names = [
        "Analysis question",
        "Material used",
        "Contrast type",
        "Contrast",
        "Generated doubt",
        "Working proposition",
        "Expected consequence if the working proposition is true",
        "Observed match, break, or missing condition",
        "Proposition status assessment",
        "Derived hypothesis candidate",
        "What evidence would update this analysis",
    ]
    analysis = {name: require_analysis_field(fields, name) for name in required_names}
    status = analysis["Proposition status assessment"]
    if status != requested_status:
        fail(f"source analysis status '{status}' does not match --status '{requested_status}'")
    if status not in PLANNABLE_STATUSES:
        fail(
            f"proposition status '{status}' does not permit creating a hypothesis plan; "
            "add material, record the contradiction, revise, split, or close the proposition first"
        )
    if is_placeholder(analysis["Derived hypothesis candidate"]):
        fail("source analysis has no derived hypothesis candidate")
    return analysis


def read_current_status(proposition_md: Path) -> str:
    lines = proposition_md.read_text(encoding="utf-8").splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "## Current status":
            start = index + 1
            break
    if start is None:
        fail(f"proposition.md missing Current status section: {proposition_md}")

    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            break
        if stripped:
            return stripped
    fail(f"proposition.md has empty Current status section: {proposition_md}")


def ensure_parent_status_plannable(proposition_md: Path) -> None:
    status = read_current_status(proposition_md)
    if status not in PARENT_PLANNABLE_STATUSES:
        fail(
            f"parent proposition current status '{status}' does not permit creating a hypothesis plan; "
            "record the contradiction, revise, split, or close the proposition first"
        )


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
        help="Source analysis proposition status; only supported and unrealized-condition can create a plan",
    )
    parser.add_argument(
        "--type",
        default="predictive / performance",
        choices=[
            "predictive / performance",
            "mechanistic",
            "causal / intervention",
            "descriptive / characterization",
            "theoretical",
            "mixed",
        ],
        help="Hypothesis type",
    )
    parser.add_argument("--expected", default=None, help="Prediction or expected observation")
    parser.add_argument("--competing", default=None, help="Competing hypothesis")
    parser.add_argument("--discriminator", default=None, help="Minimal discriminator")
    parser.add_argument("--required-evidence", default=None, help="Required evidence before claiming support")
    args = parser.parse_args()

    validate_components(args.proposition, args.id, args.slug, args.source_analysis)
    project = Path(args.project).resolve()
    propositions_root = project / "propositions"
    prop_dir = propositions_root / args.proposition
    ensure_inside(prop_dir, propositions_root, "proposition path")
    if not prop_dir.exists():
        fail(f"parent proposition does not exist: {prop_dir}")
    proposition_md = prop_dir / "proposition.md"
    if not proposition_md.exists():
        fail(f"proposition.md missing under: {prop_dir}")
    ensure_parent_status_plannable(proposition_md)
    analysis = load_source_analysis(prop_dir, args.source_analysis, args.status)

    prop_id = args.proposition.split("_", 1)[0]
    hyp_name = f"{args.id}_{args.slug}"
    hyp_dir = prop_dir / "hypotheses" / hyp_name
    ensure_inside(hyp_dir, prop_dir / "hypotheses", "hypothesis path")
    if hyp_dir.exists():
        fail(f"hypothesis already exists: {hyp_dir}")

    hyp_dir.mkdir(parents=True)
    (hyp_dir / "experiments").mkdir()
    (hyp_dir / "reports").mkdir()
    for sub in ["code", "configs", "runs", "notebooks"]:
        (hyp_dir / "experiments" / sub).mkdir(parents=True, exist_ok=True)
        (hyp_dir / "experiments" / sub / ".gitkeep").touch()
    (hyp_dir / "reports" / ".gitkeep").touch()

    prop_title = read_title(proposition_md)
    expected_observation = args.expected or analysis["Expected consequence if the working proposition is true"]
    competing = args.competing or (
        "The same material is explained by a competing condition, comparator, or measurement effect rather than this hypothesis."
    )
    discriminator = args.discriminator or analysis["What evidence would update this analysis"]
    required_evidence = args.required_evidence or analysis["What evidence would update this analysis"]
    replacements = {
        "<hypothesis_id>": args.id,
        "<Hypothesis title>": args.title,
        "<proposition_id>": prop_id,
        "<source_analysis>": args.source_analysis,
        "<hypothesis_statement>": args.hypothesis,
        "<hypothesis_type>": args.type,
        "<working proposition from the source analysis>": analysis["Working proposition"],
        "<source_status>": args.status,
        "<why this hypothesis preserves, revises, splits from, or realizes a condition of the parent proposition>": (
            f"{analysis['Generated doubt']} Status: {args.status}."
        ),
        "<what should be observed if the hypothesis is useful>": expected_observation,
        "<plausible alternative that could explain the same material>": competing,
        "<smallest experiment, analysis, derivation check, or observation that separates this hypothesis from the competitor>": discriminator,
        "<evidence needed before planning or before claiming support>": required_evidence,
    }

    hypothesis_md = render_template(ASSETS / "hypothesis" / "hypothesis.md.template", replacements)
    (hyp_dir / "hypothesis.md").write_text(hypothesis_md, encoding="utf-8")
    decisions_md = render_template(ASSETS / "hypothesis" / "decisions.md.template", replacements)
    (hyp_dir / "decisions.md").write_text(decisions_md, encoding="utf-8")

    tpl_path = ASSETS / "plan" / f"rd_plan_{args.mode}.md.template"
    if not tpl_path.exists():
        fail(f"template not found: {tpl_path}")
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
        .replace("<copy the generated doubt from the source analysis>", analysis["Generated doubt"])
        .replace("<copy the working proposition from the source analysis>", analysis["Working proposition"])
        .replace("<copy the expected consequence from the source analysis>", analysis["Expected consequence if the working proposition is true"])
        .replace("<observable result expected if the hypothesis is useful>", expected_observation)
        .replace("<source observations from observations.md>", analysis["Material used"])
        .replace("<plausible alternative under which the predicted effect should not appear>", competing)
        .replace("<smallest comparison, observation, derivation check, or controlled intervention>", discriminator)
        .replace("<plausible alternative explaining the same material>", competing)
        .replace("<smallest observation or analysis that separates them>", discriminator)
        .replace("<smallest acceptance test or measurement that separates them>", discriminator)
        .replace("<smallest derivation check, counterexample, limiting-case check, or model that separates them>", discriminator)
        .replace("<observable consequence if applicable, or state no current empirical evaluator and name the assumption-audit constraint>", expected_observation)
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
