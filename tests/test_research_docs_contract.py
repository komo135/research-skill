import json
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


def fill_analysis(
    project: Path,
    proposition: str,
    *,
    analysis_id: str = "A001",
    status: str = "supported",
    material_used: str = "O001 and proposition.md expected consequence.",
    derived_hypothesis: str = "The derived hypothesis is testable from this analysis.",
) -> None:
    prop_dir = project / "propositions" / proposition
    (prop_dir / "observations.md").write_text(
        f"""# Observations for {proposition}

## O001: Observed contrast

- Material: concrete observation from the current project.
- Measurement or evidence form: recorded comparison.
- Comparator or expected reference: expected consequence from proposition.md.
- Missing material: None for this analysis.
""",
        encoding="utf-8",
    )
    (prop_dir / "analyses.md").write_text(
        f"""# Analyses for {proposition}

## {analysis_id}: Concrete source analysis

- Analysis question: Why does the observed contrast matter?
- Material used: {material_used}
- Contrast type: expectation-break
- Contrast: expected consequence versus observed material.
- Generated doubt: whether the current representation realizes the proposition's required condition.
- Working proposition: if the required condition is realized, the expected consequence should appear.
- Expected consequence if the working proposition is true: the planned discriminator should show the expected observation.
- Observed match, break, or missing condition: observed material indicates the condition is testable.
- Proposition status assessment: {status}
- Derived hypothesis candidate: {derived_hypothesis}
- What evidence would update this analysis: a discriminator that separates this hypothesis from a competing explanation.
""",
        encoding="utf-8",
    )


def current_status_value(text: str) -> str:
    section = markdown_section(text, "## Current status")
    for line in section.splitlines():
        stripped = line.strip()
        if stripped:
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
        "## Trace contract",
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
        "research",
        "hypothesis candidate",
        "Situation question",
        "Generated doubt",
        "Working proposition",
        "Expected consequence",
        "Proposition status",
        "Derived hypothesis",
    )
    assert_ordered_fragments(
        rd_plan,
        "Proposition and hypothesis trace",
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
        "Do not require every derived hypothesis to be mechanistic",
        "Hypothesis type",
        "predictive / performance",
    )
    assert_mentions(
        plan_review,
        'if the intended claim is only "A improves metric B over baseline C," the type is predictive / performance',
        "The review must not turn a predictive / performance hypothesis into a mechanism study",
    )
    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_mentions(
            text,
            "Hypothesis type",
            "Prediction / expected observation",
            "Competing hypothesis",
            "Minimal discriminator",
            "Decision threshold",
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
        "Core lifecycle",
        "Situation question",
        "Generated doubt",
        "Working proposition",
        "Expected consequence",
        "Proposition status",
        "Derived hypothesis",
        "Hypothesis plan",
        "Execution",
        "Result analysis",
        "hypothesis status update",
        "proposition status update",
    )
    assert_mentions(
        skill,
        "Do not generate hypotheses directly from a vague topic",
        "material absence",
        "no proposition or hypothesis",
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
        "<propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md>",
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
        "## Trace contract",
        "Source observations",
        "Generated doubt",
        "Working proposition",
        "Expected consequence",
        "Proposition status",
        "Derived hypothesis",
        "Hypothesis type",
    )


def test_plan_schema_and_templates_record_lens_and_decision_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "Proposition status",
            "Derived hypothesis",
            "Hypothesis type",
            "Competing hypothesis",
            "Minimal discriminator",
        )
        assert_mentions(
            text,
            "tested-supported",
            "tested-contradicted",
            "tested-partial",
            "tested-inconclusive",
        )


def test_iteration_loop_defines_approach_transition_criteria():
    iteration_loop = read("skills/research/references/iteration_loop.md")

    assert_ordered_fragments(
        iteration_loop,
        "Proposition-First Result Feedback",
        "Update `hypothesis.md` status",
        "Append a hypothesis decision",
        "Update parent `proposition.md`",
        "Append a proposition decision",
    )
    assert_mentions(
        iteration_loop,
        "tested-supported",
        "tested-contradicted",
        "tested-partial",
        "tested-inconclusive",
        "unrealized-condition",
        "split-needed",
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
            "## Proposition and hypothesis trace",
            "## Prior-work grounding",
            "## Divergence checkpoint",
            "## Plan",
        )
        assert_mentions(
            text,
            "Generated doubt",
            "Working proposition",
            "Expected consequence",
            "Proposition status",
            "Derived hypothesis",
        )


def test_new_hypothesis_guidance_mentions_trace_before_prior_work_grounding():
    new_hypothesis = read("skills/research/scripts/new_hypothesis.py")

    assert_ordered_fragments(
        new_hypothesis,
        "proposition",
        "hypothesis.md",
        "plan.md",
        "research-plan-review",
    )


def test_mechanism_record_is_not_a_pre_execution_divergence_review():
    rd_plan = read("skills/research/references/rd_plan.md")
    reference = read("skills/research/references/mechanistic_hypothesis_generation.md")

    assert_ordered_fragments(
        rd_plan,
        "## Trace contract",
        "Generated doubt",
        "Working proposition",
        "Proposition status",
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
        "Proposition-first lifecycle",
        "Generated doubt",
        "Working proposition",
        "Proposition status",
        "Derived hypothesis",
        "prior-work grounding",
    )
    assert_mentions(
        readme,
        "hypothesis candidates",
        "predictive / performance",
        "unrealized-condition",
        "tested-supported",
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


def test_research_skill_and_hypothesis_plan_guidance_require_literature_survey_before_plan():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    readme = read("README.md")

    for text in [skill, rd_plan, readme]:
        assert_mentions(
            text,
            "Prior-work grounding",
            "Plan",
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
        "contradicted proposition state",
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
        assert_mentions(
            text,
            "Plan review",
            "Premise",
            "Hypothesis",
            "Prior-work",
        )


def test_plan_review_templates_include_prior_work_survey_check():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_mentions(text, "Survey evidence", "Citation-use map", "Prior-work grounding")


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


def test_hypothesis_plan_guidance_includes_prior_work_grounding_before_execution():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_mentions(rd_plan, "Prior-work grounding")
    assert_ordered_fragments(
        rd_plan,
        "Trace contract",
        "Prior-work grounding",
        "Divergence checkpoint",
        "Plan",
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


def test_new_project_creates_proposition_first_layout_and_next_steps():
    script = ROOT / "skills" / "research" / "scripts" / "new_project.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        result = subprocess.run(
            [sys.executable, str(script), str(target), "--name", "Proposition First"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        readme = (target / "README.md").read_text(encoding="utf-8")
        project_state = (target / "project_state.md").read_text(encoding="utf-8")
        decisions = (target / "decisions.md").read_text(encoding="utf-8")
        propositions_exists = (target / "propositions").exists()

    assert propositions_exists
    assert_mentions(result.stdout, "new_proposition.py")
    assert_absent(result.stdout, "new_plan.py")
    assert_mentions(readme, "proposition-first", "propositions/", "hypotheses/H")
    assert_mentions(project_state, "Active propositions", "Live derived hypotheses")
    assert_mentions(decisions, "Project-wide", "OPEN_PROPOSITION")


def test_new_proposition_creates_state_ledgers_and_project_decision():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Proposition Script"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "identity-reachability",
                "--title",
                "Identity Reachability",
                "--proposition",
                "Deep plain networks fail because identity-neighborhood solutions are hard to optimize.",
                "--expected",
                "A representation exposing identity should reduce degradation.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        assert result.returncode == 0, result.stderr

        prop_dir = target / "propositions" / "P001_identity-reachability"
        created_paths = {
            relative: (prop_dir / relative).exists()
            for relative in ["proposition.md", "observations.md", "analyses.md", "decisions.md", "hypotheses"]
        }
        proposition = (prop_dir / "proposition.md").read_text(encoding="utf-8")
        observations = (prop_dir / "observations.md").read_text(encoding="utf-8")
        analyses = (prop_dir / "analyses.md").read_text(encoding="utf-8")
        project_decisions = (target / "decisions.md").read_text(encoding="utf-8")

    for relative, exists in created_paths.items():
        assert exists, relative
    assert current_status_value(proposition) == "open"
    assert_mentions(
        proposition,
        "## Current status",
        "unrealized-condition",
        "split-needed",
        "Live working propositions",
        "Live derived hypotheses",
    )
    assert_mentions(
        observations,
        "Measurement or evidence form",
        "Comparator or expected reference",
        "Missing material",
    )
    assert_mentions(
        analyses,
        "Generated doubt",
        "Working proposition",
        "Proposition status assessment",
        "Derived hypothesis candidate",
        "expectation-break",
        "analogy-transfer",
        "representation-change",
    )
    assert_mentions(project_decisions, "OPEN_PROPOSITION", "P001_identity-reachability")


def test_new_hypothesis_creates_hypothesis_plan_under_parent_proposition():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Hypothesis Script"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        create_prop = subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "identity-reachability",
                "--title",
                "Identity Reachability",
                "--proposition",
                "Deep plain networks fail because identity-neighborhood solutions are hard to optimize.",
                "--expected",
                "A representation exposing identity should reduce degradation.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        assert create_prop.returncode == 0, create_prop.stderr
        fill_analysis(
            target,
            "P001_identity-reachability",
            status="unrealized-condition",
            derived_hypothesis="Residual parameterization makes the identity-neighborhood easier to optimize.",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_hypothesis),
                str(target),
                "--proposition",
                "P001_identity-reachability",
                "--id",
                "H001",
                "--slug",
                "residual-parameterization",
                "--title",
                "Residual Parameterization",
                "--category",
                "applied_research",
                "--mode",
                "confirmatory",
                "--hypothesis",
                "Residual parameterization makes the identity-neighborhood easier to optimize.",
                "--source-analysis",
                "A001",
                "--status",
                "unrealized-condition",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        hyp_dir = target / "propositions" / "P001_identity-reachability" / "hypotheses" / "H001_residual-parameterization"
        created_paths = {
            relative: (hyp_dir / relative).exists()
            for relative in ["hypothesis.md", "plan.md", "experiments", "reports", "decisions.md"]
        }
        hypothesis = (hyp_dir / "hypothesis.md").read_text(encoding="utf-8")
        plan = (hyp_dir / "plan.md").read_text(encoding="utf-8")

    assert result.returncode == 0, result.stderr
    for relative, exists in created_paths.items():
        assert exists, relative
    assert current_status_value(hypothesis) == "candidate"
    assert markdown_section(hypothesis, "## Type").strip() == "predictive / performance"
    assert_mentions(
        hypothesis,
        "Parent proposition",
        "Source analysis",
        "Proposition status that produced this hypothesis",
        "Minimal discriminator",
        "tested-supported",
        "tested-contradicted",
        "tested-partial",
        "tested-inconclusive",
    )
    assert_mentions(
        plan,
        "parent_proposition: P001",
        "source_analysis: A001",
        "hypothesis_id: H001",
        "## Proposition and hypothesis trace",
        "Generated doubt",
        "Working proposition",
        "Proposition status",
        "## Prior-work grounding",
        "### Plan visual",
    )
    assert_absent(plan, "<copy the generated doubt", "<copy the working proposition", "<observable result expected")


def test_new_hypothesis_rejects_placeholder_source_analysis_before_material_exists():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "No Material"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "no-material",
                "--title",
                "No Material",
                "--proposition",
                "A proposition cannot produce a hypothesis without material.",
                "--expected",
                "A concrete analysis must exist before planning.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_hypothesis),
                str(target),
                "--proposition",
                "P001_no-material",
                "--id",
                "H001",
                "--slug",
                "premature",
                "--title",
                "Premature",
                "--category",
                "applied_research",
                "--mode",
                "confirmatory",
                "--hypothesis",
                "This should be rejected.",
                "--source-analysis",
                "A001",
                "--status",
                "supported",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "source analysis is still placeholder-only" in result.stderr


def test_new_hypothesis_rejects_none_material_or_none_hypothesis_candidate():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "None Material"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "none-material",
                "--title",
                "None Material",
                "--proposition",
                "None-like material markers are not evidence.",
                "--expected",
                "The CLI rejects none material before planning.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        cases = [
            ("None", "A concrete hypothesis candidate."),
            ("O001 and proposition.md expected consequence.", "None"),
            ("no material yet", "A concrete hypothesis candidate."),
            ("O001 and proposition.md expected consequence.", "None: material is too early"),
        ]
        results = []
        for index, (material_used, derived_hypothesis) in enumerate(cases, start=1):
            fill_analysis(
                target,
                "P001_none-material",
                material_used=material_used,
                derived_hypothesis=derived_hypothesis,
            )
            results.append(
                subprocess.run(
                    [
                        sys.executable,
                        str(new_hypothesis),
                        str(target),
                        "--proposition",
                        "P001_none-material",
                        "--id",
                        f"H{index:03d}",
                        "--slug",
                        f"none-case-{index}",
                        "--title",
                        "None Case",
                        "--category",
                        "applied_research",
                        "--mode",
                        "confirmatory",
                        "--hypothesis",
                        "This should be rejected.",
                        "--source-analysis",
                        "A001",
                        "--status",
                        "supported",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                )
            )

    for result in results:
        assert result.returncode == 1
        assert "source analysis is still placeholder-only" in result.stderr or "source analysis has no derived hypothesis candidate" in result.stderr


def test_new_hypothesis_rejects_non_plannable_proposition_statuses():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Status Gate"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "status-gate",
                "--title",
                "Status Gate",
                "--proposition",
                "Only plannable proposition states may create a derived hypothesis.",
                "--expected",
                "The CLI rejects states that need more material or splitting.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        results = []
        for index, status in enumerate(["contradicted", "under-specified", "split-needed"], start=1):
            fill_analysis(
                target,
                "P001_status-gate",
                status=status,
                derived_hypothesis="This status should not create a plan.",
            )
            results.append(
                subprocess.run(
                    [
                        sys.executable,
                        str(new_hypothesis),
                        str(target),
                        "--proposition",
                        "P001_status-gate",
                        "--id",
                        f"H{index:03d}",
                        "--slug",
                        f"blocked-{index}",
                        "--title",
                        "Blocked",
                        "--category",
                        "applied_research",
                        "--mode",
                        "confirmatory",
                        "--hypothesis",
                        "This should be rejected.",
                        "--source-analysis",
                        "A001",
                        "--status",
                        status,
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                )
            )

    for result in results:
        assert result.returncode == 1
        assert "does not permit creating a hypothesis plan" in result.stderr


def test_new_hypothesis_rejects_contradicted_parent_current_status():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Parent Status Gate"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "contradicted-parent",
                "--title",
                "Contradicted Parent",
                "--proposition",
                "A contradicted current proposition must not parent a new hypothesis plan.",
                "--expected",
                "Only a live updated proposition can parent the next hypothesis.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        fill_analysis(
            target,
            "P001_contradicted-parent",
            status="supported",
            derived_hypothesis="This older supported analysis should not override the parent current status.",
        )
        proposition_md = target / "propositions" / "P001_contradicted-parent" / "proposition.md"
        proposition_md.write_text(
            proposition_md.read_text(encoding="utf-8").replace(
                "## Current status\n\nopen\n",
                "## Current status\n\ncontradicted\n",
            ),
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(new_hypothesis),
                str(target),
                "--proposition",
                "P001_contradicted-parent",
                "--id",
                "H001",
                "--slug",
                "blocked-by-parent",
                "--title",
                "Blocked by Parent",
                "--category",
                "applied_research",
                "--mode",
                "confirmatory",
                "--hypothesis",
                "This should be rejected because the parent proposition is currently contradicted.",
                "--source-analysis",
                "A001",
                "--status",
                "supported",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "parent proposition current status 'contradicted' does not permit creating a hypothesis plan" in result.stderr


def test_research_scripts_reject_path_traversal_components():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Path Safety"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "../escaped",
                "--title",
                "Escaped",
                "--proposition",
                "Path traversal must not be accepted.",
                "--expected",
                "No directory is created outside propositions.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "slug must be kebab-case" in result.stderr


def test_standalone_new_plan_script_is_removed():
    assert not (ROOT / "skills" / "research" / "scripts" / "new_plan.py").exists()


def test_proposition_first_docs_define_question_to_hypothesis_state_machine():
    skill = read("skills/research/SKILL.md")
    rd_plan = read("skills/research/references/rd_plan.md")
    plan_review = read("skills/research-plan-review/SKILL.md")
    result_analysis = read("skills/research-result-analysis/SKILL.md")
    readme = read("README.md")

    for text in [skill, rd_plan, readme]:
        assert_ordered_fragments(
            text,
            "Situation question",
            "Generated doubt",
            "Working proposition",
            "Expected consequence",
            "Proposition status",
            "Derived hypothesis",
            "Hypothesis plan",
        )
        assert_mentions(
            text,
            "unrealized-condition",
            "under-specified",
            "split-needed",
            "material absence",
            "no proposition or hypothesis",
        )

    assert_mentions(
        plan_review,
        "sibling `hypothesis.md`",
        "parent proposition",
        "generated doubt",
        "working proposition",
        "proposition status",
        "different question",
    )
    assert_mentions(
        result_analysis,
        "does not choose proposition decisions",
        "hypothesis status",
        "proposition status",
        "tested-supported",
        "tested-contradicted",
        "tested-partial",
        "tested-inconclusive",
    )


def test_current_docs_do_not_use_legacy_plan_first_iteration_labels():
    paths = [
        "skills/research-result-analysis/SKILL.md",
        "skills/research/references/report_format.md",
        "skills/research/references/assumption_audit.md",
        "skills/research/references/categories/basic_research.md",
        "skills/research/references/categories/applied_research.md",
        "skills/research/references/categories/experimental_development.md",
        "skills/research/references/analysis.md",
    ]

    for path in paths:
        text = read(path)
        assert not re.search(r"`(?:REFINE|ADJACENT|NEXT_STEP)`|\b(?:REFINE|ADJACENT|NEXT_STEP)\b", text), path


def test_new_hypothesis_accepts_theoretical_mode_and_generates_theoretical_sections():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Theoretical"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P042",
                "--slug",
                "closed-form-bound",
                "--title",
                "Closed Form Bound",
                "--proposition",
                "The limiting behavior can be characterized by a closed-form bound.",
                "--expected",
                "Known limiting cases reduce to the derived bound.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        fill_analysis(
            target,
            "P042_closed-form-bound",
            status="supported",
            derived_hypothesis="The proposition admits a closed-form bound.",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_hypothesis),
                str(target),
                "--proposition",
                "P042_closed-form-bound",
                "--id",
                "H001",
                "--slug",
                "closed-form-bound",
                "--title",
                "Closed Form Bound",
                "--category",
                "basic_research",
                "--mode",
                "theoretical",
                "--hypothesis",
                "The proposition admits a closed-form bound.",
                "--type",
                "theoretical",
                "--source-analysis",
                "A001",
                "--status",
                "supported",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        assert result.returncode == 0, result.stderr
        plan = (
            target
            / "propositions"
            / "P042_closed-form-bound"
            / "hypotheses"
            / "H001_closed-form-bound"
            / "plan.md"
        ).read_text(encoding="utf-8")
        hypothesis = (
            target
            / "propositions"
            / "P042_closed-form-bound"
            / "hypotheses"
            / "H001_closed-form-bound"
            / "hypothesis.md"
        ).read_text(encoding="utf-8")

    assert "mode: theoretical" in plan
    assert markdown_section(hypothesis, "## Type").strip() == "theoretical"
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
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"
    new_hypothesis = ROOT / "skills" / "research" / "scripts" / "new_hypothesis.py"
    new_run = ROOT / "skills" / "research" / "scripts" / "new_run.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Run Contract"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P007",
                "--slug",
                "artifact-contract",
                "--title",
                "Artifact Contract",
                "--proposition",
                "Completed research scripts must leave durable artifacts.",
                "--expected",
                "Runs contain manifests, logs, and at least one durable artifact.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        fill_analysis(
            target,
            "P007_artifact-contract",
            status="supported",
            derived_hypothesis="new_run creates the durable artifact scaffold.",
        )
        subprocess.run(
            [
                sys.executable,
                str(new_hypothesis),
                str(target),
                "--proposition",
                "P007_artifact-contract",
                "--id",
                "H001",
                "--slug",
                "artifact-contract",
                "--title",
                "Artifact Contract",
                "--category",
                "applied_research",
                "--mode",
                "exploratory",
                "--hypothesis",
                "new_run creates the durable artifact scaffold.",
                "--source-analysis",
                "A001",
                "--status",
                "supported",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                str(new_run),
                str(target),
                "--proposition",
                "P007_artifact-contract",
                "--hypothesis",
                "H001_artifact-contract",
                "--seed",
                "3",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        assert result.returncode == 0, result.stderr
        run_dir = (
            target
            / "propositions"
            / "P007_artifact-contract"
            / "hypotheses"
            / "H001_artifact-contract"
            / "experiments"
            / "runs"
            / "H001__001__seed3"
        )
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
        assert_mentions(
            manifest,
            "initialized",
            "command",
            "artifacts",
            "propositions/P007_artifact-contract/hypotheses/H001_artifact-contract/plan.md",
        )
        assert_mentions(readme, "print-only", "stdout is not evidence", "check_run_artifacts.py")

        manifest_path = run_dir / "run_manifest.json"
        manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        (run_dir / "outputs" / "metrics.json").write_text('{"n": 1}', encoding="utf-8")
        manifest_data.update(
            {
                "status": "completed",
                "command": "python experiments/code/run.py",
                "artifacts": ["outputs/metrics.json"],
            }
        )
        manifest_path.write_text(json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8")
        check_result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"),
                str(run_dir),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert check_result.returncode == 0, check_result.stdout + check_result.stderr


def test_check_run_artifacts_rejects_print_only_run():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "logs" / "stdout.log").write_text("accuracy 0.84\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"completed","command":"python eda.py"}',
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
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"completed","command":"python eda.py --run-dir run","artifacts":[]}',
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
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"completed","command":"python eda.py --run-dir run","artifacts":["README.md"]}',
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
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"completed","command":"python eda.py --run-dir run","artifacts":["outputs/stdout_copy.txt"]}',
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
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"failed","command":"python eda.py --run-dir run","artifacts":["outputs/metrics.json"]}',
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


def test_check_run_artifacts_requires_manifest_identity_fields_as_strings():
    script = ROOT / "skills" / "research" / "scripts" / "check_run_artifacts.py"

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        (run_dir / "logs").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "logs" / "stdout.log").write_text("wrote outputs/metrics.json\n", encoding="utf-8")
        (run_dir / "logs" / "stderr.log").write_text("", encoding="utf-8")
        (run_dir / "outputs" / "metrics.json").write_text('{"accuracy": 0.84, "n": 128}', encoding="utf-8")
        (run_dir / "run_manifest.json").write_text(
            json.dumps(
                {
                    "run_id": "",
                    "proposition": "",
                    "hypothesis": ["H001_demo"],
                    "plan_path": "",
                    "status": ["completed"],
                    "command": ["python", "eda.py"],
                    "artifacts": ["outputs/metrics.json"],
                }
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), str(run_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    assert result.returncode == 1
    assert "run_manifest.json run_id must be a non-empty string" in result.stdout
    assert "run_manifest.json proposition must be a non-empty string" in result.stdout
    assert "run_manifest.json hypothesis must be a non-empty string" in result.stdout
    assert "run_manifest.json plan_path must be a non-empty string" in result.stdout
    assert "run_manifest.json status must be a non-empty string" in result.stdout
    assert "run_manifest.json command must be a non-empty string" in result.stdout


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
            '{"run_id":"run","proposition":"P001_demo","hypothesis":"H001_demo","plan_path":"propositions/P001_demo/hypotheses/H001_demo/plan.md","status":"completed","command":"python eda.py --run-dir run","artifacts":["outputs/metrics.json"]}',
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
        "## Trace contract",
        "Generated doubt",
        "Working proposition",
        "Expected consequence",
        "Proposition status",
        "Derived hypothesis",
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
            "## Proposition and hypothesis trace",
            "Generated doubt",
            "Working proposition",
            "Expected consequence",
            "Proposition status",
            "Derived hypothesis",
            "## Prior-work grounding",
        )
        assert_mentions(
            text,
            "Competing hypothesis",
            "Minimal discriminator",
            "Required evidence" if "Required evidence" in text else "Result feedback",
        )


def test_mechanism_record_schema_and_templates_include_lens_selection_contract():
    rd_plan = read("skills/research/references/rd_plan.md")
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for text in [rd_plan] + [p.read_text(encoding="utf-8") for p in template_dir.glob("*.template")]:
        assert_ordered_fragments(
            text,
            "Generated doubt",
            "Working proposition",
            "Expected consequence",
            "Proposition status",
            "Derived hypothesis",
        )
        assert_mentions(
            text,
            "unrealized-condition",
            "under-specified",
            "split-needed",
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


def test_check_mechanism_hypothesis_record_accepts_proposition_first_template_without_legacy_record():
    template = read("skills/research/assets/plan/rd_plan_exploratory.md.template")
    result = run_mechanism_record_check(template)

    assert result.returncode == 0, result.stdout + result.stderr


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
- Plan: propositions/P001_theory/hypotheses/H001_theoretical/plan.md
- Source artifacts: propositions/P001_theory/hypotheses/H001_theoretical/experiments/runs/
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


def test_check_report_rejects_old_top_level_plan_references():
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
- Plan: `plans/01_theoretical.md`
- Source artifacts: `experiments/01_theoretical/runs/`
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

    assert result.returncode == 1
    assert "old top-level plan or run path" in result.stdout


def test_new_project_next_steps_use_formal_categories_and_theoretical_mode():
    new_project = ROOT / "skills" / "research" / "scripts" / "new_project.py"
    new_proposition = ROOT / "skills" / "research" / "scripts" / "new_proposition.py"

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        project_result = subprocess.run(
            [sys.executable, str(new_project), str(target), "--name", "Next Step Contract"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        proposition_result = subprocess.run(
            [
                sys.executable,
                str(new_proposition),
                str(target),
                "--id",
                "P001",
                "--slug",
                "next-step-contract",
                "--title",
                "Next Step Contract",
                "--proposition",
                "Next step output should be concrete and shell-safe.",
                "--expected",
                "The generated command should avoid placeholders and bash continuations.",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

    combined = project_result.stdout + "\n" + proposition_result.stdout
    assert "new_proposition.py" in project_result.stdout
    assert "new_hypothesis.py" in proposition_result.stdout
    assert "new_plan.py" not in combined
    assert "--id P001" in project_result.stdout
    assert "<slug>" not in combined
    assert not re.search(r"\\\s*$", combined, flags=re.MULTILINE)
    assert '"Title"' in combined
    assert '--slug slug' in combined
    assert f'"{target}"' in combined
