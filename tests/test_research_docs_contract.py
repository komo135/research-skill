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


def test_report_format_and_templates_define_paper_grade_contract():
    report_format = read("skills/research/references/report_format.md")
    readme = read("README.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "report"

    assert_mentions(
        report_format,
        "paper-grade report",
        "not a venue manuscript",
        "standalone evidence artifact",
        "Related Work",
        "Ablation / Sensitivity",
        "Discussion",
        "References",
    )
    assert_mentions(readme, "paper-grade", "Related Work", "Ablation / Sensitivity", "Discussion", "References")

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Summary",
            "## Background",
            "## Related Work",
        )
        assert_ordered_fragments(
            text,
            "## Ablation / Sensitivity",
            "## Discussion",
            "## Limitations",
            "## Next action",
            "## References",
        )
        assert_mentions(
            text,
            "Not applicable:",
            "plan",
            "source artifacts",
        )


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
        "anchor-stripped seed brief",
        "excluded anchors",
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


def test_ideation_reference_defines_hypothesis_generation_handoff_and_main_intake():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "De-anchoring pass",
        "Hypothesis-generation handoff",
        "Main-agent intake",
        "Assumption audit pass",
        "Anti-vacuity gate",
        "Grounded pruning pass",
        "Plan promotion",
    )
    assert_mentions(
        ideation,
        "fresh separate-context",
        "anchor-stripped seed brief is the only generation brief",
        "Excluded-anchor ledger is not input",
        "multiple working hypotheses",
        "current observations",
        "web or literature retrieval notes",
        "If the user requests web or literature",
        "Do not accept generator output as authority",
        "advance / park / kill / merge / regenerate",
        "next-plan action",
    )


def test_ideation_retrieval_skip_does_not_waive_plan_scoped_survey():
    ideation = read("skills/research/references/ideation.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        ideation,
        "does not satisfy or waive the plan-scoped literature survey",
        "Survey evidence",
    )

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_mentions(
            text,
            "does not replace Survey evidence",
        )


def test_ideation_promotion_waits_for_survey_evidence_despite_template_order():
    ideation = read("skills/research/references/ideation.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        ideation,
        "Do not finalize Grounded pruning or Promotion decision before Survey evidence exists",
    )
    assert_mentions(
        rd_plan,
        "section order is not permission to finalize promotion before Survey evidence",
    )

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_mentions(
            text,
            "not final until Survey evidence exists",
            "section order is not permission",
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


def test_ideation_reference_defines_generation_substrate_and_antivacuity_gate():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "Idea substrate pass",
        "Generation operator pass",
        "Anti-vacuity gate",
        "Hypothesis synthesis pass",
        "Evaluator feedback pass",
        "Grounded pruning pass",
    )
    assert_mentions(
        ideation,
        "candidate must cite at least two substrate ids",
        "operator",
        "changed premise",
        "predicted measurable effect",
        "minimal disconfirming test",
        "kill the candidate",
        "not post-hoc prose",
    )


def test_ideation_reference_defines_observation_discovery_before_hypothesis_synthesis():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "De-anchoring pass",
        "Raw candidate generation",
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


def test_research_lifecycle_uses_only_plan_review_and_result_analysis_subagents():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    readme = read("README.md")

    for text in [skill, rd_plan, readme]:
        assert_ordered_fragments(
            text,
            "Plan",
            "Plan review",
            "Execution",
            "Result analysis",
            "Claim",
            "Decision",
        )
        assert_mentions(text, "research-plan-review", "research-result-analysis")
        assert_absent(
            text,
            "research-review subagent",
            "main research agent must not perform result analysis itself",
        )


def test_result_analysis_subagent_prompt_uses_plan_as_only_starting_context():
    prompt = read("skills/research/references/result_analysis_subagent_prompt.md")

    assert_ordered_fragments(
        prompt,
        "Use the research-result-analysis skill.",
        "Analyze this plan:",
        "<plans/id_slug.md>",
        "Treat the plan as the only starting context.",
    )
    assert_mentions(
        prompt,
        "Do not use parent-agent summaries",
        "reconstruct necessary evidence yourself",
        "referenced runs",
        "run_manifest.json",
        "logs/stdout.log",
        "scripts",
        "outputs",
        "tables",
        "figures",
        "context_missing",
        "why the result happened",
    )


def test_plan_review_and_result_analysis_skill_boundaries_are_documented():
    plan_review = read("skills/research-plan-review/SKILL.md")
    result_analysis = read("skills/research-result-analysis/SKILL.md")

    assert_mentions(
        plan_review,
        "research-plan-review",
        "plan path",
        "research design",
        "before execution",
        "mechanism hypothesis",
        "prediction",
        "discriminating test",
    )
    assert_mentions(
        plan_review,
        "Do not execute",
        "Do not analyze results",
        "Do not write final claims",
    )
    assert_mentions(
        plan_review,
        "execution recommendation",
        "pre-execution",
        "not a claim-readiness verdict",
        "theoretical mode",
        "derivation question",
        "limiting-case checks",
    )
    assert_absent(
        plan_review,
        "Claim-readiness verdicts",
        "Claim-readiness assessment",
        "`ready`",
        "`not_ready`",
        "`invalid_evidence`",
        "GO/NO-GO",
    )
    assert_mentions(
        result_analysis,
        "research-result-analysis",
        "plan path",
        "only starting context",
        "why the result happened",
        "What happened",
        "Candidate explanations",
        "Evidence for / against",
        "Procedure / artifact explanations",
        "Discriminating next analyses",
        "context_missing",
        "artifact contract",
        "stdout is not evidence",
    )
    assert_mentions(
        result_analysis,
        "Do not write final claims",
        "Do not choose iteration decisions",
        "Do not rely on parent-agent summaries",
    )
    assert_absent(
        result_analysis,
        "Claim-readiness verdicts",
        "Claim-readiness assessment",
        "`ready`",
        "`not_ready`",
        "`invalid_evidence`",
        "GO/NO-GO",
    )


def test_result_analysis_prompt_preserves_subagent_output_before_claims():
    prompt = read("skills/research/references/result_analysis_subagent_prompt.md")

    assert_ordered_fragments(
        prompt,
        "records the returned `## Result analysis` section",
        "before writing claims, decisions, or reports",
    )
    assert_mentions(
        prompt,
        "Do not analytically summarize",
        "rewrite",
        "collapse the subagent's findings",
    )


def test_plan_templates_record_plan_review_and_result_analysis_without_research_review():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Plan",
            "## Plan review",
            "## Actual execution",
            "## Planned vs Actual",
            "## Result analysis",
            "## Claims",
        )
        assert_mentions(text, "research-plan-review", "research-result-analysis")
        assert_absent(
            text,
            "## Research review",
            "research-review subagent",
            "Claim-readiness assessment",
        )


def test_plans_separate_pre_result_commitments_from_post_result_explanations():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    plan_review = read("skills/research-plan-review/SKILL.md")
    result_analysis = read("skills/research-result-analysis/SKILL.md")

    for text in [skill, rd_plan, plan_review]:
        assert_mentions(
            text,
            "pre-result commitments",
            "post-result explanations",
            "do not explain why an unobserved result happened",
            "planned discriminating test",
        )
        assert_absent(
            text,
            "explain why the result happened before execution",
            "pre-execution result explanation",
        )

    assert_mentions(
        result_analysis,
        "post-result explanations",
        "after evidence exists",
        "candidate explanations",
        "not pre-result commitments",
    )


def test_plan_templates_do_not_invite_pre_result_result_analysis():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Result analysis",
            "Do not fill this section before execution",
            "After evidence exists",
            "record the returned `## Result analysis` section here",
            "## Claims",
        )
        result_analysis_section = text.split("## Result analysis", 1)[1].split("## Claims", 1)[0]
        assert_absent(
            result_analysis_section,
            "### Candidate explanations",
            "### Failed prediction analysis",
            "### Procedure / artifact explanations",
            "### Alternatives still live",
            "### Discriminating next analyses",
            "<explanation 1 for why the result happened>",
            "<candidate explanation for why the prediction missed>",
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
        "### Idea substrate",
        "### Generation operators",
        "### De-anchored candidates",
        "### Hypothesis-generation handoff",
        "### Main-agent intake",
        "### Anti-vacuity gate",
        "### Hypothesis synthesis",
        "Source observation",
        "Mechanism conjecture",
        "Proposed intervention",
        "Predicted effect",
        "Counter-hypothesis",
        "Minimal disconfirming test",
        "### Evaluator feedback",
        "### Grounded pruning",
    )


def test_plan_schema_and_templates_record_handoff_and_main_intake_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "## Idea portfolio",
            "### De-anchored candidates",
            "### Hypothesis-generation handoff",
            "Agent",
            "Starting context",
            "Output contract",
            "### Main-agent intake",
            "Authority check",
            "Observation trace check",
            "Mechanism review",
            "Decision",
            "Next-plan action",
            "### Anti-vacuity gate",
        )
        assert_mentions(
            text,
            "fresh separate-context hypothesis-generation agent",
            "generator output is seed material",
            "regenerate",
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


def test_ideation_uses_anchor_stripped_seed_brief_for_deanchored_raw_candidates():
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        ideation,
        "Anchor-stripped seed brief",
        "Excluded-anchor ledger",
        "Raw candidate generation",
        "Grounded pruning pass",
    )
    assert_mentions(
        ideation,
        "do not let them define the raw seed space",
        "prior work names",
        "SOTA",
        "previous best approaches",
        "user's preferred method",
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
            "anchor-stripped brief",
            "Excluded-anchor ledger",
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
    ideation = read("skills/research/references/ideation.md")

    assert_ordered_fragments(
        rd_plan,
        "anchor-stripped seed brief",
        "excluded-anchor ledger",
        "### Pre-execution divergence review",
        "parameter sweep",
        "literature-first",
        "prior-work",
        "not claims",
    )
    assert_absent(ideation, "research review")


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


def test_literature_review_contract_requires_plan_scoped_paper_survey_before_plan():
    literature = read("skills/research/references/literature_review.md")

    assert_ordered_fragments(
        literature,
        "plan-scoped paper survey",
        "before writing the Plan section",
        "Prior-work grounding",
    )
    assert_mentions(
        literature,
        "search date",
        "queries or source names",
        "selection rationale",
        "negative findings",
        "retrieval-unavailable constraint",
    )


def test_plan_templates_record_survey_evidence_before_plan():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Prior-work grounding",
            "Survey evidence",
            "Question/objective supported by",
            "## Divergence checkpoint",
            "## Plan",
        )
        assert_mentions(
            text,
            "search date",
            "queries/sources",
            "negative findings",
            "retrieval-unavailable constraint",
        )


def test_prior_work_grounding_requires_citation_use_map():
    literature = read("skills/research/references/literature_review.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        literature,
        "citation-use map",
        "how each cited work is used",
        "not enough to list papers",
    )

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "### Survey evidence",
            "### Citation-use map",
            "### Grounding scope",
        )
        assert_mentions(
            text,
            "Used for",
            "Plan dependency",
            "How it is used",
            "Claim-scope effect",
        )


def test_retrieval_unavailable_is_verifiable_and_narrows_claim_scope():
    literature = read("skills/research/references/literature_review.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    plan_review = read("skills/research-plan-review/SKILL.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [literature, rd_plan, plan_review]:
        assert_mentions(
            text,
            "retrieval-unavailable is not a survey bypass",
            "verifiable signal",
            "attempted source/tool",
            "failure evidence",
            "claim-scope narrowing",
        )

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_mentions(
            text,
            "Retrieval-unavailable evidence",
            "attempted source/tool",
            "failure evidence",
            "Claim-scope narrowing",
        )


def test_citation_role_fields_define_plan_source_of_truth():
    literature = read("skills/research/references/literature_review.md")
    rd_plan = read("skills/research/references/rd_plan.md")

    for text in [literature, rd_plan]:
        assert_mentions(
            text,
            "project-level role union",
            "plan-specific source of truth",
            "Citation-use map",
            "papers.md",
            "positioning.md",
        )


def test_plan_review_subfield_completion_is_not_grounding_sufficiency():
    plan_review = read("skills/research-plan-review/SKILL.md")

    assert_mentions(
        plan_review,
        "Sub-field completion is not grounding sufficiency",
        "substantive",
        "filled fields",
        "block_execution",
    )


def test_research_docs_require_mid_execution_literature_updates():
    literature = read("skills/research/references/literature_review.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    readme = read("README.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [literature, rd_plan, readme]:
        assert_mentions(
            text,
            "mid-execution literature update",
            "unfamiliar method",
            "unexpected result",
            "new comparator",
        )

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "## Actual execution",
            "### Mid-execution literature updates",
            "## Planned vs Actual",
        )
        assert_mentions(
            text,
            "survey trigger",
            "effect on plan",
            "rerun Plan review",
        )


def test_research_skill_and_new_plan_guidance_require_literature_survey_before_plan():
    skill = read("skills/research/SKILL.md")
    new_plan = read("skills/research/scripts/new_plan.py")
    readme = read("README.md")

    for text in [skill, new_plan, readme]:
        assert_mentions(
            text,
            "plan-scoped literature survey",
            "before the Plan section",
        )


def test_plan_review_blocks_missing_literature_survey_evidence():
    plan_review = read("skills/research-plan-review/SKILL.md")

    assert_mentions(
        plan_review,
        "Survey evidence",
        "Citation-use map",
        "literature/papers.md",
        "literature/positioning.md",
        "block_execution",
        "bibliography without use mapping",
    )
    assert_ordered_fragments(
        plan_review,
        "Read the plan",
        "Prior-work grounding",
        "Survey evidence",
        "Execution recommendation",
    )


def test_plan_review_templates_include_prior_work_survey_check():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "### Research-design checks",
            "Evidence route and artifact plan",
            "Prior-work survey evidence",
            "Scope and constraints",
            "### Required repairs before execution",
        )
        assert_mentions(text, "block if missing")


def test_research_skill_and_project_seed_positioning_not_differentiation():
    skill = read("skills/research/SKILL.md")
    new_project = read("skills/research/scripts/new_project.py")
    project_readme = read("skills/research/assets/project/README.md.template")

    for text in [skill, new_project, project_readme]:
        assert_mentions(text, "literature/positioning.md")
        assert_absent(text, "literature/differentiation.md")
    assert_absent(project_readme, "research review")

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
        "Used in plan as",
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


def test_new_plan_accepts_theoretical_mode_and_generates_theoretical_sections():
    script = ROOT / "skills" / "research" / "scripts" / "new_plan.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                str(target),
                "--id",
                "42",
                "--slug",
                "closed-form-bound",
                "--category",
                "basic_research",
                "--mode",
                "theoretical",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        assert result.returncode == 0, result.stderr
        plan = (target / "plans" / "42_closed-form-bound.md").read_text(encoding="utf-8")

    assert "mode: theoretical" in plan
    assert "### Derivation question" in plan
    assert "### Limiting-case checks" in plan
    assert "### Empirical sanity check" in plan


def test_research_scripts_must_persist_durable_artifacts_not_only_print():
    skill = read("skills/research/SKILL.md")
    analysis = read("skills/research/references/analysis.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    iterative = read("skills/research/references/iterative_ideation.md")
    project_readme = read("skills/research/assets/project/README.md.template")

    for text in [skill, analysis, rd_plan, iterative, project_readme]:
        assert_mentions(
            text,
            "print-only",
            "stdout is not evidence",
            "run_manifest.json",
            "logs/stdout.log",
            "intermediate",
            "durable artifact",
        )


def test_new_run_creates_durable_artifact_scaffold():
    new_plan = ROOT / "skills" / "research" / "scripts" / "new_plan.py"
    new_run = ROOT / "skills" / "research" / "scripts" / "new_run.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        subprocess.run(
            [
                sys.executable,
                str(new_plan),
                str(target),
                "--id",
                "07",
                "--slug",
                "artifact-contract",
                "--category",
                "applied_research",
                "--mode",
                "exploratory",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        result = subprocess.run(
            [sys.executable, str(new_run), str(target), "--plan", "07", "--slug", "artifact-contract", "--seed", "3"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        assert result.returncode == 0, result.stderr
        run_dir = target / "experiments" / "07_artifact-contract" / "runs" / "07__001__seed3"
        manifest = (run_dir / "run_manifest.json").read_text(encoding="utf-8")
        readme = (run_dir / "README.md").read_text(encoding="utf-8")

        for relative in [
            "logs/stdout.log",
            "logs/stderr.log",
            "intermediate",
            "outputs",
            "tables",
            "figures",
            "run_manifest.json",
        ]:
            assert (run_dir / relative).exists(), relative
        assert_mentions(manifest, "initialized", "command", "artifacts")
        assert_mentions(readme, "print-only", "stdout is not evidence", "check_run_artifacts.py")


def test_check_run_artifacts_rejects_print_only_run():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "logs" / "stdout.log").write_text("accuracy 0.84\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"completed","command":"python eda.py"}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "stdout is not evidence" in result.stdout
    assert "No durable artifact" in result.stdout


def test_check_run_artifacts_requires_manifest_artifact_list():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("wrote outputs/metrics.json\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "metrics.json").write_text('{"accuracy": 0.84, "n": 128}', encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"completed","command":"python eda.py --run-dir run","artifacts":[]}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "run_manifest.json artifacts must list" in result.stdout


def test_check_run_artifacts_rejects_unlisted_or_non_evidence_manifest_artifact():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("accuracy 0.84\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "metrics.json").write_text('{"accuracy": 0.84, "n": 128}', encoding="utf-8")
        (run_dir / "README.md").write_text("not evidence\n", encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"completed","command":"python eda.py --run-dir run","artifacts":["README.md"]}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "Manifest artifact is not in a durable artifact location" in result.stdout
    assert "No manifest-listed durable artifact" in result.stdout


def test_check_run_artifacts_rejects_stdout_transcript_as_artifact():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("accuracy 0.84\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "stdout_copy.txt").write_text("accuracy 0.84\n", encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"completed","command":"python eda.py --run-dir run","artifacts":["outputs/stdout_copy.txt"]}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "console transcript" in result.stdout
    assert "No manifest-listed durable artifact" in result.stdout


def test_check_run_artifacts_requires_completed_status():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("wrote outputs/metrics.json\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "metrics.json").write_text('{"accuracy": 0.84, "n": 128}', encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"failed","command":"python eda.py --run-dir run","artifacts":["outputs/metrics.json"]}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "run_manifest.json status must be 'completed'" in result.stdout


def test_check_run_artifacts_accepts_manifest_logs_and_artifact():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("wrote outputs/metrics.json\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "metrics.json").write_text('{"accuracy": 0.84, "n": 128}', encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","plan":"01_demo","status":"completed","command":"python eda.py --run-dir run","artifacts":["outputs/metrics.json"]}',
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Run artifacts pass contract checks." in result.stdout


def test_idea_portfolio_schema_and_templates_include_blind_spot_catalog():
    rd_plan = read("skills/research/references/rd_plan.md")
    assumption_audit = read("skills/research/references/assumption_audit.md")
    ideation = read("skills/research/references/ideation.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_ordered_fragments(
        rd_plan,
        "## Idea portfolio",
        "### Anti-vacuity gate",
        "### Blind-spot catalog",
        "### Hypothesis synthesis",
        "## Prior-work grounding",
    )
    assert_mentions(
        assumption_audit,
        "Blind-spot catalog",
        "surviving candidate",
        "How it could break the mechanism",
        "Claim-scope effect",
        "Required repair",
    )
    assert_mentions(
        ideation,
        "blind-spot catalog",
        "narrow claim scope",
        "trigger constraint-naming",
    )
    assert_absent(assumption_audit, "List 3-5", "3〜5", "Unknown-unknowns catalog")

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Idea portfolio",
            "### Anti-vacuity gate",
            "### Blind-spot catalog",
            "### Hypothesis synthesis",
            "## Prior-work grounding",
        )
        assert_mentions(
            text,
            "Blind-spot area",
            "How it could break the mechanism",
            "Claim-scope effect",
            "Required repair",
        )


def test_idea_portfolio_schema_and_templates_include_generation_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "## Idea portfolio",
            "### Idea substrate",
            "### Generation operators",
            "### Assumption audit",
            "### Anti-vacuity gate",
            "### Evaluator feedback",
            "### Grounded pruning",
        )
        assert_mentions(
            text,
            "substrate ids",
            "changed premise",
            "candidate is killed",
            "executable evaluator",
            "Skipped:",
        )


def test_check_idea_portfolio_rejects_vacuous_candidate_list():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Vacuous Plan

## Question / Objective

Find a better short-term reversal signal.

## Idea portfolio

### De-anchored candidates

- Candidate A: Try a better filter.
- Candidate B: Use volatility.

### Grounded pruning

- Advance: Candidate A sounds promising.

## Prior-work grounding

Placeholder.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "Missing required Idea portfolio subsection" in result.stdout


def test_check_idea_portfolio_accepts_substrate_operator_and_feedback_contract():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Non-vacuous Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.
- S3: Baseline observation - current close-to-close return explains only the previous bar.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Hypothesis-generation handoff

- Agent: fresh separate-context hypothesis-generation agent.
- Starting context: anchor-stripped seed brief is the only generation brief; Excluded-anchor ledger is not input.
- Web/literature retrieval: skipped with reason - substrate is already sufficient for raw hypothesis generation.
- Output contract: multiple working hypotheses with source observation, mechanism conjecture, predicted effect, counter-hypothesis, minimal disconfirming test, and retrieval notes.

### Main-agent intake

- Authority check: generator output is seed material, not accepted authority, claim, plan, or decision.
- Observation trace check: Candidate A traces to S1 and S2.
- Mechanism review: Candidate A explains spread-spike failures rather than merely swapping methods.
- Decision: advance Candidate A after anti-vacuity and evaluator feedback; regenerate any parameter-sweep-only alternatives.
- Next-plan action: open ADJACENT evaluator-construction plan before intervention claims.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: spread spike may mark temporary inventory pressure that resolves into reversal.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: survives

### Blind-spot catalog

- Candidate A:
  - Blind-spot area: market microstructure regimes could hide liquidity-provider inventory rules not in context.
  - How it could break the mechanism: spread compression may mark quote-stuffing cleanup rather than inventory-pressure relaxation.
  - Claim-scope effect: narrowed_claim: narrow claims to venues and periods where spread compression follows real liquidity recovery.
  - Required repair: retrieval: retrieve microstructure references or add venue-regime stratification before making a general claim.

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI that accepts signal definition and emits IC, turnover, variance.
- Effect on promotion: candidate can only advance to an ADJACENT evaluator-construction plan.

### Grounded pruning

- Advance: Candidate A only as evaluator-construction plan.
- Parked: None.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: testability medium; measurement clear; information gain high; cost medium; prior-work distance medium; claim discipline strong.

### Pre-execution divergence review

- Portfolio breadth: one surviving candidate because other candidates failed anti-vacuity.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: build evaluator.

### Promotion decision

- Promoted idea: Candidate A to ADJACENT evaluator-construction plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred until evaluator-construction plan is opened.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Idea portfolio passes contract checks." in result.stdout


def test_check_idea_portfolio_requires_handoff_and_main_intake_sections():
    plan = """# Missing Handoff Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: survives

### Blind-spot catalog

- Candidate A:
  - Blind-spot area: market microstructure regimes could hide venue-specific liquidity-provider constraints.
  - How it could break the mechanism: compression after a spike may reflect quote mechanics rather than rebound inventory pressure.
  - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
  - Required repair: narrow_conditions: add venue-regime stratification or park the general claim.

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: Candidate A can advance only after evaluator construction.

### Grounded pruning

- Advance: Candidate A only as evaluator-construction plan.
- Parked: None.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: high information gain but blocked.

### Pre-execution divergence review

- Portfolio breadth: limited.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: build evaluator.

### Promotion decision

- Promoted idea: Candidate A to ADJACENT evaluator-construction plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred.
"""

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 1
    assert "Missing required Idea portfolio subsection: 'Hypothesis-generation handoff'" in result.stdout
    assert "Missing required Idea portfolio subsection: 'Main-agent intake'" in result.stdout


def idea_portfolio_plan_with_blind_spot(blind_spot_block: str) -> str:
    return f"""# Blind Spot Contract Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Hypothesis-generation handoff

- Agent: fresh separate-context hypothesis-generation agent.
- Starting context: anchor-stripped seed brief is the only generation brief; Excluded-anchor ledger is not input.
- Web/literature retrieval: skipped with reason - substrate is already sufficient for raw hypothesis generation.
- Output contract: multiple working hypotheses with source observation, mechanism conjecture, predicted effect, counter-hypothesis, minimal disconfirming test, and retrieval notes.

### Main-agent intake

- Authority check: generator output is seed material, not accepted authority, claim, plan, or decision.
- Observation trace check: Candidate A traces to S1 and S2.
- Mechanism review: Candidate A explains spread-spike failures rather than merely swapping methods.
- Decision: advance Candidate A after anti-vacuity and evaluator feedback.
- Next-plan action: open ADJACENT evaluator-construction plan before intervention claims.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: survives

### Blind-spot catalog

{blind_spot_block.strip()}

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: candidate can only advance to an ADJACENT evaluator-construction plan.

### Grounded pruning

- Advance: Candidate A only as evaluator-construction plan.
- Parked: None.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: high information gain but blocked.

### Pre-execution divergence review

- Portfolio breadth: limited.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: build evaluator.

### Promotion decision

- Promoted idea: Candidate A to ADJACENT evaluator-construction plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred.
"""


def run_idea_portfolio_check(plan: str):
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )


def test_check_idea_portfolio_rejects_empty_or_placeholder_blind_spot_fields():
    plan = idea_portfolio_plan_with_blind_spot(
        """
- Candidate A:
  - Blind-spot area:
  - How it could break the mechanism: <failure path>
  - Claim-scope effect: None
  - Required repair: None with reason
"""
    )

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 1
    assert "blind-spot field 'Blind-spot area' is empty" in result.stdout
    assert "blind-spot field 'How it could break the mechanism' is empty" in result.stdout
    assert "blind-spot field 'Claim-scope effect' is empty" in result.stdout
    assert "blind-spot field 'Required repair' is empty" in result.stdout


def test_check_idea_portfolio_rejects_blind_spot_without_scope_or_repair_effect():
    plan = idea_portfolio_plan_with_blind_spot(
        """
- Candidate A:
  - Blind-spot area: market microstructure regime.
  - How it could break the mechanism: spread compression could mean something else.
  - Claim-scope effect: affects interpretation.
  - Required repair: think harder.
"""
    )

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 1
    assert "Claim-scope effect must start with" in result.stdout
    assert "Required repair must start with" in result.stdout


def test_check_idea_portfolio_rejects_negated_or_vague_blind_spot_markers():
    plan = idea_portfolio_plan_with_blind_spot(
        """
- Candidate A:
  - Blind-spot area: market microstructure regime.
  - How it could break the mechanism: spread compression could mean something else.
  - Claim-scope effect: not narrow.
  - Required repair: reference later.
"""
    )

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 1
    assert "Claim-scope effect must start with" in result.stdout
    assert "Required repair must start with" in result.stdout


def test_check_idea_portfolio_accepts_one_space_or_tab_field_indentation():
    plan = idea_portfolio_plan_with_blind_spot(
        """
- Candidate A:
 - Blind-spot area: market microstructure regime.
\t- How it could break the mechanism: spread compression could mean quote cleanup rather than inventory pressure.
 - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
\t- Required repair: narrow_conditions: add venue-regime stratification before broad claims.
"""
    )

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_idea_portfolio_ignores_section_notes_when_parsing_candidates():
    plan = idea_portfolio_plan_with_blind_spot(
        """
- Candidate A:
  - Blind-spot area: market microstructure regime.
  - How it could break the mechanism: spread compression could mean quote cleanup rather than inventory pressure.
  - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
  - Required repair: narrow_conditions: add venue-regime stratification before broad claims.
"""
    ).replace(
        "### Generation operators\n\n- Candidate A:",
        "### Generation operators\n\n- Note: Portfolio intentionally keeps one candidate after pruning.\n- Candidate A:",
    )

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_idea_portfolio_accepts_loose_not_applicable_objective_chosen():
    plan = """# Objective Already Chosen

## Question / Objective

Use the already selected objective.

## Idea portfolio

Not applicable: an objective was already chosen before this plan.

## Prior-work grounding

Grounding starts here.
"""

    result = run_idea_portfolio_check(plan)

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_idea_portfolio_requires_survivors_to_have_blind_spot_records():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Missing Blind Spot Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: survives

### Blind-spot catalog

- Catalog source: assumption audit was run, but no candidate-specific blind-spot record was written.

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: candidate can only advance to an ADJACENT evaluator-construction plan.

### Grounded pruning

- Advance: Candidate A only as evaluator-construction plan.
- Parked: None.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: high information gain but blocked.

### Pre-execution divergence review

- Portfolio breadth: limited.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: build evaluator.

### Promotion decision

- Promoted idea: Candidate A to ADJACENT evaluator-construction plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "missing blind-spot catalog block" in result.stdout


def test_check_idea_portfolio_rejects_unfilled_template_portfolio():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"
    template = read("skills/research/assets/plan/rd_plan_exploratory.md.template")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(template, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "placeholder-only" in result.stdout or "Missing required" in result.stdout


def test_check_idea_portfolio_rejects_inconsistent_candidate_contract():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Inconsistent Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S999
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.
- Candidate B: Try a better filter.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: killed

### Blind-spot catalog

- Candidate A:
  - Blind-spot area: market microstructure regimes could hide venue-specific liquidity-provider constraints.
  - How it could break the mechanism: compression after a spike may reflect quote mechanics rather than rebound inventory pressure.
  - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
  - Required repair: narrow_conditions: add venue-regime stratification or park the general claim.

### Hypothesis synthesis

- Candidate B:
  - Source observation: S1.
  - Mechanism conjecture: better filtering might help.
  - Proposed intervention: use a better filter.
  - Predicted effect: better results.
  - Counter-hypothesis: no effect.
  - Minimal disconfirming test: check results.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: no candidate can advance.

### Grounded pruning

- Advance: Candidate B anyway.
- Parked: None.
- Killed: Candidate A.
- Merged: None.

### Information-gain scoring

- Candidate B: vague.

### Pre-execution divergence review

- Portfolio breadth: weak.
- Parameter sweep laundering: possible.
- Anti-anchor check: not checked.
- Required repair before promotion: none.

### Promotion decision

- Promoted idea: Candidate B to plan.
- Non-promoted ideas: Candidate A killed.

## Prior-work grounding

Grounding deferred.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "undefined substrate id" in result.stdout
    assert "promoted candidate" in result.stdout


def test_check_idea_portfolio_requires_promoted_candidate_to_be_advanced():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Parked Promotion Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: survives

### Blind-spot catalog

- Candidate A:
  - Blind-spot area: market microstructure regimes could hide venue-specific liquidity-provider constraints.
  - How it could break the mechanism: compression after a spike may reflect quote mechanics rather than rebound inventory pressure.
  - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
  - Required repair: narrow_conditions: add venue-regime stratification or park the general claim.

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: no candidate can advance.

### Grounded pruning

- Advance: None.
- Parked: Candidate A until evaluator exists.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: high information gain but blocked.

### Pre-execution divergence review

- Portfolio breadth: limited by evaluator absence.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: build evaluator.

### Promotion decision

- Promoted idea: Candidate A to plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "not advanced" in result.stdout


def test_check_idea_portfolio_rejects_non_exact_survival_verdict():
    script = ROOT / "skills" / "research" / "scripts" / "check_idea_portfolio.py"

    plan = """# Bad Verdict Plan

## Question / Objective

Find a better short-term reversal signal under existing data constraints.

## Idea portfolio

### Idea substrate

- S1: Empirical observation - reversal edge decays after high spread intervals.
- S2: Failure observation - volatility filter removes both noise and useful rebound cases.

### Generation operators

- Candidate A:
  - Substrate ids: S1, S2
  - Operator: invert gating premise
  - Changed premise: spread spikes mark rebound inventory pressure rather than only noise.

### De-anchored candidates

- Candidate A: Gate reversal only after spread compression following a spike.

### Assumption audit

- Reference model challenged: short-term reversal signal treats high spread as pure contamination.
- Assumptions considered: finite liquidity recovery window; spread spike means noise; close-to-close return is enough.
- Load-bearing assumption: spread spike means noise.
- Downstream-check result: not downstream of close-to-close measurement.
- Inversion candidate: Candidate A.

### Anti-vacuity gate

- Candidate A:
  - Substrate ids: S1, S2
  - Changed premise: spread spikes can precede rebound, not just contaminate labels.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Predicted measurable effect: reversal IC improves in post-spike compression windows.
  - Counter-hypothesis: apparent rebound is just lower volatility after filtering.
  - Minimal disconfirming test: compare post-spike compression windows against matched non-spike windows.
  - Verdict: not survives

### Blind-spot catalog

- Candidate A:
  - Blind-spot area: market microstructure regimes could hide venue-specific liquidity-provider constraints.
  - How it could break the mechanism: compression after a spike may reflect quote mechanics rather than rebound inventory pressure.
  - Claim-scope effect: narrowed_claim: narrow claims to tested venues and periods.
  - Required repair: narrow_conditions: add venue-regime stratification or park the general claim.

### Hypothesis synthesis

- Candidate A:
  - Source observation: S1 and S2.
  - Mechanism conjecture: transient inventory pressure relaxes after spread compression.
  - Proposed intervention: condition reversal on spread spike followed by compression.
  - Predicted effect: higher reversal IC in the conditioned slice.
  - Counter-hypothesis: the slice merely lowers volatility.
  - Minimal disconfirming test: matched non-spike window comparison.

### Evaluator feedback

- Status: Skipped: executable evaluator unavailable in current workspace.
- Required evaluator or artifact: walk-forward CLI.
- Effect on promotion: no candidate can advance.

### Grounded pruning

- Advance: Candidate A.
- Parked: None.
- Killed: None.
- Merged: None.

### Information-gain scoring

- Candidate A: high information gain.

### Pre-execution divergence review

- Portfolio breadth: limited.
- Parameter sweep laundering: none.
- Anti-anchor check: not literature-first.
- Required repair before promotion: none.

### Promotion decision

- Promoted idea: Candidate A to plan.
- Non-promoted ideas: none.

## Prior-work grounding

Grounding deferred.
"""

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    assert result.returncode == 1
    assert "verdict must be exactly" in result.stdout


def test_check_report_rejects_reports_without_background_section():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Missing Background Report

## Summary
This report summarizes a complete analysis with enough substance for validation.

## Results
The observed result is described with enough detail to avoid placeholder text.

## Limitations
The report leaves plausible alternatives and untested conditions explicitly open.

## Next action
NEXT_STEP: continue the same plan after the reader reviews this evidence.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "Missing required section: 'Background'" in result.stdout


def test_check_report_rejects_reports_missing_paper_grade_sections():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Thin Report

## Summary
This report summarizes a complete analysis with enough substance for validation.

## Background
The work builds on a prior plan and an existing comparator.

## Methods & Conditions
The method is described in a way that a reader could re-implement.

## Results
The observed result is described with enough detail to avoid placeholder text.

## Limitations
The report leaves plausible alternatives and untested conditions explicitly open.

## Next action
NEXT_STEP: continue the same plan after the reader reviews this evidence.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "Missing required section: 'Related Work'" in result.stdout
    assert "Missing required section: 'Theory / Formulation'" in result.stdout
    assert "Missing required section: 'Ablation / Sensitivity'" in result.stdout
    assert "Missing required section: 'Discussion'" in result.stdout
    assert "Missing required section: 'References'" in result.stdout


def test_check_report_rejects_numeric_results_without_statistical_reporting_minimum():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Underreported Numeric Report

## Summary
This report summarizes the numeric result and the next research action.

## Background
Prior formulations motivate the comparison and define the known constraints.

## Related Work
The report positions the work against the directly relevant comparator.

## Methods & Conditions
The method and material conditions are described for re-implementation.

## Results
The proposed method reached accuracy 0.84 while the baseline reached 0.80.

## Ablation / Sensitivity
Not applicable: no component-causality or robustness claim is made in this report.

## Discussion
The result is interpreted as an association-level comparison, not a causal conclusion.

## Limitations
The report names untested conditions and plausible alternative explanations.

## Next action
NEXT_STEP: continue the same plan with a variance-aware rerun.

## References
- Plan: plans/01_example.md
- Source artifacts: experiments/01_example/runs/
- Prior work: [Comparator 2024] from literature/papers.md.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "numeric Results must report" in result.stdout


def test_check_report_rejects_precision_ci_false_positive_and_sample_size_only():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# False Positive Numeric Report

## Summary
This report summarizes the numeric result and the next research action.

## Background
Prior formulations motivate the comparison and define the known constraints.

## Related Work
The report positions the work against the directly relevant comparator.

## Theory / Formulation
Not applicable: the applied claim does not rest on a derivation.

## Methods & Conditions
The method and material conditions are described for re-implementation.

## Results
| Metric | Value | Source |
|---|---:|---|
| precision | 0.84 | run output |

The sample size was not recorded. n=1.

## Ablation / Sensitivity
Not applicable: no component-causality or robustness claim is made in this report.

## Discussion
The result is interpreted as an association-level comparison, not a causal conclusion.

## Limitations
The report names untested conditions and plausible alternative explanations.

## Next action
NEXT_STEP: continue the same plan with a variance-aware rerun.

## References
- Plan: plans/01_example.md
- Source artifacts: experiments/01_example/runs/
- Prior work: [Comparator 2024] from literature/papers.md.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "numeric Results must report" in result.stdout


def test_check_report_rejects_outcome_without_figure_table_or_reason():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# No Evidence Carrier Report

## Summary
This report summarizes the descriptive result and the next research action.

## Background
Prior formulations motivate the comparison and define the known constraints.

## Related Work
The report positions the work against the directly relevant comparator.

## Theory / Formulation
Not applicable: the applied claim does not rest on a derivation.

## Methods & Conditions
The method and material conditions are described for re-implementation.

## Results
The observed qualitative pattern is described in prose without a table or figure.

## Ablation / Sensitivity
Not applicable: no component-causality or robustness claim is made in this report.

## Discussion
The report explains the descriptive interpretation and avoids causal promotion.

## Limitations
The report names untested conditions and plausible alternative explanations.

## Next action
NEXT_STEP: continue the same plan with a generated figure.

## References
- Plan: plans/01_example.md
- Source artifacts: experiments/01_example/runs/
- Prior work: [Comparator 2024] from literature/papers.md.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "must include a figure, table, or 'No figure/table:' reason" in result.stdout


def test_check_report_rejects_combined_section_headings():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Combined Heading Report

## Summary
This report summarizes the numeric result and the next research action.

## Background
Prior formulations motivate the comparison and define the known constraints.

## Related Work and References
The report tries to satisfy two required sections with one combined heading.

## Theory / Formulation
Not applicable: the applied claim does not rest on a derivation.

## Methods & Conditions
The method and material conditions are described for re-implementation.

## Results
No figure/table: the outcome is a qualitative audit finding without measured values.

## Ablation / Sensitivity
Not applicable: no component-causality or robustness claim is made in this report.

## Discussion
The report explains the descriptive interpretation and avoids causal promotion.

## Limitations
The report names untested conditions and plausible alternative explanations.

## Next action
NEXT_STEP: continue the same plan with separate bibliography entries.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "Missing required section: 'Related Work'" in result.stdout
    assert "Missing required section: 'References'" in result.stdout


def test_check_report_accepts_theoretical_report_shape():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Theoretical Report

## Summary
This report summarizes a derivational result and the next research action.

## Background
Prior formulations motivate the derivation and define the known constraints.

## Related Work
This report positions the derivation against the directly relevant foundations.

## Theory / Formulation
The formulation states the objects, assumptions, and result being derived.

## Derivation context
The derivation route and limiting cases are described for independent review.

## Observations
At k=0, the formulation reduces to the known boundary case without changing the proof state.
No figure/table: theoretical limiting-case observation is summarized in prose; no measured artifact exists yet.

## Ablation / Sensitivity
Not applicable: no component-causality or robustness claim is made in this theoretical report.

## Discussion
The report explains why the limiting cases matter and what interpretation remains association-level or formal-only.

## Limitations
The report names unevaluated assumptions and conditions not covered by the derivation.

## Next action
NEXT_STEP: continue the same plan with a focused counterexample search.

## References
- Plan: plans/01_theoretical.md
- Source artifacts: experiments/01_theoretical/runs/
- Prior work: [Foundation 1948] from literature/papers.md.
"""

    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "report.md"
        report_path.write_text(report, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), str(report_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 0, result.stdout + result.stderr


def test_new_project_next_steps_use_formal_categories_and_theoretical_mode():
    script = ROOT / "skills" / "research" / "scripts" / "new_project.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        result = subprocess.run(
            [sys.executable, str(script), str(target), "--name", "Next Step Contract"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

    assert "--category <basic_research|applied_research|experimental_development>" in result.stdout
    assert "--mode <exploratory|confirmatory|milestone|theoretical>" in result.stdout
    assert "--category <basic|applied|experimental_development>" not in result.stdout
