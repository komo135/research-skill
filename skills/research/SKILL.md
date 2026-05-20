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
3. Pick exactly one canonical route from **Route Before Gate** and take its route-specific action. Do not maintain a separate lane vocabulary.

Do not ask generic research questions when the next artifact is obvious. Write the next artifact with known facts and mark unknowns as missing material.

Do not call a local file, metric, split, or competition-metadata audit "initial research complete." That audit is material, not existing-work scoping. For benchmark or competition work, a valid CSV, "minimal baseline," "safe baseline," or "no claim yet" request does not by itself make the method known or remove R&D uncertainty. If public baselines, competition writeups/notebooks/discussions, comparator conventions, evaluation protocol, or known failures have not been checked and recorded in `literature/scoping.md`, select `materialization` before baseline/comparator design or implementation.

## Route Before Gate

Gate placement comes after route selection:

- Content Gate applies at `proposition-commit` and `ambition-elevation`, not to every exploratory action.
- Paper-grade gate applies at `paper-route`, after proposition state resolution.
- Material, probe, implementation milestone, and stakeholder brief work are real outputs, but they do not promote the proposition lifecycle by themselves.

Use this single routing structure as the action selector:

| Route | Select when | Artifact to write now | Promotion explicitly forbidden | Next |
|---|---|---|---|---|
| `implementation-handoff` | outcome is known, no R&D uncertainty remains, and any requested method is supplied exactly enough to implement without choosing a baseline/comparator | normal implementation files and an `intake.md` route note if useful | proposition, hypothesis plan, paper | leave R&D workflow |
| `materialization` | material, data, logs, existing-work scoping, public baselines, competition writeups/notebooks/discussions, comparator, split, evaluator, or measurement is missing | root `observations.md`, `literature/scoping.md`, `data/raw/`, `data/processed/`, or `data/eda/` | proposition, hypothesis plan, paper, baseline/comparator implementation | collect the missing material |
| `exploratory-probe` | a concrete but under-controlled check is needed before material is interpretable | before a proposition: `data/eda/<probe_slug>.md` or generated tables/figures; after a plan: hypothesis `experiments/runs/<run_id>/` | proposition support, landmark ambition, final paper | update observations or material route |
| `implementation-milestone` | code, harness, utility, or infrastructure acceptance criteria are met | if plan-derived: hypothesis `experiments/runs/<run_id>/`; if project-wide infrastructure: `lib/` plus root `decisions.md` or `project_state.md` | proposition support unless the plan discriminator was exactly that acceptance condition | continue or close the milestone |
| `proposition-commit` | enough material exists to state Surprise, Bit, expected consequence, falsifier, and competitor | `propositions/Pxxx/{proposition,observations,analyses,decisions}.md` via `creating-propositions` | derived hypothesis if the state is blocked | proposition state router |
| `ambition-elevation` | a proposition is proposed or retained as `landmark-aspirant` | proposition `analyses.md` and Content Gate fields | landmark label without a concrete load-bearing referent | keep, downgrade, under-specify, or collect material |
| `hypothesis-plan` | parent proposition is plan-ready and source analysis has a derived hypothesis candidate | `propositions/Pxxx/hypotheses/Hxxx/{hypothesis.md,plan.md,experiments/,decisions.md}` | assumptions replacing missing discriminator, comparator, or measurement | plan review |
| `claim-resolution` | result analysis and evidence resolve the parent proposition enough to change state | hypothesis/proposition ledgers, claim records, `project_state.md` | paper before state resolution | state update |
| `paper-route` | proposition reaches `supported` or `contradicted` through claim-resolution | `propositions/Pxxx/paper.md` | provisional paper, stakeholder draft as paper | next-cycle scoping |
| `stakeholder-brief` | stakeholder needs an interim deliverable before proposition resolution | root `status_brief.md` with dated entries | paper route, next-cycle trigger, proposition support | continue the current route |

Do not require a route block for every ordinary step. Use it as a forcing function only when the route is non-obvious, the user is pushing to proceed despite missing material or unresolved evidence, the agent is about to promote work to proposition/hypothesis/support/`landmark-aspirant`/`paper.md`, a research category is being used as a closeout reason, or `provisional` appears around proposition state, support, or paper.

Route block:

```text
Route:
Why this route:
Artifact to write now:
Gate not yet applicable:
Promotion explicitly forbidden:
```

If the route is `materialization` or `exploratory-probe`, do not create a proposition. If the user asks for a "direction-setting proposition" before the material exists, write a direction-setting material/probe note instead.

If baseline/comparator design is the next action, check `materialization` before `implementation-handoff`, `implementation-milestone`, or `exploratory-probe`. A user asking to move fast, avoid paperwork, produce a valid CSV, skip novelty, or treat the run as exploratory is not evidence that public baselines, competition writeups, or comparator conventions are irrelevant.

`status_brief.md` is the only standard project-level stakeholder brief. It is not a research paper, does not count as proposition resolution, and does not trigger next-cycle proposition creation.

`basic_research`, `applied_research`, and `experimental_development` classify work; they do not determine the exit artifact. Acceptance tests for a utility or harness are proposition support only if the proposition and plan made that acceptance condition the discriminator.

Blocked output shape:

```text
Route: <canonical route or blocked>
Blocking condition: <not uncertain | material absent | no Bit | non-plan-ready state | missing review>
Missing artifact: <path or external item>
Promotion explicitly forbidden: <proposition | hypothesis plan | support | landmark-aspirant | paper | claim>
Next action: <single concrete action>
```

## Work Loop

### 1. Intake

Write or update `intake.md` with:

- user intent and desired outcome
- the uncertain-in-outcome question
- available material
- missing material
- current canonical route

If the user only wants a known method implemented exactly as described, say this is implementation work and do not open a proposition or hypothesis lifecycle. If the user reframes toward an uncertain question, continue.

### 2. Scoping

Write or update `literature/scoping.md` before proposition creation. Capture:

- existing work and whether the intent is already solved
- comparators, datasets, public baselines, competition writeups/notebooks/discussions when relevant, and known failures
- contradictions or gaps that matter for the intent
- retrieval attempts and claim-scope narrowing when sources are unavailable

Scoping is not the plan survey. It prepares proposition material and gates baseline/comparator design. Do not implement a submit-able/minimal baseline, choose a comparator, or describe a baseline as safe from a local-data-only audit. If retrieval is unavailable, record attempted sources/tools, queries or source IDs when available, failure evidence, and the narrowed implementation or claim scope before coding.

### 3. Material And EDA

Put raw or referenced material under `data/raw/`, derived data under `data/processed/`, and exploratory notebooks/tables/figures under `data/eda/`.

Write root `observations.md` as an observation backlog. Separate observed facts from interpretations. EDA can create observations, tensions, missing-measurement notes, and candidate comparators; it must not create claims.

If there is no observation, failure, success case, constraint, measurement, comparator, repeated trace, prior-work fact, theoretical tension, or bottleneck evidence, stop the research path and write the smallest material-acquisition task.

Do not use missing split identity, comparator, baseline, evaluator, discriminator, or measurement as an "Assumption" in a hypothesis plan. If the missing item controls what observation would separate the proposition from a competitor, stay in `materialization` or `exploratory-probe`.

Baseline implementation can be `implementation-handoff`, `implementation-milestone`, or `exploratory-probe` only after relevant existing-work scoping exists, or when the user supplied an exact method whose baseline/comparator choice is not part of the work. Otherwise, missing scoping keeps the route in `materialization`; do not treat "minimal baseline first" as an implementation shortcut.

### 4. Proposition Pass

When material exists and the route is `proposition-commit`, switch inline to `creating-propositions` in the same context. Do not dispatch a fresh separate-context subagent for proposition generation.

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

Positive result shape is not a closeout shortcut. If a single hypothesis under a proposition has a positive aggregate result, but same-proposition hypotheses remain open or the result analysis leaves a serious measurement/evaluator artifact explanation live, do not mark the proposition `supported`, do not draft `paper.md`, and do not move to the next proposition. Close out the executed hypothesis first:

- If the artifact, comparator, measurement, or evidence quality prevents interpretation, set the hypothesis to `tested-inconclusive` and record `TESTED_INCONCLUSIVE`.
- If part of the planned discriminator is supported but a material clause or rival explanation remains unresolved, set the hypothesis to `tested-partial` and record `TESTED_PARTIAL`.
- Update the parent proposition as still `open` or `under-specified` when the artifact branch means the proposition cannot yet support a claim.
- Write the specific material-acquisition or discriminator artifact needed to separate the live explanations before continuing.

Then the parent agent updates, in order:

1. `hypothesis.md`
2. hypothesis `decisions.md`
3. parent proposition state files using the `creating-propositions` discipline
4. proposition `decisions.md` when state changes
5. root `project_state.md`

Claims are evidence records, not proposition statuses. Before state-changing decisions or paper prose depends on a claim, run `scripts/check_claims.py`.

`provisional support` is not a proposition state and is not a promotion basis. Informal prose may hedge uncertainty only if the route does not change to `supported`, `paper-route`, or next-cycle work.

### 8. Paper And Next Cycle

Create `propositions/Pxxx_slug/paper.md` only when a proposition reaches `supported` or `contradicted` through `claim-resolution`. Do not postpone the paper because per-hypothesis notes exist, because the project may continue, or because a future summary seems easier. The resolution transition is the publication trigger.

Do not create a provisional `paper.md`. A stakeholder draft, meeting memo, progress report, or one-positive-result summary before proposition resolution is `stakeholder-brief` and goes to root `status_brief.md`. `status_brief.md` is not a paper and does not trigger the next cycle.

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
|-- status_brief.md
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

- `research`: `intake.md`, root `observations.md`, root `status_brief.md`, `literature/{scoping,papers,positioning}.md`, `data/{raw,processed,eda}/`, `project_state.md`, root `decisions.md`, `propositions/Pxxx/paper.md`, and hypothesis files.
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

- `literature/scoping.md`: before proposition creation and before baseline/comparator design, identify existing work, public baselines, competition writeups/notebooks/discussions when relevant, comparators, datasets, known failures, and whether the intent is already solved.
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
