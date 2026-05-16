import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_mentions(text: str, *terms: str):
    lowered = text.lower()
    missing = [term for term in terms if term.lower() not in lowered]
    assert not missing, f"missing terms: {missing}"


def assert_ordered_fragments(text: str, *fragments: str):
    normalized = " ".join(text.lower().split())
    cursor = 0
    missing = []
    for fragment in fragments:
        index = normalized.find(fragment.lower(), cursor)
        if index == -1:
            missing.append(fragment)
        else:
            cursor = index + len(fragment)
    assert not missing, f"missing ordered fragments: {missing}"


def assert_absent(text: str, *terms: str):
    lowered = text.lower()
    present = [term for term in terms if term.lower() in lowered]
    assert not present, f"unexpected terms present: {present}"


def test_report_format_distinguishes_material_conditions_from_env_locks():
    report_format = read("skills/research/references/report_format.md")

    assert_ordered_fragments(
        report_format,
        "reports should describe material conditions",
        "not environment locks",
        "methods reproducibility",
        "not computational replicability",
    )
    assert_ordered_fragments(
        report_format,
        "seed information",
        "variability disclosure",
        "not a substitute for reporting variance",
    )


def test_research_skill_frames_provenance_as_audit_not_reproducibility_itself():
    skill = read("skills/research/SKILL.md")

    assert_mentions(skill, "material execution conditions")
    assert_ordered_fragments(
        skill,
        "provenance",
        "audit pointer",
        "not the source of reproducibility",
    )
    assert_ordered_fragments(
        skill,
        "claim-to-artifact",
        "integrity check",
        "rather than making the method reproducible",
    )


def test_report_format_frames_claim_to_artifact_as_integrity_not_reproducibility():
    report_format = read("skills/research/references/report_format.md")

    assert_mentions(
        report_format,
        "claim-to-artifact",
        "evidence-integrity",
    )
    assert_ordered_fragments(
        report_format,
        "claim-to-artifact consistency",
        "evidence-integrity check",
        "not a separate reproducibility theory",
    )


def test_plan_schema_requires_material_conditions_not_env_locks():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "audit trail",
        "not a substitute for methodology",
    )
    assert_ordered_fragments(
        rd_plan,
        "methods reproducibility",
        "material conditions",
        "not env locks or commit hashes",
    )
    assert_ordered_fragments(
        rd_plan,
        "changing a seed value",
        "before seeing outcomes",
        "usually not material",
        "changing the seed policy",
        "train/test split seed",
        "after seeing a result",
        "is material",
    )


def test_readme_keeps_experiment_replicability_out_of_the_core_contract():
    readme = read("README.md")

    assert_ordered_fragments(
        readme,
        "research-level reproducibility",
        "is enforced",
        "experiment-level replicability",
        "agent's discretion",
    )
    assert_ordered_fragments(
        readme,
        "reports record",
        "material conditions",
        "not environment locks",
    )
    assert_ordered_fragments(
        readme,
        "claim-to-artifact consistency checks",
        "evidence-integrity checks",
        "rather than a replacement for methods reproducibility",
    )
    assert_ordered_fragments(
        readme,
        "experiment-level replicability infrastructure",
        "not skill-enforced",
        "provenance or variability logs",
        "not substitutes for methods reproducibility",
    )


def test_report_templates_prompt_for_material_conditions():
    template_dir = ROOT / "skills" / "research" / "assets" / "report"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "Material conditions" in text, template
        assert "when applicable" in text.lower(), template
        assert "not environment locks" in text, template


def test_applied_report_keeps_material_conditions_in_methods_area():
    text = read("skills/research/assets/report/applied_research_report.md.template")

    material_position = text.index("### Material conditions")
    results_position = text.index("## Results")

    assert material_position < results_position


def test_claim_and_analysis_docs_frame_evidence_and_seed_variability():
    claim_structure = read("skills/research/references/claim_structure.md")
    analysis = read("skills/research/references/analysis.md")

    assert_ordered_fragments(
        claim_structure,
        "evidence-integrity anchor",
        "not by itself a reproducibility guarantee",
        "method and tested conditions",
        "reproducibility burden",
    )
    assert_ordered_fragments(
        analysis,
        "do not treat a single fixed seed as reproducibility",
        "report seed count, dispersion, and failed seeds",
        "claim is supported by the distribution of outcomes",
    )


def test_quant_docs_use_seed_variability_and_artifact_auditability_terms():
    modeling = read("skills/quant-research/references/shared/modeling_approach.md")
    feature_construction = read("skills/quant-research/references/shared/feature_construction.md")

    assert "Seed variability / RNG sensitivity" in modeling
    assert "report distribution over multiple seeds" in modeling
    assert "breaks artifact provenance and downstream auditability" in feature_construction


def test_plan_templates_prompt_for_material_conditions():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "material conditions" in text, template


def test_every_plan_template_requires_prior_work_grounding_before_plan():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "## Prior-work grounding" in text, template
        assert text.index("## Prior-work grounding") < text.index("## Plan"), template
        assert_mentions(
            text,
            "bounded but sufficient",
            "question/objective",
            "inherited assumptions",
            "method choice",
            "baselines/evaluation protocol",
            "known limitations",
        )
        assert_absent(
            text,
            "Novelty / differentiation thesis",
            "unknown-not-yet-reviewed if no novelty claim is made",
            "literature/differentiation.md",
        )


def test_plan_schema_makes_prior_work_grounding_first_class_not_novelty_optional():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "## Question / Objective",
        "## Prior-work grounding",
        "## Divergence checkpoint",
        "## Plan",
    )
    assert_mentions(
        rd_plan,
        "bounded but sufficient",
        "question/objective",
        "inherited assumptions",
        "method choice",
        "baselines/evaluation protocol",
        "known limitations",
        "named constraint",
        "narrow or block relevant claims",
    )
    assert_absent(
        rd_plan,
        "Novelty / differentiation thesis",
        "unknown-not-yet-reviewed",
        "literature/differentiation.md",
    )


def test_research_skill_routes_research_idea_generation_to_ideation_reference():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_mentions(
        skill,
        "research idea",
        "hypothesis candidate",
        "what should we try next",
        "references/ideation.md",
        "fresh de-anchoring subagent",
        "sanitized brief",
        "must not generate raw candidates itself",
        "before Prior-work grounding",
    )
    assert_ordered_fragments(
        rd_plan,
        "Idea portfolio",
        "Prior-work grounding",
        "Divergence checkpoint",
        "## Plan",
    )


def test_ideation_reference_defines_deanchoring_before_grounded_pruning():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "De-anchoring pass",
        "Transformation pass",
        "Quality-diversity pass",
        "Grounded pruning pass",
        "Information-gain scoring",
        "Pre-execution divergence review",
        "Plan promotion",
    )
    assert_mentions(
        ideation,
        "do not read prior work first",
        "prior work is applied after raw candidates exist",
        "method / mechanism / data assumption / metric / evaluation protocol / system design / problem framing",
        "failed idea",
        "not a claim",
        "parked / killed / merged",
    )


def test_ideation_reference_requires_hypothesis_synthesis_not_just_candidate_listing():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "Hypothesis synthesis pass",
        "Source observation",
        "Mechanism conjecture",
        "Proposed intervention",
        "Predicted effect",
        "Counter-hypothesis",
        "Minimal disconfirming test",
    )
    assert_mentions(
        ideation,
        "landmark papers",
        "historical exemplars",
        "Attention Is All You Need",
        "ResNet",
        "DQN",
        "Generative Pre-Training",
        "candidate list is not enough",
    )


def test_ideation_reference_defines_observation_discovery_before_hypothesis_synthesis():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "De-anchoring pass",
        "Raw candidate generation",
        "Main-agent handoff",
        "Transformation pass",
        "Observation discovery pass",
        "Observation is not yet a hypothesis",
        "Empirical observation",
        "Literature observation",
        "Failure-mode observation",
        "Tension observation",
        "Baseline observation",
        "User/problem observation",
        "Hypothesis synthesis pass",
    )
    assert_mentions(
        ideation,
        "observed phenomenon",
        "mechanism conjecture",
        "References can supply observations",
        "References later ground candidates",
    )


def test_research_skill_orders_lifecycle_from_observation_to_decision():
    skill = read("skills/research/SKILL.md")

    assert_ordered_fragments(
        skill,
        "Research lifecycle",
        "Observation discovery",
        "Hypothesis synthesis",
        "Intervention idea",
        "Prior-work grounding",
        "Plan",
        "Execution",
        "Analysis",
        "Claim",
        "Decision",
    )
    assert_mentions(
        skill,
        "observation is not yet a hypothesis",
        "prior work has two roles",
        "material for observations",
        "grounding after candidates exist",
    )


def test_confirmatory_plan_template_requires_hypothesis_rationale_chain():
    template = read("skills/research/assets/plan/rd_plan_confirmatory.md.template")

    assert_ordered_fragments(
        template,
        "### Hypothesis rationale",
        "Source observation",
        "Mechanism conjecture",
        "Proposed intervention",
        "Predicted effect",
        "Counter-hypothesis",
        "Minimal disconfirming test",
        "### Hypothesis",
    )


def test_plan_schema_records_hypothesis_synthesis_in_idea_portfolio():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "## Idea portfolio",
        "### De-anchored candidates",
        "### Transformation axes",
        "### Hypothesis synthesis",
        "Source observation",
        "Mechanism conjecture",
        "Proposed intervention",
        "Predicted effect",
        "Counter-hypothesis",
        "Minimal disconfirming test",
        "### Grounded pruning",
    )


def test_iteration_loop_defines_approach_transition_criteria():
    iteration_loop = read("skills/research/references/iteration_loop.md")

    assert_ordered_fragments(
        iteration_loop,
        "Approach transition criteria",
        "stay with the current approach",
        "REFINE",
        "ADJACENT",
        "PARK",
        "CLOSE",
    )
    assert_mentions(
        iteration_loop,
        "mechanism conjecture",
        "method family",
        "data assumption",
        "evaluation target",
        "repairable cause",
        "information gain",
        "alternative approach",
    )


def test_research_skill_docs_are_english_only():
    checked_paths = [
        ROOT / "skills" / "research" / "SKILL.md",
        *sorted((ROOT / "skills" / "research" / "references").rglob("*.md")),
        *sorted((ROOT / "skills" / "research" / "assets").rglob("*.template")),
    ]

    offenders = []
    for path in checked_paths:
        text = path.read_text(encoding="utf-8")
        if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", text):
            offenders.append(str(path.relative_to(ROOT)))

    assert not offenders, f"Japanese/CJK text found in skill docs: {offenders}"


def test_ideation_uses_fresh_subagent_for_deanchored_raw_candidates():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "Sanitized brief",
        "Fresh de-anchoring subagent",
        "Raw candidate generation",
        "Grounded pruning pass",
    )
    assert_mentions(
        ideation,
        "The main agent must not generate raw candidates itself after seeing anchors.",
        "prior work names",
        "SOTA",
        "previous best approaches",
        "user-preferred method",
        "convenient dataset details",
    )


def test_plan_templates_include_idea_portfolio_before_prior_work_grounding():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Question / Objective",
            "## Idea portfolio",
            "## Prior-work grounding",
            "## Divergence checkpoint",
            "## Plan",
        )
        assert_mentions(
            text,
            "Not applicable: objective already chosen",
            "research ideas",
            "hypothesis candidates",
            "what should we try next",
            "references/ideation.md",
            "sanitized brief",
            "fresh de-anchoring subagent",
        )


def test_new_plan_guidance_mentions_idea_portfolio_before_prior_work_grounding():
    new_plan = read("skills/research/scripts/new_plan.py")

    assert_ordered_fragments(
        new_plan,
        "Question / Objective",
        "Idea portfolio",
        "Prior-work grounding",
        "Divergence checkpoint",
        "Plan",
        "time-anchor",
    )


def test_idea_portfolio_records_pre_execution_divergence_review():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "fresh de-anchoring subagent",
        "### Pre-execution divergence review",
        "parameter sweep",
        "literature-first",
        "prior-work",
        "not claims",
    )


def test_readme_documents_research_ideation_before_prior_work_grounding():
    readme = read("README.md")

    assert_ordered_fragments(
        readme,
        "Question / Objective",
        "Research ideation",
        "Idea portfolio",
        "prior-work grounding",
    )
    assert_mentions(
        readme,
        "research ideas",
        "hypothesis candidates",
        "what should we try next",
        "de-anchored",
        "parked / killed / merged",
        "ideation.md",
    )


def test_literature_review_contract_uses_positioning_for_grounding_not_default_novelty():
    literature = read("skills/research/references/literature_review.md")

    assert_mentions(
        literature,
        "prior-work grounding",
        "bounded but sufficient",
        "literature/positioning.md",
        "stands on prior work",
        "claim scope",
        "comprehensive literature survey",
        "to our knowledge",
    )
    assert_ordered_fragments(
        literature,
        "every plan needs prior-work grounding",
        "not optional just because no novelty claim is made",
    )
    assert_absent(
        literature,
        "A brief pass is appropriate",
        "literature/differentiation.md",
        "differentiation.md format",
    )


def test_research_skill_and_project_seed_positioning_not_differentiation():
    skill = read("skills/research/SKILL.md")
    new_project = read("skills/research/scripts/new_project.py")
    project_readme = read("skills/research/assets/project/README.md.template")

    for text in [skill, new_project, project_readme]:
        assert_mentions(text, "literature/positioning.md")
        assert_absent(text, "literature/differentiation.md")

    assert_mentions(
        new_project,
        "positioning.md",
        "how the work stands on prior work",
    )
    assert_absent(new_project, "differentiation.md")


def test_readme_and_plugin_metadata_describe_prior_work_grounding():
    readme = read("README.md")
    codex_plugin = read(".codex-plugin/plugin.json")
    claude_plugin = read(".claude-plugin/plugin.json")
    marketplace = read(".claude-plugin/marketplace.json")

    for text in [readme, codex_plugin, claude_plugin, marketplace]:
        assert_mentions(text, "prior-work grounding")

    assert_mentions(readme, "literature/{papers.md,positioning.md}")
    assert_absent(readme, "literature/{papers.md,differentiation.md}")


def test_research_docs_do_not_preserve_legacy_light_review_loopholes():
    docs = [
        "skills/research/SKILL.md",
        "skills/research/references/literature_review.md",
        "skills/research/references/rd_plan.md",
        "skills/research/assets/plan/rd_plan_exploratory.md.template",
        "skills/research/assets/plan/rd_plan_confirmatory.md.template",
        "skills/research/assets/plan/rd_plan_milestone.md.template",
        "README.md",
    ]

    for path in docs:
        assert_absent(
            read(path),
            "brief pass",
            "light review",
            "unknown-not-yet-reviewed if no novelty claim is made",
            "unknown-not-yet-reviewed is allowed only when",
            "Novelty / differentiation thesis",
            "literature/differentiation.md",
        )


def test_new_plan_guidance_includes_prior_work_grounding_before_plan_commit():
    new_plan = read("skills/research/scripts/new_plan.py")

    assert_mentions(new_plan, "Prior-work grounding")
    assert_ordered_fragments(
        new_plan,
        "Question / Objective",
        "Prior-work grounding",
        "Divergence checkpoint",
        "Plan",
        "time-anchor",
    )


def test_new_project_seeds_positioning_with_required_fields():
    script = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    required_fields = [
        "What it establishes",
        "Inherited assumption",
        "Baseline / protocol use",
        "Known limitation",
        "Position of this work",
        "Claim scope",
    ]

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(script), str(target), "--name", "Positioning Seed Test"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        positioning = (target / "literature" / "positioning.md").read_text(encoding="utf-8")

    assert "literature/positioning.md" in positioning
    for field in required_fields:
        assert field in positioning
    assert_absent(positioning, "Use the format from `references/literature_review.md`.")
