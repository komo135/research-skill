from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


class ProjectBoundaryTests(unittest.TestCase):
    def test_plugin_version_metadata_is_consistent(self) -> None:
        expected = "1.0.6"
        codex_plugin = json.loads(read_text(".codex-plugin/plugin.json"))
        claude_plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        claude_marketplace = json.loads(read_text(".claude-plugin/marketplace.json"))
        readme = read_text("README.md")

        self.assertEqual(expected, codex_plugin["version"])
        self.assertEqual(expected, claude_plugin["version"])
        self.assertEqual(expected, claude_marketplace["plugins"][0]["version"])
        self.assertIn(f"### v{expected} (current)", readme)

    def test_skill_defines_framework_boundary_contract(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")

        for phrase in [
            "## Framework Boundary",
            "protocol layer",
            "project instance layer",
            "Generated reports are snapshots",
            "Do not embed active candidates",
        ]:
            self.assertIn(phrase, skill)

    def test_skill_keeps_research_contracts_out_of_evidence_artifacts(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")

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
                    str(ROOT / "skills/quant-research/scripts/new_project.py"),
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
            self.assertIn("Choose tracking backend", result.stdout)
            self.assertIn("Run inventory/export", result.stdout)

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
            self.assertIn("Run inventory/export", decisions)

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
                    str(ROOT / "skills/quant-research/scripts/new_project.py"),
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
                        "Trial design (copied from frozen pre-reg)",
                        "State updates (explanation_ledger.md)",
                    ],
                ),
            ]:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "skills/quant-research/scripts/new_project.py"),
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
                        str(ROOT / "skills/quant-research/scripts/new_trial.py"),
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
        index_template = read_text("skills/quant-research/assets/shared/INDEX.md.template")

        self.assertIn("evidence artifact", index_template.lower())
        self.assertIn("ledger assessment", index_template.lower())
        for phrase in [
            "linked capability/explanation",
            "state row updated",
            "done only when it changes the project state",
        ]:
            self.assertNotIn(phrase, index_template)

    def test_results_rows_are_evidence_records_not_protocol_state_records(self) -> None:
        aggregate_results = load_module("skills/quant-research/scripts/aggregate_results.py")
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
                    str(ROOT / "skills/quant-research/scripts/new_project.py"),
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
                    str(ROOT / "skills/quant-research/scripts/new_trial.py"),
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
        schema = read_text("skills/quant-research/references/shared/results_db_schema.md")

        self.assertIn("queryable evidence records", schema.lower())
        self.assertIn("ledger assessment", schema.lower())
        for phrase in [
            "state_row_id",
            "hypothesis_id",
            "Append when the result has an interpretation and updates a named research-state row",
        ]:
            self.assertNotIn(phrase, schema)

    def test_rd_readme_template_keeps_state_details_in_ledgers(self) -> None:
        readme_template = read_text("skills/quant-research/assets/rd/README.md.template")

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
                read_text("skills/quant-research/assets/purpose.py.template"),
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
        new_project = read_text("skills/quant-research/scripts/new_project.py")
        new_trial = read_text("skills/quant-research/scripts/new_trial.py")

        self.assertNotIn("legacy", new_project.lower())
        self.assertNotIn("legacy", new_trial.lower())
        self.assertNotIn("purpose.py.template", new_trial)

    def test_kill_policy_reserves_kill_for_terminal_evidence(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")
        stages = read_text("skills/quant-research/references/rd/rd_stages.md")

        self.assertNotIn("A kill criterion firing once is sufficient to kill", skill)
        self.assertNotIn("Go/Kill gate", skill)
        self.assertNotIn("de-risk to kill", skill)
        self.assertNotIn("default to Kill under uncertainty", stages)
        self.assertIn("Kill requires A4+ evidence", skill)
        self.assertIn("Default to Hold or Recycle under uncertainty", stages)
        self.assertIn("Re-scope", stages)

    def test_reproducibility_contract_is_scoped_and_not_overclaimed(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")
        reproducibility = read_text("skills/quant-research/references/shared/reproducibility.md")

        self.assertNotIn("Every trial that produces a metric", skill)
        self.assertIn("promotion-eligible or claim-cited trial", skill)
        self.assertIn("minimum rerun anchor", reproducibility)
        self.assertNotIn("machine-verifiable proof", reproducibility)
        self.assertNotIn("produce the same result", reproducibility)
        self.assertIn("traceable", reproducibility.lower())
        self.assertIn("rerunnable", reproducibility.lower())
        self.assertIn("reproduced", reproducibility.lower())
        self.assertIn("validated", reproducibility.lower())

    def test_reproducibility_docs_match_stamp_script_outputs(self) -> None:
        reproducibility = read_text("skills/quant-research/references/shared/reproducibility.md")
        process_review = read_text("skills/quant-research/references/review/process_review.md")

        self.assertNotIn("Captures `git rev-parse HEAD` and writes to a per-trial line", reproducibility)
        self.assertNotIn("auto-detected via Python import scan", reproducibility)
        self.assertNotIn("--project <project_name>", reproducibility)
        self.assertIn("--project-dir <project_dir>", reproducibility)
        self.assertIn("prints a JSON stamp record", reproducibility)
        self.assertIn("The trial notebook or caller persists this record", reproducibility)
        self.assertIn("promotion-eligible or claim-cited", process_review)
        self.assertNotIn("per-trial entry in `results.parquet`", process_review)
        self.assertIn("durable run log", process_review)

    def test_tracking_backend_contract_requires_auditable_inventory(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")
        schema = read_text("skills/quant-research/references/shared/results_db_schema.md")
        process_review = read_text("skills/quant-research/references/review/process_review.md")
        conclusion_review = read_text("skills/quant-research/references/review/conclusion_review.md")

        self.assertIn("complete run inventory/export", skill.lower())
        self.assertIn("not enough to resolve only the cited winning runs", skill)
        self.assertIn("R&D transition to `matured`", skill)
        self.assertIn("## Conditional required fields", schema)
        self.assertIn("When an external tracker is the canonical run store", schema)
        self.assertIn("failed runs, abandoned parameter combinations", schema)
        self.assertIn("model-selection attempts", schema)
        self.assertIn("Complete run inventory exists", process_review)
        self.assertIn("missing pre-trial backend selection is a logged gap", process_review)
        self.assertIn("complete run inventory/export", process_review.lower())
        self.assertIn("selected tracker record / exported", conclusion_review)
        self.assertIn("run inventory", conclusion_review)
        self.assertNotIn("project trial count from\n    `results.parquet`", process_review)

    def test_reproducibility_stamp_scope_mentions_claim_cited_trials(self) -> None:
        stamp_script = read_text("skills/quant-research/scripts/reproducibility_stamp.py")

        self.assertIn("promotion-eligible or claim-cited trial", stamp_script)

    def test_exploratory_runs_must_rerun_before_promotion_citation(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")

        self.assertNotIn("stamp or", skill)
        self.assertIn("rerun under the promotion-eligible protocol", skill)

    def test_reproducibility_stamp_does_not_write_when_worktree_dirty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "reproducibility").mkdir(parents=True)
            (project / "data").mkdir()
            (project / "reproducibility" / "uv.lock").write_text("lock\n", encoding="utf-8")
            (project / "data" / "prices.csv").write_text("x\n1\n", encoding="utf-8")

            subprocess.run(["git", "init"], check=True, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subprocess.run(["git", "add", "."], check=True, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "-m",
                    "initial",
                ],
                check=True,
                cwd=project,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            (project / "dirty.txt").write_text("uncommitted\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/quant-research/scripts/reproducibility_stamp.py"),
                    "--project-dir",
                    str(project),
                    "--trial-id",
                    "trial_001",
                    "--data-paths",
                    str(project / "data" / "prices.csv"),
                    "--seed",
                    "42",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse((project / "reproducibility" / "data_hashes.txt").exists())
            self.assertFalse((project / "reproducibility" / "env_lock_hash.txt").exists())
            self.assertFalse((project / "reproducibility" / "seed.txt").exists())


if __name__ == "__main__":
    unittest.main()
