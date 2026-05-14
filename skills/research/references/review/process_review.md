# process_review.md

Process review asks whether the discipline needed for a named report package,
state transition, or externally shared load-bearing claim was followed. This is
the first of two review axes; `conclusion_review.md` asks whether the claim is
warranted by the presented evidence.

Process review is targeted. It checks only the process commitments that could
invalidate the specific claim, report package, or transition under review. It is
not a complete audit of every exploratory run.

## When to read

- Before a report package is used to support a durable state transition
- Before an externally shared load-bearing claim
- Reviewing another agent's claim-bearing report package
- Reviewing a project mid-stream when a process gap may affect the next
  decision

## Purpose

Process review separates blocking violations from logged gaps. A load-bearing
process violation blocks the named claim or transition. A non-load-bearing
record gap is logged, may narrow the claim, and may require cleanup, but does
not by itself invalidate unrelated exploratory work.

The report package requirements in this file are reporting-side requirements.
They apply when a package is presented as evidence for a claim or decision; they
are not continuous tracking contracts for all research activity.

## How to run

Name the claim, report package, or state transition under review, then read only
the sections that can affect it. Do not perform a full project inventory unless
selection correction, reproducibility, or the claim itself depends on that
inventory.

For in-scope items, write:

```markdown
- [x] item -- evidence: <file:line, reference, or specific observation>
- [ ] item -- FAIL: <what is missing or violated>
- [ ] item -- N/A (justify why)
```

"Looks good" and "obvious from context" are not valid at claim-bearing decision
points. Load-bearing passes require a citation. Out-of-scope items should be
marked `N/A -- not load-bearing for this review`.

## Common pre-conditions

These checks apply to every selected workstream label:

- [ ] **Workstream label is explicitly declared** in `project_state.md` and
  matches the selected state object
  - Evidence: `project_state.md` workstream row, selected workstream
    `README.md`, and relevant `decisions.md` entry
- [ ] **No silent state-object switch**: the project did not change between
  `rd_plan.md`, `explanation_ledger.md`, or another declared state object
  without a decision-log entry explaining add / split / handoff / scope change
  - Evidence: targeted `decisions.md` review
- [ ] **Durable state changes are logged where they matter**: claim adoption,
  report-package acceptance, kill decisions, pivots, scope changes, and
  externally shared conclusions have ledger or decision-log entries
  - Evidence: inspect only the decisions and ledgers touched by this review
- [ ] **Decision-log covers the decision under review**: `decisions.md` has the
  entries needed to explain this transition, kill, pivot, or external claim; it
  does not need to narrate every experiment
  - Evidence: targeted per-decision presence check
- [ ] **Entry guardrails respected**: no claim-bearing confirmation trial or
  report-package conclusion was executed before the relevant plan was ready
  enough to define the question, scope, method, and decision criteria
  - Evidence: first claim-cited run, plan status, and report package chronology
- [ ] **Presented evidence can be resolved** for the named claim or report
  package
  - Scope: the report package and presented evidence only.
  - Evidence: data version, git commit, environment pin, seed when relevant,
    and stable artifact path or tracker ID when those anchors are needed to
    challenge or rerun the reported result
  - The anchor can be a local run note, tracker record, results row, or report
    provenance entry.
- [ ] **Presented evidence set exists** when multiple-testing, selection
  correction, or support judgment depends on it
  - Evidence: `results/results.parquet`, tracker query/export, durable
    `tracking/` file, or report provenance file covering cited winners,
    relevant failed attempts, parameter sweeps, model-selection attempts, and
    robustness variants
- [ ] **Planning artifacts were not silently rewritten**: material plan changes
  that affect claims have explicit change entries and are reflected in the
  report package's `Transparent Changes` section when a package exists
  - Evidence: relevant `decisions.md` entries, current planning files, and
    report package

## R&D Workstream process review

Use this section for workstreams labeled `R&D Workstream`. The state object is
`rd_plan.md`.

### R&D identity

- [ ] **The work is correctly framed as R&D**
  - Evidence: `rd_plan.md` shows why the work is novel, creative, uncertain,
    systematic, and transferable or reproducible
- [ ] **R&D category is declared**
  - Evidence: `rd_plan.md` labels the work as `basic research`,
    `applied research`, or `experimental development`, with a one-paragraph
    rationale
- [ ] **The category fits the claim**
  - Evidence: report package and plan do not claim a product-ready development
    outcome from a basic-research evidence base, or a general knowledge claim
    from a narrow development validation

### Plan readiness

- [ ] **`rd_plan.md` exists at the workstream root**
  - Evidence: file path + size > 0
- [ ] **Plan status is ready for the reviewed claim-bearing work**
  - Evidence: `rd_plan.md` status and approval/review note before the cited run
- [ ] **Question, objective, and decision criteria are concrete**
  - Evidence: the plan states what uncertainty is being reduced, what evidence
    would count, and what decisions the evidence can support
- [ ] **Scope boundaries are explicit**
  - Evidence: in-scope and out-of-scope populations, systems, periods,
    datasets, operating conditions, or implementation contexts are named
- [ ] **Kill / stop / pivot criteria are observable**
  - Evidence: criteria use numeric or behaviorally observable thresholds where
    possible, not "if it does not work"
- [ ] **Costs and constraints are described at the right level**
  - Evidence: the plan distinguishes one-time work, recurring maintenance,
    operational constraints, and known external dependencies where relevant

### Execution discipline

- [ ] **Plan-before-execute discipline was followed for claim-cited work**
  - Evidence: plan timestamp/status precedes execution of the run cited by the
    report package
- [ ] **Material deviations are visible**
  - Evidence: report package `Transparent Changes` lists material differences
    from `rd_plan.md`, explains why they occurred, and states whether they
    narrow or invalidate the original decision criteria
- [ ] **Exploratory findings are labeled honestly**
  - Evidence: exploratory or diagnostic outputs are not presented as planned
    confirmatory evidence unless rerun or reported with the appropriate
    caveat
- [ ] **Implementation and validation work are separable enough to review**
  - Evidence: the package identifies what was built, what was measured, which
    artifacts are evidence, and which checks are prerequisites for trusting the
    measurement
- [ ] **Dependencies and downstream invalidation are recorded where relevant**
  - Evidence: the report package or `decisions.md` names upstream artifacts and
    states what must be rerun if they change

### Evidence package

- [ ] **Presented evidence maps to each decision criterion**
  - Evidence: report package traceability table or equivalent narrative mapping
- [ ] **Negative and ambiguous results are included when they affect the claim**
  - Evidence: decision-relevant failures, abandoned variants, and robustness
    checks are visible in the package or presented evidence set
- [ ] **Transferability or reproducibility is addressed**
  - Evidence: package includes replication, independent rerun, environment
    pinning, design rationale, or other evidence appropriate to the R&D
    category and claim strength
- [ ] **No overclaim from category mismatch**
  - Evidence: basic research, applied research, and experimental development
    outputs are described at the level actually tested

## Phenomenon / Mechanism Research workstream process review

Use this section for phenomenon- or mechanism-oriented research workstreams
that use `explanation_ledger.md` and the pre-registration templates.

### PR/FAQ

- [ ] **PR/FAQ exists** at workstream root (`prfaq.md`)
- [ ] **PR/FAQ is reviewed and ready**
  - Evidence: `prfaq.md` status is `READY`
- [ ] **Part 1 is concrete**: states the finding, mechanism, scope,
  alternatives ruled out, and evidence form
- [ ] **Part 2 has enough FAQ coverage** for statistical sufficiency,
  robustness, mechanism, alternatives, replication, scope, practical
  implication, and post-hoc rationalization risk

### Targeted literature

- [ ] **Targeted literature search happened after the question was scoped**
  - Evidence: literature notes are scoped to the ready question
- [ ] **Literature is genuinely targeted**
  - Evidence: per-paper `relation to this research` field is specific, not
    generic background

### Pre-registration as general discipline

Pre-registration is plan -> execute -> compare -> report discipline. It fixes
the planned question, method, evidence, and decision criteria before a run is
used as claim-cited evidence. Exploratory pre-registration bounds a search and
does not make a result confirmatory by itself.

#### Confirmatory pre-registration

- [ ] **Confirmatory pre-registration exists** for every cited confirmatory
  trial (`prereg/PR_<id>_<slug>.md`)
- [ ] **Confirmatory pre-registration was reviewed before claim-cited
  execution**
- [ ] **Study information and shared fields are complete**
- [ ] **Hypotheses or competing explanations are stated before execution**
- [ ] **Design plan is concrete enough to identify what was run**
- [ ] **Analysis plan is specific enough to execute and audit**
- [ ] **Inference / decision criteria are fixed before seeing results**
- [ ] **Data exclusion / missing data handling is specified**

#### Exploratory pre-registration

- [ ] **Exploratory pre-registration was reviewed before execution if cited as
  a planned exploratory run**
- [ ] **Exploratory objective states the uncertainty being reduced**
- [ ] **Exploration scope bounds the search area**
- [ ] **Allowed transformations / procedures bound researcher degrees of
  freedom**
- [ ] **Selection or follow-up criteria are stated before execution**
- [ ] **Expected outputs state the intended artifact kind**

### Trial execution and outcome reporting

- [ ] **Transparent Changes exists for every preregistered outcome report**
  - Evidence: report package includes either "No material changes from the
    preregistration." or per-change description, rationale, and effect on
    results or conclusions
- [ ] **Material changes were handled without overclaiming**
  - Evidence: report package, trial notes, and `decisions.md` explain whether
    the result is narrowed, marked exploratory, or rerun under a suitable plan
- [ ] **Verification checks ran before the main test where applicable**
  - Evidence: trial notebook verification section + pass status
- [ ] **No post-hoc explanation addition into the current claim**
  - Evidence: post-trial candidate explanations are flagged and parked for
    future planned work

### Explanation ledger update

- [ ] **Claim-cited evidence updates the explanation ledger where it changes
  support status, scope, or competing explanations**
  - Evidence: relevant `explanation_ledger.md` row cites the trial, results
    row, tracker run, or notebook note
- [ ] **Rejected or weakened explanations are not reopened without a new plan**
  - Evidence: ledger entry explains the reopen and points to the new planned
    trial

### IMRAD draft

- [ ] **IMRAD draft started after question readiness**
- [ ] **Sections 1-2 evolved with literature and plans; Sections 3-4 are
  trial-backed**
- [ ] **Methods lists Transparent Changes** from pre-registration or states
  that there were no material changes

## Common process violations

| Violation | Symptom | Where caught |
|---|---|---|
| Silent state-object switch | Workstream changes state object without a decision entry | Common pre-conditions |
| Premature claim-bearing execution | Metrics are cited before the relevant plan was ready | Entry guardrails |
| Plan rewritten after results | Material plan change has no decision entry or Transparent Changes note | Planning artifacts |
| Category mismatch | Evidence from one R&D category is used to claim a stronger category outcome | R&D identity |
| Exploratory output overclaimed | Diagnostic search result is presented as confirmatory evidence | Execution discipline |
| Missing presented evidence set | Selection correction ignores failed or abandoned variants | Common pre-conditions |
| Post-hoc pre-registration | Pre-registration was completed after the result it claims to plan | Pre-registration |
| Material change treated as irrelevant | Transparent Changes says "none" despite a changed plan, scope, threshold, or result-bearing procedure | Outcome reporting |
| Generic terminal labels in conclusions | "model is good" / "regime suited" / "noise" patterns | `conclusion_review.md` analysis depth axis |

## Outcome of process review

- **All in-scope load-bearing checks pass with citations** -> process review
  CLEAN for the named claim or transition; proceed to `conclusion_review.md`
- **Any in-scope load-bearing check fails or N/A without justification** ->
  process review FAILED; the claim must be fixed, narrowed, or decoupled from
  the failed process commitment
- **Process review report** may be written into `decisions.md` when a durable
  record is needed

The report includes:

- Date and reviewer
- Scope of review and each in-scope check + status + evidence citation
- Failed items + remediation plan or claim narrowing
- Sign-off: process review clean / fail

## Relationship to other references

- Pre-condition for `references/review/conclusion_review.md`
- Complements workstream planning files such as `rd_plan.md`,
  `prfaq.md`, pre-registration files, and report packages
- Uses `references/shared/reproducibility.md`,
  `references/shared/results_db_schema.md`, and
  `references/shared/analysis_depth.md` when those surfaces bear on the claim
