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

## Workflow

1. **Read the plan**  
   Identify the question/objective, Plan, Actual execution, Planned vs Actual, References, and any existing Observations. Note material deviations and the claim or decision pressure if present.

2. **Reconstruct evidence**  
   Follow plan references to runs, `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, scripts, configs, outputs, tables, figures, reports, and literature entries. Verify that cited artifact paths exist when filesystem access is available. If a referenced item is missing or ambiguous, record it under `context_missing`.

3. **Analyze**  
   Separate literal observations from interpretations. Apply the disclosure floor appropriate to the claim type: leakage probes, stochastic variance, comparator fairness, ablations, slice checks, calibration, perturbation, error analysis, robustness, or theoretical limiting-case checks when relevant. Do not turn exploratory observations into confirmatory conclusions.

4. **Return**  
   Return a plan-ready `## Result analysis` section. Use artifact paths, numeric values, table/figure references, and missing-context entries that a research-review agent can inspect.

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
| Collapsing observation and interpretation | Write literal artifact facts first, then interpretations separately. |
