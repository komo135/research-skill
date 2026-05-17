---
name: research-result-analysis
description: Use when analyzing completed R&D plan results from a plan path, especially when an independent agent must reconstruct evidence, explain why the observed result happened, or analyze why a prediction failed without writing claims or decisions.
---

# Research Result Analysis

## Overview

Independent result analysis for a completed research plan. The plan path is the only starting context; the agent reconstructs evidence from referenced artifacts and decomposes why the result happened. When the result missed the plan's prediction or threshold, the analysis must also explain why it failed.

This skill does not decide what can be claimed, whether to ship, or which iteration branch to choose.

Result analysis produces **post-result explanations** after evidence exists. It is not a continuation of planning and not a place to create **pre-result commitments** retroactively; result-analysis outputs are not pre-result commitments. The plan should already contain the question, prediction or expected observation, primary measure, planned discriminating test, evidence route, and artifact expectations.

## Core Rule

Treat the plan as the only starting context. Do not rely on parent-agent summaries, expected conclusions, private notes, or unstated expectations. If the plan does not identify enough evidence to explain the result, report `context_missing` and narrow the analysis.

Result analysis is not only a validity audit. Procedure defects, leakage, broken comparators, missing artifacts, and script bugs are candidate explanations for the observed result, not separate verdict labels. Failed predictions require failed-prediction analysis: observed gap plus live candidate explanations, not a note that the threshold was missed and not forced category labels.

This skill owns analysis only. Do not write final claims, do not choose iteration decisions, do not assess readiness for promotion, and do not draft human-facing reports.

## Required Reference

Before analyzing, read `skills/research/references/analysis.md` from this plugin. Apply its artifact contract, analysis depth stop rule, Observation -> Interpretation -> Claim staging, and Pearl ladder constraint.

Minimum evidence rule: stdout is not evidence. A completed run needs `run_manifest.json`, captured logs, and at least one manifest-listed non-log durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`. If the plan points only to terminal text or missing files, treat artifact/provenance failure as a live procedure / artifact explanation and record `context_missing`.

## Workflow

1. **Read the plan**
   Identify the question/objective, Plan, Actual execution, Planned vs Actual, References, and any existing observations. Note material deviations and any pressure to produce a claim or decision.

2. **Reconstruct evidence**
   Follow plan references to runs, `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, scripts, configs, outputs, tables, figures, reports, and literature entries. Verify that cited artifact paths exist when filesystem access is available. If a referenced item is missing or ambiguous, record it under `context_missing`.

3. **Describe what happened**
   Separate literal observations from interpretation. Describe the result shape before explaining it: aggregate movement, slices, seed variability, failures, anomalies, traces, and condition-specific effects.

4. **Decompose why**
   Generate candidate explanations for why the result happened. Include procedure / artifact explanations when relevant: leakage, split mismatch, broken comparator, script bug, measurement artifact, missing provenance, or stdout-only evidence. For each candidate explanation, record supporting evidence, contradicting evidence, and the missing discriminator.

   If the observed result missed the plan's prediction, threshold, or expected effect, construct failed-prediction analysis. Start from the observed gap, then generate candidate explanations for why the prediction missed. Use premise / mechanism, approach / intervention, procedure / artifact / data / comparator / implementation / measurement, and evaluation / power / metric / scope as coverage lenses only. Do not force every lens into the output and do not assign a single verdict category. Record only live explanations with why they could explain the miss, evidence for and against, what would be true if they are correct, and the missing discriminator.

5. **Return**
   Return a plan-ready `## Result analysis` section. Use artifact paths, numeric values, table/figure references, and missing-context entries that the parent research agent can inspect before writing claims or decisions.

## Analysis Quality Gate

Do not score depth by length, number of caveats, or how many extra checks are proposed. Score it by whether the analysis decomposes the result into plausible causes and stops before over-analysis.

A result analysis is acceptable only when it is:

| Check | Requirement |
|---|---|
| artifact-faithful | Every observation traces to a plan reference or inspected artifact; missing files become `context_missing`. |
| arithmetically checked | Deltas, thresholds, counts, seed summaries, and sample-size statements are recomputed or explicitly marked unavailable. |
| explanation-fit checked | Candidate explanations are compared against evidence for and against them; missing discriminating tests are explicit. |
| depth-calibrated | Additional analysis is limited to discriminators needed to separate live candidate explanations. |
| reviewable | A later reader can identify each required observation, candidate explanation, required missing context, and proposed discriminator without re-inferring the analysis. |

For pressure-test and review scenarios, compare the output against an answer key with:

- required observation: artifact facts that must appear for the analysis to be correct
- candidate explanations: plausible causes for the observed result, including procedure / artifact explanations
- failed-prediction analysis when prediction missed: observed gap plus live candidate failure explanations; coverage lenses are checked but not forced into verdict categories
- evidence for / against each explanation: supporting evidence and contradicting evidence listed separately
- required missing context: absent artifacts, comparators, logs, scripts, controls, slices, traces, or failure samples
- discriminating analysis: tests, ablations, slices, trace checks, perturbations, failure samples, or theoretical checks that would separate live explanations
- forbidden conclusion: claims, promotion-readiness assessments, deployment decisions, iteration branches, or final reports

## Explanation Analysis Contract

Result analysis is not only a validity audit. After evidence is reconstructed, explain why the result happened using this sequence:

1. **What happened**: aggregate movement, slice differences, seed variability, failures, anomalies, traces, and condition-specific effects.
2. **Prediction comparison**: compare observed values to planned predictions, thresholds, support requirements, and expected conditions.
3. **Candidate explanations**: at least two plausible causes when artifacts permit them. Include null, procedure, or artifact explanations when relevant.
4. **Failed-prediction analysis when prediction missed**: explain why the result fell short from the observed gap through live candidate explanations. Use premise/mechanism, approach/intervention, procedure/artifact/data, and evaluation/power/metric only as coverage lenses, not required verdict categories.
5. **Evidence for / against each explanation**: cite support and contradiction separately. Do not hide contradicting evidence in generic limitations.
6. **Procedure / artifact explanations**: explicitly consider whether the observed result could come from research execution mistakes, evaluation defects, leakage, broken comparators, or missing evidence.
7. **Alternatives still live**: explanations not yet excluded.
8. **Discriminating next analyses**: the smallest additional analysis that would separate the leading explanations.

Association-only evidence can motivate an explanation candidate, but it does not establish a mechanism. Pearl ladder applies: diagnostic correlation is not enough for intervention or counterfactual explanation.

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
- context_missing: <None, or missing/ambiguous plan references, artifacts, logs, scripts, metrics, comparators, controls, slices, traces, or failure samples>

### What happened
- <literal artifact-grounded fact about aggregate result, slices, seeds, failures, traces, anomalies, or conditions>

### Prediction comparison
- <planned prediction / threshold / expected condition versus observed value; note whether the prediction was met, missed, reversed, or only partly satisfied>

### Candidate explanations
- <candidate cause>
  - Evidence for: <artifact-grounded support>
  - Evidence against: <artifact-grounded contradiction or weakness>
  - Missing discriminator: <what would separate this from alternatives>

### Failed prediction analysis
- Observed gap: <prediction, threshold, or expected condition versus observed result>
- Candidate failure explanations:
  - <candidate explanation for why the prediction missed>
    - Why this could explain the miss: <mechanism connecting evidence to the missed prediction>
    - Evidence for: <artifact-grounded support>
    - Evidence against: <artifact-grounded contradiction or weakness>
    - What would be true if this explanation is correct: <testable implication>
    - Missing discriminator: <smallest analysis that would separate this explanation from alternatives>
- Coverage check: <which lenses were considered: premise/mechanism, approach/intervention, procedure/artifact/data/comparator/implementation/measurement, evaluation/power/metric/scope. Do not force a category; record only live explanations above.>

### Procedure / artifact explanations
- <whether leakage, split mismatch, broken comparator, script bug, measurement artifact, missing provenance, or stdout-only evidence could explain the result>

### Alternatives still live
- <plausible explanation, confound, missing control, untested condition, or theoretical gap not yet excluded>

### Discriminating next analyses
- <smallest analysis, ablation, slice, trace check, perturbation, failure sample, theoretical check, repair, or rerun that would separate live explanations>
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Using a parent-agent summary as evidence | Ignore it; trace the plan and artifacts directly. |
| Treating missing references as harmless | Record `context_missing` and include missing evidence as a procedure / artifact explanation when it can explain the observation. |
| Writing final claims | Return why-analysis only; the parent research protocol records claims. |
| Choosing `NEXT_STEP`, `REFINE`, `ADJACENT`, `PARK`, or `CLOSE` | Leave iteration decisions to the parent research skill. |
| Translating analysis into deployment action | Do not choose ship, block, or rollout actions. |
| Stopping at "the result is valid" | Continue to what happened, candidate explanations, evidence for/against, and discriminating next analyses. |
| Stopping at "the prediction failed" | Explain why it failed with live candidate explanations and discriminators; use failure lenses for coverage, not as forced verdict categories. |
| Putting all why-analysis into generic limitations | Evaluate candidate explanations explicitly; limitations are not a substitute for decomposition. |
