# AGENTS.md

This repository contains the `research` Codex/Claude Code plugin and its related skills. Keep this file practical and update it when repeated agent mistakes reveal a durable project rule.

Always use the OpenAI developer documentation MCP server if you need to work with the OpenAI API, ChatGPT Apps SDK, Codex, or related docs without me having to explicitly ask.

## Repository Layout

- `.codex-plugin/plugin.json` is the plugin manifest. Update it when the public plugin protocol, version, or user-facing description changes.
- `skills/research/` owns the proposition-first research lifecycle.
- `skills/research-plan-review/` owns independent pre-execution plan review.
- `skills/research-result-analysis/` owns independent post-execution result analysis.
- `skills/quant-research/` extends `research` for time-series and quantitative R&D.
- `tests/test_research_docs_contract.py` protects stable repository and script contracts.
- `tests/test_multiple_testing.py` covers the quant multiple-testing implementation.

## Working Agreements

- Work on a feature branch.
- When work is complete, inspect the full diff, run relevant checks, commit, push, and update the PR.
- Do not refuse to commit or push just because some requested changes were made by another tool or agent. If the user asks to ship the current task scope, treat the relevant working tree state as the task output.
- Do not revert unrelated user or agent changes unless explicitly asked. If unrelated changes make the task ambiguous, inspect the diff and explain the boundary before proceeding.
- Prefer concise, factual English in repository documentation unless the user explicitly requests another language.

## Build And Test Commands

- Run all tests: `python -m pytest`
- Run research contract tests only: `python -m pytest tests/test_research_docs_contract.py`
- Run quant multiple-testing tests only: `python -m pytest tests/test_multiple_testing.py`
- Validate plugin manifest JSON: `python -m json.tool .codex-plugin/plugin.json`
- Check staged or unstaged whitespace issues: `git diff --check`

## Test Admission Gate

Before adding or changing tests, classify the work:

- Behavior / public contract change
- Bug regression
- Characterization / protection test
- Documentation contract
- Release / packaging / cache operation
- Refactor only

Add repository tests only when they protect externally observable contracts that should remain true across future versions.

Good repository-test targets:

- Public script inputs, outputs, generated files, and failure modes.
- Required template structure.
- Generated project layouts.
- Mechanical release-quality gates such as CJK text checks for distributed English skill docs.
- Stable public surface checks, such as ensuring removed commands do not reappear.

Do not add repository tests for:

- Current version numbers.
- Release checklist state.
- Cache or installation state.
- PR, push, or merge state.
- Implementation path preferences.
- Non-contractual wording.
- Preferred `SKILL.md` phrasing enforced through string-search tests.

For release, packaging, cache, or plugin metadata work, use verification commands and report evidence instead of adding tests.

## Skill Documentation Testing

Do not confuse skill pressure testing with repository unit tests.

For `SKILL.md` behavior, use subagent pressure scenarios:

- Give the subagent only the skill content and the scenario.
- Hide the SPEC and expected answer.
- Check whether the agent makes the intended judgment under pressure.
- Record the observed failure or rationalization as the RED evidence.
- Tighten the skill text only after the failure mode is clear.

Examples of skill-pressure failures:

- The agent jumps from a vague topic directly to hypotheses.
- The agent creates a hypothesis plan from an `under-specified`, `split-needed`, `split`, `closed`, or `contradicted` proposition.
- The agent writes a plausible candidate where the lifecycle should require `None: <reason>` or material acquisition.

Do not add brittle repository tests that merely assert a sentence exists in `SKILL.md`.

## Research Lifecycle Rules

The plugin is proposition-first.

- The top-level research unit is a proposition, not a plan.
- A hypothesis plan tests exactly one derived hypothesis under a parent proposition.
- Do not generate hypotheses directly from a vague topic.
- If there is material absence, create a material-acquisition task instead of a proposition or hypothesis.
- `under-specified`, `split-needed`, `split`, `closed`, and `contradicted` parent propositions are not plan-ready.
- `research-plan-review` and `research-result-analysis` both start from the plan path and reconstruct local state from referenced files.
- Result analysis does not choose final proposition or hypothesis decisions. The parent workflow updates ledgers after reviewing result-analysis evidence.

## Plugin Version Updates

When the public protocol or lifecycle changes:

- Bump `.codex-plugin/plugin.json` according to the size of the public behavior change.
- Update `description`, `interface.shortDescription`, and `interface.longDescription` so they match current behavior.
- Keep version-number checks out of repository tests.
- Run JSON validation and the relevant pytest suite before committing.

## Definition Of Done

Before reporting completion:

- The diff matches the requested scope.
- Relevant tests or verification commands have been run and read.
- `git diff --check` is clean.
- The work is committed and pushed when the user requested PR-ready work.
- The final response names the commit, branch, PR state, and verification evidence.
