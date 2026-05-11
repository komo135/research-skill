from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CJK_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_module(path: str):
    module_path = ROOT / path
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_tree_text(path: str) -> str:
    root = ROOT / path
    parts = []
    for file in sorted(root.rglob("*")):
        if file.is_file() and file.suffix in {".md", ".py", ".template"}:
            parts.append(f"\n--- {file.relative_to(ROOT)} ---\n")
            parts.append(file.read_text(encoding="utf-8"))
    return "\n".join(parts)


def normalize_for_assertion(text: str) -> str:
    return " ".join(text.lower().split())


class ProjectBoundaryTests(unittest.TestCase):
    def test_plugin_version_metadata_is_consistent(self) -> None:
        expected = "1.1.4"
        codex_plugin = json.loads(read_text(".codex-plugin/plugin.json"))
        claude_plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        claude_marketplace = json.loads(read_text(".claude-plugin/marketplace.json"))
        readme = read_text("README.md")

        self.assertEqual(expected, codex_plugin["version"])
        self.assertEqual(expected, claude_plugin["version"])
        self.assertEqual(expected, claude_marketplace["plugins"][0]["version"])
        self.assertIn(f"### v{expected} (current)", readme)

    def test_plugin_identity_is_research_skill(self) -> None:
        codex_plugin = json.loads(read_text(".codex-plugin/plugin.json"))
        agents_marketplace = json.loads(read_text(".agents/plugins/marketplace.json"))
        claude_plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        claude_marketplace = json.loads(read_text(".claude-plugin/marketplace.json"))
        readme = read_text("README.md")
        old_plugin = "quant-research" + "@" + "quant-research" + "-skill"

        self.assertEqual("research", codex_plugin["name"])
        self.assertEqual("Research", codex_plugin["interface"]["displayName"])
        self.assertEqual("research-skill", agents_marketplace["name"])
        self.assertEqual("research", agents_marketplace["plugins"][0]["name"])
        self.assertEqual("research", claude_plugin["name"])
        self.assertEqual("research-skill", claude_marketplace["name"])
        self.assertEqual("research", claude_marketplace["plugins"][0]["name"])
        self.assertIn("# research-skill", readme)
        self.assertIn("research@research-skill", readme)
        self.assertNotIn("/plugin install " + old_plugin, readme)
        self.assertIn(f"old plugin identity was `{old_plugin}`", readme.lower())

    def test_public_skills_are_research_and_quant_research_only(self) -> None:
        skill_dirs = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())

        self.assertEqual(["quant-research", "research"], skill_dirs)
        self.assertIn("name: research", read_text("skills/research/SKILL.md"))
        self.assertIn("name: quant-research", read_text("skills/quant-research/SKILL.md"))
        retired_skill = ROOT / "skills" / ("experiment" + "-review") / "SKILL.md"
        self.assertFalse(retired_skill.exists())

    def test_skill_defines_framework_boundary_contract(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        for phrase in [
            "## Framework Boundary",
            "protocol layer",
            "project instance layer",
            "Generated reports are snapshots",
            "Do not embed active candidates",
        ]:
            self.assertIn(phrase, skill)

    def test_skill_keeps_research_contracts_out_of_evidence_artifacts(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        for phrase in [
            "Evidence artifacts do not own research contracts",
            "Framework code must not require capability IDs",
            "capability_map.md is not an implementation API",
        ]:
            self.assertIn(phrase, skill)

    def test_new_project_scaffold_separates_protocol_from_instance_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "alpha",
                    "--mode",
                    "rd",
                    "--root",
                    tmp,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertIn("Choose a lightweight tracking path", result.stdout)
            self.assertIn("before the first load-bearing claim", result.stdout)

            project = Path(tmp) / "alpha"
            for path in [
                "charter.md",
                "capability_map.md",
                "decisions.md",
                "configs/.gitkeep",
                "src/.gitkeep",
                "tests/.gitkeep",
                "results/figures/.gitkeep",
                "results/intermediate/.gitkeep",
                "tracking/.gitkeep",
            ]:
                self.assertTrue((project / path).exists(), path)

            decisions = (project / "decisions.md").read_text(encoding="utf-8")
            self.assertIn("tracking backend selected", decisions)
            self.assertIn("Decision-relevant run set", decisions)

            readme = (project / "README.md").read_text(encoding="utf-8")
            for phrase in [
                "Boundary contract",
                "Protocol/state source of truth",
                "Project-instance artifacts",
                "Generated report snapshots",
            ]:
                self.assertIn(phrase, readme)

    def test_pure_research_scaffold_creates_first_preregistration_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "alpha",
                    "--mode",
                    "pure-research",
                    "--root",
                    tmp,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            project = Path(tmp) / "alpha"
            self.assertTrue((project / "prereg/PR_001.md").exists())
            content = (project / "prereg/PR_001.md").read_text(encoding="utf-8")
            self.assertIn("Pre-Registration", content)

    def test_trial_scaffold_is_protocol_agnostic_evidence_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for project_name, mode, forbidden in [
                (
                    "alpha",
                    "rd",
                    [
                        "Capability under test",
                        "Parent core technology",
                        "TRL transition target",
                        "Exit criterion under evaluation",
                        "Kill criterion under evaluation",
                    ],
                ),
                (
                    "beta",
                    "pure-research",
                    [
                        "Question under test",
                        "E-pair being discriminated",
                        "Trial design (copied from reviewed pre-reg)",
                        "State updates (explanation_ledger.md)",
                    ],
                ),
            ]:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "skills/research/scripts/new_project.py"),
                        project_name,
                        "--mode",
                        mode,
                        "--root",
                        tmp,
                    ],
                    check=True,
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                project = Path(tmp) / project_name
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "skills/research/scripts/new_trial.py"),
                        "--project-dir",
                        str(project),
                        "--slug",
                        "latency_benchmark",
                    ],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                trial = project / "purposes/trial_001_latency_benchmark.py"
                self.assertTrue(trial.exists())
                content = trial.read_text(encoding="utf-8")
                self.assertIn("Evidence artifact", content)
                self.assertIn("purposes/trial_001_latency_benchmark.py", content)
                self.assertNotIn("purposes/trial_001_latency benchmark.py", content)
                for phrase in forbidden:
                    self.assertNotIn(phrase, content)

    def test_trial_index_tracks_evidence_artifacts_not_ledger_state_updates(self) -> None:
        index_template = read_text("skills/research/assets/shared/INDEX.md.template")

        self.assertIn("evidence artifact", index_template.lower())
        self.assertIn("ledger assessment", index_template.lower())
        for phrase in [
            "linked capability/explanation",
            "state row updated",
            "done only when it changes the project state",
        ]:
            self.assertNotIn(phrase, index_template)

    def test_results_rows_are_evidence_records_not_protocol_state_records(self) -> None:
        aggregate_results = load_module("skills/research/scripts/aggregate_results.py")
        for mode in ["rd", "pure-research"]:
            row = {
                "project": "alpha",
                "trial_id": "trial_001",
                "mode": mode,
                "run_timestamp": "2026-05-06T00:00:00Z",
                "verdict": "observed",
                "notebook_path": "purposes/trial_001_latency_benchmark.py",
                "analysis_tier": "A2",
            }

            self.assertEqual([], aggregate_results.validate_row(row))

    def test_new_trial_inserts_entries_inside_index_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "alpha",
                    "--mode",
                    "rd",
                    "--root",
                    tmp,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            project = Path(tmp) / "alpha"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--slug",
                    "latency_benchmark",
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            index = (project / "purposes/INDEX.md").read_text(encoding="utf-8")
            row = "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | none | in-progress | pending |"
            self.assertIn(row, index)
            self.assertLess(index.index(row), index.index("## Artifact-status legend"))

    def test_results_schema_doc_describes_queryable_evidence_not_state_transitions(self) -> None:
        schema = read_text("skills/research/references/shared/results_db_schema.md")

        self.assertIn("queryable evidence records", schema.lower())
        self.assertIn("ledger assessment", schema.lower())
        for phrase in [
            "state_row_id",
            "hypothesis_id",
            "Append when the result has an interpretation and updates a named research-state row",
        ]:
            self.assertNotIn(phrase, schema)

    def test_rd_readme_template_keeps_state_details_in_ledgers(self) -> None:
        readme_template = read_text("skills/research/assets/rd/README.md.template")

        self.assertIn("evidence artifacts", readme_template.lower())
        self.assertIn("capability assessment", readme_template.lower())
        for phrase in [
            "stage-N-on-Cn",
            "TRL <current>/<target>",
            "includes analysis_tier and core_tech_id",
            "Critical path summary",
        ]:
            self.assertNotIn(phrase, readme_template)

    def test_public_docs_do_not_describe_trials_as_protocol_anchored(self) -> None:
        combined_docs = "\n".join(
            [
                read_text("README.md"),
                read_text("skills/research/assets/purpose.py.template"),
            ]
        )

        self.assertIn("evidence artifact", combined_docs.lower())
        for phrase in [
            "anchored to a capability or pre-registration",
            "capability + Stage-Gate anchored",
            "pre-registration + explanation-discrimination anchored",
            "core_tech_id, `lifecycle`",
        ]:
            self.assertNotIn(phrase, combined_docs)

    def test_project_helpers_do_not_fall_back_to_retired_templates(self) -> None:
        new_project = read_text("skills/research/scripts/new_project.py")
        new_trial = read_text("skills/research/scripts/new_trial.py")

        self.assertNotIn("legacy", new_project.lower())
        self.assertNotIn("legacy", new_trial.lower())
        self.assertNotIn("purpose.py.template", new_trial)

    def test_kill_policy_reserves_kill_for_terminal_evidence(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        stages = read_text("skills/research/references/rd/rd_stages.md")

        self.assertNotIn("A kill criterion firing once is sufficient to kill", skill)
        self.assertNotIn("Go/Kill gate", skill)
        self.assertNotIn("de-risk to kill", skill)
        self.assertNotIn("default to Kill under uncertainty", stages)
        self.assertIn("Kill requires A4+ evidence", skill)
        self.assertIn("Default to Hold or Recycle under uncertainty", stages)
        self.assertIn("Re-scope", stages)

    def test_reproducibility_contract_is_scoped_and_not_overclaimed(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")

        self.assertNotIn("Every trial that produces a metric", skill)
        self.assertIn("promotion-eligible or claim-cited trial", skill)
        self.assertIn("Rerun guidance", reproducibility)
        self.assertNotIn("machine-verifiable proof", reproducibility)
        self.assertNotIn("produce the same result", reproducibility)
        self.assertIn("traceable", reproducibility.lower())
        self.assertIn("rerunnable", reproducibility.lower())
        self.assertIn("reproduced", reproducibility.lower())
        self.assertIn("validated", reproducibility.lower())

    def test_reproducibility_docs_match_tracking_contract(self) -> None:
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")
        process_review = read_text("skills/research/references/review/process_review.md")

        self.assertNotIn("Captures `git rev-parse HEAD` and writes to a per-trial line", reproducibility)
        self.assertNotIn("auto-detected via Python import scan", reproducibility)
        self.assertNotIn("--project <project_name>", reproducibility)
        self.assertIn("data_versions.txt", reproducibility)
        self.assertIn("env_lock_ref.txt", reproducibility)
        self.assertIn("Local note or tracker record", reproducibility)
        self.assertIn("promotion-eligible or claim-cited", process_review)
        self.assertNotIn("per-trial entry in `results.parquet`", process_review)
        self.assertIn("durable run log", process_review)

    def test_tracking_backend_contract_is_decision_relevant_not_full_inventory(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        schema = read_text("skills/research/references/shared/results_db_schema.md")
        process_review = read_text("skills/research/references/review/process_review.md")
        conclusion_review = read_text("skills/research/references/review/conclusion_review.md")

        self.assertIn("complete inventory/export is not mandatory", skill.lower())
        self.assertIn("decision-relevant evidence", skill)
        self.assertIn("R&D transition to `matured`", skill)
        self.assertIn("## Conditional required fields", schema)
        self.assertIn("When an external tracker is the canonical run store", schema)
        self.assertIn("decision-relevant run set", schema)
        self.assertIn("failed runs, abandoned parameter combinations", schema)
        self.assertIn("model-selection attempts", schema)
        self.assertIn("Decision-relevant run set exists", process_review)
        self.assertIn("missing early backend selection is a logged gap", process_review)
        self.assertIn("complete export of", process_review.lower())
        self.assertIn("tracker record / exported", conclusion_review)
        self.assertIn("run record", conclusion_review)
        self.assertNotIn("project trial count from\n    `results.parquet`", process_review)

    def test_lightweight_review_contract_removes_session_and_trial_forcing(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/SKILL.md"),
                read_text("skills/research/references/rd/rd_workflow.md"),
                read_text("skills/research/references/pure_research/pr_workflow.md"),
                read_text("skills/research/references/pure_research/explanation_ledger_schema.md"),
                read_text("skills/research/assets/pure_research/explanation_ledger.md.template"),
                read_text("skills/research/scripts/standup.py"),
            ]
        )

        for forbidden in [
            "Every session must end",
            "every session\neither moves a ledger row",
            "Every trial\nmust move at least one row",
            "Every trial **must** update",
            "Every trial must move at least one explanation row",
            "4+ weeks without a session",
        ]:
            self.assertNotIn(forbidden, combined)

        for phrase in [
            "Only sessions that change durable research state",
            "Ordinary exploration",
            "Claim-cited or promotion-relevant results update",
            "lightweight run notes",
        ]:
            self.assertIn(phrase, combined)

    def test_program_layer_is_coordination_not_third_discipline(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        program = read_text("skills/research/references/program/program_map.md")
        normalized_program = " ".join(program.split())

        self.assertIn("R&D Program", skill)
        self.assertIn("coordination layer, not a third discipline", skill)
        self.assertIn("does not own TRL, analysis tier, promotion, or claim truth", program)
        for phrase in [
            "active symbols",
            "tuned parameters",
            "current performance metrics",
            "research_to_rd",
            "rd_to_rd",
            "rd_observation_to_research",
            "shared_infra",
            "integration",
            "Relationship / routing labels",
        ]:
            self.assertIn(phrase, normalized_program)
        for forbidden in [
            "Program discipline",
            "third discipline",
            "program-supported",
            "program-promoted",
            "Dependency types",
            "Current child state",
            "rd_to_research",
        ]:
            self.assertNotIn(forbidden, program)

    def test_research_skill_owns_generic_research_protocol(self) -> None:
        research = read_text("skills/research/SKILL.md")
        research_tree = read_tree_text("skills/research")

        for phrase in [
            "Use for serious research or R&D projects",
            "Do not use for ordinary fact lookup",
            "First Decision: Choose the Discipline",
            "R&D Program",
            "Right-Sized Rigor",
            "Result-to-Question",
            "Result-to-Capability",
            "A4 minimum",
        ]:
            self.assertIn(phrase, research)

        for forbidden in [
            "Sharpe",
            "PnL",
            "portfolio capacity",
            "transaction cost",
            "walk-forward validation",
            "backtest",
            "bp/side",
            "slippage",
            "intraday futures",
            "gross edge",
            "fee_model",
            "static fee model",
            "EURUSD",
            "USDJPY",
            "GBPUSD",
            "forex",
            "FX",
        ]:
            self.assertNotIn(forbidden, research_tree)

    def test_quant_research_is_finance_adapter_not_protocol_owner(self) -> None:
        quant = read_text("skills/quant-research/SKILL.md")

        for phrase in [
            "finance adapter",
            "Use research first",
            "financial machine learning",
            "backtest",
            "walk-forward",
            "leakage",
            "Sharpe",
            "PnL",
            "transaction cost",
            "portfolio",
        ]:
            self.assertIn(phrase, quant)

        for forbidden in [
            "any empirical research where conclusions must survive replication",
            "First Decision: Choose the Discipline",
            "coordination layer, not a third discipline",
        ]:
            self.assertNotIn(forbidden, quant)

    def test_right_sized_rigor_preserves_promotion_requirements(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        self.assertIn("## Right-Sized Rigor", skill)
        self.assertIn("Rigor is sized to the research state being changed", skill)
        for phrase in [
            "A4+ for `supported`, `matured`, `established`, or `promoted`",
            "Reviewed pre-registration",
            "Reviewed charter and kill criteria",
            "Reproducibility records",
            "Maintenance plan requirements",
        ]:
            self.assertIn(phrase, skill)

    def test_research_skill_requires_user_facing_outcome_reports(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        description = "\n".join(skill.splitlines()[:12])

        for phrase in [
            "## User-Facing Outcome Reports",
            "human-judgment artifact",
            "visual or tabular evidence",
            "intuitive evidence",
            "plain-language decision",
            "Evidence citations for every load-bearing claim",
            "file:line",
            "artifact URI",
            "run ID",
            "ledger row",
        ]:
            self.assertIn(phrase, skill)
        self.assertIn("user-facing outcome reports", description)

    def test_quant_research_names_finance_visual_evidence_examples(self) -> None:
        quant = read_text("skills/quant-research/SKILL.md")
        normalized_quant = " ".join(quant.split())

        for phrase in [
            "## Finance Reporting Addendum",
            "equity curve",
            "drawdown curve",
            "fee-sensitivity table or heatmap",
            "regime-segmented performance",
            "artifact path",
            "run ID",
            "data period",
            "cost assumptions",
        ]:
            self.assertIn(phrase, quant)
        self.assertIn(
            "must include the applicable finance-specific visuals or tables",
            normalized_quant,
        )

    def test_result_loops_route_to_mode_specific_state_objects(self) -> None:
        pr_workflow = read_text("skills/research/references/pure_research/pr_workflow.md")
        rd_stages = read_text("skills/research/references/rd/rd_stages.md")
        result_analysis = read_text("skills/research/references/shared/result_analysis.md")

        self.assertIn("Result-to-Question Loop", pr_workflow)
        self.assertIn("explanation_ledger.md", pr_workflow)
        self.assertIn("Result-to-Capability Loop", rd_stages)
        self.assertIn("capability_map.md", rd_stages)
        self.assertIn("Pure Research returns to Q/E state", result_analysis)
        self.assertIn("R&D returns to capability state", result_analysis)
        self.assertIn("goalpost shifting", rd_stages)
        self.assertIn("prospective re-scope", rd_stages)

    def test_pure_research_preregistration_separates_target_from_initial_approach(self) -> None:
        preregistration = read_text("skills/research/references/pure_research/preregistration.md")
        pr_workflow = read_text("skills/research/references/pure_research/pr_workflow.md")
        preregistration_template = read_text("skills/research/assets/pure_research/preregistration.md.template")
        combined = "\n".join([preregistration, pr_workflow, preregistration_template])

        for document in [preregistration, pr_workflow, preregistration_template]:
            normalized = normalize_for_assertion(document)
            for phrase in [
                "confirmation target",
                "initial approach",
                "not the confirmation target itself",
                "not a major deviation",
                "new pr is not required",
                "hypothesis failure",
                "threshold miss",
                "result interpretation",
                "not deviation",
            ]:
                self.assertIn(phrase, normalized)

        self.assertIn(
            "purpose, question to resolve, and initial approach",
            normalize_for_assertion(preregistration),
        )

        for document in [preregistration, pr_workflow]:
            normalized = normalize_for_assertion(document)
            for phrase in [
                "harking",
                "goalpost",
                "changing thresholds",
                "after seeing results",
                "major",
            ]:
                self.assertIn(phrase, normalized)

        self.assertIsNone(CJK_RE.search(combined))

    def test_pure_research_separates_exploratory_and_confirmatory_research(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        preregistration = read_text("skills/research/references/pure_research/preregistration.md")
        pr_workflow = read_text("skills/research/references/pure_research/pr_workflow.md")
        process_review = read_text("skills/research/references/review/process_review.md")
        promotion_gate = read_text("skills/research/references/pure_research/pr_promotion_gate.md")
        project_readme_template = read_text("skills/research/assets/pure_research/README.md.template")
        prfaq_template = read_text("skills/research/assets/pure_research/prfaq.md.template")
        preregistration_template = read_text("skills/research/assets/pure_research/preregistration.md.template")
        new_project = read_text("skills/research/scripts/new_project.py")
        combined = "\n".join(
            [
                skill,
                preregistration,
                pr_workflow,
                process_review,
                promotion_gate,
                project_readme_template,
                prfaq_template,
                preregistration_template,
                new_project,
            ]
        )
        normalized = " ".join(combined.split())

        for document in [skill, preregistration, pr_workflow, project_readme_template, prfaq_template]:
            normalized_document = normalize_for_assertion(document)
            self.assertIn("exploratory research", normalized_document)
            self.assertIn("confirmatory research", normalized_document)

        for document in [skill, preregistration]:
            normalized_document = normalize_for_assertion(document)
            for phrase in [
                "clearly separates exploratory research from confirmatory research",
                "pre-registration is a confirmatory-research tool",
                "not exploratory research itself",
                "higher reliability",
                "does not have to be followed by confirmatory research",
                "supported / external claim / high reliability claim",
                "move to confirmatory research",
            ]:
                self.assertIn(phrase, normalized_document)

        for document, phrases in [
            (
                skill,
                ["before execution", "`pr_<id>`", "current state", "comparing the pre-reg"],
            ),
            (
                preregistration,
                ["before execution", "`pr_<id>`", "current state", "comparing the pre-reg"],
            ),
            (
                pr_workflow,
                ["before execution", "`pr_<id>`", "current state", "comparing the pre-reg"],
            ),
            (
                project_readme_template,
                ["before each confirmatory execution", "`pr_<id>`", "current state"],
            ),
            (
                prfaq_template,
                ["before execution", "`pr_<id>`", "current state"],
            ),
        ]:
            normalized_document = normalize_for_assertion(document)
            for phrase in phrases:
                self.assertIn(phrase, normalized_document)

        self.assertIn("Exploratory Research Loop", combined)
        self.assertIn("Confirmatory Research Loop", combined)
        self.assertIn(
            "In confirmatory research, before execution, compare `PR_<id>` against the current state",
            normalized,
        )
        self.assertIn("claim-bearing confirmation trial", combined)
        self.assertIn("invalidated confirmatory use under the original PR", combined)
        self.assertIn("Every claim-cited, promotion-eligible, externally shared, or", project_readme_template)
        self.assertIn("high-reliability trial has a reviewed pre-registration", project_readme_template)
        self.assertIn("Then choose the next path", prfaq_template)
        self.assertIn("Exploratory research", prfaq_template)
        self.assertIn("Confirmatory research", prfaq_template)
        self.assertNotIn("Every active or completed trial has a reviewed pre-registration", project_readme_template)
        self.assertNotIn("pre-registration of trial 1", project_readme_template)
        self.assertNotIn("then pre-registration per", prfaq_template)
        self.assertNotIn("same standard to all Pure Research trials", preregistration)
        self.assertNotIn("pre-register first trial", combined)
        self.assertNotIn("no implementation / trial evidence-producing runs on day 1", combined)
        self.assertIsNone(CJK_RE.search(preregistration))
        self.assertIsNone(CJK_RE.search(pr_workflow))
        self.assertIsNone(CJK_RE.search(project_readme_template))
        self.assertIsNone(CJK_RE.search(prfaq_template))
        self.assertIsNone(CJK_RE.search(preregistration_template))

    def test_program_metadata_stays_out_of_evidence_artifacts_and_framework_apis(self) -> None:
        combined_templates = "\n".join(
            [
                read_text("skills/research/assets/rd/rd_trial.py.template"),
                read_text("skills/research/assets/pure_research/pr_trial.py.template"),
                read_text("skills/research/scripts/new_trial.py"),
                read_text("skills/research/scripts/new_project.py"),
            ]
        )

        for phrase in [
            "program_id",
            "program_map",
            "Program status",
            "handoff_contract",
        ]:
            self.assertNotIn(phrase, combined_templates)

    def test_reproducibility_contract_mentions_claim_cited_trials(self) -> None:
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")

        self.assertIn("promotion-eligible or claim-cited trial", reproducibility)

    def test_exploratory_runs_must_rerun_before_promotion_citation(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        self.assertNotIn("retroactively relabel exploratory output as complete", skill)
        self.assertIn("rerun under the promotion-eligible protocol", skill)

    def test_removed_reproducibility_scripts_are_not_referenced(self) -> None:
        research_tree = read_tree_text("skills/research")

        for phrase in [
            "reproducibility_" + "st" + "amp.py",
            "reproducibility_" + "verify.py",
            "data_" + "ha" + "shes.txt",
            "env_lock_" + "ha" + "sh.txt",
            "plan-vs-actual " + "helper",
            "planning-record " + "helper",
            "rerun" + "-anchor " + "helper",
        ]:
            self.assertNotIn(phrase, research_tree)

    def test_registration_proof_artifacts_are_not_reintroduced(self) -> None:
        research_tree = read_tree_text("skills/research")

        for phrase in [
            "note " + "reference",
            "dated " + "note",
            "record " + "matches",
            "written " + "down at",
            "pre-reg " + "reference",
            "pre-registration " + "record",
            "env " + "reference",
            "environment pin " + "reference",
            "record " + "timestamp",
            "byte-" + "for-byte",
            "reference " + "b9",
            "reference on " + "file",
            "selected tracker " + "record",
            "git " + "history",
            "git " + "log",
            "commit " + "timestamp",
            "ledger consistency " + "review",
            "planning " + "note",
            "pre-registration " + "log",
            "project " + "history",
            "trial notes " + "identify",
        ]:
            self.assertNotIn(phrase, research_tree)


if __name__ == "__main__":
    unittest.main()
