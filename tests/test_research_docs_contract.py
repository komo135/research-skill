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


def markdown_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    assert start is not None, f"missing section: {heading}"

    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(rf"^#{{1,{level}}}\s+\S", lines[index]):
            end = index
            break
    return "\n".join(lines[start:end])


def first_subheading(section: str) -> str:
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped
    return ""


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
            "## References",
        )
        assert_absent(text, "## Next action", "## Next hypothesis", "## Next hypotheses")
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


def test_research_skill_routes_research_idea_generation_to_mechanistic_reference():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_mentions(
        skill,
        "research idea",
        "hypothesis candidate",
        "what should we try next",
        "references/mechanistic_hypothesis_generation.md",
        "Research situation diagnosis",
        "Analysis lenses considered",
        "Mechanism hypothesis record",
        "before Prior-work grounding",
    )
    assert_ordered_fragments(
        rd_plan,
        "Hypothesis generation",
        "Prior-work grounding",
        "Divergence checkpoint",
        "## Plan",
    )


def test_mechanistic_generation_starts_with_research_situation_diagnosis():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Research situation diagnosis",
        "Available material",
        "Missing material",
        "Why hypothesis generation is allowed or blocked",
        "Analysis lenses considered",
        "Adopted analysis lenses",
        "Mechanistic analysis",
        "Mechanism hypothesis record",
    )
    assert_mentions(
        reference,
        "do not start from candidate ideas",
        "do not create a candidate portfolio",
        "successes",
        "failures or limits",
        "evaluation or measurement",
        "counterfactuals",
    )
    assert_absent(reference, "Idea portfolio")


def test_hypothesis_generation_separates_performance_from_mechanism_contract():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")
    skill = read("skills/research/SKILL.md")
    plan_review = read("skills/research-plan-review/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        reference,
        "beating a baseline/SOTA or improving a metric",
        "choose `predictive / performance`",
        "do not add a Mechanism hypothesis record to a predictive / performance plan",
        '"A improves metric B over baseline C," choose `predictive / performance`, not `mechanistic`',
        "Do not make why-it-worked decomposition the main plan unless",
    )
    assert_mentions(
        skill,
        "Do not collapse all hypotheses into mechanism hypotheses",
        "Predictive / performance hypothesis",
        "Do not force predictive, causal, descriptive, or performance hypotheses into a Mechanism hypothesis record",
    )
    assert_mentions(
        plan_review,
        'if the intended claim is only "A improves metric B over baseline C," the type is predictive / performance',
        "The review must not turn a predictive / performance hypothesis into a mechanism study",
    )
    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_mentions(
            text,
            "Type-specific hypothesis record",
            "Mechanism claim included",
            "Omitted: hypothesis type is <type>; no Mechanism hypothesis record",
            "Prediction / expected observation",
            "Primary evidence route",
            "Fair comparator or baseline",
            "Support threshold",
            "Rejection / park condition",
        )


def test_mechanistic_generation_compares_lenses_before_adopting_one():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Analysis lenses considered",
        "What it inspects",
        "What it may miss",
        "Use decision",
        "Adopted analysis lenses",
        "Primary lens",
        "Auxiliary lenses",
    )
    assert_mentions(
        reference,
        "Success mechanism lens",
        "Failure dynamics lens",
        "Lineage-difference lens",
        "Center-auxiliary inversion lens",
        "Problem-form transformation lens",
        "Measurement and evaluation lens",
        "Constraint relocation lens",
        "Sparse-information lens",
        "Cross-domain mechanism transfer lens",
    )


def test_mechanistic_generation_turns_analysis_into_discriminating_records():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Observation",
        "Mechanistic analysis",
        "Mechanism hypothesis",
        "Competing hypothesis",
        "Discriminating prediction",
        "Minimal test",
    )
    assert_mentions(
        reference,
        "intervention fragment",
        "Transformer",
        "evaluation metric",
        "not a mechanism hypothesis",
        "same observation",
        "different outcome",
    )


def test_mechanistic_generation_retrieval_skip_does_not_waive_plan_scoped_survey():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        reference,
        "does not satisfy or waive the plan-scoped literature survey",
        "Survey evidence",
    )

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_mentions(
            text,
            "does not replace Survey evidence",
        )


def test_mechanistic_generation_commit_waits_for_survey_evidence_despite_template_order():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        reference,
        "Do not finalize commit before Survey evidence exists",
    )
    assert_mentions(
        rd_plan,
        "section order is not permission to finalize commit before Survey evidence",
    )

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_mentions(
            text,
            "not final until Survey evidence exists",
            "section order is not permission",
        )


def test_mechanistic_generation_blocks_sparse_information_hypothesis_fabrication():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Sparse-information lens",
        "park hypothesis generation",
        "observable quantities",
        "invariants",
        "symmetries",
        "limits",
        "minimal model",
        "comparators or counterfactuals",
    )
    assert_mentions(
        reference,
        "quantum",
        "do not fill missing evidence with fashionable terms",
        "what observation would narrow the hypothesis space",
    )


def test_mechanistic_generation_defines_evaluator_grounded_refinement():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Evaluator-grounded refinement",
        "failed hypothesis",
        "hypothesis type",
        "new observation",
        "what explanation, prediction, comparator, threshold, or mechanism was ruled out",
        "which alternatives remain live",
        "revised typed hypothesis-generation record",
        "Decision",
    )
    assert_mentions(
        reference,
        "do not return to a new list of ideas",
        "commit / park / kill",
    )


def test_mechanistic_generation_uses_success_papers_as_design_samples_not_runtime_work():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Using successful papers",
        "Architecture-shift samples",
        "Objective or pretraining-shift samples",
        "Measurement and evaluation-shift samples",
        "Constraint-breaking or systematization samples",
        "Theory and sparse-domain samples",
        "Cross-domain transfer samples",
    )
    assert_mentions(
        reference,
        "do not make a paper table mandatory at runtime",
        "extract analysis operations",
        "do not collapse them into one universal principle",
    )


def test_research_skill_orders_lifecycle_from_observation_to_decision():
    skill = read("skills/research/SKILL.md")

    assert_ordered_fragments(
        skill,
        "Research lifecycle",
        "Research situation diagnosis",
        "Mechanistic analysis",
        "Mechanism hypothesis record",
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
        "grounding after hypothesis-generation records exist",
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


def test_plan_schema_and_templates_require_plan_visuals():
    rd_plan = read("skills/research/references/rd_plan.md")
    skill = read("skills/research/SKILL.md")
    plan_review = read("skills/research-plan-review/SKILL.md")
    readme = read("README.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_mentions(
        rd_plan,
        "### Plan visual",
        "Mermaid",
        "PlantUML",
        "ASCII",
        "architecture",
        "data flow",
        "evaluation flow",
        "mechanism diagram",
        "No diagram:",
    )
    assert_mentions(
        skill,
        "Every Plan section starts with `### Plan visual`",
        "Mermaid",
        "PlantUML",
        "ASCII",
        "No diagram:",
    )
    assert_mentions(
        plan_review,
        "Check the Plan visual",
        "Plan must start with `### Plan visual`",
        "No diagram:",
    )
    assert_mentions(
        readme,
        "Plan visual",
        "architecture, data/evaluation flow",
    )

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Plan",
            "### Plan visual",
            "Visual format",
            "What it shows",
            "Reader check",
        )
        assert_mentions(
            text,
            "Mermaid",
            "PlantUML",
            "ASCII",
            "No diagram:",
        )
        assert first_subheading(markdown_section(text, "## Plan")) == "### Plan visual"
        assert_mentions(
            markdown_section(text, "## Plan review"),
            "Plan visual",
        )


def test_plan_schema_records_mechanistic_hypothesis_generation_contract():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "## Hypothesis generation",
        "### Research situation diagnosis",
        "Available material",
        "Missing material",
        "Why hypothesis generation is allowed or blocked",
        "### Analysis lenses considered",
        "Lens",
        "What it would inspect",
        "What it may miss",
        "Use decision",
        "### Mechanistic analysis",
        "Observation",
        "Mechanistic interpretation",
        "### Mechanism hypothesis record",
        "Hypothesis",
        "Competing hypothesis",
        "Discriminating prediction",
        "Minimal test",
        "Decision",
    )


def test_plan_schema_and_templates_record_lens_and_decision_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "## Hypothesis generation",
            "### Research situation diagnosis",
            "### Analysis lenses considered",
            "### Mechanistic analysis",
            "### Mechanism hypothesis record",
            "Hypothesis",
            "Competing hypothesis",
            "Discriminating prediction",
            "Minimal test",
            "Decision",
        )
        assert_mentions(
            text,
            "commit / park / kill",
            "required when the plan began from research ideas",
            "does not replace Survey evidence",
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


def test_mechanistic_generation_rejects_candidate_listing_and_method_names_as_hypotheses():
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        reference,
        "Candidate-list pressure",
        "time pressure",
        "method-name pressure",
        "paper-name pressure",
        "analogy pressure",
        "return to diagnosis",
    )
    assert_mentions(
        reference,
        "10 ideas",
        "attention",
        "ResNet",
        "annealing",
        "intervention fragment",
    )


def test_plan_templates_include_mechanism_record_before_prior_work_grounding():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Question / Objective",
            "## Hypothesis generation",
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
            "references/mechanistic_hypothesis_generation.md",
            "Research situation diagnosis",
            "Analysis lenses considered",
            "commit / park / kill",
        )


def test_new_plan_guidance_mentions_mechanism_record_before_prior_work_grounding():
    new_plan = read("skills/research/scripts/new_plan.py")

    assert_ordered_fragments(
        new_plan,
        "Question / Objective",
        "Mechanism hypothesis record",
        "Prior-work grounding",
        "Divergence checkpoint",
        "Plan",
        "time-anchor",
    )


def test_mechanism_record_is_not_a_pre_execution_divergence_review():
    rd_plan = read("skills/research/references/rd_plan.md")
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        rd_plan,
        "## Hypothesis generation",
        "### Mechanism hypothesis record",
        "Decision",
        "## Prior-work grounding",
        "## Divergence checkpoint",
    )
    assert_mentions(
        reference,
        "not a Plan",
        "not a claim",
        "not a substitute for the Divergence checkpoint",
    )


def test_readme_documents_hypothesis_generation_before_prior_work_grounding():
    readme = read("README.md")

    assert_ordered_fragments(
        readme,
        "Question / Objective",
        "Hypothesis generation and typed records",
        "hypothesis type",
        "Mechanism hypothesis record",
        "prior-work grounding",
    )
    assert_mentions(
        readme,
        "research ideas",
        "hypothesis candidates",
        "what should we try next",
        "research situation diagnosis",
        "predictive / performance",
        "Mechanistic hypotheses are narrower",
        "commit / park / kill",
        "mechanistic_hypothesis_generation.md",
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


def test_plan_review_blocks_wrong_premises_and_invalid_validation_methods():
    plan_review = read("skills/research-plan-review/SKILL.md")
    readme = read("README.md")

    for text in [plan_review, readme]:
        assert_mentions(
            text,
            "wrong",
            "unsupported",
            "unverified premise",
            "hypothesis validation method",
            "block_execution",
        )

    assert_mentions(
        plan_review,
        "mechanically runnable",
        "discredited proxy",
        "contradicted project state",
        "Stop decision",
    )
    assert_ordered_fragments(
        plan_review,
        "Review purpose",
        "Premise check",
        "Hypothesis validation method",
        "block_execution",
    )


def test_plan_review_templates_center_premise_and_validation_method():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "### Research-design checks",
            "Premise check",
            "Hypothesis validation method",
            "Prior-work survey evidence",
            "Stop decision",
            "### Required repairs before execution",
        )
        assert_mentions(
            text,
            "wrong / unsupported / unverified premise",
            "distinguish it from plausible alternatives",
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
    assert "### Plan visual" in plan
    assert first_subheading(markdown_section(plan, "## Plan")) == "### Plan visual"
    assert "### Derivation question" in plan
    assert "### Limiting-case checks" in plan
    assert "### Empirical sanity check" in plan


def test_research_scripts_must_persist_durable_artifacts_not_only_print():
    skill = read("skills/research/SKILL.md")
    analysis = read("skills/research/references/analysis.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    mechanism_generation = read("skills/research/references/mechanistic_hypothesis_generation.md")
    project_readme = read("skills/research/assets/project/README.md.template")

    for text in [skill, analysis, rd_plan, mechanism_generation, project_readme]:
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


def test_mechanism_record_schema_and_templates_include_assumptions_and_required_evidence():
    rd_plan = read("skills/research/references/rd_plan.md")
    assumption_audit = read("skills/research/references/assumption_audit.md")
    mechanism_generation = read("skills/research/references/mechanistic_hypothesis_generation.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    assert_ordered_fragments(
        rd_plan,
        "## Hypothesis generation",
        "### Mechanistic analysis",
        "Assumptions exposed",
        "What would be different if this interpretation is true",
        "### Mechanism hypothesis record",
        "Required evidence",
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
        mechanism_generation,
        "Assumptions exposed",
        "Required evidence",
        "commit / park / kill",
    )
    assert_absent(assumption_audit, "List 3-5", "3〜5", "Unknown-unknowns catalog")

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert_ordered_fragments(
            text,
            "## Hypothesis generation",
            "### Mechanistic analysis",
            "Assumptions exposed",
            "What would be different if this interpretation is true",
            "### Mechanism hypothesis record",
            "Required evidence",
            "## Prior-work grounding",
        )
        assert_mentions(
            text,
            "Hypothesis",
            "Competing hypothesis",
            "Discriminating prediction",
            "Minimal test",
            "Reason",
        )


def test_mechanism_record_schema_and_templates_include_lens_selection_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "## Hypothesis generation",
            "### Research situation diagnosis",
            "### Analysis lenses considered",
            "What it would inspect",
            "What it may miss",
            "Use decision",
            "### Adopted analysis lenses",
            "Primary lens",
            "Auxiliary lenses",
        )
        assert_mentions(
            text,
            "hypothesis generation is blocked",
            "available material",
            "missing material",
            "commit / park / kill",
        )


def complete_mechanism_record(decision: str = "park", blocked: bool = False) -> str:
    block_reason = (
        "blocked until a matched-market-regime comparison and evaluator exist"
        if blocked
        else "allowed because observed failures, baseline behavior, evaluation target, and comparator path are available"
    )
    return f"""# Mechanism Record Plan

## Question / Objective

Find why a time-series model fails in high-spread market regimes.

## Mechanism hypothesis record

### Research situation diagnosis

- Available material: failure logs by spread regime, a simple reversal baseline, standard average-return metric, and candidate matched windows.
- Missing material: matched non-spike windows and a durable evaluator artifact.
- Why hypothesis generation is allowed or blocked: {block_reason}.

### Analysis lenses considered

- Lens: Failure dynamics lens
  - What it would inspect: where information flow or state persistence breaks in high-spread windows.
  - What it may miss: whether the average-return evaluator is hiding tail losses.
  - Use decision: use as primary because the observed collapse is condition-specific.
- Lens: Measurement and evaluation lens
  - What it would inspect: whether average return hides tail failures.
  - What it may miss: the internal state mechanism that causes the collapse.
  - Use decision: use as auxiliary because evaluation mismatch is a plausible competing explanation.

### Adopted analysis lenses

- Primary lens: Failure dynamics lens.
- Auxiliary lenses: Measurement and evaluation lens.
- Reason: the main discriminator is whether high-spread windows break state information or merely expose a hidden evaluation target.

### Mechanistic analysis

- Observation: the model wins on average but loses sharply after spread spikes.
- Analysis lens used: Failure dynamics lens with Measurement and evaluation lens as auxiliary.
- Mechanistic interpretation: hidden state updates treat spread spikes as noise, suppressing rebound information exactly when inventory pressure may be resolving.
- Assumptions exposed: spread spikes can encode temporary inventory pressure; matched non-spike windows can separate volatility from inventory effects.
- What would be different if this interpretation is true: post-spike compression windows should show rebound information that matched low-volatility windows do not.

### Mechanism hypothesis record

- Hypothesis: post-spike spread compression carries rebound information that the current model suppresses as noise.
- Competing hypothesis: apparent gains come only from lower realized volatility after filtering, not from inventory-pressure relaxation.
- Discriminating prediction: a matched post-spike compression slice improves reversal IC while a volatility-matched non-spike slice does not.
- Minimal test: compare post-spike compression windows against volatility-matched non-spike windows with the same horizon and transaction-cost assumptions.
- Required evidence: run artifact with slice-level IC, dispersion, sample count, and matching criteria.
- Decision: {decision}
- Reason: evaluator and matched-comparison evidence must exist before execution claims advance.

## Prior-work grounding

Grounding starts here.
"""


def complete_predictive_hypothesis_record() -> str:
    return """# Predictive Plan

## Question / Objective

Test whether method A improves metric B over baseline C.

## Hypothesis generation

### Research situation diagnosis

- Available material: baseline score, metric definition, data split, prior failure logs, and candidate method description.
- Missing material: internal mechanism observations.
- Why hypothesis generation is allowed or blocked: allowed because material supports an observable prediction.
- Hypothesis type: predictive / performance

### Type-specific hypothesis record

- Hypothesis type: predictive / performance
- Situation-grounding: baseline C underperforms on split X and method A changes the input representation.
- Hypothesis statement: method A improves metric B over baseline C on benchmark X.
- Prediction / expected observation: method A exceeds baseline C by at least two points on metric B.
- Primary evidence route: benchmark X evaluation with the same split and metric.
- Fair comparator or baseline: baseline C using the same split, metric, tuning budget, and data preprocessing.
- Support threshold: metric B improves by at least two points over baseline C.
- Rejection / park condition: improvement is below threshold or split/evaluator is invalid.
- Mechanism claim included: no

### Analysis lenses considered

Omitted: hypothesis type is predictive / performance; analysis lenses are not required because no mechanism claim is being made.

### Adopted analysis lenses

Omitted: hypothesis type is predictive / performance; no mechanism lenses adopted.

### Mechanistic analysis

Omitted: hypothesis type is predictive / performance; no mechanism explanation is being tested.

### Mechanism hypothesis record

Omitted: hypothesis type is predictive / performance; no Mechanism hypothesis record.

## Prior-work grounding

Grounding starts here.
"""


def run_mechanism_record_check(plan: str):
    script = ROOT / "skills" / "research" / "scripts" / "check_mechanism_hypothesis_record.py"

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.md"
        path.write_text(plan, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(script), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )


def test_check_mechanism_hypothesis_record_rejects_candidate_list_without_record():
    plan = """# Vacuous Mechanism Plan

## Question / Objective

Find a better short-term reversal signal.

## Mechanism hypothesis record

- Candidate A: Try a better filter.
- Candidate B: Use attention.

## Prior-work grounding

Placeholder.
"""

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "Missing required Mechanism hypothesis record subsection" in result.stdout


def test_check_mechanism_hypothesis_record_accepts_complete_record():
    result = run_mechanism_record_check(complete_mechanism_record())

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Mechanism hypothesis record passes contract checks." in result.stdout


def test_check_mechanism_hypothesis_record_requires_discriminating_fields():
    plan = complete_mechanism_record().replace(
        "- Competing hypothesis: apparent gains come only from lower realized volatility after filtering, not from inventory-pressure relaxation.\n"
        "- Discriminating prediction: a matched post-spike compression slice improves reversal IC while a volatility-matched non-spike slice does not.\n"
        "- Minimal test: compare post-spike compression windows against volatility-matched non-spike windows with the same horizon and transaction-cost assumptions.\n",
        "",
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "missing required field: 'Competing hypothesis'" in result.stdout
    assert "missing required field: 'Discriminating prediction'" in result.stdout
    assert "missing required field: 'Minimal test'" in result.stdout


def test_check_mechanism_hypothesis_record_rejects_candidate_preamble_before_diagnosis():
    plan = complete_mechanism_record().replace(
        "## Mechanism hypothesis record\n\n### Research situation diagnosis",
        "## Mechanism hypothesis record\n\n- Candidate A: Try a better filter.\n- Candidate B: Use attention.\n\n### Research situation diagnosis",
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "must start with '### Research situation diagnosis'" in result.stdout
    assert "candidate-list preamble" in result.stdout


def test_check_mechanism_hypothesis_record_requires_multiple_lenses_considered():
    plan = complete_mechanism_record().replace(
        "- Lens: Measurement and evaluation lens\n"
        "  - What it would inspect: whether average return hides tail failures.\n"
        "  - What it may miss: the internal state mechanism that causes the collapse.\n"
        "  - Use decision: use as auxiliary because evaluation mismatch is a plausible competing explanation.\n",
        "",
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "Analysis lenses considered must include at least two Lens entries" in result.stdout


def test_check_mechanism_hypothesis_record_rejects_multiple_primary_or_too_many_auxiliary_lenses():
    plan = (
        complete_mechanism_record()
        .replace(
            "- Primary lens: Failure dynamics lens.",
            "- Primary lens: Failure dynamics lens; Measurement and evaluation lens.",
        )
        .replace(
            "- Auxiliary lenses: Measurement and evaluation lens.",
            "- Auxiliary lenses: Measurement and evaluation lens; Success mechanism lens; Constraint relocation lens.",
        )
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "Primary lens must name exactly one lens" in result.stdout
    assert "Auxiliary lenses must name 0-2 lenses" in result.stdout


def test_check_mechanism_hypothesis_record_rejects_and_joined_adopted_lens_lists():
    plan = (
        complete_mechanism_record()
        .replace(
            "- Primary lens: Failure dynamics lens.",
            "- Primary lens: Failure dynamics lens and Measurement and evaluation lens.",
        )
        .replace(
            "- Auxiliary lenses: Measurement and evaluation lens.",
            "- Auxiliary lenses: Measurement and evaluation lens and Success mechanism lens and Constraint relocation lens.",
        )
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "Primary lens must name exactly one lens" in result.stdout
    assert "Auxiliary lenses must name 0-2 lenses" in result.stdout


def test_check_mechanism_hypothesis_record_requires_fields_for_each_considered_lens():
    plan = complete_mechanism_record().replace(
        "- Lens: Measurement and evaluation lens\n"
        "  - What it would inspect: whether average return hides tail failures.\n"
        "  - What it may miss: the internal state mechanism that causes the collapse.\n"
        "  - Use decision: use as auxiliary because evaluation mismatch is a plausible competing explanation.\n",
        "- Lens: Measurement and evaluation lens\n",
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 1
    assert "Lens entry 2 missing required field: 'What it would inspect'" in result.stdout
    assert "Lens entry 2 missing required field: 'What it may miss'" in result.stdout
    assert "Lens entry 2 missing required field: 'Use decision'" in result.stdout


def test_check_mechanism_hypothesis_record_rejects_invalid_decision():
    result = run_mechanism_record_check(complete_mechanism_record(decision="advance"))

    assert result.returncode == 1
    assert "Decision must be exactly one of: commit, park, kill" in result.stdout


def test_check_mechanism_hypothesis_record_blocks_commit_when_generation_is_blocked():
    result = run_mechanism_record_check(complete_mechanism_record(decision="commit", blocked=True))

    assert result.returncode == 1
    assert "blocked diagnosis cannot commit" in result.stdout


def test_check_mechanism_hypothesis_record_allows_commit_when_diagnosis_says_not_blocked():
    plan = complete_mechanism_record(decision="commit").replace(
        "Why hypothesis generation is allowed or blocked: allowed because observed failures, baseline behavior, evaluation target, and comparator path are available.",
        "Why hypothesis generation is allowed or blocked: not blocked; material supports an observable prediction.",
    )

    result = run_mechanism_record_check(plan)

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_mechanism_hypothesis_record_accepts_not_applicable_objective_chosen():
    plan = """# Objective Already Chosen

## Question / Objective

Use the already selected objective.

## Mechanism hypothesis record

Not applicable: an objective was already chosen before this plan.

## Prior-work grounding

Grounding starts here.
"""

    result = run_mechanism_record_check(plan)

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_mechanism_hypothesis_record_accepts_non_mechanistic_typed_record():
    result = run_mechanism_record_check(complete_predictive_hypothesis_record())

    assert result.returncode == 0, result.stdout + result.stderr


def test_check_mechanism_hypothesis_record_rejects_unfilled_template_record():
    template = read("skills/research/assets/plan/rd_plan_exploratory.md.template")
    result = run_mechanism_record_check(template)

    assert result.returncode == 1
    assert "placeholder-only" in result.stdout or "Missing required" in result.stdout


def test_check_report_rejects_reports_without_background_section():
    script = ROOT / "skills" / "research" / "scripts" / "check_report.py"

    report = """# Missing Background Report

## Summary
This report summarizes a complete analysis with enough substance for validation.

## Results
The observed result is described with enough detail to avoid placeholder text.

## Limitations
The report leaves plausible alternatives and untested conditions explicitly open.
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
This report summarizes the numeric result.

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
This report summarizes the numeric result.

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
This report summarizes the descriptive result.

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
This report summarizes the numeric result.

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
This report summarizes a derivational result.

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
