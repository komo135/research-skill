from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_report_format_distinguishes_material_conditions_from_env_locks():
    report_format = read("skills/research/references/report_format.md")

    assert "material conditions" in report_format
    assert "not environment locks" in report_format
    assert "Seed information is a variability disclosure" in report_format


def test_research_skill_frames_provenance_as_audit_not_reproducibility_itself():
    skill = read("skills/research/SKILL.md")

    assert "material execution conditions" in skill
    assert "audit pointer, not the source of reproducibility" in skill
    assert "claim-to-artifact consistency is an integrity check" in skill


def test_plan_schema_requires_material_conditions_not_env_locks():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert "material conditions that affect interpretation" in rd_plan
    assert "not env locks or commit hashes" in rd_plan
    assert "audit trail, not a substitute for methodology" in rd_plan
    assert "Changing a seed value before seeing outcomes is usually not material" in rd_plan
    assert "Changing the seed policy" in rd_plan


def test_readme_keeps_experiment_replicability_out_of_the_core_contract():
    readme = read("README.md")
    readme_lower = readme.lower()

    assert "material conditions, not environment locks" in readme
    assert "seed variability" in readme
    assert "claim-to-artifact consistency checks are evidence-integrity checks" in readme_lower


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

    assert "evidence-integrity anchor" in claim_structure
    assert "not by itself a reproducibility guarantee" in claim_structure
    assert "seed count, dispersion, and failed seeds" in analysis


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
