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


class ProjectBoundaryTests(unittest.TestCase):
    def test_plugin_version_metadata_is_consistent(self) -> None:
        expected = "1.1.8"
        codex_plugin = json.loads(read_text(".codex-plugin/plugin.json"))
        claude_plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        claude_marketplace = json.loads(read_text(".claude-plugin/marketplace.json"))
        readme = read_text("README.md")

        self.assertEqual(expected, codex_plugin["version"])
        self.assertEqual(expected, claude_plugin["version"])
        self.assertEqual(expected, claude_marketplace["plugins"][0]["version"])
        self.assertIn(f"### v{expected} (current)", readme)

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
            workstream = project / "workstreams" / "WS001-capability"
            for path in [
                "project_state.md",
                "workstreams/WS001-capability/charter.md",
                "workstreams/WS001-capability/capability_map.md",
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
            self.assertTrue(workstream.exists())

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
                    "WS001-capability",
                    "Capability / Technology Research workstream",
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
            cap_project = Path(tmp) / "cap"
            cap_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/render_capability_dag.py"),
                    "--project-dir",
                    str(cap_project),
                    "--workstream",
                    "WS001-capability",
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertEqual(cap_result.returncode, 0, cap_result.stderr)
            self.assertIn("flowchart", cap_result.stdout)

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
            "does not re-score trl, support status, or a-tier",
            "phenomenon / mechanism research",
            "capability / technology research",
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
            capability = project / "workstreams" / "WS002-capability"
            phenomenon = project / "workstreams" / "WS001-phenomenon"
            capability.mkdir(parents=True)
            phenomenon.mkdir(parents=True)
            (capability / "charter.md").write_text("# Charter\n", encoding="utf-8")
            (capability / "capability_map.md").write_text("# Capability Map\n", encoding="utf-8")
            (phenomenon / "prfaq.md").write_text("# PR/FAQ\n", encoding="utf-8")
            (phenomenon / "explanation_ledger.md").write_text("# Explanation Ledger\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/research/scripts/new_trial.py"),
                    "--project-dir",
                    str(project),
                    "--workstream",
                    "WS002-capability",
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
                "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | WS002-capability | in-progress | pending |",
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
                "Capability / Technology Research",
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
                "Capability / Technology Research",
                "Phenomenon / Mechanism Research",
            ],
            state_options,
        )

    def test_capability_entry_guidance_does_not_overclassify_or_ban_scaffolding(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/SKILL.md"),
                read_text("skills/research/references/rd/rd_workflow.md"),
                read_text("skills/research/references/review/process_review.md"),
            ]
        )
        normalized = normalize_for_assertion(combined)

        for phrase in [
            "do not classify the whole project as capability / technology research",
            "provisional workstream fit",
            "non-load-bearing scaffold",
            "interface probe",
            "smoke test",
            "promotion-relevant or claim-bearing implementation",
            "wait until the charter and kill criteria exist",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

        for forbidden in [
            "Capability / Technology Research first day: no implementation",
            "Capability / Technology Research first day permits **only**",
            "Any implementation that runs",
            "Day 1 implementation",
            "Code commits before charter",
        ]:
            self.assertNotIn(normalize_for_assertion(forbidden), normalized)

    def test_new_trial_rejects_mixed_artifacts_inside_one_workstream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "alpha"
            (project / "purposes").mkdir(parents=True)
            (project / "workstreams" / "WS999-ambiguous").mkdir(parents=True)
            ambiguous = project / "workstreams" / "WS999-ambiguous"
            (ambiguous / "capability_map.md").write_text("# Capability Map\n", encoding="utf-8")
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
            (external / "capability_map.md").write_text("# Capability Map\n", encoding="utf-8")
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
            row = "| trial_001 | rd | purposes/trial_001_latency_benchmark.py | WS001-capability | in-progress | pending |"
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

    def test_process_review_uses_workstream_labels_not_project_modes(self) -> None:
        process_review = read_text("skills/research/references/review/process_review.md")

        self.assertIn("Workstream label is explicitly declared", process_review)
        self.assertIn("Capability / Technology Research workstream", process_review)
        self.assertIn("Phenomenon / Mechanism Research workstream", process_review)
        for phrase in [
            "Mode is explicitly declared",
            "Mode field",
            "No mode mixing",
            "Mode mixing",
            "For R&D projects only",
            "For Pure Research projects only",
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
        stages = read_text("skills/research/references/rd/rd_stages.md")

        self.assertNotIn("A kill criterion firing once is sufficient to kill", skill)
        self.assertNotIn("Go/Kill gate", skill)
        self.assertNotIn("de-risk to kill", skill)
        self.assertNotIn("default to Kill under uncertainty", stages)
        self.assertIn("Kill requires A4+ evidence", skill)
        self.assertIn("Default to Hold or Recycle under uncertainty", stages)
        self.assertIn("Re-scope", stages)

    def test_a4_rigor_is_reserved_for_claim_bearing_or_promotion_decisions(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        normalized = normalize_for_assertion(skill)

        for phrase in [
            "a4+ is reserved for supported, matured, established, promoted, external claim, or deployment recommendation",
            "a2-a3 may decide the next experiment, provisional go / no-go, park, deprioritize, or reject-for-now",
            "exploratory decisions do not create a load-bearing claim or promotion",
        ]:
            self.assertIn(phrase, normalized)

    def test_kill_a4_requirement_does_not_cover_exploratory_pruning(self) -> None:
        combined = "\n".join(
            [
                read_text("skills/research/SKILL.md"),
                read_text("skills/research/references/rd/capability_map_schema.md"),
                read_text("skills/research/references/rd/rd_stages.md"),
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
            "Use for serious research or capability/technology workstreams",
            "Do not use for ordinary fact lookup",
            "First Decision: Map the Current Research State",
            "project decision gate",
            "Capability / Technology Research",
            "Phenomenon / Mechanism Research",
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

    def test_evidence_citation_covers_established_core_technology_claims(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        normalized = normalize_for_assertion(skill)

        self.assertIn(
            "supports `supported`, `matured`, `established`, `promoted`, `killed`",
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
            "finance-specific checks are promotion-relevant or claim-bearing checks",
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
        rd_stages = read_text("skills/research/references/rd/rd_stages.md")
        result_analysis = read_text("skills/research/references/shared/result_analysis.md")

        self.assertIn("Result-to-Question Loop", pr_workflow)
        self.assertIn("explanation_ledger.md", pr_workflow)
        self.assertIn("Result-to-Capability Loop", rd_stages)
        self.assertIn("capability_map.md", rd_stages)
        normalized_result_analysis = " ".join(result_analysis.split())
        self.assertIn("selected workstream state object", normalized_result_analysis)
        self.assertIn("Phenomenon / Mechanism Research", result_analysis)
        self.assertIn("Capability / Technology Research", result_analysis)
        self.assertNotIn("mode-specific state object", result_analysis)
        self.assertNotIn("Pure Research returns to Q/E state", result_analysis)
        self.assertNotIn("R&D returns to capability state", result_analysis)
        self.assertIn("goalpost shifting", rd_stages)
        self.assertIn("prospective re-scope", rd_stages)

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
        content = "\n".join(
            [
                "legacy: <REPLACE: optional prereg/PR_<id>.md>",
                "current: <REPLACE: optional prereg/PR_<id>_<slug>.md>",
                "generic: <REPLACE: optional prereg reference>",
            ]
        )

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
            3,
        )
        self.assertNotIn("<REPLACE: optional prereg/PR_<id>.md>", rendered)

    def test_new_trial_next_steps_match_current_preregistration_reporting(self) -> None:
        new_trial = read_text("skills/research/scripts/new_trial.py")
        normalized = normalize_for_assertion(new_trial)

        self.assertIn("pr_001_initial", normalized)
        self.assertIn("transparent changes", normalized)
        self.assertNotIn("deviation review note", normalized)
        self.assertNotIn("drifted from pr_001_initial", normalized)

    def test_preregistered_outcome_reports_use_lightweight_package_shape(self) -> None:
        skill = read_text("skills/research/SKILL.md")
        outcome_report = read_text("skills/research/references/shared/outcome_reports.md")
        outcome_report_template = read_text("skills/research/assets/shared/outcome_report.md.template")
        new_project = read_text("skills/research/scripts/new_project.py")
        combined = "\n".join([skill, outcome_report, outcome_report_template, new_project])
        normalized = normalize_for_assertion(combined)

        for phrase in [
            "results/reports/",
            "RPT_<id>_<slug>",
            "report.md",
            "report.pdf",
            "figures/",
            "tables/",
            "attachments/",
            "Plan-to-Result Table",
            "Transparent Changes",
            "Scope / Limitations",
            "planned_item | executed_as_planned | result_summary | evidence | notes",
        ]:
            self.assertIn(normalize_for_assertion(phrase), normalized)

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
