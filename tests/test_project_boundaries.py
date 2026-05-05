from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectBoundaryTests(unittest.TestCase):
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

    def test_new_project_scaffold_separates_protocol_from_instance_work(self) -> None:
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
            for path in [
                "charter.md",
                "capability_map.md",
                "decisions.md",
                "configs/.gitkeep",
                "src/.gitkeep",
                "tests/.gitkeep",
                "results/figures/.gitkeep",
                "results/intermediate/.gitkeep",
            ]:
                self.assertTrue((project / path).exists(), path)

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
