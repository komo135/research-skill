---
name: research
description: >-
  Use for serious research or capability/technology workstreams where conclusions, claims, or
  technical capabilities must survive replication, review, or later decision
  use. Supports workstream-aware research projects, Pure Research and R&D
  compatibility labels, R&D Program coordination,
  Result-to-Question loops, Result-to-Capability loops, A0-A5 analysis depth,
  right-sized rigor, promotion gates, kill criteria, pre-registration,
  reproducibility, lightweight two-axis review at promotion time, and
  user-facing outcome reports.
  Do not use for ordinary fact lookup, quick background research, or simple
  summaries.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Research

A protocol skill for agent-driven serious research and R&D. The job is not to
produce quick answers. The job is to keep research state honest, push analysis
to estimation or assertion level, and progress by the smallest defensible step.

## Prime Directive

**Fact collection is not research. Fact + causal analysis at A4 (estimation)
or A5 (assertion) is research.**

A `supported` claim — for either a capability / technology research result or
a phenomenon / mechanism research finding — requires the analysis to reach
**A4 minimum**. "It worked" and "it failed" are both A0, not results. Read
`references/shared/analysis_depth.md` before any trial interpretation, and
`references/shared/result_analysis.md` before writing any explanation of
success or failure.

## First Decision: Map the Current Research State

Before any charter, capability map, hypothesis, or trial design, map the
current research state. The first question is not "which discipline is this
project?" It is "which uncertainty is blocking progress, and which state will
this work update?"

A project can contain multiple workstreams. The project itself is not Pure
Research or R&D, and it must not be locked into an exclusive mode at startup.
The project owns the final intent, decision context, uncertainty list,
workstream list, cross-workstream dependencies, and durable decision log. A
workstream is the unit that selects a state object and gate. When the final
intent is to build a system, do not classify the whole project as Capability /
Technology Research. Say that Capability / Technology Research is a
provisional workstream fit only when the next blocking uncertainty is whether a
technical capability can be made to work under stated conditions.

Use these implemented workstream labels to choose the local ledger and
protocol gate:

| Workstream label | Use when | State object | Gate / review |
|---|---|---|---|
| **Phenomenon / Mechanism Research** (Pure Research-compatible) | Reduce uncertainty about a phenomenon, mechanism, cause, or boundary condition without making an artificial capability the direct deliverable | `explanation_ledger.md` | PR/FAQ, targeted literature, confirmatory pre-registration when a claim needs high reliability, A4+ support gate |
| **Capability / Technology Research** (R&D-compatible) | Reduce technical uncertainty about an unestablished capability by identifying design hypotheses, success conditions, failure conditions, and operating constraints | `capability_map.md` | reviewed charter, kill criteria, TRL / stage gate, A4+ promotion-relevant analysis |

Evaluation, design, exploration, and engineering support are activities or
artifacts inside a selected workstream, not workstream labels. Do not create a
new durable ledger or classification for them. If such work needs to support a
claim, state whether the claim updates an explanation question or a capability
claim, then use the matching state object and gate above.

R&D remains a compatibility label for Capability / Technology Research; it is
not PoC development. A prototype is an evidence device and possible
deliverable, but "it runs" does not update research state unless the analysis
identifies why it works or fails, under what boundary conditions, against which
alternatives, and with what reproducibility. Pure Research remains a
compatibility label for Phenomenon / Mechanism Research; it is not the only
place where mechanism work can happen.

Start with the smallest defensible state map:

1. Write project intent: what decision, explanation, capability, or artifact
   the project ultimately serves.
2. List current uncertainties that block progress.
3. Pick the initial workstream with the highest decision value. The label is
   provisional.
4. Select exactly one implemented state object for that workstream:
   `explanation_ledger.md` for Phenomenon / Mechanism Research or
   `capability_map.md` for Capability / Technology Research.
5. Write the evidence plan: which artifact could update which explanation
   question or capability claim.
6. Select the protocol gate. A capability workstream that produces
   promotion-relevant evidence needs reviewed charter and kill criteria. A
   phenomenon workstream that can support a claim needs PR/FAQ, targeted
   literature, and reviewed pre-registration when entering confirmatory
   research. A4+, reproducibility, focused process review, and conclusion
   review are not relaxed.
7. Add, split, merge, park, or retire workstreams as evidence reveals new
   uncertainty.

Workstream operations must not become silent pivots. `add` may introduce a new
dependent workstream when new uncertainty appears. `split`, `merge`, `park`,
and `retire` require a `decisions.md` entry naming the trigger, affected
workstream IDs and ledger rows, evidence reused or excluded, parent / child
links, and the gate that applies next. Quietly relabeling scope, thresholds,
interpretation, support status, or TRL is forbidden.

## Project Decision Gate

The project decision gate decides project completion, park, kill, handoff, or
external sharing by citing child workstream gate results. It does not re-score
TRL, support status, or A-tier, and it does not create a project-level support
status that overrides child ledgers.

Project decisions must cite the authoritative workstream source:
`capability_map.md`, `explanation_ledger.md`, the relevant promotion or support
review, and the durable `decisions.md` entry. If a project-level question
requires changing TRL, support status, analysis tier, claim scope, kill state,
or promotion, stop and perform that change inside the affected workstream's
protocol first.

## R&D Program

An R&D Program is an optional coordination layer, not a third discipline. Use
it only when several projects or major workstreams need a shared roadmap,
dependency view, or sequencing discussion across separate ledgers.

The program layer reads child project or workstream gate results and dependency
declarations. It does not re-score TRL, analysis tier, promotion, claim truth,
kill state, or support status. Those decisions remain inside each child
project or workstream's `capability_map.md`, `explanation_ledger.md`,
promotion gate, and `decisions.md`.

Read `references/program/program_map.md` when coordinating multiple projects.
Program notes may summarize why one child blocks another, which handoff is
pending, and which next project decision is needed, but they must cite the
child ledger instead of creating a second state system.

## Right-Sized Rigor

Rigor is sized to the research state being changed. Orientation, literature
triage, scaffold setup, smoke tests, and non-load-bearing exploration may use
lighter notes because they do not move durable research state. Any update that
changes a claim, TRL, support status, scope, kill decision, promotion, or
cross-workstream or cross-project dependency uses the full protocol required by
that state transition.

Right-sized rigor is not a relaxation path. These requirements are
non-relaxed:

- A4+ for `supported`, `matured`, `established`, or `promoted`.
- Reviewed pre-registration for Pure Research trials that can support a claim.
- Reviewed charter and kill criteria before R&D evidence-producing work can fire
  a kill or promotion-relevant decision.
- Reproducibility records for every promotion-eligible or claim-cited trial.
- Focused process review and conclusion review before promotion or externally
  shared load-bearing claims.
- Maintenance plan requirements for any `継続改善型` core technology.

## Framework Boundary

This skill defines the **protocol layer**. It must stay separate from the
**project instance layer**.

| Layer | Owns | Must not contain |
|---|---|---|
| Protocol layer | Schemas, gates, status vocabulary, required evidence, promotion rules | Active candidates, selected symbols, tuned parameters, current performance metrics, experiment-specific conclusions |
| Project instance layer | Concrete research target, candidate definitions, data paths, configs, implementation, generated reports | New protocol rules, reusable workflow changes, hidden state transitions |

**Evidence artifacts do not own research contracts.** Notebooks under
`purposes/`, rows in `results/results.parquet`, files under `configs/`,
and framework code under `src/` produce observations, metrics, logs, and
run metadata. They do not decide capability maturity, support status,
promotion, kill, park, or pivot.

**Framework code must not require capability IDs.** Implementation APIs,
configs, and reusable framework modules must not require `capability_id`,
`core_tech_id`, TRL, stage, exit criteria, kill criteria, or explanation
IDs as part of their normal operation. Those identifiers may appear in
ledger assessment entries that cite evidence artifacts, not as required
inputs to the implementation itself.

**capability_map.md is not an implementation API.** It is a research
state ledger. The correct flow is: project-instance code produces a
neutral artifact; the protocol layer later cites that artifact as
evidence; the review layer checks whether the cited evidence warrants the
claimed state transition.

Do not embed active candidates in reusable workflow docs, skill templates, or
protocol references. A phrase like "the current candidate in cohort B" belongs
in a project trial report, a config, a decision entry, or a project state
index, not in this skill or its reusable templates.

Generated reports are snapshots. Evidence artifacts are snapshots too. They
may summarize observations, but they are not the source of truth for state
transitions. The authoritative state lives in `capability_map.md` or
`explanation_ledger.md`, with durable transitions in `decisions.md` and
evidence links to trial artifacts.

When inheriting an existing project, diagnose boundary violations before doing
new research:

- Protocol documents should describe schemas and gates only.
- State ledgers should contain IDs, status, TRL / analysis tier, blockers,
  exit criteria, kill criteria, and evidence links.
- Project-instance artifacts should contain concrete symbols, universes,
  model classes, parameter grids, data paths, code, configs, and generated
  reports.
- If a file tries to be workflow guide + current candidate report + TODO list,
  split it before promoting any claim.

### Status terminology (R&D)

Three distinct status terms apply at three different scopes. They are not
interchangeable; conflating them invalidates promotion review.

| Term | Scope | Meaning | Gate it controls |
|---|---|---|---|
| **matured** | Capability (Layer 2) | Reached its target TRL (≤ TRL-6 for ship), kill criteria un-fired | End of capability's trial loop |
| **established** | Core technology (Layer 1) | All child capabilities matured, kill criteria un-fired, analysis at A4+ | Core tech ready for upstream consumption |
| **promoted** | Project (target) | All core techs established, integration test ran AFTER upstream exits, and (if any core tech is `継続改善型`) maintenance plan filed | Project closure or transition to maintenance cadence |

For Phenomenon / Mechanism Research, the equivalent claim-level term is
**`supported`**, with the same A4+ requirement at the analysis-depth axis.

## Capability / Technology Research (R&D-compatible)

Capability / Technology Research establishes the knowledge needed for a
technical capability to work under stated conditions. R&D is retained as a
compatibility label for this workstream type. Required sequence — read each
linked reference before executing the step:

1. **Charter** (`references/rd/rd_charter.md`) — answer the 8 Heilmeier
   questions, including kill criteria (H6: what evidence would kill this
   workstream or target). Without a charter on file, decomposition is
   forbidden.
2. **Core Technologies** (`references/rd/core_technologies.md`) —
   intellectual decomposition. Identify the minimal set of technologies that
   require research investment to establish for this target. Each core
   technology gets a research question, target contribution, lifecycle type
   (永続型 / 継続改善型), and prior-work link. See § Decomposition Discipline
   below for the operational filter.
3. **Capability map** (`references/rd/capability_map_schema.md`) —
   operational decomposition. For each core technology, list capabilities
   sized so one evidence package changes one capability's TRL claim. Each capability row
   references its parent `core_tech_id` (or `integration` for cross-cutting),
   and carries a kill criterion alongside its exit criterion.
4. **Maturity** (`references/rd/trl_scale.md`) — assign TRL-0 to TRL-6. TRL-6
   (operational prototype) is the promotion line. TRL advancement is evidence-based;
   do not claim a level unless the evidence meets that level's definition.
5. **Stages** (`references/rd/rd_stages.md`) — for each capability run
   Scoping → De-risk → Build → Validate → Integrate, with Go / Kill /
   Hold / Recycle decision points between each. Tackle the hardest
   sub-question first; de-risk to learn whether to continue, hold, recycle,
   or terminate, not to confirm.
6. **Workflow** (`references/rd/rd_workflow.md`) — initial-day prohibitions,
   state-change logging, stop conditions.
7. **Promotion** (`references/rd/rd_promotion_gate.md`) — promote a target
   only when every core technology is `established` (all child capabilities
   matured to TRL-6 with kill criteria un-fired and analysis at A4+),
   integration test ran AFTER all upstream exits fired (ordering verified),
   and — if any core technology is `継続改善型` — a maintenance plan is on
   file in `decisions.md`.

## Phenomenon / Mechanism Research (Pure Research-compatible)

Phenomenon / Mechanism Research reduces ignorance about a phenomenon,
mechanism, cause, or boundary condition. Pure Research is retained as a
compatibility label for this workstream type. Required sequence — read each
linked reference before executing the step:

1. **PR/FAQ** (`references/pure_research/prfaq.md`) — write the press release
   for the finding you would publish if research succeeded. If you cannot
   write a coherent PR/FAQ, the question is not ready. **Do this first**:
   without a scoped question, literature search is unfocused and
   pre-registration is premature.
2. **Targeted literature** (`references/shared/literature_review.md`) —
   survey prior work scoped by the PR/FAQ, including the user's own past
   notebooks and decisions. Stop when competing explanations are clear and
   prior failure modes are documented.
3. **Exploratory / confirmatory research choice** — Pure Research clearly
   separates exploratory research from confirmatory research. Exploratory
   research handles purpose, current-state assessment, hypothesis or
   explanation candidates, initial-approach search, and observations; its
   outputs remain `exploratory` / `diagnostic`. Confirmatory research exists
   to confirm exploratory findings with higher reliability. Exploratory
   research does not have to be followed by confirmatory research.
   If the outcome is a map of observations, candidate explanations, or a
   stop/park decision, exploratory work may be sufficient. If the result will
   become a `supported / external claim / high reliability claim`, then
   move to confirmatory research.
4. **Pre-registration** (`references/pure_research/preregistration.md`) —
   pre-registration is a confirmatory-research tool, not exploratory
   research itself.
   state the question, competing explanations (≥2), test design, and expected
   contrast under each explanation before the trial. In confirmatory research,
   before execution, compare `PR_<id>` against the current state: exploratory
   result, data availability, assumptions, implementation constraints, and
   current question. The purpose of comparing the pre-reg against the current
   state is not only to follow the pre-reg, but also to verify that the current
   state has not broken the PR's assumptions.
   After the trial, compare actual analysis against the planned design and
   note any deviations.
5. **Explanation ledger**
   (`references/pure_research/explanation_ledger_schema.md`) — single state
   object. Claim-cited or promotion-relevant results update explanation rows;
   exploratory observations may stay in run notes until they become
   load-bearing.
6. **Workflow** (`references/pure_research/pr_workflow.md`) — Exploratory
   Research Loop and Confirmatory Research Loop, deviation handling,
   state-change logging, stop conditions. Push analysis depth on the current
   result before collecting more data or designing a confirmatory trial.
7. **Promotion** (`references/pure_research/pr_promotion_gate.md`) — promote a
   claim only when a discriminating test against ≥1 serious alternative
   passed, multiple-testing correction is honest, analysis depth reaches
   A4+, and an IMRAD draft (`references/pure_research/imrad_draft.md`) is
   producible.

## Analysis Depth (all workstreams)

Analysis depth is the primary deliverable, not a side note. Tier scale:

| Tier | Meaning |
|---|---|
| A0 | Observation only |
| A1 | Hypothesized explanation named, no evidence |
| A2 | ≥1 competing explanation identified |
| A3 | Discriminating evidence between primary and ≥1 alternative (preliminary) |
| A4 | Estimation: mechanism named, alternatives excluded, scope precise, multiple sources of supporting evidence |
| A5 | Assertion: mechanism causal, alternatives systematically excluded, replicable across conditions and periods, external prediction holds |

`supported` requires A4 minimum. A3 is `preliminary`. Below A3 is observation
only.

The principle applies symmetrically to success and failure. "It worked
because the model is good" is A1 with a generic terminal label and is
forbidden as a final claim. The same standard applies to "it failed because
of noise / context shift / resource constraint / data quality" — see
`references/shared/result_analysis.md` for decomposition patterns and bad/good
examples.

Before designing a new trial, push the analysis on the current trial as far
as it can go. Increasing analysis depth on existing data is research;
collecting more data without analyzing existing observations is not.

## Tracking Backend

Choose the run tracking backend briefly during project initialization or before
the first load-bearing claim, whichever comes first. This is not a ceremony:
name where run notes, tracker runs, or results rows will live, and how a
reviewer can resolve the evidence for a claim. This skill defines review
anchors, not a single mandatory tool.

Acceptable choices include MLflow, Weights & Biases, Neptune, Trackio,
TensorBoard, Sacred, DVC, local parquet / SQLite / flat-file ledgers, or an
existing organizational tracker. Ordinary exploration, smoke tests, debugging,
and early parameter probing may be recorded as a lightweight run note, tracker
run, notebook note, or `results` row with enough context to interpret the
result later.

Promotion-eligible, externally shared, or claim-cited results need stronger
anchors: durable run ID or artifact path, params, headline metrics, data version
note, code version, environment pin, seed where relevant, and enough rerun instructions for
a reviewer to reproduce or challenge the claim. If an exploratory result later
becomes load-bearing, rerun it under this protocol instead of
retroactively pretending the earlier note was complete.

Record the backend decision in `decisions.md` by project initialization or
before the first load-bearing claim. Name the selected tool or file pattern,
where runs are stored, and how reviewers resolve `trial_id` to a run record.

`results/results.parquet` is the portable default evidence index, not the only
valid source of run metadata. If an external tracker is selected, `results`
may store a compact index row with `tracker`, `tracking_uri`, `run_id`, and
`artifact_uri`, while the tracker owns detailed metrics and artifacts. Ledgers
still own state transitions; trackers and result tables only provide evidence.

A complete inventory/export is not mandatory for every project. Keep only the
run set needed to support honest selection correction, multiple-testing
adjustment, failed-attempt interpretation, or promotion review. A small project
may need only a few result rows. A sweep-heavy project must retain the sweep
space and selection history that informed the claim. The rule is coverage of
the decision-relevant evidence, not archival completeness for its own sake.

## Decomposition Discipline (R&D)

R&D decomposition is a **two-layer** structure. Mixing the layers, or skipping
the intellectual layer to go straight to capabilities, hides the research
questions that justify the project.

### Layer 1: Core Technologies (intellectual)

The minimal set of technologies that require research investment to establish
for this target. Each row in `capability_map.md` Section 1:

| Field | Meaning |
|---|---|
| ID | K1, K2, ... |
| コア技術 | Name (1 short phrase) |
| 研究で確立する問い | The single research question this core tech needs answered |
| target への寄与 | Why this is needed for the target |
| 発展性 | `永続型` (establish-once) or `継続改善型` (continuous-improvement, requires maintenance plan) |
| 先行研究 | Link to `literature/papers.md` section |
| Status | active / established / blocked / split / merged / stale / parked |

**Operational filter for "is this a core tech?"** A candidate qualifies only
when ALL three hold:

1. Requires research / establishment work for THIS target (cannot be obtained
   off-the-shelf).
2. Can be expressed as a single distinct research question.
3. The question is independent of other core techs' questions.

If the candidate fails (1) → it is a dependency (use as-is, do not list).
If it fails (3) → merge into the parent core tech.
If you cannot write a research question for it → it is a capability or task,
not a core tech.

There is **no count target**. Target difficulty determines the count
naturally; if you find yourself with 20+ candidates, the filter is too loose
(many are dependencies); if 1, decompose harder or reconsider whether this
should be Pure Research instead.

### Layer 2: Capabilities (operational)

For each core technology, list capabilities sized so one evidence package can
change one capability's TRL claim without moving the whole stack. Each capability row references its
parent `core_tech_id` (or `integration` for cross-cutting work). See
`references/rd/capability_map_schema.md` for the full schema.

### Lifecycle implications

A target's promotion expression and termination semantics depend on the
lifecycle composition of its core technologies:

- All core techs `永続型` and `established` → "fully completed", project closes.
- Any core tech `継続改善型` → completion = "v1 established + maintenance plan
  scheduled". The project's closing entry in `decisions.md` MUST name the
  re-evaluation cadence and the re-investment trigger condition.

### Decomposition status transitions

Same vocabulary at both layers (active / established (core tech only) /
matured (capability only, = TRL reached target) / blocked / split / merged /
stale / parked). Splits create child rows under the parent; merges absorb
duplicate rows; stale rows are kept (not deleted) for historical traceability.

## Review (run before promotion or external load-bearing claims)

Two-axis review is a focused promotion review, not a full-project inspection. Run
the relevant parts before any R&D transition to `matured`, `established`, or
`promoted`, before any Pure Research promotion to `supported`, or before an
externally shared load-bearing claim:

- **Process review** (`references/review/process_review.md`) — was the
  relevant discipline followed for the claim being promoted? Read only the
  process areas that could invalidate this state change.
- **Conclusion review** (`references/review/conclusion_review.md`) — are the
  conclusions warranted? Check only the load-bearing axes: implementation
  correctness, statistical sufficiency, claim discipline, **analysis depth
  (A4+)**, reproducibility, and cold-eye review where they bear on the claim.
  For claim-bearing notebook artifacts, the focused four-reviewer procedure in
  `references/review/experiment_review_protocol.md` may be used as a
  conclusion-review subprocedure, not as a separate promotion gate.

The review documents are menus of possible checks, not mandatory full
checklists. Mark non-applicable items as out of scope, and do not read or review
unrelated history. Promotion-blocking items and state transitions require
concrete evidence citation (file:line, reference, numeric value, run ID, artifact
URI, or tool output). Lightweight process observations may be summarized when
they are not load-bearing. "Overall OK" / "looks good" / "appears correct"
verdicts are forbidden at promotion or external-claim decision points.

## User-Facing Outcome Reports

When reporting a research outcome, promotion, kill, park, pivot, or deployment
recommendation to the user, produce a **human-judgment artifact** in the final
answer or as a linked report artifact. The user should not have to inspect raw
notebooks, ledgers, or tracker exports to understand what happened and what
decision remains.

The report must include:

- The plain-language decision: what changed, what did not change, and whether
  the result is `supported`, `preliminary`, blocked, killed, parked, or still
  observation-only.
- At least one piece of visual or tabular evidence that makes the result
  intuitive: a figure, chart, DAG, timeline, comparison table, confusion/error
  table, before/after table, or compact metric table. Choose the form that
  best exposes the key uncertainty, not the form that flatters the result.
- Evidence citations for every load-bearing claim, linking each visual or table
  back to file:line, artifact URI, run ID, reference, numeric output, or ledger row.
- A scope and caveat note: what conditions the result covers, what alternatives
  remain plausible, and what evidence would change the decision.
- The next decision or action requested from the user, if any.

Visuals and tables are explanatory snapshots, not state owners. The ledger and
review gates still decide support, maturity, promotion, kill, and pivot. If no
visual is possible, state why and provide the smallest table that lets the user
compare the evidence directly. Do not hide the outcome behind "see notebook";
the final report must carry enough intuitive evidence for human judgment.

## Guardrails

- **Kill requires A4+ evidence**. A kill criterion firing is a trigger for
  terminal review, not an automatic terminal state. Mark `killed` only after
  mechanism-level analysis rules out repairable causes such as config error,
  data defect, scope error, or dependency immaturity. Promotion still requires
  every promotion-blocking checklist item to pass.
- **Evidence citation is mandatory for load-bearing claims**. Any claim of
  "passed" / "verified" / "confirmed" that supports `supported`, `matured`,
  `promoted`, `killed`, external sharing, deployment recommendation, major
  deviation, or claim-scope change must reference a specific file:line, reference,
  numeric value, or tool output. Summary verdicts without citation are
  forbidden at those decision points.
- **Entry guardrails**.
  - Capability / Technology Research: promotion-relevant or claim-bearing
    implementation must wait until the charter and kill criteria exist. A
    non-load-bearing scaffold, interface probe, smoke test, environment setup,
    data plumbing, or file scaffold is allowed when it is labeled as enabling
    work and is not used to advance TRL, fire a kill criterion, promote a
    capability, or support an external claim. *Why*: kill criteria (Heilmeier
    H6) must be ready before a trial can fire one. Evidence-producing code
    created before kill criteria exist can accumulate sunk cost that biases
    future kill decisions.
  - Phenomenon / Mechanism Research first day: do not run a claim-bearing confirmation trial.
    PR/FAQ, targeted literature, exploratory planning, explanation
    candidates, lightweight exploratory probes, scaffold setup, and — when a
    claim will need high reliability — pre-registration are allowed. *Why*:
    exploratory research may map the problem before a confirmation target
    exists, but a claim-bearing confirmatory trial must survive the garden of
    forking paths. A confirmation trial run before the pre-registration is
    ready is a shopping trip — once you have seen the data,
    "pre-registration" is theater.
  - **What IS allowed on day 1**: data infrastructure setup, environment
    pinning (`uv.lock`), data version recording, raw data sourcing, scaffold
    file creation. The prohibition targets evidence-producing work
    (implementation that runs / trial that produces metrics), not
    enabling work.
- **Session-level Capability / Technology Research sequencing**. Once the
  charter is complete, the seven R&D-compatible steps must preserve dependency
  order:
  - No capability row may be written until its parent Layer 1 core technology
    has complete fields and passes the operational filter (§ Decomposition
    Discipline).
  - **No Stage gate (Scoping–De-risk–Build–Validate–Integrate) may be run on
    a capability while its parent K, declared dependencies, or integration
    path have incomplete Layer 1 fields.** Unrelated sibling K rows do not
    globally block the branch. If a Stage gate surfaces a new upstream K,
    suspend the affected branch, document the deviation, re-scope the dependency
    path, then resume.
  - Any rollback to an earlier step requires a dated deviation entry in
    `decisions.md` citing the blocker. State-change logging alone does
    not satisfy this — moving any ledger row is necessary but not
    sufficient.
- **State-change logging**. Sessions that change durable research state must
  move at least one ledger row or record `no progress: <reason>` in
  `decisions.md`. Short orientation, environment setup, and interrupted
  sessions may remain outside the durable log unless they change a claim,
  state transition, or gate decision.
- **Lightweight run tracking is enough for exploration**. Ordinary exploratory,
  smoke-test, debugging, and non-load-bearing experiments may use a short run
  note, tracker run, notebook note, or results row. Do not turn every trial into
  a decision-log entry or full review package.
- **Reproducibility 3-tuple**. Every promotion-eligible or claim-cited trial
  records data version + git commit + environment pin via the selected tracking backend
  or equivalent local note. Exploratory, smoke-test, and
  debugging runs may use lightweight run notes. If later needed for promotion,
  rerun under the promotion-eligible protocol; do not retroactively relabel
  exploratory output as if it had been captured at trial time.
- **Planning artifacts**. Charter, pre-registration, and kill criteria must be
  reviewed before they become load-bearing. Any load-bearing amendment requires
  an explicit deviation entry in `decisions.md` or a new planning artifact.
- **No placeholders in deliverables**. Templates produce real content; any
  remaining `TBD`, `TODO`, `XXX`, `???`, or `{{...}}` blocks the deliverable.

## Required Artifacts

Common to a workstream-aware project:

```
project_state.md                 # project intent, uncertainties, workstreams
README.md                        # goal, current state, entry points
decisions.md                     # durable state transitions only
literature/papers.md             # prior work
literature/differentiation.md    # how this differs from prior work
purposes/INDEX.md                # evidence artifact index
results/results.parquet          # portable default evidence index
configs/                         # project-instance experiment configs
src/                             # project-instance implementation, if any
tests/                           # project-instance verification, if any
reproducibility/{uv.lock,env_lock_ref.txt,data_versions.txt,shared_pins.txt,seed.txt}
tracking/                        # optional local tracker config / exported run refs
workstreams/                     # recommended home for workstream ledgers
```

Capability / Technology Research workstreams add:

```
charter.md                       # reviewed charter (Heilmeier 8 Q)
capability_map.md                # primary state object
                                 #   Section 1: Core Technologies (intellectual layer)
                                 #   Section 2: Capabilities (operational layer, with core_tech_id)
```

Phenomenon / Mechanism Research workstreams add:

```
prfaq.md                         # working-backwards entry document
prereg/PR_<id>.md                # reviewed pre-registration, one per trial
explanation_ledger.md            # primary state object
imrad_draft.md                   # paper-shaped deliverable, started early
```

## References

Read only what applies to your current step. References are organized by
audience.

**Shared (all workstreams)**

| Reference | When to read |
|---|---|
| `shared/analysis_depth.md` | Before any trial interpretation. MANDATORY. |
| `shared/result_analysis.md` | Before writing any explanation of success or failure. |
| `shared/literature_review.md` | Project initialization, before any new hypothesis or capability. |
| `shared/reproducibility.md` | Setting up data version + git commit + environment pin for promotion-eligible or claim-cited trials. |
| `shared/results_db_schema.md` | Appending interpreted trial results. |

**Capability / Technology Research (R&D-compatible)** — see the entry sequence above. Key references:
`rd/rd_charter.md` (Heilmeier 8 Q) ·
`rd/core_technologies.md` (intellectual decomposition, lifecycle) ·
`rd/capability_map_schema.md` (operational decomposition with core_tech_id) ·
`rd/trl_scale.md` ·
`rd/rd_stages.md` (Cooper Stage-Gate per capability) ·
`rd/rd_workflow.md` ·
`rd/rd_promotion_gate.md`.

**Phenomenon / Mechanism Research (Pure Research-compatible)** — see the entry
sequence.

**Program coordination** — optional multi-project roadmap:
`program/program_map.md`.

**Review** — see § Review above.

## Bundled Helper Scripts

| Script | Purpose |
|---|---|
| `new_project.py` | Initialize a project shell; compatibility `--mode rd|pure-research` may create a first workstream layout |
| `new_trial.py` | Generate a numbered neutral evidence artifact |
| `aggregate_results.py` | Append interpreted trial rows (mode-aware schema, includes `analysis_tier`) |
| ledger consistency helper | Lint capability_map / explanation_ledger / analysis-section consistency |
| `render_capability_dag.py` | Mermaid DAG of the R&D capability dependency graph |
| `render_explanation_dag.py` | Mermaid DAG of the explanation hierarchy |
| `charter_interview.py` | Interactive Heilmeier 8-question elicitation |
| `draft_imrad.py` | Generate IMRAD draft from explanation_ledger + decisions + results |
| `standup.py` | Summarize the last 24h of decisions.md transitions |
| `lit_fetch.py` | Batch fetch prior-work metadata from arXiv and Semantic Scholar |
