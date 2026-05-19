---
name: research-result-analysis
description: Use when completed R&D plan results need a why-explanation, especially when an agent may collapse into support/contradiction labels, threshold verdicts, validity audits, or generic limitations instead of explaining the mechanism that produced the observed result.
---

# Research Result Analysis

## Overview

Independent post-result explanation for a completed hypothesis plan. The plan path is the only starting context. The job is to explain **why this observed result was produced** by reconstructing result shape, process, state transitions, factor interactions, and competing generative explanations.

This skill is analysis only. It does not judge whether the result is good, bad, valid, supported, contradicted, claim-ready, promotion-ready, or decision-ready. It does not write state-update inputs. The parent `research` workflow reads the analysis later and makes any hypothesis, proposition, claim, report, or next-action decision.

## Core Rule

Analyze the result as an outcome to be explained, not a verdict to be assigned.

Use the planned prediction only as a contrast that tells you what part of the observed outcome needs explanation. Do not make the prediction comparison the center of the output. A threshold pass, threshold miss, or aggregate improvement is not an analysis.

Forbidden outputs:

- hypothesis status or proposition status recommendations
- `State-update inputs`
- `supported`, `contradicted`, `tested-supported`, `tested-contradicted`, `tested-partial`, or `tested-inconclusive` labels
- promotion readiness, claim readiness, deployment recommendation, or iteration branch
- final claims or human-facing report prose
- an evidence verdict that replaces the explanation

## Required Reference

Before analyzing, read `skills/research/references/analysis.md` from this plugin. Apply its explanation-first result-analysis discipline. If a referenced document discusses claims, artifacts, or decisions, treat those as downstream consumers of the explanation. They do not change this skill's job.

## Workflow

1. **Load the plan and result material**
   Start from the plan path only. Inspect the plan, sibling `hypothesis.md`, referenced proposition material, Actual execution, Planned vs Actual, runs, logs, outputs, tables, traces, configs, scripts, and reports when available. Use these as material for explanation, not as a validity trial.
   Do not treat parent-agent summaries, user-provided summaries, private notes, or unstated expectations as result material unless the plan or a plan-referenced artifact contains them.

2. **Inventory the result shape**
   Describe the outcome before explaining it. Include aggregate movement, slices, regimes, seeds or repetitions, traces over time, failure cases, anomalies, state transitions, resource patterns, and condition-specific effects. If a result is uneven, the unevenness is usually the most important material.

3. **Name the explanatory contrast**
   State the planned expectation and the observed shape only to locate the puzzle: what needs explaining? Examples: aggregate improved but one slice collapsed; p50 improved while p99 worsened; training fit improved while validation barely moved; a proof worked only under a boundary condition.

4. **Build a factor map**
   Decompose possible result-producing factors. Choose only factors relevant to the observed material:

   | Factor | Use when the result may come from |
   |---|---|
   | Input / data | data composition, slices, labels, regimes, ordering, distribution, sampling, or perturbations |
   | Representation | variables, features, state representation, abstraction boundary, tokenization, coordinate system, or metric space |
   | Model / method | architecture, algorithm, objective, update rule, search rule, cache policy, parser rule, proof move, or heuristic |
   | Process / dynamics | training trajectory, convergence, mode switching, queue buildup, control flow, recursion, scheduling, or feedback loops |
   | Resource / system | contention, memory locality, IO, synchronization, batching, latency tail, throughput, or hardware interaction |
   | Measurement / evaluator | metric sensitivity, aggregation, slice weighting, threshold definition, instrumentation, or benchmark behavior |
   | Interaction | two individually plausible factors combine to produce an unexpected outcome |

5. **Construct mechanism traces**
   For each serious explanation candidate, write the chain:

   `starting condition -> local process/activity -> intermediate state -> result-producing step -> observed result feature`

   A candidate explanation is not acceptable until it states which result features it explains and which result features it does not explain. Do not hide unexplained features in a generic limitations paragraph.

6. **Compare explanatory rivals**
   Compare candidates by explanatory fit, not by verdict. Ask:

   - Which parts of the result shape become expected under this explanation?
   - Which parts remain surprising?
   - What competing explanation would produce the same aggregate but a different slice, trace, or state transition?
   - What minimal discriminator would separate the live explanations?

7. **Return the analysis**
   Return a `## Result analysis` section. The parent research agent may later use it for state updates, claims, or planning, but this output must remain an explanation record.

## Analysis Lenses

Use these as thinking tools, not required headings:

| Lens | Question |
|---|---|
| Mechanism decomposition | What entities, activities, ordering, and conditions produced the result? |
| Cause-effect trace | What changed first, what intermediate state followed, and where did the final result become likely? |
| Slice and regime analysis | Which subset, condition, scale, or regime carries the result? |
| Variance-source analysis | Could seeds, sampling, initialization, hyperparameters, or environment variation produce the observed shape? |
| Error / failure analysis | What do representative failures have in common? |
| Ablation / contribution analysis | Which component or step is necessary for the result pattern, and which is incidental? |
| Resource and contention analysis | Did queues, locks, memory, IO, scheduling, or batching create the outcome? |
| Representation analysis | Did the chosen variables or abstraction make the effect appear, disappear, or move? |
| Evaluator behavior analysis | Did the metric or evaluator emphasize one behavior while hiding another? |
| Interaction analysis | Did two factors combine so that neither alone explains the result? |

## Quality Gate

A result analysis is acceptable only when it is:

| Check | Requirement |
|---|---|
| outcome-centered | The output explains the observed result shape, not whether the plan passed. |
| shape-complete | Aggregate, slice, trace, anomaly, and condition-specific material are considered when available. |
| mechanism-explicit | Each candidate has a chain from starting condition to result-producing step. |
| factorized | At least the relevant factors from the factor map are considered; irrelevant factors are skipped. |
| rival-aware | More than one live explanation is considered when the material permits it. |
| discriminator-ready | The output names what would separate live explanations without turning that into a next-action decision. |
| non-decision | No hypothesis status, proposition status, claim readiness, promotion readiness, or deployment recommendation appears. |

Stop when the leading explanations account for the important result features and the remaining open branches are specific. Do not keep adding generic caveats. Do continue if the output still says only "the metric missed", "the hypothesis was supported", "more evidence is needed", or "there may be a bug".

## Output Shape

```markdown
## Result analysis

### Analyzer
- Agent: <fresh separate-context result-analysis subagent>
- Skill: research-result-analysis
- Only starting context: <plan path>
- Analyzed at: <YYYY-MM-DD>

### Material used for explanation
- Plan: <plan path>
- Local research state inspected: <hypothesis/proposition/observations/analyses paths, or Not available>
- Result material inspected: <plan-referenced runs/logs/tables/figures/traces/configs/scripts/reports, or Not available>
- Explanation-scope gaps: <missing material that would change the why-analysis; include any untraceable supplied summary here, or None>

### Result shape
- Aggregate shape: <what moved overall>
- Slice / condition shape: <where it differed by subset, condition, scale, regime, or input family>
- Trace / process shape: <time sequence, state transition, training dynamics, queue behavior, control flow, proof steps, or anomaly path>
- Concentrated cases: <failures, successes, outliers, or examples that carry the pattern>

### Explanatory contrast
- Planned expectation: <only the expectation needed to locate the puzzle>
- Observed result needing explanation: <the result feature or mismatch to explain>
- Why this is a puzzle: <what cannot be explained by the aggregate alone>

### Factor decomposition
| Factor | How it could produce the observed result | Result features touched | Interaction with other factors |
|---|---|---|---|
| <factor> | <generative role> | <features> | <interaction or None> |

### Mechanism traces
#### E1: <candidate explanation>
- Chain: <starting condition -> local process/activity -> intermediate state -> result-producing step -> observed result feature>
- Explains: <specific result features made expected by this chain>
- Does not explain: <specific result features still not accounted for>
- Competing explanation: <near rival, or None if genuinely unavailable>
- Discriminator: <slice, trace, perturbation, ablation, failure sample, limiting case, or theoretical check that would separate explanations>

### Interaction analysis
- <where two or more factors combine to produce the observed result, or None if the result is single-factor under current material>

### Explanatory summary
- <concise why-explanation of the result, preserving uncertainty without assigning status>

### Open explanatory branches
- <specific remaining why-branches and what result feature each branch would explain>
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Turning result analysis into a status decision | Do not write status labels or state-update inputs; explain the result-producing process only. |
| Centering the threshold | Use thresholds only to locate the explanatory contrast; then analyze why the observed shape occurred. |
| Writing `Evidence for` / `Evidence against` lists as the main analysis | Replace them with mechanism chains, explained features, unexplained features, rivals, and discriminators. |
| Stopping at aggregate metrics | Look for slices, traces, regimes, failures, anomalies, and condition-specific effects. |
| Treating missing artifacts as the conclusion | Name explanation-scope gaps only if they affect the why-analysis; do not turn them into a validity verdict. |
| Accepting an external result summary as the result | Trace the result through the plan and plan-referenced artifacts; untraceable summaries are explanation-scope gaps, not material. |
| Calling a result "partial support" | Describe which result features share a generating mechanism and which features require another explanation. |
| Saying "more analysis is needed" generically | Name the specific discriminator and the live explanations it would separate. |
| Adding every lens mechanically | Use only lenses that can plausibly explain the observed result shape. |
| Explaining only successes | Successful aggregate results can still hide slice-specific mechanisms, failures, and interactions. |
| Explaining only failures | A missed prediction can still reveal a real mechanism in a narrower condition. |

## Pressure-Test Expectations

In pressure tests, the output fails if it:

- obeys user pressure to "just mark supported/contradicted"
- includes `State-update inputs`
- ends with hypothesis/proposition status evidence
- treats artifact completeness as the main result
- accepts an untraceable supplied summary instead of plan-referenced result material
- lists candidates without mechanism chains
- ignores the slice or trace that actually explains the outcome

It passes only when the analysis explains how the observed result was generated and leaves downstream decisions to the parent workflow.
