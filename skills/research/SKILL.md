---
name: research
description: Use when conducting R&D work that needs proposition state, claim discipline, planning structure, scoping literature, EDA, research papers, or maintained research state. Triggers when starting from an intent, generating hypotheses, planning experiments, designing baselines, writing findings, deciding what to do after a result, characterizing a phenomenon, building a prototype, or maintaining research state across sessions.
---

# Research

This is an operating procedure for proposition-first R&D. Do not respond by reciting the protocol. In normal use, take the next concrete step: create or update the artifact if you can write files, or name the exact path and missing input that blocks the write.

The top-level research unit is a **proposition**, not a standalone plan. A plan tests one derived hypothesis under one live proposition. `creating-propositions` owns proposition generation and proposition state files; this skill runs the project workflow around it.

## First Move

Before analysis, establish the project state.

If this skill is invoked alone, the minimum read set is `intake.md`, `project_state.md`, root `observations.md`, `literature/scoping.md`, and current `propositions/*/proposition.md`; if they do not exist, create the project layout first.

1. If there is no project root, run `scripts/new_project.py <project-root> --name "<name>"`.
2. If a project exists, read `intake.md`, `project_state.md`, root `observations.md`, `literature/scoping.md`, and the current proposition statuses.
3. Pick exactly one lane:
   - known implementation only: route out of R&D, no proposition lifecycle
   - missing intake: write/update `intake.md`
   - missing material: write a material-acquisition task and the target artifact path
   - material exists but no proposition: switch inline to `creating-propositions`
   - plan-ready proposition exists: create or continue one derived hypothesis
   - execution happened: run result analysis, then update ledgers
   - proposition reached `supported` or `contradicted`: draft/check `paper.md`

Do not ask generic research questions when the next artifact is obvious. Write the next artifact with known facts and mark unknowns as missing material.

## Route Table

Use this table as the execution contract under pressure:

| Trigger | Read | Write | Stop condition | Next action |
|---|---|---|---|---|
| No project exists | user request | generated project layout | `new_project.py` succeeds | fill `intake.md` |
| Intent is known implementation | user request, `intake.md` if present | `intake.md` route note | outcome is not uncertain | leave R&D workflow |
| Intent is uncertain but underspecified | user request | `intake.md` | uncertain question and missing material named | material acquisition |
| Material missing | `intake.md`, `literature/scoping.md`, root `observations.md` | root `observations.md` or material-acquisition note | smallest missing artifact named | collect material |
| Material exists, no proposition | intake/scoping/observations/material | proposition handoff summary | handoff bundle ready | inline `creating-propositions` |
| Proposition is plan-ready | proposition files, source analysis | `hypotheses/Hxxx/*` | plan created and review requested | `research-plan-review` |
| Execution finished | plan, run artifacts, Planned vs Actual | analysis/ledger updates | `research-result-analysis` reviewed | update proposition state |
| Proposition resolved | proposition files, claims, runs | `propositions/Pxxx/paper.md` | `check_paper.py` passes | next-cycle scoping |
| Paper exists, next cycle | prior `paper.md`, `literature/scoping.md` | dated re-survey in `literature/scoping.md` + own-paper observations in root `observations.md` | re-survey dated AND own-paper observations extracted | inline `creating-propositions` |

Blocked output shape:

```text
Route: blocked
Blocking condition: <not uncertain | material absent | no Bit | non-plan-ready state | missing review>
Missing artifact: <path or external item>
Do not create: <proposition | hypothesis | paper | claim>
Next action: <single concrete action>
```

## Work Loop

### 1. Intake

Write or update `intake.md` with:

- user intent and desired outcome
- the uncertain-in-outcome question
- available material
- missing material
- current route: R&D, implementation, or blocked

If the user only wants a known method implemented exactly as described, say this is implementation work and do not open a proposition or hypothesis lifecycle. If the user reframes toward an uncertain question, continue.

### 2. Scoping

Write or update `literature/scoping.md` before proposition creation. Capture:

- existing work and whether the intent is already solved
- comparators, datasets, baselines, and known failures
- contradictions or gaps that matter for the intent
- retrieval attempts and claim-scope narrowing when sources are unavailable

Scoping is not the plan survey. It prepares proposition material.

### 3. Material And EDA

Put raw or referenced material under `data/raw/`, derived data under `data/processed/`, and exploratory notebooks/tables/figures under `data/eda/`.

Write root `observations.md` as an observation backlog. Separate observed facts from interpretations. EDA can create observations, tensions, missing-measurement notes, and candidate comparators; it must not create claims.

If there is no observation, failure, success case, constraint, measurement, comparator, repeated trace, prior-work fact, theoretical tension, or bottleneck evidence, stop the research path and write the smallest material-acquisition task.

### 4. Proposition Pass

When material exists, switch inline to `creating-propositions` in the same context. Do not dispatch a fresh separate-context subagent for proposition generation.

Expected handoff to `creating-propositions`:

- relevant `intake.md` lines
- `literature/scoping.md` findings
- root `observations.md` entries
- relevant prior `propositions/Pxxx/paper.md` when in a later cycle

Expected return from `creating-propositions`:

- opened/updated/blocked proposition path
- current 9-state status
- decision ledger entry written or needed
- next research action: material acquisition, split/merge, hypothesis creation, or paper

### 5. Hypothesis Planning

Use `scripts/new_hypothesis.py` only after both are true:

- parent proposition status is `open`, `supported`, or `unrealized-condition`
- source analysis contains a non-placeholder derived hypothesis candidate

The plan lives at `propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md`.

The plan cites the parent `proposition.md`, source `analyses.md`, and `hypothesis.md`; it may summarize them but must not rewrite them. If proposition state changes before execution (for example the parent moves to `contradicted`, `split`, `under-specified`, or `parked`), amend or regenerate the plan from the updated proposition and re-run `research-plan-review`. Do not execute a plan built on stale proposition state.

Every Plan section starts with `### Plan visual`. It may use Mermaid, PlantUML, ASCII, a linked figure/table, or `No diagram:` with a reason. A plan commits before execution to one hypothesis, the proposition trace, Hypothesis type, prediction, competitor, discriminator, primary measure, controls/comparators or limiting-case checks, evidence route, artifacts, material conditions, and stop/status criteria.

Do not require every derived hypothesis to be mechanistic. Hypothesis type may be `predictive / performance`, `mechanistic`, `causal / intervention`, `descriptive / characterization`, `theoretical`, or `mixed`.

Before execution, dispatch `research-plan-review` with only the plan path. If review blocks, update the plan or material; do not execute through the blocker.

### 6. Execution Evidence

Print-only output is not evidence. A completed run needs `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, and at least one manifest-listed durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`. Run `scripts/check_run_artifacts.py` before using a run as evidence.

### 7. Result Closeout

After execution and Planned vs Actual are written, dispatch `research-result-analysis` with only the plan path. It explains why the observed result happened; it does not write final claims, state-update inputs, or decisions.

Then the parent agent updates, in order:

1. `hypothesis.md`
2. hypothesis `decisions.md`
3. parent proposition state files using the `creating-propositions` discipline
4. proposition `decisions.md` when state changes
5. root `project_state.md`

Claims are evidence records, not proposition statuses. Before state-changing decisions or paper prose depends on a claim, run `scripts/check_claims.py`.

### 8. Paper And Next Cycle

Create `propositions/Pxxx_slug/paper.md` when a proposition reaches `supported` or `contradicted`. Do not postpone the paper because per-hypothesis notes exist, because the project may continue, or because a future summary seems easier. The resolution transition is the publication trigger.

The paper synthesizes across the proposition's hypotheses and must pass `scripts/check_paper.py`. Required paper-grade structure includes Related Work, Theory / Formulation, Methods & Conditions or System description, Results/Observations/Performance, Ablation / Sensitivity, Claim-to-result alignment, Discussion, Limitations, Reproducibility, and References. Numeric evidence needs sample size plus variance/dispersion, CI, effect size, significance, or an explicit non-applicability reason.

In the next cycle, treat the paper as material. This is not optional and is the same strength as the resolution trigger above: two concrete writes are required before the next proposition pass.

1. Re-survey literature for the new cycle and append a dated entry to `literature/scoping.md` recording the search date and the queries/sources actually attempted. A retrieval-unavailable note must still record what was attempted on this date, not just "nothing new." Reusing the original scoping unchanged does not count as a re-survey.
2. Extract the open branches and findings of your own `paper.md` into root `observations.md` as fact-level entries citing the paper. Own research is part of the Bit source for later propositions; an unwritten "I know my own results" does not satisfy this.

Do not open the next proposition before both writes exist.

## Layout And Ownership

`references/project_layout.md` is the layout source of truth.

```text
project-root/
|-- intake.md
|-- literature/
|   |-- scoping.md
|   |-- papers.md
|   `-- positioning.md
|-- data/{raw,processed,eda}/
|-- observations.md
|-- project_state.md
|-- decisions.md
|-- lib/{data,eval,viz,utils,tests}/
`-- propositions/
    `-- P001_slug/
        |-- proposition.md
        |-- observations.md
        |-- analyses.md
        |-- decisions.md
        |-- paper.md
        `-- hypotheses/
            `-- H001_slug/
                |-- hypothesis.md
                |-- plan.md
                |-- experiments/{code,configs,notebooks,runs}/
                `-- decisions.md
```

Ownership:

- `research`: `intake.md`, root `observations.md`, `literature/{scoping,papers,positioning}.md`, `data/{raw,processed,eda}/`, `project_state.md`, root `decisions.md`, `propositions/Pxxx/paper.md`, and hypothesis files.
- `creating-propositions`: `propositions/Pxxx/{proposition,observations,analyses,decisions}.md`.

Root `decisions.md` records project structure only: `OPEN_PROPOSITION`, `SPLIT_PROPOSITION`, `MERGE_PROPOSITION`, `CHANGE_SCOPE`, `CHANGE_PROTOCOL`.

Proposition `decisions.md` records proposition state only: `SUPPORT`, `CONTRADICT`, `UNREALIZED_CONDITION`, `UNDER_SPECIFY`, `SPLIT_NEEDED`, `PARK`, `UNPARK`, `REVISE`, `CLOSE`, `REOPEN`.

Hypothesis `decisions.md` records hypothesis lifecycle only: `COMMIT`, `PARK`, `KILL`, `TESTED_SUPPORTED`, `TESTED_CONTRADICTED`, `TESTED_PARTIAL`, `TESTED_INCONCLUSIVE`, `REVISE`.

## Proposition State Router

Plan-ready states are exactly `open`, `supported`, and `unrealized-condition`.

All proposition states are `open`, `supported`, `unrealized-condition`, `under-specified`, `contradicted`, `split-needed`, `split`, `parked`, and `closed`.

Blocked state routing:

- `under-specified`: acquire material or revise until a discriminating expected consequence exists.
- `contradicted`: record the contradiction, then revise, split, or close before planning.
- `split-needed`: split before planning.
- `split`: continue through child propositions.
- `parked`: satisfy the unblock condition before planning.
- `closed`: do not plan unless reopened with a recorded reason.

`closed -> open` requires a `REOPEN` entry in proposition `decisions.md` naming the new material or reconsideration basis. `parked -> previous live state` requires `UNPARK` and evidence that the unblock condition is satisfied.

## Literature Is Two-Layered

Scoping literature and hypothesis-specific grounding are non-substitutable.

- `literature/scoping.md`: before proposition creation, identify existing work, comparators, datasets, known failures, and whether the intent is already solved.
- Plan-scoped Prior-work grounding: before claim-bearing execution, ground the specific hypothesis, method, baseline, metric, and validation route. Include Survey evidence and Citation-use map even when scoping exists.

If scoping breaks the intended novelty claim, stop the novelty framing. Narrow, revise, replicate, or choose an honest boundary before planning.

## Old Paths

Old top-level `plans/`, top-level `experiments/<id>/runs/`, `literature/differentiation.md`, and per-hypothesis `reports/` are not compatibility paths. Reject them except in explicit old-path rejection tests.

There is no standalone `new_plan.py`.

## End-Of-Turn Output

When reporting progress, give the user the operational state, not a protocol summary:

- artifact paths created or updated
- current proposition and hypothesis state
- blockers and exact missing artifact, if blocked
- verification command run, if any
- next concrete action

## Capability Guard

This workflow should improve reasoning, not create paperwork. Keep labels subordinate to the actual contrast, expected consequence, discriminator, evidence, and decision. Do not turn EDA into a claim, do not inflate incremental results, and do not create hypotheses from absent material.

Do not force a single best hypothesis or rank live propositions while several remain plan-ready. Multiple working propositions and derived hypotheses may coexist until evidence separates them; converge because a discriminator resolved them, not because one track is more convenient.
