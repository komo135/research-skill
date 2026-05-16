---
name: research-result-analysis
description: Use when analyzing completed R&D plan results from a plan path, especially before research claims, state-changing decisions, or reports, and when an independent agent must reconstruct evidence without parent-agent summaries.
---

# Research Result Analysis

## Overview

Independent result analysis for a completed research plan. The plan path is the only starting context; the agent reconstructs evidence from referenced artifacts and returns staged analysis, not final claims or decisions.

## Core Rule

Treat the plan as the only starting context. Do not rely on parent-agent summaries, expected conclusions, private notes, or unstated expectations. If the plan does not identify enough evidence to support analysis, report `context_missing` instead of guessing.

This skill owns analysis only. Do not write final claims, do not choose iteration decisions, and do not draft human-facing reports.

## Required Reference

Before judging claim-readiness, read `skills/research/references/analysis.md` from this plugin. Apply its artifact contract, disclosure floor, analysis depth stop rule, Observation → Interpretation → Claim staging, and Pearl ladder constraint.

Minimum evidence rule: stdout is not evidence. A completed run needs `run_manifest.json`, captured logs, and at least one manifest-listed non-log durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`. If the plan points only to terminal text or missing files, record `context_missing` and do not mark the result `ready`.

## Workflow

1. **Read the plan**  
   Identify the question/objective, Plan, Actual execution, Planned vs Actual, References, and any existing Observations. Note material deviations and the claim or decision pressure if present.

2. **Reconstruct evidence**  
   Follow plan references to runs, `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, scripts, configs, outputs, tables, figures, reports, and literature entries. Verify that cited artifact paths exist when filesystem access is available. If a referenced item is missing or ambiguous, record it under `context_missing`.

3. **Analyze**  
   Separate literal observations from interpretations. Apply the disclosure floor appropriate to the claim type: leakage probes, stochastic variance, comparator fairness, ablations, slice checks, calibration, perturbation, error analysis, robustness, or theoretical limiting-case checks when relevant. Do not turn exploratory observations into confirmatory conclusions.

4. **Return**  
   Return a plan-ready `## Result analysis` section. Use artifact paths, numeric values, table/figure references, and missing-context entries that a research-review agent can inspect.

## Claim-readiness verdicts

- `ready`: the applicable disclosure floor is met, evidence is durable and artifact-grounded, alternatives and untested conditions are named, and no missing context or reliability issue blocks the planned claim strength.
- `not_ready`: the result may be usable later, but required analysis, artifacts, comparators, variance, controls, robustness checks, or context are missing and repairable.
- `invalid_evidence`: a script bug, data defect, leakage, invalid procedure, broken comparator, corrupted artifact, or unrecoverable provenance gap may have distorted the result. The affected result is not claim evidence until repaired and rerun.

Do not mark causal, mechanism, or counterfactual claim-readiness from association-only evidence. Pearl ladder applies: diagnostic correlation is not enough for intervention or counterfactual claims.

## Analysis quality gate

Do not score depth by length, number of caveats, or how many extra checks are proposed. Score it by whether the analysis is sufficient for the claim strength under review and stops before over-analysis.

A result analysis is acceptable only when it is:

| Check | Requirement |
|---|---|
| artifact-faithful | Every observation traces to a plan reference or inspected artifact; missing files become `context_missing`. |
| arithmetically checked | Deltas, thresholds, counts, seed summaries, and sample-size statements are recomputed or explicitly marked unavailable. |
| claim-fit checked | The evidence type matches the requested claim strength, mode, and Pearl rung; association-only evidence cannot support intervention or counterfactual claims. |
| depth-calibrated | The applicable disclosure floor is applied, required alternatives are named, and additional analysis is limited to blockers for this claim. |
| reviewable | A later reviewer can identify each required observation, forbidden conclusion, required missing context, and verdict rationale without re-inferring the analysis. |

For pressure-test and review scenarios, compare the output against an answer key with:

- required observation: artifact facts that must appear for the analysis to be correct
- forbidden conclusion: claims, GO/NO-GO decisions, causal leaps, or final reports the analyzer must not write
- required missing context: absent artifacts, comparators, logs, scripts, or controls that must be named
- verdict expectation: `ready`, `not_ready`, or `invalid_evidence`, with the blocking reason
- depth boundary: checks required before the planned claim, and checks that would be over-analysis for this claim

Claim-readiness is not a release decision. Never translate `ready`, `not_ready`, or `invalid_evidence` into GO/NO-GO, ship, CLOSE, NEXT_STEP, REFINE, ADJACENT, or PARK. State implications for evidence only; the parent research protocol decides actions.

## Output Shape

```markdown
## Result analysis

### Analyzer
- Agent: <fresh separate-context result-analysis subagent>
- Skill: research-result-analysis
- Only starting context: <plan path>
- Analyzed at: <YYYY-MM-DD>

### Evidence traced
- Plan: <plan path>
- Runs and artifacts: <manifest/log/output/table/figure/script paths inspected>
- context_missing: <None, or missing/ambiguous plan references, artifacts, logs, scripts, metrics, comparators, or literature entries>

### Observations
- <literal artifact-grounded fact; no interpretation>

### Interpretations
- <possible explanation of observations; include uncertainty>

### Alternatives not excluded
- <plausible explanation, confound, leakage path, comparator issue, missing control, untested condition, or theoretical gap>

### Required additional analysis
- <None, or named analysis/rerun/repair required before a claim, decision, or report>

### Claim-readiness assessment
- <ready / not_ready / invalid_evidence>: <rationale tied to evidence, missing context, and alternatives>
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Using a parent-agent summary as evidence | Ignore it; trace the plan and artifacts directly. |
| Treating missing references as harmless | Record `context_missing` and narrow or block claim readiness. |
| Writing final claims | Return claim-readiness only; the parent research protocol records claims. |
| Choosing `NEXT_STEP`, `REFINE`, `ADJACENT`, `PARK`, or `CLOSE` | Explain implications, but leave iteration decisions to the parent research skill. |
| Translating analysis into GO/NO-GO | Claim-readiness is not a release decision; do not choose ship, block, or rollout actions. |
| Collapsing observation and interpretation | Write literal artifact facts first, then interpretations separately. |
