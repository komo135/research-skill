from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import importlib.util
import json
import os
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


def assert_phrases_present(testcase: unittest.TestCase, document: str, phrases: list[str]) -> None:
    normalized = normalize_for_assertion(document)
    missing = [phrase for phrase in phrases if normalize_for_assertion(phrase) not in normalized]
    testcase.assertEqual([], missing)


class ProjectBoundaryTests(unittest.TestCase):
    def test_plugin_version_metadata_is_consistent(self) -> None:
        expected = "1.1.10"
        codex_plugin = json.loads(read_text(".codex-plugin/plugin.json"))
        claude_plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        claude_marketplace = json.loads(read_text(".claude-plugin/marketplace.json"))
        readme = read_text("README.md")

        self.assertEqual(expected, codex_plugin["version"])
        self.assertEqual(expected, claude_plugin["version"])
        self.assertEqual(expected, claude_marketplace["plugins"][0]["version"])
        self.assertIn(f"v{expected}", codex_plugin["description"])
        self.assertIn(f"v{expected}", codex_plugin["interface"]["longDescription"])
        self.assertIn(f"v{expected}", claude_plugin["description"])
        self.assertIn(f"v{expected}", claude_marketplace["plugins"][0]["description"])
        self.assertIn(f"Version {expected}", readme)
        self.assertIn(f"### v{expected} (current)", readme)

    def test_packaged_skill_surfaces_do_not_restore_retired_rd_protocol_terms(self) -> None:
        combined = "\n".join(
            [
                read_text("README.md"),
                read_text(".codex-plugin/plugin.json"),
                read_text(".claude-plugin/plugin.json"),
                read_text(".claude-plugin/marketplace.json"),
                read_text(".agents/plugins/marketplace.json"),
                read_tree_text("skills"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for forbidden in [
            "trl",
            "technology readiness level",
            "target_trl",
            "current_trl",
            "capability / technology research",
            "core technologies",
            "core technology",
            "capability map",
            "capability_map",
            "stage-gate",
            "stage gate",
            "result-to-capability",
            "r&d program",
            "program map",
            "charter",
            "rd_charter",
            "integration-pattern",
            "integration_patterns",
            "technology decomposition",
            "technology_decomposition",
            "rd_promotion_gate",
            "promotion-eligible",
        ]:
            self.assertNotIn(
                normalize_for_assertion(forbidden),
                normalized,
                f"Retired R&D protocol term remains on a packaged skill surface: {forbidden}",
            )

    def test_superpowers_specs_are_not_tracked_plugin_artifacts(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "docs/superpowers/specs"],
            check=True,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        self.assertEqual("", result.stdout.strip())

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

    def test_skill_keeps_report_contracts_out_of_evidence_artifacts(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        for phrase in [
            "Evidence artifacts do not own state decisions or report contracts",
            "Framework code must not require research-state IDs",
            "rd_plan.md is not an implementation API",
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
            self.assertIn("Review the R&D plan", result.stdout)
            self.assertIn("Compare execution and results against the pre-registration", result.stdout)

            project = Path(tmp) / "alpha"
            workstream = project / "workstreams" / "WS001-rd"
            for path in [
                "project_state.md",
                "workstreams/WS001-rd/rd_plan.md",
                "workstreams/WS001-rd/prereg/PR_001_initial.md",
                "decisions.md",
                "configs/.gitkeep",
                "src/.gitkeep",
                "tests/.gitkeep",
                "results/figures/.gitkeep",
                "results/intermediate/.gitkeep",
                "tracking/.gitkeep",
            ]:
                self.assertTrue((project / path).exists(), path)
            self.assertFalse((project / "charter.md").exists())
            self.assertFalse((project / "capability_map.md").exists())
            self.assertFalse((workstream / "charter.md").exists())
            self.assertFalse((workstream / "capability_map.md").exists())
            self.assertTrue(workstream.exists())

            decisions = (project / "decisions.md").read_text(encoding="utf-8")
            self.assertIn("report provenance note", decisions)
            self.assertIn("Presented evidence", decisions)

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
            result = subprocess.run(
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
            workstream = project / "workstreams" / "WS001-phenomenon"
            self.assertTrue((workstream / "prereg/PR_001_initial.md").exists())
            self.assertFalse((project / "prereg/PR_001.md").exists())
            self.assertFalse((project / "explanation_ledger.md").exists())
            content = (workstream / "prereg/PR_001_initial.md").read_text(encoding="utf-8")
            self.assertIn("Pre-Registration", content)
            self.assertIn("preregistration_type: exploratory", content)
            self.assertNotIn("preregistration_type: confirmatory | exploratory", content)
            self.assertIn("## Exploratory body", content)
            self.assertNotIn("## Confirmatory body", content)
            self.assertNotIn("Delete the body section", content)
            self.assertIn("results/reports/RPT_001_initial/", content)
            self.assertNotIn("RPT_<id>_<slug>", content)
            self.assertNotIn("--prereg-id PR_001_initial --question-id", result.stdout)
            self.assertIn("Create a separate confirmatory pre-registration", result.stdout)

    def test_mode_shortcut_generated_docs_do_not_reclassify_the_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for project_name, mode, workstream_name, expected_label in [
                (
                    "cap",
                    "rd",
                    "WS001-rd",
                    "R&D Workstream",
                ),
                (
                    "phen",
                    "pure-research",
                    "WS001-phenomenon",
                    "Phenomenon / Mechanism Research workstream",
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
                workstream = project / "workstreams" / workstream_name
                generated_docs = "\n".join(
                    file.read_text(encoding="utf-8")
                    for file in sorted([*workstream.glob("*.md"), project / "decisions.md"])
                )

                self.assertIn(expected_label, generated_docs)
                self.assertIn("Workstream", generated_docs)
                for phrase in [
                    "R&D project",
                    "Pure Research project",
                    "this R&D project",
                    "separate Pure Research project",
                    "kill this project",
                    "- **Mode**:",
                    "[Project / R&D / Pure Research]",
                ]:
                    self.assertNotIn(phrase, generated_docs)

    def test_workstream_helpers_resolve_mode_shortcut_state_objects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "cap",
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
            rd_project = Path(tmp) / "cap"
            rd_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(rd_project),
                    "--slug",
                    "initial_probe",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(rd_result.returncode, 0, rd_result.stderr)
            self.assertTrue((rd_project / "purposes/trial_001_initial_probe.py").exists())
            self.assertFalse((ROOT / "skills/research/scripts/render_capability_dag.py").exists())

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "phen",
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
            phen_project = Path(tmp) / "phen"
            phen_workstream = phen_project / "workstreams" / "WS001-phenomenon"
            explanation_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/render_explanation_dag.py"),
                    "--project-dir",
                    str(phen_project),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(explanation_result.returncode, 0, explanation_result.stderr)
            self.assertIn("flowchart", explanation_result.stdout)

            imrad_output = phen_workstream / "imrad_draft.md"
            imrad_output.unlink()
            imrad_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/draft_imrad.py"),
                    "--project-dir",
                    str(phen_project),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(imrad_result.returncode, 0, imrad_result.stderr)
            self.assertTrue(imrad_output.exists())
            self.assertFalse((phen_project / "imrad_draft.md").exists())

    def test_draft_imrad_copies_report_package_transparent_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "phen",
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
            project = Path(tmp) / "phen"
            workstream = project / "workstreams" / "WS001-phenomenon"
            report_dir = project / "results" / "reports" / "RPT_001_initial"
            report_dir.mkdir(parents=True)
            (report_dir / "report.md").write_text(
                "\n".join(
                    [
                        "# Outcome Report",
                        "",
                        "## Summary",
                        "Exploratory diagnostic run.",
                        "",
                        "## Transparent Changes",
                        "",
                        "### Change 1: expanded date window",
                        "- Description of change: extended the data window by one month.",
                        "- Rationale: original source snapshot was unavailable.",
                        "- Effect on study results or conclusions: result has weaker diagnostic value.",
                        "",
                        "## Scope / Limitations",
                        "Local example.",
                    ]
                ),
                encoding="utf-8",
            )
            other_report_dir = project / "results" / "reports" / "RPT_999_other"
            other_report_dir.mkdir(parents=True)
            (other_report_dir / "report.md").write_text(
                "\n".join(
                    [
                        "# Unrelated Outcome Report",
                        "",
                        "## Transparent Changes",
                        "",
                        "### Change 1: unrelated workstream change",
                        "- Description of change: this belongs to another preregistration.",
                        "- Rationale: unrelated.",
                        "- Effect on study results or conclusions: should not appear.",
                    ]
                ),
                encoding="utf-8",
            )

            imrad_output = workstream / "imrad_draft.md"
            imrad_output.unlink()
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/draft_imrad.py"),
                    "--project-dir",
                    str(project),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            content = imrad_output.read_text(encoding="utf-8")
            self.assertIn("expanded date window", content)
            self.assertIn("Effect on study results or conclusions", content)
            self.assertNotIn("unrelated workstream change", content)
            self.assertNotIn("No material changes recorded in decisions.md", content)

    def test_draft_imrad_preserves_existing_workstream_draft_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "phen",
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
            project = Path(tmp) / "phen"
            workstream = project / "workstreams" / "WS001-phenomenon"
            imrad_output = workstream / "imrad_draft.md"
            original = imrad_output.read_text(encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/draft_imrad.py"),
                    "--project-dir",
                    str(project),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("--force", result.stderr)
            self.assertEqual(original, imrad_output.read_text(encoding="utf-8"))

            force_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/draft_imrad.py"),
                    "--project-dir",
                    str(project),
                    "--force",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(force_result.returncode, 0, force_result.stderr)
            self.assertNotEqual(original, imrad_output.read_text(encoding="utf-8"))

    def test_research_skill_maps_state_before_workstream_gates(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        normalized = normalize_for_assertion(skill)

        self.assertIn("First Decision: Map the Current Research State", skill)
        self.assertNotIn("First Decision: Choose the Discipline", skill)
        for phrase in [
            "project can contain multiple workstreams",
            "project itself is not pure research or r&d",
            "workstream is the unit that selects a state object and gate",
            "project decision gate",
            "does not override child workstream claims or report conclusions",
            "phenomenon / mechanism research",
            "r&d workstream",
        ]:
            self.assertIn(phrase, normalized)

    def test_mixed_project_scaffold_does_not_require_exclusive_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_project.py"),
                    "alpha",
                    "--root",
                    tmp,
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Map the current research state", result.stdout)
            self.assertIn("Create the first workstream", result.stdout)

            project = Path(tmp) / "alpha"
            for path in [
                "README.md",
                "project_state.md",
                "decisions.md",
                "workstreams",
                "purposes/INDEX.md",
                "configs/.gitkeep",
                "src/.gitkeep",
                "tests/.gitkeep",
            ]:
                self.assertTrue((project / path).exists(), path)
            for old_mode_root_artifact in [
                "charter.md",
                "capability_map.md",
                "prfaq.md",
                "explanation_ledger.md",
            ]:
                self.assertFalse((project / old_mode_root_artifact).exists())

    def test_new_trial_uses_selected_workstream_state_in_mixed_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "purposes").mkdir(parents=True)
            (project / "purposes" / "INDEX.md").write_text(
                read_text("skills/research/assets/shared/INDEX.md.template"),
                encoding="utf-8",
            )
            capability = project / "workstreams" / "WS002-rd"
            phenomenon = project / "workstreams" / "WS001-phenomenon"
            capability.mkdir(parents=True)
            phenomenon.mkdir(parents=True)
            (capability / "rd_plan.md").write_text("# R&D Plan\n", encoding="utf-8")
            (phenomenon / "prfaq.md").write_text("# PR/FAQ\n", encoding="utf-8")
            (phenomenon / "explanation_ledger.md").write_text("# Explanation Ledger\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--workstream",
                    "WS002-rd",
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
            index = (project / "purposes/INDEX.md").read_text(encoding="utf-8")
            self.assertIn(
                "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | WS002-rd | in-progress | pending |",
                index,
            )

    def test_research_skill_exposes_only_implemented_workstream_labels(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        table = "| Workstream label |" + skill.split(
            "| Workstream label |",
            maxsplit=1,
        )[1].split("\n\n", maxsplit=1)[0]
        labels = []
        for line in table.splitlines():
            match = re.match(r"\| \*\*(.*?)\*\*", line)
            if match:
                labels.append(match.group(1))

        self.assertEqual(
            [
                "Phenomenon / Mechanism Research",
                "R&D Workstream",
            ],
            labels,
        )

    def test_project_state_template_offers_only_implemented_state_objects(self) -> None:
        project_state = read_text("skills/research/assets/shared/project_state.md.template")
        match = re.search(
            r"\| <REPLACE: workstream name> \| <REPLACE: ([^>]+)> \|",
            project_state,
        )

        self.assertIsNotNone(match)
        assert match is not None
        state_options = [option.strip() for option in match.group(1).split(";")]
        self.assertEqual(
            [
                "R&D Workstream",
                "Phenomenon / Mechanism Research",
            ],
            state_options,
        )

    def test_rd_entry_guidance_uses_general_r_and_d_without_technology_maturation_stack(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/SKILL.md"),
                read_text("skills/research/references/rd/rd_workflow.md"),
                read_text("skills/research/references/review/process_review.md"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for phrase in [
            "basic research",
            "applied research",
            "experimental development",
            "current-state assessment is orientation, not an r&d category",
            "hypothesis validation is evidence discipline, not an r&d category",
            "r&d workstream",
            "rd_plan.md",
            "plan -> execute -> compare -> report",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "capability / technology research",
            "core technologies",
            "capability map",
            "stage-gate",
            "stage gate",
            "technology readiness level",
            "target_trl",
            "heilmeyer",
            "heilmeier",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_new_trial_rejects_mixed_artifacts_inside_one_workstream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "purposes").mkdir(parents=True)
            (project / "workstreams" / "WS999-ambiguous").mkdir(parents=True)
            ambiguous = project / "workstreams" / "WS999-ambiguous"
            (ambiguous / "rd_plan.md").write_text("# R&D Plan\n", encoding="utf-8")
            (ambiguous / "prfaq.md").write_text("# PR/FAQ\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--workstream",
                    "WS999-ambiguous",
                    "--slug",
                    "ambiguous_trial",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("mixed workstream artifacts", result.stderr.lower())

    def test_new_trial_rejects_workstream_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            workstreams = project / "workstreams"
            external = Path(tmp) / "external"
            workstreams.mkdir(parents=True)
            external.mkdir()
            (external / "rd_plan.md").write_text("# R&D Plan\n", encoding="utf-8")
            link = workstreams / "WS999-link"
            try:
                os.symlink(external, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is not available in this environment")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--workstream",
                    "WS999-link",
                    "--slug",
                    "escape_trial",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("must resolve under", result.stderr.lower())

    def test_new_trial_uses_workstream_preregistration_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "purposes").mkdir(parents=True)
            (project / "purposes" / "INDEX.md").write_text(
                read_text("skills/research/assets/shared/INDEX.md.template"),
                encoding="utf-8",
            )
            phenomenon = project / "workstreams" / "WS001-phenomenon"
            (phenomenon / "prereg").mkdir(parents=True)
            (phenomenon / "prfaq.md").write_text("# PR/FAQ\n", encoding="utf-8")
            (phenomenon / "explanation_ledger.md").write_text("# Explanation Ledger\n", encoding="utf-8")
            (phenomenon / "prereg" / "PR_001_regime_probe.md").write_text(
                "# Pre-Registration\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--workstream",
                    "WS001-phenomenon",
                    "--slug",
                    "regime_probe",
                    "--prereg-id",
                    "PR_001_regime_probe",
                    "--question-id",
                    "Q1",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (project / "purposes/trial_001_regime_probe.py").read_text(encoding="utf-8")
            self.assertIn("workstreams/WS001-phenomenon/prereg/PR_001_regime_probe.md", content)
            self.assertIn("- **Optional ledger target**: Q1", content)
            self.assertNotIn("<REPLACE: optional prereg", content)

    def test_new_trial_uses_rd_workstream_preregistration_path(self) -> None:
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

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--slug",
                    "initial_probe",
                    "--prereg-id",
                    "PR_001_initial",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (project / "purposes/trial_001_initial_probe.py").read_text(encoding="utf-8")
            self.assertIn("workstreams/WS001-rd/prereg/PR_001_initial.md", content)
            self.assertNotIn("<REPLACE: rd_plan.md section / relevant preregistration>", content)

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
            row = "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | WS001-rd | in-progress | pending |"
            self.assertIn(row, index)
            self.assertLess(index.index(row), index.index("## Artifact-status legend"))

    def test_new_trial_recreates_missing_index_before_appending_entry(self) -> None:
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
            index_path = project / "purposes/INDEX.md"
            index_path.unlink()

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
            self.assertTrue(index_path.exists())
            index = index_path.read_text(encoding="utf-8")
            self.assertIn("## Artifact-status legend", index)
            self.assertIn(
                "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | WS001-rd | in-progress | pending |",
                index,
            )

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
        self.assertIn("r&d category", readme_template.lower())
        self.assertIn("plan-to-result", readme_template.lower())
        for phrase in [
            "capability assessment",
            "stage-N-on-Cn",
            "TRL <current>/<target>",
            "includes analysis_tier and core_tech_id",
            "Critical path summary",
            "Core Technologies",
            "Capability map",
            "Stage-Gate",
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
            "Capability / Technology Research",
        ]:
            self.assertNotIn(phrase, combined_docs)

    def test_active_skill_surfaces_do_not_contain_japanese_text(self) -> None:
        japanese_text = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
        checked_suffixes = {".md", ".py", ".template", ".json", ".toml", ".txt"}
        violations: list[str] = []

        for skill_root in [ROOT / "skills/research", ROOT / "skills/quant-research"]:
            for path in sorted(skill_root.rglob("*")):
                if not path.is_file() or path.suffix not in checked_suffixes:
                    continue
                text = path.read_text(encoding="utf-8")
                for line_number, line in enumerate(text.splitlines(), start=1):
                    if japanese_text.search(line):
                        violations.append(f"{path.relative_to(ROOT)}:{line_number}: {line}")

        self.assertEqual([], violations)

    def test_project_helpers_do_not_fall_back_to_retired_templates(self) -> None:
        new_project = read_text("skills/research/scripts/new_project.py")
        new_trial = read_text("skills/research/scripts/new_trial.py")
        new_purpose = read_text("skills/research/scripts/new_purpose.py")
        root_index_template = read_text("skills/research/assets/INDEX.md.template")

        self.assertNotIn("legacy", new_project.lower())
        self.assertNotIn("legacy", new_trial.lower())
        self.assertNotIn("purpose.py.template", new_trial)
        for user_facing_surface in [new_purpose, root_index_template]:
            self.assertNotIn("research_state.md", user_facing_surface)
            self.assertNotIn("hypotheses.md", user_facing_surface)

    def test_new_purpose_fails_fast_without_writing_retired_stub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "purposes").mkdir(parents=True)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_purpose.py"),
                    "--project",
                    "alpha",
                    "--slug",
                    "old_flow",
                    "--hyp",
                    "H1",
                    "--root",
                    tmp,
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("retired", result.stderr.lower())
            self.assertIn("new_trial.py", result.stderr)
            self.assertEqual([], list((project / "purposes").glob("pur_*.py")))

    def test_new_project_exploratory_prereg_filter_fails_when_markers_move(self) -> None:
        new_project = load_module("skills/research/scripts/new_project.py")

        for malformed in [
            "# Pre-registration\n\n## Exploratory body\nOnly exploratory remains.",
            "# Pre-registration\n\n## Confirmatory body\nOnly confirmatory remains.",
        ]:
            with self.assertRaises(ValueError):
                new_project.keep_only_exploratory_body(malformed)

    def test_process_review_uses_workstream_labels_not_project_modes(self) -> None:
        process_review = read_text("skills/research/references/review/process_review.md")

        self.assertIn("Workstream label is explicitly declared", process_review)
        self.assertIn("R&D Workstream", process_review)
        self.assertIn("Phenomenon / Mechanism Research workstream", process_review)
        for phrase in [
            "Mode is explicitly declared",
            "Mode field",
            "No mode mixing",
            "Mode mixing",
            "For R&D projects only",
            "For Pure Research projects only",
            "Capability / Technology Research workstream",
            "Stage gate",
        ]:
            self.assertNotIn(phrase, process_review)

    def test_retired_docs_do_not_reintroduce_project_mode_protocol(self) -> None:
        retired_docs = "\n".join(
            [
                read_text("skills/research/references/research_state.md"),
                read_text("skills/research/assets/decisions.md.template"),
                read_text("skills/research/assets/purpose.py.template"),
                read_text("skills/quant-research/references/hypothesis_quality.md"),
            ]
        )

        self.assertIn("workstream", retired_docs.lower())
        for phrase in [
            "mode-specific",
            "project's mode",
            "- **Mode**",
            "[R&D / Pure Research]",
            "R&D and Pure Research are separate disciplines",
        ]:
            self.assertNotIn(phrase, retired_docs)

    def test_kill_policy_reserves_kill_for_terminal_evidence(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        rd_workflow = read_text("skills/research/references/rd/rd_workflow.md")

        self.assertNotIn("A kill criterion firing once is sufficient to kill", skill)
        self.assertNotIn("Go/Kill gate", skill)
        self.assertNotIn("de-risk to kill", skill)
        self.assertNotIn("default to Kill under uncertainty", rd_workflow)
        self.assertIn("Kill requires A4+ evidence", skill)
        self.assertIn("terminal decision", rd_workflow)
        self.assertIn("prospective re-scope", rd_workflow)

    def test_a4_rigor_is_reserved_for_claim_bearing_or_promotion_decisions(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        normalized = normalize_for_assertion(skill)

        for phrase in [
            "a4+ is reserved for `supported`, external claim, deployment recommendation, or terminal decision",
            "a2-a3 may decide the next experiment, provisional go / no-go, park, deprioritize, or reject-for-now",
            "exploratory decisions do not create a load-bearing claim",
        ]:
            self.assertIn(phrase, normalized)

    def test_kill_a4_requirement_does_not_cover_exploratory_pruning(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/SKILL.md"),
                read_text("skills/research/references/rd/rd_workflow.md"),
                read_text("skills/research/references/review/process_review.md"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        self.assertIn("kill requires a4+ evidence only for terminal kill", normalized)
        self.assertIn(
            "candidate drop, reject-for-now, and deprioritize are exploratory pruning decisions",
            normalized,
        )
        self.assertIn("exploratory pruning decisions do not require a4+ evidence", normalized)

        for forbidden in [
            "candidate drop requires a4",
            "reject-for-now requires a4",
            "deprioritize requires a4",
        ]:
            self.assertNotIn(forbidden, normalized)

    def test_report_provenance_is_scoped_and_not_trial_tracking_contract(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")
        combined = "\n".join([skill, reproducibility])

        self.assertNotIn("Every trial that produces a metric", skill)
        self.assertIn("presented evidence", skill)
        self.assertIn("claim-bearing report package", reproducibility)
        self.assertIn("Rerun guidance", reproducibility)
        self.assertNotIn("machine-verifiable proof", reproducibility)
        self.assertNotIn("produce the same result", reproducibility)
        for forbidden in [
            "Tracking Backend",
            "tracking backend selected",
            "before the first load-bearing claim",
            "promotion-eligible or claim-cited trial",
            "Every promotion-eligible or claim-cited trial",
            "Reproducibility 3-tuple",
            "selected tracking backend",
        ]:
            self.assertNotIn(forbidden.lower(), combined.lower())
        self.assertIn("traceable", reproducibility.lower())
        self.assertIn("rerunnable", reproducibility.lower())
        self.assertIn("reproduced", reproducibility.lower())
        self.assertIn("validated", reproducibility.lower())

    def test_trial_templates_do_not_force_report_provenance_fields(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/assets/rd/rd_trial.py.template"),
                read_text("skills/research/assets/pure_research/pr_trial.py.template"),
            ]
        )

        self.assertIn("## Optional report provenance", combined)
        self.assertIn("Fill this only if the artifact is cited by a report package", combined)
        for forbidden in [
            "## Reproducibility",
            "- Data version:",
            "- Git commit:",
            "- Environment pin:",
            "- Run note / provenance path:",
        ]:
            self.assertNotIn(forbidden, combined)

    def test_reproducibility_docs_match_report_provenance_boundary(self) -> None:
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")
        process_review = read_text("skills/research/references/review/process_review.md")
        combined = "\n".join([reproducibility, process_review])

        self.assertNotIn("Captures `git rev-parse HEAD` and writes to a per-trial line", reproducibility)
        self.assertNotIn("auto-detected via Python import scan", reproducibility)
        self.assertNotIn("--project <project_name>", reproducibility)
        self.assertIn("report provenance", reproducibility.lower())
        self.assertIn("presented evidence", reproducibility)
        self.assertIn("claim-bearing report package", process_review)
        self.assertNotIn("per-trial entry in `results.parquet`", process_review)
        self.assertNotIn("durable run log", process_review)
        self.assertNotIn("promotion-eligible", combined)
        self.assertNotIn("claim-cited trial", combined)

    def test_report_provenance_does_not_require_backend_contract(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        schema = read_text("skills/research/references/shared/results_db_schema.md")
        process_review = read_text("skills/research/references/review/process_review.md")
        conclusion_review = read_text("skills/research/references/review/conclusion_review.md")
        combined = "\n".join([skill, schema, process_review, conclusion_review])

        self.assertIn("report provenance", skill.lower())
        self.assertIn("presented evidence", skill)
        self.assertIn("claim-bearing report package", skill)
        self.assertIn("## Conditional required fields", schema)
        self.assertIn("When a report package cites an external tracker", schema)
        self.assertIn("presented evidence set", schema)
        self.assertIn("failed runs, abandoned parameter combinations", schema)
        self.assertIn("model-selection attempts", schema)
        self.assertIn("Presented evidence can be resolved", process_review)
        self.assertNotIn("missing early backend selection is a logged gap", process_review)
        self.assertNotIn("complete export of", process_review.lower())
        self.assertIn("tracker record / exported", conclusion_review)
        self.assertIn("report provenance", conclusion_review.lower())
        self.assertNotIn("tracking backend selected", combined.lower())
        self.assertNotIn("before the first load-bearing claim", combined.lower())
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
            "Claim-bearing report packages and supported findings cite",
            "lightweight run notes",
        ]:
            self.assertIn(phrase, combined)

    def test_research_skill_does_not_reintroduce_r_and_d_program_layer(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        self.assertNotIn("R&D Program", skill)
        self.assertNotIn("program-promoted", read_tree_text("skills/research"))

    def test_active_surfaces_do_not_reference_internal_charter_or_program_map(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        combined = "\n".join([read_text("README.md"), read_tree_text("skills")])
        normalized = normalize_for_assertion(combined)

        for forbidden in [
            ".rebuild/charter.md",
            "charter c",
            "program map",
            "initial-day prohibitions",
            "charter and kill criteria exist",
            "promotion-eligible",
        ]:
            self.assertNotIn(forbidden, normalized)
        for forbidden in [
            "Program discipline",
            "third discipline",
            "program-supported",
            "program-promoted",
            "Relationship / routing labels",
            "research_to_rd",
            "rd_to_rd",
            "rd_observation_to_research",
        ]:
            self.assertNotIn(forbidden, skill)

    def test_research_skill_owns_generic_research_protocol(self) -> None:
        research = read_text("skills/research/SKILL.md")
        research_tree = read_tree_text("skills/research")

        for phrase in [
            "Use for serious research or R&D workstreams",
            "Do not use for ordinary fact lookup",
            "First Decision: Map the Current Research State",
            "project decision gate",
            "R&D Workstream",
            "Phenomenon / Mechanism Research",
            "basic research",
            "applied research",
            "experimental development",
            "Right-Sized Rigor",
            "Result-to-Question",
            "A4 minimum",
        ]:
            self.assertIn(phrase, research)

        for forbidden in [
            "Capability / Technology Research",
            "Core Technologies",
            "Capability Map",
            "Stage-Gate",
            "TRL",
        ]:
            self.assertNotIn(forbidden, research)

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
            "A4+ for `supported`, external claim, deployment recommendation, or terminal decision",
            "Reviewed pre-registration",
            "Report provenance and rerun guidance",
            "claim-bearing report packages",
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

    def test_evidence_citation_covers_load_bearing_claims(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        normalized = normalize_for_assertion(skill)

        self.assertIn(
            "supports `supported`, terminal decision, external sharing, deployment recommendation",
            normalized,
        )

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

    def test_quant_adapter_scopes_finance_checks_to_claim_bearing_decisions(self) -> None:
        quant = read_text("skills/quant-research/SKILL.md")
        normalized = normalize_for_assertion(quant)

        for phrase in [
            "finance-specific checks are claim-bearing checks",
            "they are not mandatory gates for exploratory finance work",
            "exploratory finance work may choose the next experiment, provisional go / no-go, park, deprioritize, or reject-for-now before the full finance check battery",
        ]:
            self.assertIn(phrase, normalized)

        self.assertNotIn(
            "read `references/shared/time_series_validation.md` and `references/shared/sanity_checks.md` before trusting numbers",
            normalized,
        )

    def test_result_loops_route_to_workstream_state_objects(self) -> None:
        pr_workflow = read_text("skills/research/references/pure_research/pr_workflow.md")
        rd_workflow = read_text("skills/research/references/rd/rd_workflow.md")
        result_analysis = read_text("skills/research/references/shared/result_analysis.md")

        self.assertIn("Result-to-Question Loop", pr_workflow)
        self.assertIn("explanation_ledger.md", pr_workflow)
        self.assertIn("Result-to-R&D Plan Loop", rd_workflow)
        self.assertIn("rd_plan.md", rd_workflow)
        normalized_result_analysis = " ".join(result_analysis.split())
        self.assertIn("selected workstream state object", normalized_result_analysis)
        self.assertIn("Phenomenon / Mechanism Research", result_analysis)
        self.assertIn("R&D Workstream", result_analysis)
        self.assertNotIn("mode-specific state object", result_analysis)
        self.assertNotIn("Pure Research returns to Q/E state", result_analysis)
        self.assertNotIn("R&D returns to capability state", result_analysis)
        self.assertIn("transparent changes", rd_workflow.lower())
        self.assertIn("prospective re-scope", rd_workflow)

    def test_rd_flow_uses_general_research_and_development_categories(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        rd_workflow = read_text("skills/research/references/rd/rd_workflow.md")
        expected_phrases = [
            "basic research",
            "applied research",
            "experimental development",
            "current-state assessment is orientation, not an r&d category",
            "hypothesis validation is evidence discipline, not an r&d category",
            "novel",
            "creative",
            "uncertain",
            "systematic",
            "transferable or reproducible",
        ]

        assert_phrases_present(self, skill, expected_phrases)
        assert_phrases_present(
            self,
            rd_workflow,
            [
                "current-state assessment is orientation, not an r&d category",
                "hypothesis validation is evidence discipline, not an r&d category",
                "basic research",
                "applied research",
                "experimental development",
                "plan -> execute -> compare -> report",
            ],
        )

        skill_normalized = normalize_for_assertion(skill)
        rd_normalized = normalize_for_assertion(rd_workflow)
        for phrase in ["r&d workstream", "rd_plan.md", "pre-registration"]:
            self.assertIn(phrase, skill_normalized)
        for phrase in ["rd_plan.md", "pre-registration", "report"]:
            self.assertIn(phrase, rd_normalized)

        for document in [skill, rd_workflow]:
            self.assertNotIn(
                "capability / technology research",
                normalize_for_assertion(document),
            )

    def test_rd_plan_template_defines_plan_execution_comparison_report_flow(self) -> None:
        rd_plan_template = read_text("skills/research/assets/rd/rd_plan.md.template")
        normalized = normalize_for_assertion(rd_plan_template)

        for phrase in [
            "R&D Plan",
            "R&D category",
            "planned_item",
            "expected_output",
            "pre-registration",
            "decision_or_follow_up",
            "execution status",
            "evidence",
            "report package",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "technology readiness level",
            "trl",
            "capability map",
            "stage-gate",
            "stage gate",
            "technology decomposition",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_preregistration_docs_define_plan_execution_comparison_report_flow(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        preregistration = read_text("skills/research/references/pure_research/preregistration.md")
        preregistration_template = read_text("skills/research/assets/pure_research/preregistration.md.template")

        flow_phrases = [
            "plan -> execute -> compare -> report",
            "plan: write or select the pre-registration before work starts",
            "execute: run the work against the written plan",
            "compare: compare actual execution and results against the pre-registration",
            "report: publish the plan-to-result table, transparent changes, evidence, and limitations",
            "pre-registration is a plan, not a prison",
            "midstream pre-registration governs future work or explicit reruns only",
            "prior work is prior or exploratory evidence",
        ]
        field_phrases = [
            "question / objective",
            "scope",
            "data / input plan",
            "variables / measures or inspection targets",
            "planned procedure",
            "expected outputs",
            "decision / follow-up criteria",
            "non-claim-bearing condition",
            "what would prevent outputs from being used as claim-bearing evidence",
            "future preregistered rerun or narrower report claim",
        ]
        contract_phrases = [
            "report contracts apply to report packages and presented evidence, not to research or experiments",
            "reporting-side requirement, not a continuous research tracking contract",
        ]

        assert_phrases_present(self, preregistration, flow_phrases + field_phrases + contract_phrases)
        assert_phrases_present(self, preregistration_template, flow_phrases + field_phrases + contract_phrases)
        assert_phrases_present(
            self,
            skill,
            [
                "Pre-registration is a general planning and reporting discipline",
                "Plan -> execute -> compare -> report",
                "report contracts apply to report packages and presented evidence, not to research or experiments",
            ],
        )

    def test_outcome_reports_define_reader_quality_contract(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        outcome_report = read_text("skills/research/references/shared/outcome_reports.md")
        outcome_report_template = read_text("skills/research/assets/shared/outcome_report.md.template")

        quality_phrases = [
            "report quality contract",
            "a reader can identify the decision, evidence, plan comparison, limitations, and next action without opening notebooks or ledgers",
            "supported",
            "not supported",
            "inconclusive",
            "decision deferred",
            "exploratory only",
            "blocked",
        ]
        section_phrases = [
            "Executive Decision",
            "Research Stage and Claim Boundary",
            "Preregistration Reference",
            "Plan-to-Result Table",
            "Key Evidence",
            "Evidence Integrity Checks",
            "Transparent Changes",
            "Reproducibility Capsule",
            "Scope / Limitations / Alternative Explanations",
            "Next Action",
        ]
        claim_row_phrases = [
            "claim-to-artifact check row",
            "claim_id",
            "reported_value",
            "cited_artifact_path",
            "commit_or_hash",
            "extraction_method",
            "observed_source_value",
            "comparison_status",
            "generating_command_or_entrypoint",
            "numeric, boolean, categorical, and count claim",
            "failed, missing, or not run cannot be treated as supported",
        ]

        for document in [outcome_report, outcome_report_template]:
            assert_phrases_present(self, document, quality_phrases + section_phrases + claim_row_phrases)

        assert_phrases_present(
            self,
            skill,
            [
                "Short outcome summary",
                "decision, evidence, limitation, and next action",
                "Formal report package contract",
                "preregistered or claim-bearing report package",
                "claim-to-artifact checks",
                "reproducibility capsule",
            ],
        )

    def test_rd_active_surface_removes_technology_maturation_protocol(self) -> None:
        combined = "\n".join(
            [
                read_text("README.md"),
                read_text("skills/research/SKILL.md"),
                read_tree_text("skills/research/assets/shared"),
                read_tree_text("skills/research/references/rd"),
                read_tree_text("skills/research/assets/rd"),
                read_text("skills/research/scripts/new_project.py"),
                read_text("skills/research/scripts/new_trial.py"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for phrase in [
            "basic research",
            "applied research",
            "experimental development",
            "rd_plan.md",
            "pre-registration",
            "plan-to-result",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "core technologies",
            "core technology",
            "charter",
            "program map",
            "initial-day prohibitions",
            "promotion-eligible",
            "capability map",
            "capability_map.md",
            "technology readiness level",
            "target_trl",
            "current_trl",
            "trl-",
            "stage-gate",
            "stage gate",
            "cooper",
            "heilmeier",
            "matured",
            "established",
            "result-to-capability",
            "layer 1",
            "layer 2",
            "capability claim",
            "recycle a capability",
        ]:
            self.assertNotIn(
                forbidden,
                normalized,
                f"Old technology-maturation protocol term remains: {forbidden}",
            )

    def test_removed_rd_maturation_reference_files_are_not_packaged(self) -> None:
        existing = {path.name for path in (ROOT / "skills/research/references/rd").glob("*.md")}

        self.assertEqual({"rd_workflow.md"}, existing)

        for removed in [
            "core_technologies.md",
            "capability_map_schema.md",
            "trl_scale.md",
            "rd_stages.md",
            "rd_promotion_gate.md",
            "rd_charter.md",
            "integration_patterns.md",
        ]:
            self.assertFalse((ROOT / "skills/research/references/rd" / removed).exists())

    def test_rd_preregistration_template_scopes_report_contracts_to_reports(self) -> None:
        template = read_text("skills/research/assets/rd/preregistration.md.template")

        assert_phrases_present(
            self,
            template,
            [
                "report contracts apply to report packages and presented evidence, not to research or experiments",
                "reporting-side requirement, not a continuous research tracking contract",
            ],
        )

    def test_pr_promotion_gate_does_not_treat_weakened_as_terminal_status(self) -> None:
        promotion_gate = read_text("skills/research/references/pure_research/pr_promotion_gate.md")
        normalized = normalize_for_assertion(promotion_gate)

        self.assertFalse(
            "terminal status (rejected / weakened / merged)" in normalized,
            "`weakened` is still listed as a terminal alternative status.",
        )
        self.assertFalse(
            "terminal status (rejected / weakened" in normalized,
            "`weakened` is still listed in a terminal status group.",
        )
        self.assertTrue("weakened is not terminal" in normalized, "Missing explicit non-terminal `weakened` contract.")

    def test_quant_robustness_battery_uses_current_research_protocol_docs(self) -> None:
        quant_current_refs = "\n".join(
            [
                read_text("skills/quant-research/references/shared/robustness_battery.md"),
                read_text("skills/quant-research/references/shared/feature_construction.md"),
                read_text("skills/quant-research/references/shared/prediction_to_decision.md"),
            ]
        )
        normalized = normalize_for_assertion(quant_current_refs)

        for forbidden in [
            "hypothesis_quality.md",
            "hypotheses.md",
            "research_state.md",
        ]:
            self.assertFalse(
                forbidden in normalized,
                f"Quant current references still mention retired protocol surface: {forbidden}",
            )

    def test_rolling_window_stability_is_not_named_true_walk_forward(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/quant-research/references/shared/robustness_battery.md"),
                read_text("skills/quant-research/references/shared/time_series_validation.md"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for forbidden in [
            "walk-forward sharpe distribution",
            "running walk-forward in the robustness phase",
            "walk-forward (3-month)",
            "- walk-forward:",
            "walk-forward unstable",
        ]:
            self.assertFalse(
                forbidden in normalized,
                f"Rolling-window stability is still labeled as walk-forward: {forbidden}",
            )
        for phrase in [
            "rolling-window stability",
            "true walk-forward",
            "refit",
        ]:
            self.assertTrue(phrase in normalized, f"Missing terminology distinction phrase: {phrase}")

    def test_multiple_testing_does_not_reference_retired_preregistration_section(self) -> None:
        multiple_testing = read_text("skills/quant-research/references/shared/multiple_testing.md")
        normalized = normalize_for_assertion(multiple_testing)

        for forbidden in [
            "`preregistration.md` § 3.5",
            "preregistration.md § 3.5",
            "pre-register the correction method in `preregistration.md` § 3.5",
        ]:
            self.assertFalse(
                normalize_for_assertion(forbidden) in normalized,
                f"Multiple-testing doc still references retired preregistration section: {forbidden}",
            )

    def test_quant_adapter_defers_to_research_workstream_state_not_project_discipline(self) -> None:
        quant_skill = read_text("skills/quant-research/SKILL.md")
        normalized_quant = " ".join(quant_skill.split())

        self.assertIn("Use research first for the project workstream", normalized_quant)
        self.assertIn("state object", quant_skill)
        self.assertNotIn("project discipline", quant_skill)
        self.assertNotIn("Pure Research vs R&D", quant_skill)

    def test_skill_corpus_does_not_restore_project_discipline_language(self) -> None:
        combined = "\n".join(
            [
                read_tree_text("skills/research"),
                read_tree_text("skills/quant-research"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for phrase in [
            "R&D project",
            "Pure Research project",
            "project discipline",
            "R&D mode",
            "Pure Research mode",
            "mode-specific",
            "Mode is explicitly declared",
            "Mode mixing",
            "single 4-section ledger",
            "- **Mode**:",
            "Project / R&D / Pure Research",
        ]:
            self.assertNotIn(normalize_for_assertion(phrase), normalized)

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
                "not a plan-breaking material change",
                "new pr is not required",
                "hypothesis failure",
                "threshold miss",
                "result interpretation",
                "not a plan-breaking material change",
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
                "plan-breaking",
            ]:
                self.assertIn(phrase, normalized)

        self.assertIsNone(CJK_RE.search(combined))

    def test_preregistration_policy_is_general_planning_discipline(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        readme = read_text("README.md")
        preregistration = read_text("skills/research/references/pure_research/preregistration.md")
        pr_workflow = read_text("skills/research/references/pure_research/pr_workflow.md")
        process_review = read_text("skills/research/references/review/process_review.md")
        promotion_gate = read_text("skills/research/references/pure_research/pr_promotion_gate.md")
        project_readme_template = read_text("skills/research/assets/pure_research/README.md.template")
        prfaq_template = read_text("skills/research/assets/pure_research/prfaq.md.template")
        preregistration_template = read_text("skills/research/assets/pure_research/preregistration.md.template")
        new_project = read_text("skills/research/scripts/new_project.py")
        outcome_report = read_text("skills/research/references/shared/outcome_reports.md")
        outcome_report_template = read_text("skills/research/assets/shared/outcome_report.md.template")
        combined = "\n".join(
            [
                skill,
                readme,
                preregistration,
                pr_workflow,
                process_review,
                promotion_gate,
                project_readme_template,
                prfaq_template,
                preregistration_template,
                new_project,
                outcome_report,
                outcome_report_template,
            ]
        )
        normalized = " ".join(combined.split())

        for document in [skill, readme, preregistration, pr_workflow, project_readme_template, prfaq_template]:
            normalized_document = normalize_for_assertion(document)
            self.assertIn("exploratory research", normalized_document)
            self.assertIn("confirmatory research", normalized_document)

        for document in [skill, preregistration, preregistration_template]:
            normalized_document = normalize_for_assertion(document)
            for phrase in [
                "general planning and reporting discipline",
                "preregistration_type: confirmatory | exploratory",
                "study information",
                "sampling / data plan",
                "variables / measures",
                "transparent changes policy",
            ]:
                self.assertIn(phrase, normalized_document)

        for document, phrases in [
            (preregistration, ["confirmatory preregistration", "exploratory preregistration"]),
            (
                preregistration_template,
                [
                    "confirmatory body",
                    "exploratory body",
                    "hypotheses",
                    "analysis plan",
                    "exploratory objective",
                    "selection or follow-up criteria",
                    "expected outputs",
                ],
            ),
            (
                pr_workflow,
                ["before execution", "`pr_<id>_<slug>.md`", "current state", "transparent changes"],
            ),
            (
                project_readme_template,
                ["before claim-bearing confirmatory execution", "`pr_<id>_<slug>.md`", "current state"],
            ),
            (prfaq_template, ["before execution", "`pr_<id>_<slug>.md`", "current state"]),
        ]:
            normalized_document = normalize_for_assertion(document)
            for phrase in phrases:
                self.assertIn(phrase, normalized_document)

        self.assertIn("Exploratory Research Loop", combined)
        self.assertIn("Confirmatory Research Loop", combined)
        self.assertIn("prereg/PR_<id>_<slug>.md", combined)
        self.assertIn("claim-bearing confirmation trial", combined)
        self.assertIn("affected result has weaker diagnostic value", combined)
        self.assertIn("Every claim-bearing, externally shared, or terminal-decision", project_readme_template)
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
        self.assertNotIn("pre-registration is a confirmatory-research tool", normalize_for_assertion(combined))
        self.assertNotIn("study type", normalize_for_assertion(combined))
        self.assertIsNone(CJK_RE.search(preregistration))
        self.assertIsNone(CJK_RE.search(pr_workflow))
        self.assertIsNone(CJK_RE.search(project_readme_template))
        self.assertIsNone(CJK_RE.search(prfaq_template))
        self.assertIsNone(CJK_RE.search(preregistration_template))

    def test_process_review_uses_current_preregistration_sections(self) -> None:
        process_review = read_text("skills/research/references/review/process_review.md")
        pure_research_review_surfaces = "\n".join(
            [
                process_review,
                read_text("skills/research/references/pure_research/explanation_ledger_schema.md"),
                read_text("skills/research/references/pure_research/imrad_draft.md"),
                read_text("skills/research/references/pure_research/pr_workflow.md"),
            ]
        )
        normalized = normalize_for_assertion(process_review)
        normalized_surfaces = normalize_for_assertion(pure_research_review_surfaces)

        for phrase in [
            "Confirmatory pre-registration",
            "Exploratory pre-registration",
            "Study Information",
            "Hypotheses",
            "Design Plan",
            "Analysis Plan",
            "Inference / Decision Criteria",
            "Data Exclusion / Missing Data Handling",
            "Exploratory Objective",
            "Exploration Scope",
            "Allowed Transformations / Procedures",
            "Expected Outputs",
            "Transparent Changes",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "preregistration.md` § 2",
            "pre-reg § 3.5",
            "`deviation review`",
            "deviation review exit code",
            "HARKing prevention discipline",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized_surfaces)

    def test_imrad_template_uses_current_preregistration_sections(self) -> None:
        imrad_template = read_text("skills/research/assets/pure_research/imrad_draft.md.template")
        normalized = normalize_for_assertion(imrad_template)

        for phrase in [
            "Study Information",
            "Hypotheses",
            "Exploratory Objective",
            "Design Plan",
            "Exploration Scope",
            "Analysis Plan",
            "Allowed Transformations",
            "Data Exclusion / Missing Data Handling",
            "Expected Outputs",
            "Transparent Changes",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "pre-reg § 1",
            "pre-reg § 2",
            "pre-reg § 3",
            "pre-reg § 4",
            "deviation status",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_imrad_reference_and_generator_use_current_preregistration_sections(self) -> None:
        surfaces = [
            read_text("skills/research/references/pure_research/imrad_draft.md"),
            read_text("skills/research/assets/pure_research/imrad_draft.md.template"),
            read_text("skills/research/scripts/draft_imrad.py"),
        ]

        for document in surfaces:
            normalized = normalize_for_assertion(document)
            for phrase in [
                "Study Information",
                "Hypotheses",
                "Exploratory Objective",
                "Design Plan",
                "Exploration Scope",
                "Analysis Plan",
                "Allowed Transformations",
                "Data Exclusion / Missing Data Handling",
                "Expected Outputs",
                "Transparent Changes",
            ]:
                self.assertIn(normalize_for_assertion(phrase), normalized)

        combined = normalize_for_assertion("\n".join(surfaces))
        for forbidden in [
            "Deviations from pre-registration",
            "Competing explanations (≥2 + null)",
            "1. Question",
            "2. Competing explanations",
            "3. Test design",
            r"1\.\s*Question",
            r"2\.\s*Competing\s*explanations",
            r"3\.\s*Test\s*design",
            "pre-reg §",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), combined)

    def test_promotion_gate_uses_transparent_changes_for_preregistration_changes(self) -> None:
        promotion_gate = read_text("skills/research/references/pure_research/pr_promotion_gate.md")
        normalized = normalize_for_assertion(promotion_gate)

        for phrase in [
            "Transparent Changes",
            "No material changes from the preregistration.",
            "Description of change",
            "Rationale",
            "Effect on study results or conclusions",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "Deviation status",
            "per-deviation `decisions.md` entry",
            "deviation severity",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_conclusion_review_uses_current_preregistration_claim_checks(self) -> None:
        conclusion_review = read_text("skills/research/references/review/conclusion_review.md")
        normalized = normalize_for_assertion(conclusion_review)

        for phrase in [
            "Hypotheses",
            "Inference / Decision Criteria",
            "Transparent Changes",
            "claim wording",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "evidence_type",
            "preregistration.md` § 2",
            "preregistration.md § 2",
            "Pre-reg evidence_type",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_new_trial_replaces_legacy_and_current_prereg_placeholders(self) -> None:
        new_trial = load_module("skills/research/scripts/new_trial.py")
        expected_placeholders = [
            "<REPLACE: optional prereg/PR_<id>.md>",
            "<REPLACE: optional prereg/PR_<id>_<slug>.md>",
            "<REPLACE: optional prereg reference>",
        ]
        content = "\n".join(f"placeholder: {placeholder}" for placeholder in expected_placeholders)

        rendered = new_trial.substitute_pr(
            content,
            prereg_id="PR_001_initial",
            question_id=None,
            discriminating=None,
            slug="alpha",
            nnn="001",
            project_name="project",
            workstream="WS001-phenomenon",
        )

        self.assertEqual(
            rendered.count("workstreams/WS001-phenomenon/prereg/PR_001_initial.md"),
            len(expected_placeholders),
        )
        for placeholder in expected_placeholders:
            self.assertNotIn(placeholder, rendered)

    def test_new_trial_exposes_single_template_prereg_placeholder_contract(self) -> None:
        new_trial = load_module("skills/research/scripts/new_trial.py")
        template = read_text("skills/research/assets/pure_research/pr_trial.py.template")

        self.assertIn("<REPLACE: optional prereg reference>", new_trial.PREREG_PLACEHOLDERS)
        self.assertEqual(
            (
                "<REPLACE: optional prereg reference>",
                "<REPLACE: optional prereg/PR_<id>.md>",
                "<REPLACE: optional prereg/PR_<id>_<slug>.md>",
            ),
            new_trial.PREREG_PLACEHOLDERS,
        )
        self.assertEqual(
            ["<REPLACE: optional prereg reference>"],
            [placeholder for placeholder in new_trial.PREREG_PLACEHOLDERS if placeholder in template],
        )

    def test_new_trial_next_steps_match_current_preregistration_reporting(self) -> None:
        new_trial = read_text("skills/research/scripts/new_trial.py")
        normalized = normalize_for_assertion(new_trial)

        self.assertIn("pr_001_initial", normalized)
        self.assertIn("transparent changes", normalized)
        self.assertNotIn("deviation review note", normalized)
        self.assertNotIn("drifted from pr_001_initial", normalized)

    def test_review_docs_point_to_pr_trial_analysis_section(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/references/shared/analysis_depth.md"),
                read_text("skills/research/references/shared/result_analysis.md"),
                read_text("skills/research/references/review/conclusion_review.md"),
            ]
        )

        self.assertNotIn("pr_trial.py.template § 6", combined)
        self.assertNotIn("§ 5.3 / 6.3", combined)
        self.assertNotIn("§ 6.3", combined)
        self.assertIn("assets/pure_research/pr_trial.py.template` § 5", combined)

    def test_trial_template_generator_comments_match_new_trial_cli(self) -> None:
        pure_template = read_text("skills/research/assets/pure_research/pr_trial.py.template")
        rd_template = read_text("skills/research/assets/rd/rd_trial.py.template")

        self.assertIn(
            "Generated by `scripts/new_trial.py` for a Phenomenon / Mechanism Research workstream.",
            pure_template,
        )
        self.assertIn(
            "Generated by `scripts/new_trial.py` for an R&D Workstream.",
            rd_template,
        )
        self.assertNotIn("--mode", pure_template)
        self.assertNotIn("--mode", rd_template)

    def test_retired_root_readme_points_to_actual_mixed_readme_template(self) -> None:
        template = read_text("skills/research/assets/README.md.template")

        self.assertIn("assets/shared/README.md.template", template)
        self.assertNotIn("assets/shared/project_state.md.template", template)

    def test_preregistered_outcome_reports_use_lightweight_package_shape(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        root_readme = read_text("README.md")
        outcome_report = read_text("skills/research/references/shared/outcome_reports.md")
        outcome_report_template = read_text("skills/research/assets/shared/outcome_report.md.template")
        readme_template = read_text("skills/research/assets/pure_research/README.md.template")
        combined = "\n".join([skill, root_readme, outcome_report, outcome_report_template, readme_template])
        normalized = normalize_for_assertion(combined)

        core_shape_phrases = [
            "Required core files",
            "results/reports/",
            "RPT_<id>_<slug>",
            "report.md",
            "report.html",
            "figures/",
            "tables/",
            "attachments/",
            "required core directories may be empty",
        ]
        optional_shape_phrases = [
            "Optional / situation-specific files",
            "report.pdf is optional snapshot/export",
            "provenance/ for claim-bearing or L2/L3 reports",
            "manifest.json",
            "integrity_checks.md",
            "rerun.md",
            "L2/L3 reports means claim-bearing reports and state-promotion or terminal-decision report packages",
            "report package level, not analysis tier",
            "report.html is the primary readable artifact for l2/l3 reports",
            "report.md is editable source",
        ]

        assert_phrases_present(self, outcome_report, core_shape_phrases + optional_shape_phrases)
        assert_phrases_present(self, outcome_report_template, core_shape_phrases + optional_shape_phrases)
        assert_phrases_present(self, readme_template, core_shape_phrases + optional_shape_phrases)
        assert_phrases_present(
            self,
            skill,
            [
                "required core files: `report.md`, `report.html`, `figures/`, `tables/`, and `attachments/`",
                "report.pdf is optional snapshot/export",
                "provenance/` only for claim-bearing or L2/L3 reports",
            ],
        )
        assert_phrases_present(
            self,
            combined,
            [
                "Plan-to-Result Table",
                "Transparent Changes",
                "Scope / Limitations",
                "planned_item | executed_as_planned | result_summary | evidence | notes",
            ],
        )

        for phrase in [
            "Description of change",
            "Rationale",
            "Effect on study results or conclusions",
            "No material changes from the preregistration.",
        ]:
            self.assertIn(phrase, combined)

        self.assertIn("External tracker run IDs are optional", combined)
        self.assertIn("External tracker run ID: <omit unless a tracker was actually used>", combined)
        self.assertNotIn("external tracker run id is required", normalized)
        for forbidden in [
            "report.pdf is the provided report artifact",
            "with report.md, report.pdf",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

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

    def test_reproducibility_contract_mentions_claim_bearing_reports(self) -> None:
        reproducibility = read_text("skills/research/references/shared/reproducibility.md")

        self.assertIn("claim-bearing report package", reproducibility)
        self.assertIn("presented evidence", reproducibility)

    def test_exploratory_runs_must_rerun_before_claim_bearing_citation(self) -> None:
        skill = read_text("skills/research/SKILL.md")

        self.assertNotIn("retroactively relabel exploratory output as complete", skill)
        self.assertIn("rerun under the claim-bearing plan", skill)

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
