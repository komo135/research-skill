---
name: research
description: >-
  Use for serious research or R&D workstreams where conclusions, claims, or
  decisions must survive replication, review, or later decision use. Supports
  workstream-aware research projects, general R&D categories, Result-to-Question
  loops, A0-A5 analysis depth, right-sized rigor, pre-registration,
  reproducibility, focused two-axis review, and user-facing outcome reports.
  Do not use for ordinary fact lookup, quick background research, or simple
  summaries.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Research

A protocol skill for agent-driven serious research and R&D. The job is to keep
research state honest while preserving research velocity: explore quickly,
record what was learned, and reserve stronger review for claims that actually
need to carry weight.

## Prime Directive

**Fact collection is not enough for a strong research claim.** Exploration can
start at A0-A2; external sharing, deployment-grade conclusions, and terminal
decisions need deeper analysis.

A4+ is reserved for `supported`, external claim, deployment recommendation, or
terminal decision. A2-A3 may decide the next experiment, provisional go / no-go,
park, deprioritize, or reject-for-now. Exploratory decisions do not create a
load-bearing claim. Terminal kill also requires A4+ because it closes a
workstream or target under the current scope.

"It worked" and "it failed" are both A0 until interpreted. Read
`references/shared/analysis_depth.md` before any claim-bearing interpretation,
and `references/shared/result_analysis.md` before writing any explanation of
success or failure that will guide a durable state change.

## First Decision: Map the Current Research State

Before any plan, hypothesis, or trial design, map the current research state.
The first question is not "which discipline is this project?" It is "which
uncertainty is blocking progress, and which state will this work update?"

Use the general R&D categories as compatibility language:

- **Basic research**: original work to acquire new knowledge without a specific
  immediate practical application.
- **Applied research**: original investigation directed toward a specific
  practical aim or objective.
- **Experimental development**: systematic work drawing on research and
  practical experience to produce new or improved products, processes, or
  methods.

For this skill, R&D work should be novel, creative, uncertain, systematic, and
transferable or reproducible. Current-state assessment is orientation, not an
R&D category. Hypothesis validation is evidence discipline, not an R&D
category.

A project can contain multiple workstreams. The project itself is not Pure
Research or R&D, and it must not be locked into an exclusive mode at startup.
The project owns the final intent, decision context, uncertainty list,
workstream list, cross-workstream dependencies, and durable decision log. A
workstream is the unit that selects a state object and gate.

Use these implemented workstream labels to choose the local state object and
review path:

| Workstream label | Use when | State object | Gate / review |
|---|---|---|---|
| **Phenomenon / Mechanism Research** (Pure Research-compatible) | Reduce uncertainty about a phenomenon, mechanism, cause, or boundary condition | `explanation_ledger.md` | PR/FAQ, targeted literature, pre-registration when useful or claim-bearing, A4+ support review |
| **R&D Workstream** (R&D-compatible) | Reduce uncertainty through basic research, applied research, or experimental development | `rd_plan.md` | R&D plan, pre-registration when useful or claim-bearing, plan-to-result comparison, A4+ review for load-bearing claims |

Evaluation, design, exploration, and engineering support are activities or
artifacts inside a selected workstream, not workstream labels. If such work
needs to support a claim, state whether the claim updates an explanation
question or an R&D objective, then use the matching state object and review path
above.

Start with the smallest defensible state map:

1. Write project intent: what decision, explanation, R&D objective, or artifact
   the project ultimately serves.
2. List current uncertainties that block progress.
3. Pick the initial workstream with the highest decision value. The label is
   provisional.
4. Select exactly one implemented state object for that workstream:
   `explanation_ledger.md` for Phenomenon / Mechanism Research or `rd_plan.md`
   for an R&D Workstream.
5. Write the evidence plan: which artifact could update which explanation
   question or R&D objective.
6. Select the review path. R&D uses plan -> execute -> compare -> report.
   Phenomenon work uses PR/FAQ, targeted literature, and pre-registration when
   the work is claim-bearing or needs planning/reporting discipline.
7. Add, split, merge, park, or retire workstreams as evidence reveals new
   uncertainty.

Workstream operations must not become silent pivots. `add` may introduce a new
dependent workstream when new uncertainty appears. `split`, `merge`, `park`,
and `retire` require a `decisions.md` entry naming the trigger, affected
workstream IDs and state rows or sections, evidence reused or excluded, parent
/ child links, and the review path that applies next. Quietly relabeling scope,
thresholds, interpretation, support status, or claim boundary is forbidden.

## Project Decision Gate

The project decision gate decides project completion, park, kill, handoff, or
external sharing by citing child workstream results. It does not override child
workstream claims or report conclusions.

Project decisions must cite the authoritative workstream source:
`rd_plan.md`, `explanation_ledger.md`, the relevant review or report package,
and the durable `decisions.md` entry. If a project-level question requires
changing support status, analysis tier, claim scope, kill state, or report
decision, stop and perform that change inside the affected workstream first.

## R&D Workstream

R&D in this skill follows the common research-and-development categories:
basic research, applied research, and experimental development. Read
`references/rd/rd_workflow.md` when creating or operating an R&D Workstream.

The R&D state object is `rd_plan.md`. It records:

- category: basic research, applied research, or experimental development
- current-state assessment and blocking uncertainty
- objective / question
- planned evidence and pre-registration references
- result summaries and plan-to-result comparison
- report package links when the result is claim-bearing or preregistered
- next decision or follow-up work

Pre-registration is available in every R&D category. It is a planning and
reporting discipline, not a prison: write or select the plan before work
starts, execute against the written plan, compare actual work and results with
the plan, disclose material changes, then report evidence and limitations.

## Phenomenon / Mechanism Research (Pure Research-compatible)

Phenomenon / Mechanism Research reduces ignorance about a phenomenon,
mechanism, cause, or boundary condition. Required sequence; read each linked
reference before executing the step:

1. **PR/FAQ** (`references/pure_research/prfaq.md`) - write the press release
   for the finding you would publish if research succeeded.
2. **Targeted literature** (`references/shared/literature_review.md`) - survey
   prior work scoped by the PR/FAQ, including the user's own past notebooks and
   decisions.
3. **Exploratory / confirmatory research choice** - exploratory research maps
   observations and candidate explanations; confirmatory research exists to
   confirm exploratory findings with higher reliability.
4. **Pre-registration** (`references/pure_research/preregistration.md`) -
   pre-registration is a general planning and reporting discipline. Plan ->
   execute -> compare -> report: Plan: write or select the pre-registration
   before work starts; Execute: run the work against the written plan; Compare:
   compare actual execution and results against the pre-registration; Report:
   publish the plan-to-result table, transparent changes, evidence, and
   limitations. Each file declares
   `preregistration_type: confirmatory | exploratory` and includes Study
   Information, Sampling / Data Plan, Variables / Measures, and a Transparent
   Changes Policy. Pre-registration is a plan, not a prison. A midstream
   pre-registration governs future work or explicit reruns only; prior work is
   prior or exploratory evidence.
5. **Explanation ledger**
   (`references/pure_research/explanation_ledger_schema.md`) - single state
   object. Claim-cited results update explanation rows; exploratory
   observations may stay in run notes until they become load-bearing.
6. **Workflow** (`references/pure_research/pr_workflow.md`) - Exploratory
   Research Loop and Confirmatory Research Loop, Transparent Changes handling,
   state-change logging, stop conditions. The Result-to-Question Loop routes
   observations back to the selected question.
7. **Support review** (`references/pure_research/pr_promotion_gate.md`) -
   support a claim only when a discriminating test against at least one serious
   alternative passed, multiple-testing correction is honest, analysis depth
   reaches A4+, and an IMRAD draft is producible.

## Analysis Depth (all workstreams)

Analysis depth is the primary deliverable, not a side note.

| Tier | Meaning |
|---|---|
| A0 | Observation only |
| A1 | Hypothesized explanation named, no evidence |
| A2 | At least one competing explanation identified |
| A3 | Discriminating evidence between primary and at least one alternative, preliminary |
| A4 | Estimation: mechanism named, alternatives excluded, scope precise, multiple sources of supporting evidence |
| A5 | Assertion: mechanism causal, alternatives systematically excluded, replicable across conditions and periods, external prediction holds |

`supported` is a load-bearing claim status and always requires A4 minimum. A3
is `preliminary`. Below A3 is observation only for claim status, but it can
still guide exploration.

The principle applies symmetrically to success and failure. "It worked because
the model is good" is A1 with a generic terminal label and is forbidden as a
final claim. The same standard applies to "it failed because of noise / context
shift / resource constraint / data quality" - see
`references/shared/result_analysis.md` for decomposition patterns and bad/good
examples.

## Report Evidence Provenance

Do not choose a tracking system as a research-startup contract. Ordinary
exploration, smoke tests, debugging, and early parameter probing may use a
short run note, tracker run, notebook note, or `results` row with enough
context to interpret the result later.

When a formal report package or external claim presents evidence, the package
must say how a reviewer resolves that presented evidence. Acceptable sources
include local notes, result rows, artifact paths, tracker records from MLflow,
Weights & Biases, Neptune, Trackio, TensorBoard, Sacred, DVC, an organizational
store, or another project-specific provenance note. The tool is optional; the
report provenance is what matters.

Claim-bearing report packages need enough anchors for the presented evidence:
data snapshot, code version, environment pin, seed when relevant, parameters,
headline metrics, artifact path or run ID when one exists, and rerun guidance
when a rerun is expected. If an exploratory result later becomes load-bearing,
rerun under the claim-bearing plan or clearly narrow the report claim; do not
present the exploratory output as if it already satisfied report provenance.

No complete run inventory is required by default. Keep the presented evidence
set, plus failed runs, abandoned parameter combinations, model-selection
attempts, or robustness variants only when they affect selection correction,
multiple-testing, or the report claim. The rule is transparency for the claim
being presented, not archival completeness for its own sake.

## Right-Sized Rigor

Rigor is sized to the research state being changed. Orientation, literature
triage, scaffold setup, smoke tests, and non-load-bearing exploration may use
lighter notes because they do not move durable research state. A2-A3 evidence
can be enough to choose the next experiment, provisional go / no-go, park,
deprioritize, reject-for-now, or split the question for exploration. Any update
that changes a load-bearing claim, support status, terminal decision, external
claim, deployment recommendation, or cross-workstream dependency uses the full
protocol required by that state transition.

Right-sized rigor is not a relaxation path. These requirements are
non-relaxed:

- A4+ for `supported`, external claim, deployment recommendation, or terminal decision.
- Reviewed pre-registration for trials that can support a claim or are reported
  as preregistered.
- Report provenance and rerun guidance for claim-bearing report packages and
  externally shared claims.
- Focused process review and conclusion review before externally shared
  load-bearing claims.
- Report quality requirements for claim-bearing report packages.

## Framework Boundary

This skill defines the **protocol layer**. It must stay separate from the
**project instance layer**.

| Layer | Owns | Must not contain |
|---|---|---|
| Protocol layer | Schemas, gates, status vocabulary, required evidence, review rules | Active candidates, selected symbols, tuned parameters, current performance metrics, experiment-specific conclusions |
| Project instance layer | Concrete research target, candidate definitions, data paths, configs, implementation, generated reports | New protocol rules, reusable workflow changes, hidden state transitions |

**Evidence artifacts do not own state decisions or report contracts.** Notebooks under
`purposes/`, rows in `results/results.parquet`, files under `configs/`, and
framework code under `src/` produce observations, metrics, logs, and run
metadata. They do not decide support status, terminal decisions, park, pivot,
or report conclusions.

**Framework code must not require research-state IDs.** Implementation APIs,
configs, and reusable framework modules must not require workstream IDs,
question IDs, R&D objective IDs, exit criteria, kill criteria, or explanation
IDs as part of their normal operation. Those identifiers may appear in state
assessment entries that cite evidence artifacts, not as required inputs to the
implementation itself.

**rd_plan.md is not an implementation API.** It is a research state document.
The correct flow is: project-instance code produces a neutral artifact; the
protocol layer later cites that artifact as evidence; the review layer checks
whether the cited evidence warrants the claimed state or report decision.

Do not embed active candidates in reusable workflow docs, skill templates, or
protocol references. A phrase like "the current candidate in cohort B" belongs
in a project trial report, a config, a decision entry, or a project state
index, not in this skill or its reusable templates.

Generated reports are snapshots. Evidence artifacts are snapshots too. They
may summarize observations, but they are not the source of truth for state
changes. Authoritative state lives in `rd_plan.md`, `explanation_ledger.md`,
durable transitions in `decisions.md`, and evidence links to trial artifacts.

When inheriting an existing project, diagnose boundary violations before doing
new research:

- Protocol documents should describe schemas, review rules, and report
  requirements only.
- State documents should contain objective, status, blockers, criteria,
  pre-registration links, plan-to-result comparisons, and evidence links.
- Project-instance artifacts should contain concrete symbols, universes, model
  classes, parameter grids, data paths, code, configs, and generated reports.
- If a file tries to be workflow guide + current candidate report + TODO list,
  split it before making any claim-bearing decision.

## Review (run before external load-bearing claims)

Two-axis review is a focused claim review, not a full-project inspection. Run
the relevant parts before any externally shared load-bearing claim, terminal
decision, deployment recommendation, or report package that carries the claim:

- **Process review** (`references/review/process_review.md`) - was the
  relevant discipline followed for the claim being made? Read only the process
  areas that could invalidate this state or report decision.
- **Conclusion review** (`references/review/conclusion_review.md`) - are the
  conclusions warranted? Check only the load-bearing axes: implementation
  correctness, statistical sufficiency, claim discipline, **analysis depth
  (A4+)**, reproducibility, and cold-eye review where they bear on the claim.
  For claim-bearing notebook artifacts, the focused four-reviewer procedure in
  `references/review/experiment_review_protocol.md` may be used as a
  conclusion-review subprocedure.

The review documents are menus of possible checks, not mandatory full
checklists. Mark non-applicable items as out of scope, and do not read or
review unrelated history. Blocking items and state changes require concrete
evidence citation (file:line, reference, numeric value, run ID, artifact URI,
or tool output). Lightweight process observations may be summarized when they
are not load-bearing. "Overall OK" / "looks good" / "appears correct" verdicts
are forbidden at external-claim decision points.

## User-Facing Outcome Reports

When reporting a research outcome, terminal decision, park, pivot, or
deployment recommendation to the user, produce a **human-judgment artifact** in
the final answer or as a linked report artifact. The user should not have to
inspect raw notebooks, ledgers, or tracker exports to understand what happened
and what decision remains.

### Short outcome summary

The normal final answer or short outcome summary has a minimum shape: decision,
evidence, limitation, and next action. Use one decision label when applicable:
`supported`, `not supported`, `inconclusive`, `decision deferred`,
`exploratory only`, or `blocked`.

Short summaries may cite file:line, artifact URI, run ID, reference, numeric
output, or ledger row when the point is load-bearing. They do not require
Preregistration Reference, Plan-to-Result Table, Evidence Integrity Checks, or
Reproducibility Capsule unless the answer is presenting a formal report package
or making the report itself the claim-carrying artifact.

### Formal report package contract

Use the formal report package contract only for a preregistered or
claim-bearing report package. It is also appropriate for terminal-decision,
externally shared, or deployment-recommendation report packages. Report
contracts apply to report packages and presented evidence, not to research or
experiments. Claim-to-artifact checks are a reporting-side requirement, not a
continuous research tracking contract.

Report quality contract: a reader can identify the decision, evidence, plan
comparison, limitations, and next action without opening notebooks or ledgers.

The formal report package must include:

- Executive Decision: the plain-language decision, what changed, what did not
  change, and whether the result is `supported`, `not supported`,
  `inconclusive`, `decision deferred`, `exploratory only`, or `blocked`.
- Research Stage and Claim Boundary.
- Preregistration Reference when the package reports preregistered work; state
  `N/A` only when no preregistration applies.
- Plan-to-Result Table for preregistered or plan-based work.
- At least one piece of visual or tabular evidence that makes the result
  intuitive: a figure, chart, DAG, timeline, comparison table, confusion/error
  table, before/after table, or compact metric table. Choose the form that best
  exposes the key uncertainty, not the form that flatters the result.
- Evidence Integrity Checks for claims presented in the report.
- Evidence citations for every load-bearing claim, linking each visual or table
  back to file:line, artifact URI, run ID, reference, numeric output, or ledger
  row.
- Transparent Changes for preregistered or plan-based work.
- Reproducibility Capsule for claim-bearing report packages.
- Scope / Limitations / Alternative Explanations: what conditions the result
  covers, what alternatives remain plausible, and what evidence would change
  the decision.
- Next Action requested from the user, if any.

Preregistered or claim-bearing work that produces a report uses the package
shape from `references/shared/outcome_reports.md`:

```text
results/reports/
  RPT_<id>_<slug>/
    # Required core files
    report.md
    report.html
    figures/
    tables/
    attachments/
    # Optional / situation-specific files
    report.pdf
    provenance/
      manifest.json
      integrity_checks.md
      rerun.md
```

The required core files: `report.md`, `report.html`, `figures/`, `tables/`,
and `attachments/`. Here, `figures/`, `tables/`, and `attachments/` are
directories, and required core directories may be empty. `report.html` is the
primary readable artifact for L2/L3 reports; `report.md` is editable source;
report.pdf is optional snapshot/export. Use `provenance/` only for
claim-bearing or L2/L3 reports, with `manifest.json`, `integrity_checks.md`,
and `rerun.md` under it. L2/L3 reports means claim-bearing reports and
state-promotion or terminal-decision report packages; it is report package
level, not analysis tier.

External tracker run IDs are optional for these reports. Evidence should point
to figures, tables, appendices, local source artifacts, artifact URI, run ID,
or ledger row only when that source actually exists and helps a reviewer.

For each key numeric, boolean, categorical, and count claim presented in the
report, include a claim-to-artifact check row with `claim_id`,
`reported_value`, `cited_artifact_path`, `commit_or_hash`, `extraction_method`,
`observed_source_value`, `comparison_status`, and
`generating_command_or_entrypoint`. Failed, missing, or not run cannot be
treated as supported.

Visuals and tables are explanatory snapshots, not state owners. The state
documents and review path still decide support, terminal decisions, kill, and
pivot. If no visual is possible, state why and provide the smallest table that
lets the user compare the evidence directly. Do not hide the outcome behind
"see notebook"; the final report must carry enough intuitive evidence for
human judgment.

## Guardrails

- **Kill requires A4+ evidence**. Kill requires A4+ evidence only for terminal
  kill. A kill criterion firing is a trigger for terminal review, not an
  automatic terminal state. Mark terminal kill only after mechanism-level
  analysis rules out repairable causes such as config error, data defect, scope
  error, or missing dependency. Candidate drop, reject-for-now, and
  deprioritize are exploratory pruning decisions; exploratory pruning
  decisions do not require A4+ evidence.
- **Evidence citation is mandatory for load-bearing claims**. Any claim of
  "passed" / "verified" / "confirmed" that supports `supported`, terminal
  decision, external sharing, deployment recommendation, material change from a
  plan, or claim-scope change must reference a specific file:line, reference,
  numeric value, or tool output. Summary verdicts without citation are
  forbidden at those decision points.
- **Pre-registration is available at every research stage**. It is useful for
  basic research, applied research, and experimental development. It can be
  amended prospectively, but prior work remains prior or exploratory evidence.
- **State-change logging**. Sessions that change durable research state must
  update the selected state object or record `no progress: <reason>` in
  `decisions.md`. Short orientation, environment setup, and interrupted
  sessions may remain outside the durable log unless they change a claim, state
  transition, or gate decision.
- **Lightweight run tracking is enough for exploration**. Ordinary exploratory,
  smoke-test, debugging, and non-load-bearing experiments may use a short run
  note, tracker run, notebook note, or results row. Do not turn every trial into
  a decision-log entry or full review package.
- **Report provenance**. Claim-bearing report packages record enough
  provenance for presented evidence: data snapshot, code version, environment
  pin, seed when relevant, and artifact path or run ID when one exists.
  Exploratory, smoke-test, and debugging runs may use lightweight run notes. If
  later needed for an externally shared or claim-bearing result, rerun under
  the claim-bearing plan; do not present exploratory output as if it already
  satisfied report provenance.
- **Planning artifacts**. Pre-registration and planning criteria must be
  reviewed before they become load-bearing. Any load-bearing amendment requires
  an explicit decision entry, report Transparent Changes entry, or a new
  planning artifact.
- **No placeholders in deliverables**. Templates produce real content; any
  remaining `TBD`, `TODO`, `XXX`, `???`, or `{{...}}` blocks the deliverable.

## Required Artifacts

Common to a workstream-aware project:

```text
project_state.md                 # project intent, uncertainties, workstreams
README.md                        # goal, current state, entry points
decisions.md                     # durable state transitions only
literature/papers.md             # prior work
literature/differentiation.md    # how this differs from prior work
purposes/INDEX.md                # evidence artifact index
results/results.parquet          # portable default evidence index
results/reports/                 # preregistered report packages
configs/                         # project-instance experiment configs
src/                             # project-instance implementation, if any
tests/                           # project-instance verification, if any
reproducibility/{uv.lock,env_lock_ref.txt,data_versions.txt,shared_pins.txt,seed.txt}
tracking/                        # optional local tracker config / exported run refs
workstreams/                     # recommended home for workstream state
```

R&D Workstreams add:

```text
rd_plan.md                       # R&D category, objective, plan/result state
prereg/PR_<id>_<slug>.md         # optional or claim-bearing pre-registration
```

Phenomenon / Mechanism Research workstreams add:

```text
prfaq.md                         # working-backwards entry document
prereg/PR_<id>_<slug>.md         # reviewed pre-registration, confirmatory or exploratory
explanation_ledger.md            # primary state object
imrad_draft.md                   # paper-shaped deliverable, started early
```

## References

Read only what applies to your current step.

**Shared (all workstreams)**

| Reference | When to read |
|---|---|
| `shared/analysis_depth.md` | Before claim-bearing interpretation, external claim, deployment recommendation, or terminal decision. |
| `shared/result_analysis.md` | Before writing any explanation of success or failure. |
| `shared/literature_review.md` | Project initialization or before a new question. |
| `shared/reproducibility.md` | Preparing report provenance and rerun guidance for claim-bearing report packages. |
| `shared/results_db_schema.md` | Appending interpreted trial results. |
| `shared/outcome_reports.md` | Creating preregistered report packages, report HTML, and optional PDF exports. |

**R&D Workstream** - `rd/rd_workflow.md`.

**Phenomenon / Mechanism Research** - see the entry sequence above.

**Review** - see Review above.

## Bundled Helper Scripts

| Script | Purpose |
|---|---|
| `new_project.py` | Initialize a project shell; compatibility `--mode rd|pure-research` may create a first workstream layout |
| `new_trial.py` | Generate a numbered neutral evidence artifact |
| `aggregate_results.py` | Append interpreted trial rows (mode-aware schema, includes `analysis_tier`) |
| `render_explanation_dag.py` | Mermaid DAG of the explanation hierarchy |
| `draft_imrad.py` | Generate IMRAD draft from explanation_ledger + decisions + results |
| `standup.py` | Summarize the last 24h of decisions.md transitions |
| `lit_fetch.py` | Batch fetch prior-work metadata from arXiv and Semantic Scholar |
