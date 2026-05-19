# Hypothesis Plan File Schema

## Purpose

`propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md` is the execution design for one derived hypothesis. It is not the top-level research state. The top-level state is the parent proposition:

```text
Situation question
→ Generated doubt
→ Working proposition
→ Expected consequence
→ Proposition status
→ Derived hypothesis
→ Hypothesis plan
```

The plan tests the derived hypothesis. It cites proposition state but does not rewrite it. A contradicted proposition is not a plannable parent: record the contradiction, revise, split, or close the proposition, then derive the next hypothesis under the updated proposition. Git history is an audit trail, not a substitute for methodology; methods reproducibility comes from the method, data, evaluation protocol, material conditions, and material execution conditions, not env locks or commit hashes.

## File template

```markdown
---
plan_id: <hypothesis id>
slug: <hypothesis slug>
parent_proposition: <Pxxx>
parent_proposition_path: propositions/<Pxxx_slug>/proposition.md
source_analysis: <Axxx>
hypothesis_id: <Hxxx>
hypothesis_path: propositions/<Pxxx_slug>/hypotheses/<Hxxx_slug>/hypothesis.md
category: basic_research | applied_research | experimental_development
mode: exploratory | confirmatory | milestone | theoretical
status: planned | in_progress | completed | parked | killed | replaced
created_at: YYYY-MM-DD
created_commit: <git sha — auto-filled by new_hypothesis.py>
last_updated: YYYY-MM-DD
---

# <Plan title>

## Proposition and hypothesis trace
- Parent proposition:
- Source observations:
- Source analysis:
- Generated doubt:
- Working proposition:
- Expected consequence:
- Proposition status:
- Derived hypothesis:
- Hypothesis type:

## Prior-work grounding
## Divergence checkpoint
## Plan
## Plan review
## Actual execution
### Mid-execution literature updates

- Survey trigger:
- Effect on plan:
- Rerun Plan review:
## Planned vs Actual
## Result analysis
## Claims
## Result feedback
## References
```

## Trace contract

The `## Proposition and hypothesis trace` section is mandatory. It prevents a plan from drifting into a convenient different question. It must include:

- Source observations from `observations.md`.
- Source analysis from `analyses.md`.
- Generated doubt.
- Working proposition.
- Expected consequence.
- Prediction / expected observation.
- Proposition status that produced the hypothesis.
- Derived hypothesis statement from `hypothesis.md`.
- Hypothesis type.
- Competing hypothesis and Minimal discriminator from `hypothesis.md`.
- Decision threshold when the mode is confirmatory.

If the plan cannot trace its hypothesis to a Generated doubt, Working proposition, Expected consequence, and Proposition status, do not execute. Repair the proposition or hypothesis state first.

If the trace shows `contradicted`, the plan is invalid as written. Repair means revising, splitting, or closing the parent proposition first; only the updated proposition can become the parent for a next hypothesis plan.

## Prior-work grounding

### Survey evidence
### Citation-use map
- Used for:
- Plan dependency:
- How it is used:
- Claim-scope effect:
### Grounding scope

Every hypothesis plan records bounded but sufficient prior-work grounding before execution and before the Plan section. This grounding supports the parent proposition, question/objective, inherited assumptions, method choice, controls/comparators, baselines/evaluation protocol, and known limitations. The plan-specific source of truth is the plan-specific Citation-use map; `literature/papers.md` and `literature/positioning.md` keep the project-level role union when a project uses literature files.

Section order is not permission to finalize commit before Survey evidence. Survey evidence comes before claim-bearing execution.

Required:

- Survey evidence: search date, queries/sources, selection rationale, negative findings, retrieval-unavailable constraint/evidence, and claim-scope narrowing.
- Citation-use map: each cited work has a plan dependency and a concrete role.
- Grounding scope: parent proposition support/constraint, inherited assumptions, method choice, controls/comparators/evaluation protocol, known limitations.

Retrieval-unavailable is not a survey bypass. It needs a verifiable signal, attempted source/tool, failure evidence, Retrieval-unavailable evidence, a named constraint, and Claim-scope narrowing that can narrow or block relevant claims.

## Divergence checkpoint

Before execution, record:

- Approach portfolio: primary route and alternatives, or a hard constraint with claim-scope narrowing.
- Anchoring audit: imported result, approach, dataset, theorem, or formulation; risk; revalidation/control.
- Disconfirming evidence: observation that would force hypothesis status update, proposition status update, split, park, or closure.

Mid-execution literature update: if an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal appears, record a mid-execution literature update before claim-bearing execution continues.

## Plan section

Every Plan section starts with `### Plan visual`. Use Mermaid, PlantUML, ASCII, a linked figure/table, or `No diagram:` with a specific reason.

The visual is part of the design: architecture, data flow, evaluation flow, mechanism diagram, causal graph, variable-space map, system boundary, decision flow, derivation dependency, or acceptance-test flow. `No diagram:` is allowed only with a specific reason.

Plan modes:

- `exploratory`: characterize variable space, regimes, traces, observations, or evaluator behavior.
- `confirmatory`: test a prediction against threshold, comparator, control, or discriminator.
- `milestone`: build or improve an artifact with acceptance criteria and performance targets.
- `theoretical`: derive, prove, bound, or characterize a formal relation with limiting-case checks.

All modes record material conditions: data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, collection date, formal assumptions, seed variability, or other conditions that affect interpretation. These are material conditions, not env locks or commit hashes. Changing a seed value before seeing outcomes is usually not material; changing the seed policy, train/test split seed, or any seed after seeing a result is material.

Pre-result commitments include the planned discriminating test and do not explain why an unobserved result happened. Post-result explanations belong to Result analysis after evidence exists.

## Plan review

Before execution, dispatch a fresh separate-context subagent using `research-plan-review` and pass only the plan path. Plan review checks the Premise, proposition trace, hypothesis validation method, Prior-work survey evidence, evidence route, artifact plan, scope, and constraints.

The reviewer reconstructs local state from:

- sibling `hypothesis.md`
- parent `proposition.md`
- parent `observations.md`
- parent `analyses.md`

The extra proposition-first review question:

```text
Does this plan actually test the derived hypothesis produced by the source analysis,
or did it drift into testing a convenient different question?
```

If trace or grounding is missing, review returns `block_execution` or `revise_before_execution`.

## Actual execution

### Mid-execution literature updates

Completed runs must leave durable evidence. Print-only execution is incomplete:

- `run_manifest.json` with `status: completed`
- `logs/stdout.log`
- `logs/stderr.log`
- at least one manifest-listed non-log durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`

Stdout is not evidence. Run `scripts/check_run_artifacts.py` before using a run for observations, Result analysis, Claims, decisions, or reports.

## Result analysis

After evidence exists, dispatch `research-result-analysis` with the plan path only. The returned `## Result analysis` section explains what happened and why. It does not choose proposition decisions, hypothesis decisions, iteration branches, deployment actions, or final claims.

## Result feedback

After Result analysis, update state in this order:

1. Update `hypothesis.md` to one of `tested-supported`, `tested-contradicted`, `tested-partial`, `tested-inconclusive`, `parked`, or `killed`.
2. Append a hypothesis-level decision.
3. Update parent `proposition.md` if proposition status, expected consequence, live hypotheses, or key material changed.
4. Append a proposition-level decision when proposition status changes.
5. Open a next derived hypothesis only if the updated proposition state warrants it.

The update must name whether the result supported, contradicted, under-specified, showed `split-needed`, completed a `split`, or showed an `unrealized-condition` for the parent proposition.

## Claims

Every load-bearing claim in `plan.md` and reports uses:

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]
```

Run `scripts/check_claims.py` before report drafting or state-changing decisions that depend on a claim.

## Common failures

- Generating a hypothesis from no material. Material absence means no proposition or hypothesis.
- Treating observation as a proposition.
- Jumping from a topic to a plan without Generated doubt, Working proposition, Expected consequence, and Proposition status.
- Marking everything `contradicted` when the actual state is `unrealized-condition`.
- Keeping a hypothesis status as plain `tested` instead of `tested-supported`, `tested-contradicted`, `tested-partial`, or `tested-inconclusive`.
- Writing result-analysis explanations before evidence exists.
- Letting Result analysis choose proposition decisions; the parent agent updates proposition and hypothesis ledgers.
