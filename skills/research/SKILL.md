---
name: research
description: Use when conducting R&D work that needs proposition state, claim discipline, planning structure, or human-facing reports. Triggers when generating hypotheses, planning experiments, designing baselines, writing findings, deciding what to do after a result, characterizing a phenomenon, building a prototype, or maintaining research state across sessions.
---

# Research

Protocol skill for agent-driven R&D. The top-level research unit is a **proposition**, not a plan. A plan tests one derived hypothesis under one proposition. The job is to make question generation, hypothesis generation, evidence, claims, and state updates inspectable without turning the protocol into bureaucracy.

Research-level reproducibility is about whether another researcher can re-implement from the described method, material execution conditions, data, evaluation protocol, and statistical setup. Provenance is an audit pointer, not the source of reproducibility; claim-to-artifact consistency is an integrity check rather than making the method reproducible by itself.

## Core lifecycle

```text
Situation question
→ observation / analysis
→ proposition P
→ expected observation E if P is true
→ compare observed O with E
→ decide whether P is contradicted or whether P's required condition is unrealized
→ if P remains live, derive hypothesis H that preserves, revises, splits from, or realizes a condition of P
→ predict what should happen if H is true
→ Hypothesis plan
→ Plan review
→ Execution
→ Result analysis
→ hypothesis status update
→ proposition status update
```

Do not generate hypotheses directly from a vague topic. If there is no observation, failure, success case, constraint, measurement, comparator, repeated trace, prior-work fact, theoretical tension, or search/evaluation bottleneck, there is material absence: create a material-acquisition task, no proposition or hypothesis.

The material-acquisition task should name the missing observation, comparator or expected reference, measurement or evidence form, minimal reproduction or trace, and next artifact to collect. This keeps the agent moving without inventing a proposition.

A contradicted proposition is not a plannable parent: record the contradiction, revise, split, or close the proposition, then derive the next hypothesis under the updated proposition. Do not create a hypothesis plan under a proposition whose current state says the proposition itself is broken.

## Proposition-first objects

| Object | Meaning | Lifetime | File |
|---|---|---|---|
| Proposition | Large research-level proposition that can generate multiple derived hypotheses | Long-lived | `propositions/Pxxx_slug/proposition.md` |
| Observation | Material used to generate or update a proposition | Until superseded | `propositions/Pxxx_slug/observations.md` |
| Analysis | Contrast that produces a Generated doubt, Working proposition, Expected consequence, Proposition status, and possible derived hypothesis | Analysis-scoped unless it changes state | `propositions/Pxxx_slug/analyses.md` |
| Derived hypothesis | Testable hypothesis derived from a proposition or working proposition | Plan-scoped until supported, contradicted, partial, inconclusive, parked, or killed | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/hypothesis.md` |
| Hypothesis plan | Execution design for testing one derived hypothesis | Execution-scoped | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md` |

Propositions are not claims. A proposition status records the state of a research program. A claim still requires the claim structure after evidence exists.

## Question generation

The skill distinguishes:

- **Situation question**: broad user or project question.
- **Generated doubt**: precise tension produced by analysis.
- **Research question**: question that can generate propositions and hypotheses.

Questions are produced by contrast operations, not by asking the agent to be creative:

| Operation | Use when | Question shape |
|---|---|---|
| `expectation-break` | Expected relation and observation diverge | If the expected relation should hold, what hidden condition is missing, unrealized, or false? |
| `constraint-joint-fit` | Several constraints must hold together | What proposition makes the constraints consequences of one structure or process? |
| `required-component-doubt` | A component is treated as necessary | Can its function be supplied by another mechanism plus minimal replacement for what is lost? |
| `trace-meaning` | Repeated, symmetric, ratio-like, or leftover traces appear | What process, memory, control system, or mechanism would make this trace expected? |
| `static-to-process` | Static pattern may record generation, movement, update, or decay | What process produced this pattern as historical record? |
| `analogy-transfer` | A source-domain mechanism may map to the target domain | What proposition makes the source mechanism valid here despite mismatches? |
| `search-or-evaluation-bottleneck` | The bottleneck is search, score, representation, or evaluator | Can the bottleneck move into an indirect, learned, or constrained process? |
| `representation-change` | Current variables make a plausible proposition hard to realize or test | Would residuals, differences, ratios, invariants, latent variables, or proxy tasks make it testable? |

The labels route thinking; they are less important than the written contrast and Generated doubt.

## Analysis contract

Every hypothesis-generating analysis must write this sequence:

1. Situation question.
2. Material used: observation, measurement, comparator, trace, prior-work fact, theoretical tension, failure, success case, or bottleneck.
3. Contrast type and explicit contrast.
4. Generated doubt.
5. Working proposition.
6. Expected consequence if the working proposition is true.
7. Observed match, break, or missing condition.
8. Proposition status.
9. Derived hypothesis candidate only when the status permits one. If the status blocks hypothesis creation, write `None: <reason>` instead of a candidate.

Proposition status values:

- `supported`: material matches the expected consequence enough to derive or continue a hypothesis.
- `contradicted`: material breaks the proposition itself.
- `unrealized-condition`: the proposition may hold, but the current method, representation, measurement, evaluator, or system does not realize a required condition. If the material is theoretical only and the expected consequence can be written but has not yet been empirically realized, this is `unrealized-condition`, not `under-specified`.
- `under-specified`: the proposition cannot yet produce a discriminating expected consequence. If you were able to write the expected consequence, the proposition is not `under-specified`.
- `split-needed`: one proposition hides multiple separable propositions.
- `split`: child propositions have been opened; continue through children.
- `closed`: the proposition is resolved, superseded, killed, or no longer useful.

Routing:

| Status | Next state action |
|---|---|
| `supported` | Create or continue a derived hypothesis |
| `contradicted` | Record the contradiction, then revise, split, or close the proposition before deriving a hypothesis under the updated proposition |
| `unrealized-condition` | Derive a hypothesis that makes the condition realizable |
| `under-specified` | Add observation, measurement, comparator, or formulation before planning; do not create a formal derived hypothesis or plan |
| `split-needed` | Split before planning |
| `split` | Continue through child propositions, not the old parent |
| `closed` | Do not derive new hypotheses from this proposition |

This is the anti-handwave rule: a derived hypothesis is not produced until the agent can say which proposition status produced it. When the status is `under-specified`, the analysis may record the missing discriminator but must not smuggle a plausible hypothesis into the Derived hypothesis field.

## Project structure

```text
project-root/
├── README.md
├── project_state.md
├── decisions.md                         # project-wide decisions only
└── propositions/
    └── P001_slug/
        ├── proposition.md
        ├── observations.md
        ├── analyses.md
        ├── decisions.md                 # proposition state transitions
        └── hypotheses/
            └── H001_slug/
                ├── hypothesis.md
                ├── plan.md              # hypothesis plan
                ├── experiments/
                ├── reports/
                └── decisions.md         # derived-hypothesis transitions
```

Use scripts:

- `scripts/new_project.py` initializes the project with `propositions/`.
- `scripts/new_proposition.py` opens a proposition and appends `OPEN_PROPOSITION` to project `decisions.md`.
- `scripts/new_hypothesis.py` creates `hypothesis.md`, `plan.md`, `experiments/`, `reports/`, and hypothesis `decisions.md` under a proposition.
- `scripts/new_run.py` creates durable run evidence under a derived hypothesis.

There is no standalone `new_plan.py`. A top-level plan is the old lifecycle.

## Decisions

Top-level `decisions.md` is for project-wide structure, scope, and protocol only.

Decision locations:

- Project: `decisions.md` with `OPEN_PROPOSITION`, `SPLIT_PROPOSITION`, `MERGE_PROPOSITION`, `CHANGE_SCOPE`, `CHANGE_PROTOCOL`.
- Proposition: `propositions/Pxxx_slug/decisions.md` with `SUPPORT`, `CONTRADICT`, `UNREALIZED_CONDITION`, `UNDER_SPECIFY`, `SPLIT_NEEDED`, `SPLIT`, `CLOSE`, `REOPEN`.
- Hypothesis: `propositions/Pxxx_slug/hypotheses/Hxxx_slug/decisions.md` with `COMMIT`, `PARK`, `KILL`, `TESTED_SUPPORTED`, `TESTED_CONTRADICTED`, `TESTED_PARTIAL`, `TESTED_INCONCLUSIVE`, `REVISE`.

A decision that does not update project, proposition, or hypothesis state belongs in analysis notes.

## R&D categories

Every hypothesis plan declares exactly one category:

| Category | When to use | Default mode | Report shape |
|---|---|---|---|
| `basic_research` | New knowledge about underlying foundations without a particular application in view | `exploratory` | Phenomenon -> mechanism/principle -> learned -> refined proposition |
| `applied_research` | New knowledge directed toward a specific practical aim | `confirmatory` | Objective -> method/procedure -> evidence -> limits |
| `experimental_development` | Systematic work producing additional knowledge while creating or improving a product/process | `milestone` | System/process -> performance -> limits -> next iteration |

Plan modes are `exploratory`, `confirmatory`, `milestone`, and `theoretical`.

## Hypothesis plan

`hypotheses/Hxxx_slug/plan.md` is the moved `rd_plan` role. It cites:

- parent `proposition.md`
- source `observations.md`
- source `analyses.md`
- current `hypothesis.md`

The plan may summarize those sources but must not rewrite them. If proposition state changes before execution, amend or regenerate the plan from the updated hypothesis.

The Plan and Plan review contain **pre-result commitments**: proposition trace, hypothesis, prediction or expected observation, primary measure, controls/comparators or limiting-case checks, evidence route, artifacts, material conditions, and stop/status criteria. They do not explain why an unobserved result happened.

Post-result explanations belong to Result analysis after evidence exists. If the claim requires one, the plan names the planned discriminating test before execution.

Prior-work grounding remains required before claim-bearing execution; projects may use `literature/papers.md` and `literature/positioning.md` for prior-work state.

Do not require every derived hypothesis to be mechanistic. Hypothesis type may be `predictive / performance`, `mechanistic`, `causal / intervention`, `descriptive / characterization`, `theoretical`, or mixed.

Every Plan section starts with `### Plan visual`. Use Mermaid, PlantUML, ASCII, a linked figure/table, or `No diagram:` with a specific reason.

## Plan review

Before execution, dispatch a fresh separate-context plan-review subagent using `research-plan-review`. Pass only the plan path. Because the plan lives inside `propositions/Pxxx_slug/hypotheses/Hxxx_slug/`, the reviewer reconstructs local state from sibling `hypothesis.md` and parent proposition files referenced by the plan.

Plan review checks whether the plan actually tests the derived hypothesis produced by the source analysis, or drifted into a convenient different question. If the plan cannot trace its hypothesis to a Generated doubt, Working proposition, Expected consequence, and Proposition status, it returns `block_execution` or `revise_before_execution`.

## Execution evidence

For research scripts, print-only output is not evidence. stdout is not evidence. A completed run needs:

- `run_manifest.json` with `status: completed`
- `logs/stdout.log`
- `logs/stderr.log`
- at least one manifest-listed durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`

Run `scripts/check_run_artifacts.py` before using a run as evidence for Result analysis, observations, claims, decisions, or reports.

## Result analysis and feedback

After execution and Planned vs Actual, dispatch a fresh separate-context result-analysis subagent using `research-result-analysis`. Pass only the plan path. Result analysis explains what happened and why; it does not write final claims, choose proposition decisions, or choose hypothesis decisions.

After Result analysis, the parent agent updates state in this order:

1. `hypothesis.md` status.
2. hypothesis `decisions.md`.
3. parent `proposition.md` when proposition status, expected consequence, live hypotheses, or key material changes.
4. proposition `decisions.md` when proposition status changes.
5. open the next derived hypothesis only if the updated proposition state warrants it.

This is the hypothesis status update and proposition status update phase of the lifecycle.

Hypothesis result states:

- `tested-supported`: planned discriminator supported the hypothesis against the named competitor under tested conditions.
- `tested-contradicted`: planned discriminator contradicted the hypothesis.
- `tested-partial`: evidence supported part of the hypothesis but left a material clause, condition, or competitor unresolved.
- `tested-inconclusive`: execution happened but evidence quality, measurement, or comparator failure prevents interpretation.

## Claims

Claims are evidence records, not proposition statuses. Every load-bearing claim uses:

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]
```

Strength is read from alternatives and tested conditions. Empty lists claim exhaustion and are open to audit.

## Reports

Reports live under the derived hypothesis: `propositions/Pxxx_slug/hypotheses/Hxxx_slug/reports/`. Reports are human-facing evidence artifacts. Required sections are Summary, Background, Related Work, Theory / Formulation, Methods & Conditions or category-specific equivalent, Results/Observations/Performance, Ablation / Sensitivity, Discussion, Limitations, and References. Sections that do not apply still appear with `Not applicable:` and a reason. Reports do not carry next-action or next-hypothesis queues.

## Capability-uplift guard

This protocol should improve reasoning:

- It gives operations for producing questions.
- It preserves intermediate state across sessions.
- It lets multiple Generated doubts and Working propositions coexist.
- It distinguishes `unrealized-condition`, `under-specified`, and `split-needed` from true/false.
- It lets results feed back into propositions before the next hypothesis is generated.

It must not become restrictive bureaucracy:

- Do not require every contrast type.
- Do not require every derived hypothesis to be mechanistic.
- Do not require a plan before proposition material exists.
- Do not force a single best hypothesis while multiple working propositions remain live.
- Do not turn observation collection into a claim that a proposition exists.
- Do not make labels more important than contrast, Generated doubt, Working proposition, Expected consequence, Proposition status, and Derived hypothesis trace.

Hard stops for hypothesis or plan creation are material absence and a parent proposition whose current state is `contradicted`, `under-specified`, `split-needed`, `split`, or `closed`. These are not dead ends: they route to material acquisition, contradiction recording, revision, split, child propositions, or closure before the next hypothesis is generated.
