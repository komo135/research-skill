---
name: research-result-analysis
description: Use when completed R&D plan results need a why-explanation, missed-prediction root-cause analysis, or post-result mechanism analysis, especially when an agent may collapse into status labels, threshold verdicts, generic limitations, or shallow "X caused Y" summaries.
---

# Research Result Analysis

## Purpose

Independent post-result explanation for a completed hypothesis plan. The only starting context is the plan path. The job is to explain **why the observed result shape was produced** by reconstructing material, selecting the right analysis route, tracing mechanisms, and naming supported root-cause candidates or live explanatory branches.

This skill is analysis only. It does not judge whether the result is good, bad, valid, supported, contradicted, claim-ready, promotion-ready, deployment-ready, or decision-ready. The parent `research` workflow reads the analysis later and makes any hypothesis, proposition, claim, paper, or next-action decision.

## Required Reference

Before analyzing, read `references/analysis_workflow.md` in this skill. That file is the method catalog and detailed workflow. This `SKILL.md` defines how the agent moves; the reference explains the methods.

When broader research context is needed, read `../research/references/analysis.md` for shared analysis discipline, artifact expectations, and observation-to-claim staging. Do not copy downstream claim or decision behavior back into this skill.

## Core Rule

Analyze the result as an outcome to be explained, not a verdict to be assigned.

Use the planned prediction only to locate the explanatory contrast. A threshold pass, threshold miss, aggregate improvement, or apparent prediction hit is not an analysis. Even a "hit" requires a why-analysis: did the predicted mechanism generate the result, or did a slice, evaluator, artifact, or interaction make the aggregate look right for another reason?

Forbidden outputs:

- hypothesis status or proposition status recommendations
- `State-update inputs`
- `supported`, `contradicted`, `tested-supported`, `tested-contradicted`, `tested-partial`, or `tested-inconclusive` labels
- promotion readiness, claim readiness, deployment recommendation, or iteration branch
- final claims or human-facing paper prose
- an evidence verdict that replaces the explanation

## Agent Workflow

1. **Reconstruct the material boundary**
   Start from the plan path only. Inspect the plan, sibling `hypothesis.md`, referenced proposition material, Actual execution, Planned vs Actual, runs, manifests, logs, outputs, tables, traces, configs, scripts, and proposition `paper.md` when available. Do not treat parent-agent summaries, user summaries, private notes, or unstated expectations as material unless the plan or a plan-referenced artifact contains them.

2. **Build a result-feature ledger before explaining**
   Inventory aggregate movement, slices, regimes, seeds or repetitions, traces over time, concentrated failures or successes, anomalies, state transitions, resource patterns, and condition-specific effects. For prediction or forecasting results, include error sign, magnitude, horizon, residual behavior, calibration, tail cases, and train/validation/test differences when available. Unevenness is usually the key material.

3. **Select the explanatory target**
   Name the result feature that needs explanation. Common targets are: apparent aggregate hit with slice regressions, missed prediction, partial or mixed result, system tail behavior, single-run stochastic surprise, implementation-change regression, distribution shift, evaluator artifact, or mechanism claim not isolated by the run.

4. **Route to the right methods**
   Pick the smallest set of methods from `references/analysis_workflow.md` that can explain the target. Do not run every lens mechanically.

   | Observed shape | Primary route |
   |---|---|
   | Aggregate hit but slices disagree | Apparent-hit and mixed-results workflow |
   | Prediction missed or reversed | Missed-prediction workflow |
   | Forecast or temporal error | Forecast-error diagnostics plus slice/regime analysis |
   | Degradation under changed data | Distribution-shift decomposition |
   | One seed/run surprises | Variance-source analysis before mechanism claims |
   | New code/config/procedure changed outcome | Change analysis plus barrier/control analysis |
   | Component contribution is claimed | Ablation/contribution analysis |
   | Latency, throughput, memory, or tail behavior moved | Resource and measurement analysis |
   | Mechanism or counterfactual is implied | Mechanism trace plus root-cause confidence gate |

5. **Build explanation packets**
   For each serious candidate, state the exact result features it explains, the features it does not explain, the mechanism chain, the evidence boundary, a serious rival when available, and a discriminator that would separate the rival. Do not hide unexplained features in a generic limitations paragraph.

6. **Drill from proximate cause to root-cause candidates**
   A root-cause candidate is the deepest currently supported result-generating factor, control gap, or factor interaction that explains why the observed shape occurred. Separate proximate triggers, contributing factors, current root-cause candidates, and evidence boundaries. If the material does not support root-cause depth, say no root cause is identified yet and leave live causal branches with discriminators.

7. **Return the explanation record**
   Return one `## Result analysis` section. Use the output template in `references/analysis_workflow.md`, compacting it only when the user asks for brevity. Concision is not permission to drop result shape, causal factor tree, mechanism traces, evidence boundary, or discriminators.

If no plan path is available because this is a pressure test, dry run, or design review, say that the plan-path material boundary is unavailable and analyze only the scenario material provided. Do not pretend the scenario is a plan-referenced artifact.

If secondary metrics move, such as latency moving during an accuracy experiment, analyze them as separate explanatory branches unless artifacts show they are part of the same result-producing mechanism. Do not force one root cause to cover unrelated result features.

## Root-Cause Minimum

Do not write "root cause: X" unless the analysis also answers:

- What exact result feature did X generate?
- Why did X exist, dominate, or escape the planned controls?
- What proximate trigger and contributing factors led to X?
- What artifact supports the chain?
- What serious rival remains live?
- What discriminator would separate the leading explanation from that rival?

If several factors are jointly necessary, name the interaction as the candidate instead of forcing a single cause.

## Output Contract

Return `## Result analysis` with these sections unless a section is genuinely not available:

- `### Analyzer`
- `### Material used for explanation`
- `### Result shape`
- `### Explanatory contrast`
- `### Method route`
- `### Factor decomposition`
- `### Causal factor tree`
- `### Mechanism traces`
- `### Interaction analysis`
- `### Explanatory summary`
- `### Open explanatory branches`

The output fails if it becomes a status decision, a threshold verdict, a generic limitation list, an evidence-for/evidence-against table, or a single-line root-cause assertion.

For a concise response, keep this minimum: method route, result shape, leading candidate or `No root cause identified yet`, evidence boundary, discriminator, and the result feature each candidate explains.

## Pressure-Test Expectations

In pressure tests, the output passes only when the agent visibly follows the workflow:

- plan-path-only material reconstruction
- result-feature ledger before explanation
- explicit method route chosen from the observed shape
- causal factor tree with proximate triggers, contributing factors, current root-cause candidates, and evidence boundary
- mechanism traces that say what they explain and do not explain
- rivals and discriminators for live explanations
- no downstream status labels or state-update inputs

It fails if it treats an apparent hit as proof of the planned mechanism, treats a missed prediction as merely "the model did not generalize", calls the nearest observed factor the root cause, or drops the causal tree because the answer is meant to be concise.
