# rd_workflow.md

Operating rules for an R&D Workstream. This workflow follows general R&D
usage: basic research, applied research, and experimental development.

## When to read

- First session of a new R&D Workstream
- Writing or reviewing `rd_plan.md`
- Preparing pre-registration for R&D work
- Comparing executed work with a prior plan
- Creating a claim-bearing or preregistered outcome report
- Closing, parking, splitting, or handing off a workstream

## General R&D categories

Use one category as the current best label. A workstream may change category
prospectively when the uncertainty changes; record the reason in
`decisions.md`.

| Category | Use when | Typical output |
|---|---|---|
| Basic research | The work aims to acquire new knowledge without a specific immediate application | clarified mechanism, map of observations, narrowed question |
| Applied research | The work is original investigation directed toward a specific practical objective | evaluated method, boundary conditions, decision evidence |
| Experimental development | The work systematically uses research and practical experience to produce or improve a product, process, or method | prototype evidence, comparison table, improvement report |

For this skill, R&D work should be novel, creative, uncertain, systematic, and
transferable or reproducible. Current-state assessment is orientation, not an
R&D category. Hypothesis validation is evidence discipline, not an R&D
category.

## State object

`rd_plan.md` is the R&D state object. It should stay small enough to keep the
work legible:

- category
- current-state assessment
- objective / question
- uncertainty being reduced
- planned evidence and pre-registration links
- actual execution and result summary
- plan-to-result comparison
- report package links, when produced
- next decision

Evidence artifacts under `purposes/`, tracker runs, result rows, figures, and
reports do not update state by themselves. Cite them from `rd_plan.md` or
`decisions.md` when they become decision-relevant.

## Plan -> execute -> compare -> report

### Plan

Before claim-bearing work starts, write or select the plan that will be used to
judge it. For R&D, this may be a section in `rd_plan.md` or a
pre-registration under `prereg/PR_<id>_<slug>.md`.

The plan should name:

- objective / question
- R&D category
- scope and inputs
- procedure or inspection path
- expected outputs
- decision or follow-up criteria
- what would prevent the output from being used as claim-bearing evidence

### Execute

Run the work against the written plan. Exploratory, smoke-test, debugging, and
orientation work may be recorded with lighter notes when it is not presented as
claim-bearing evidence.

### Compare

After execution, compare actual work and results against the plan:

- what was executed as planned
- what changed and why
- what result was observed
- what evidence supports that statement
- what remains uncertain
- whether the result is claim-bearing, exploratory only, or blocked

Pre-registration is a plan, not a prison. If the plan should change, amend it
prospectively and disclose the change. A midstream plan governs future work or
explicit reruns only; prior work is prior or exploratory evidence.

### Report

When the work is preregistered, claim-bearing, externally shared, or used for a
terminal decision, produce a report package that carries enough evidence for a
reader to understand the decision without opening raw notebooks. Follow
`references/shared/outcome_reports.md`.

Report contracts apply to report packages and presented evidence, not to
research or experiments. Claim-to-artifact checks are a reporting-side
requirement, not a continuous research tracking contract.

## Result-to-R&D Plan Loop

Every interpreted result should return to `rd_plan.md` with one of these
outcomes:

- keep objective and run the next planned step
- revise objective prospectively
- add a narrower workstream
- split into a phenomenon question and an R&D objective
- park until a named unblock condition appears
- reject-for-now or deprioritize without making a terminal claim
- open terminal review if A4+ evidence supports it

Use transparent changes for any plan or report drift. Avoid goalpost shifting:
do not change success criteria after seeing the result and then present the old
run as if it had been planned that way. If a result shows the original scope was
wrong, record a prospective re-scope and rerun the relevant work under the new
plan before making a load-bearing claim.

## State-change logging

Only sessions that change durable research state need a `decisions.md` entry.
Orientation, environment setup, interrupted work, smoke tests, debugging, and
ordinary exploration may stay in run notes, tracker runs, notebook notes, or
result rows unless they change a claim, state transition, gate decision,
terminal decision, pivot, or scope.

### Outcome A - State changed

Update `rd_plan.md` and append a short summary to `decisions.md`:

```markdown
## YYYY-MM-DD HH:MM session summary
- R&D Workstream <name>: <state change or decision>
- Evidence: <artifact path, run ID, table, or report package>
- Next: <next planned step>
```

### Outcome B - No state changed

Record `no progress` only when the session was explicitly attempting a durable
state change and the blocker itself matters for future project state:

```markdown
## YYYY-MM-DD HH:MM no progress: <reason>
- Attempted: <one sentence>
- Blocked by: <named missing evidence, dependency, or decision>
- Next: <what would unblock>
```

## Stop conditions

An R&D Workstream can close by:

- **Completed**: the planned question or objective has a clear answer for the
  declared scope, with report and evidence where needed.
- **Terminal kill**: A4+ evidence shows the objective is not viable under the
  declared scope, after repairable causes have been ruled out.
- **Parked**: a named external unblock condition is required.
- **Split / handoff**: the work revealed a separate phenomenon question,
  applied objective, or experimental development task.

Terminal decision is different from exploratory pruning. Candidate drop,
reject-for-now, and deprioritize may use A2-A3 evidence when they do not claim
the objective is impossible.

## Shared infrastructure governance

Many workstreams use the same data pipeline, feature library, or trial harness
as other workstreams. The workstream state rule applies to decision tracking,
not to infrastructure code.

Shared infrastructure should live outside any single project folder when it is
intended for reuse:

```text
workspace/
├── shared/
│   ├── data_pipeline/
│   ├── feature_lib/
│   └── trial_harness/
└── projects/
    └── alpha/
        ├── project_state.md
        ├── decisions.md
        ├── workstreams/
        │   ├── WS001-rd/
        │   │   ├── rd_plan.md
        │   │   └── prereg/
        │   └── WS002-phenomenon/
        │       ├── prfaq.md
        │       ├── prereg/
        │       └── explanation_ledger.md
        ├── purposes/
        ├── results/
        └── reproducibility/
```

Pin shared infrastructure with `reproducibility/shared_pins.txt` or an
equivalent tracker field when it affects claim-bearing evidence.

## Code reuse on workstream handoff

When an R&D Workstream adds, splits, or hands off to another workstream,
existing code, notebooks, and figures may be relevant. Reuse must be explicit.

Reusable:

- data pipeline code
- feature definitions and computations
- validation harnesses
- plot helpers and reporting templates
- sanity check scripts

Not reusable as-is:

- trial notebooks whose design belongs to the old workstream role
- decision log entries without a new state link
- state documents with a different objective or category
