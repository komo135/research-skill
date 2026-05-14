# pr_workflow.md

Operating rules for a Phenomenon / Mechanism Research workstream across
sessions. This is the Pure Research-compatible workflow for exploratory
research loop, confirmatory research loop, pre-registration comparison,
Transparent Changes, state-change logging, stop conditions, shared
infrastructure governance, and handoff to R&D Workstreams.

## When to read

- First session of a new Phenomenon / Mechanism Research workstream
- After any trial result, before deciding whether to update the ledger
  or run the next trial
- When a material change from pre-registration is being considered
- Setting up shared infrastructure
- Adding, splitting, or handing off to an R&D Workstream
  workstream

## Entry guardrails

Phenomenon / Mechanism Research first day permits **only** the following:

- PR/FAQ (`references/pure_research/prfaq.md`)
- Targeted literature review (`references/shared/literature_review.md`)
  scoped by the PR/FAQ
- Exploratory research planning, current-state assessment, hypothesis or
  explanation candidates, and initial-approach search
- Pre-registration (`references/pure_research/preregistration.md`) when work
  needs a written plan before execution. It may be exploratory or
  confirmatory; use `prereg/PR_<id>_<slug>.md`.
- Empty `explanation_ledger.md` skeleton with workstream ID and label declared
- Data infrastructure setup, environment pinning (`uv.lock`), data version
  recording, raw data sourcing, scaffold file creation

The preregistered flow is plan -> execute -> compare -> report:

- Plan: write or select the pre-registration before work starts.
- Execute: run the work against the written plan.
- Compare: compare actual execution and results against the pre-registration.
- Report: publish the plan-to-result table, transparent changes, evidence, and limitations.

Pre-registration is a plan, not a prison. A midstream pre-registration governs
future work or explicit reruns only; prior work is prior or exploratory
evidence. Report contracts apply to report packages and presented evidence,
not to research or experiments. Evidence integrity checks are a reporting-side
requirement, not a continuous research tracking contract.

Phenomenon / Mechanism Research first day **prohibits**:

- Claim-bearing confirmation trial execution before a reviewed
  pre-registration is ready
- Presenting exploratory observations as confirmatory, `supported`, or
  externally reliable
- Any explanation row marked anything other than `active`

Why: exploratory research is allowed to learn what is going on. The
prohibited move is using the same data-dependent discovery as if it had been
planned independently. A claim-bearing confirmation trial run before the
pre-registration is ready is a shopping trip; once you have seen the outcome,
"pre-registration" written afterwards is theater.

## Exploratory Research Loop

Use this loop when the goal is to understand the current situation, generate
candidate explanations, test data feasibility, or find a workable initial
approach. Exploratory work may inspect data and iterate. Its outputs are
`exploratory` / `diagnostic`, not `supported`.

```
1. State the purpose and current uncertainty.
2. Inspect the current situation: available data, prior notes, constraints,
   failure modes, and obvious sanity checks.
3. Generate or refine Q/E candidates in `explanation_ledger.md` only as
   candidates; keep statuses `active` unless evidence is already
   claim-bearing.
4. Try the smallest useful analyses, plots, probes, or model checks.
5. Record observations, assumptions tested, and approach changes in run notes,
   tracker rows, notebook notes, result rows, or a preregistered report package.
6. Label conclusions explicitly as exploratory / diagnostic.
7. Decide next: continue exploring, park/stop, write an exploratory
   preregistration for a scoped diagnostic pass, or move to confirmatory
   research if a specific finding needs higher reliability.
```

Exploratory research does not have to be followed by confirmatory research.
Exploration can end with a map, a negative diagnostic result, a parked
question, or a decision that no claim is worth confirming. If the result will
become a `supported / external claim / high reliability claim`, move to
confirmatory research.

## Confirmatory Research Loop

Use this loop when an exploratory result, literature-derived prediction, or
explicit research question is ready for a reliability-raising test. This is
where a confirmatory pre-registration belongs.

```
1. Identify the question to advance (which Q-row in explanation_ledger)
2. Identify which E pair to discriminate (or test against null)
3. Write or select the pre-registration (`prereg/PR_<id>_<slug>.md`, `Status: READY`)
4. Before execution, compare `PR_<id>_<slug>.md` against the current state: current
   question, exploratory result, data availability, assumptions,
   implementation constraints, and analyst/data exposure. The purpose of
   comparing the pre-reg against the current state is not only to follow the
   pre-reg, but also to verify that the current state has not broken the PR's
   assumptions.
5. If the PR no longer matches the current situation, do not force it. Return
   to exploratory research, write Transparent Changes, or create a new PR.
6. Run the confirmatory trial (data fetch, computation, verification checks)
7. Transparent Changes review against the pre-registration
8. Analysis section: observation, decomposition, evidence weighing,
   tier rating, gap to next tier (per pr_trial.py.template § 5)
9. If the result is cited in a claim or changes support, scope, or status, update
   explanation_ledger row(s): which E weakened / strengthened / rejected /
   unchanged
10. Record durable state transitions in decisions.md when the result changes a
   claim, promotion path, scope, park decision, workstream operation, or other
   commitment
11. Decide next: push analysis depth on this trial, design next
   discriminating trial, or escalate to promotion gate
```

The loop runs until a stop condition (below) or a question is
`answered`.

## Result-to-Question Loop

After every claim-bearing interpreted result, the
workstream returns to Q/E state in `explanation_ledger.md`. The result may
strengthen, weaken, reject, split, merge, park, or leave unchanged one or more
explanation rows. Ordinary exploratory observations may stay in run notes,
tracker runs, notebook notes, or result rows until they become load-bearing.

Use the existing discriminating trial loop; this section names the return path
so results do not become orphan observations:

1. State the observed pattern and analysis tier.
2. Compare the result to the pre-registration and publish Transparent Changes.
3. Identify which Q row and E rows the result touches.
4. Update `explanation_ledger.md` only as far as the evidence warrants when
   the result changes support, scope, status, or next discriminating step.
5. Record durable transitions in `decisions.md`; do not record ordinary
   exploratory runs there.
6. Decide whether the next move is deeper analysis on the current result,
   another discriminating trial, promotion review, park, add, split, or handoff.

This loop does not create a second research-state object. The ledger remains
the source of truth for questions and explanations.

## Push analysis depth before designing a new trial

Before designing a new discriminating trial, the agent must push the
**current trial's analysis depth as far as it can go**. This follows the
analysis-depth rules in `references/shared/analysis_depth.md`.

Concretely: if the most recent trial reached A2 (one alternative
identified), the next move is **not** "design a new trial" — it is
"can we push this trial to A3 by running a discriminating sub-test or
by re-analyzing existing data?" Often the answer is yes (e.g., feature
ablation on existing model, regime-conditional breakdown of existing
trial run, additional sub-period analysis). These extensions stay
inside the current trial and advance it from A2 → A3 → A4 without
requiring a fresh pre-registration.

A new trial is justified only when:

- The current trial has reached its analysis ceiling (further analysis
  on the same data cannot discriminate further), AND
- The next discriminating question requires a different test design
  (e.g., different data, different period, different metric)

Increasing analysis depth on existing data is research; collecting more
data without analyzing existing observations is not.

## Transparent Changes and severity

After preregistered work runs, compare actual work against the
pre-registration. Every report package includes `Transparent Changes`.

If no material changes occurred:

```markdown
No material changes from the preregistration.
```

If material changes occurred:

```markdown
### Change <n>: <short name>
- Description of change:
- Rationale:
- Effect on study results or conclusions:
```

Effects should be honest about uncertainty. If a change was made with
knowledge of its effect on the outcome, the report says the affected result
has weaker diagnostic value. If the original plan no longer answers the
intended question, the report says so plainly.

Confirmatory work may still need a claim-cited-use judgment when a material
change affects interpretation. The comparison first separates **confirmation
target** from **initial approach**.

The confirmation target is the thing being tested: question, competing
explanations, scope, primary metric, thresholds, and interpretation rules. The
initial approach is the planned way to answer it: analysis method, estimator,
period-fetch mechanics, data-acquisition route, implementation path, and
operational choices.
The initial approach is not the confirmation target itself.

An initial-approach change that preserves the confirmation target, threshold,
scope, and interpretation is not a plan-breaking material change. Record the
rationale in Transparent Changes and continue; a new PR is not required, and
do not treat the change as hypothesis failure. If the change alters the
confirmation target, threshold, scope, interpretation, or multiple-testing
family, treat it as plan-breaking for claim-cited use.

| Material change | Claim-cited effect | Action |
|---|---|---|
| Parameter within +/-10% of pre-reg (e.g., bandwidth slightly different) | usually preserved | Disclose in Transparent Changes and continue |
| Sample size differs by < 5% (e.g., a few rows dropped due to data quality) | usually preserved | Disclose in Transparent Changes and continue |
| Imputation method specified differently (e.g., median vs mean) but methodologically equivalent | usually preserved | Disclose in Transparent Changes and continue |
| Test statistic logic adjusted within the same family (e.g., Pearson -> robust Pearson under same hypothesis) | usually preserved | Disclose in Transparent Changes and continue |
| Initial approach changed while confirmation target, threshold, scope, interpretation, and multiple-testing family are unchanged | preserved | Disclose rationale and continue under the same PR |
| **Population/scope period shifted by > 1 year** (e.g., confirmation target changes from 2015-2024 to 2018-2024) | **plan-breaking** | **Treat the result as exploratory for the original claim. Use a new pre-registration with the new scope period before claim-cited use.** |
| **Sample size differs by > 10%** | **potentially plan-breaking** | Disclose effect; if the original plan no longer answers the intended question, use a new pre-registration |
| **Test statistic or estimator changed across families in a way that changes the primary metric, threshold meaning, or interpretation** (e.g., Pearson threshold reinterpreted as Spearman threshold after seeing data) | **plan-breaking** | Disclose effect and use a new pre-registration before claim-cited use |
| **Competing explanation added post-hoc** | **plan-breaking for the original confirmation** | Disclose; park for a future pre-registration before claim-cited use |
| **Threshold changed after seeing data** (e.g., kill threshold relaxed) | **plan-breaking** | Disclose and use a new pre-registration before claim-cited use |
| **Multiple-testing trial count under-reported** | **plan-breaking unless corrected** | Re-compute correction with honest count; if claim no longer holds, mark E `weakened` |
| **Imputation method changed in a way that affects test power** (e.g., dropping vs imputing missing) | **potentially plan-breaking** | Disclose effect; rerun or use a new pre-registration if the intended question changed |
| **Hypothesis threshold near-miss**: primary metric within 10% of pre-reg threshold band (e.g., pre-reg said r > 0.6, observed r = 0.58) | result interpretation | Threshold miss is result interpretation, not a plan-breaking material change. Document the observed miss; the explanation does not get the predicted support, treat as `weakened` rather than `supported`/`rejected`. New PR is not required unless future work changes threshold, scope, or interpretation. |
| **Hypothesis threshold large miss**: primary metric > 10% from pre-reg threshold (e.g., pre-reg said r > 0.6, observed r = 0.30) | result interpretation | Threshold miss is result interpretation, not a plan-breaking material change. Interpret under the pre-registered rule, usually `rejected` or strongly `weakened`; do not create a new PR merely because the threshold was missed. |

Plan-breaking material changes invalidate the result for claim-cited use under
the original PR. Disclose the change in the report package, create a new
pre-registration for the changed design when a claim still matters, and rerun.
The original result remains exploratory or diagnostic for the changed claim.

This is non-negotiable. The matrix exists because "still answers the original
question" vs "plan-breaking" is ambiguous in practice; without an explicit
rubric, agents and humans both default to "this is harmless" and the discipline
collapses.

HARKing and goalpost shifting remain blocking: changing thresholds or scope
after seeing results, changing interpretation after seeing data, or adding a
favorable explanation post-hoc is plan-breaking. The allowed flexibility
applies only to initial-approach improvements that preserve what was being
checked.

## State-change logging

Same as R&D's state-change logging rule (see `references/rd/rd_workflow.md` §
State-change logging). Use `decisions.md` only for:

- durable support/status/scope transitions in `explanation_ledger.md`
- promotion, rejection, park, pivot, or plan-breaking material-change decisions
- blockers that prevent an intended durable state transition

Ordinary exploration, smoke tests, debugging, interrupted work, and lightweight
run notes do not need `decisions.md` entries. The loop discipline above (push
analysis before new trial, Transparent Changes and material-change rubric
applied) still applies when the result is claim-cited.

## Stop conditions — when does a phenomenon workstream end?

A workstream terminates when one of:

### Promotion (positive finding)

An explanation reaches `supported` status, IMRAD draft is producible,
all sibling E's are at terminal status (rejected / merged / stale /
parked), promotion review passes (`pr_promotion_gate.md`).

The closing entry in `decisions.md`:

```markdown
## YYYY-MM-DD project promoted (Q<id> answered, E<id> supported)

Question: <Q-statement>
Supported claim: <E-statement, no stronger than evidence>
Scope conditions: <where this applies>
IMRAD draft: <path>
Sibling explanations status: E2 rejected (trial T_xxx), E_null rejected (trial T_yyy)
Reproducibility: data version, git commit, environment pin recorded for each cited trial
```

### Promotion (negative / null finding)

All explanations under a Q reach `rejected`. The Q is `answered` with
"none of the candidate explanations holds." This is a real finding.
The IMRAD draft documents the elimination.

### Park

The Q cannot progress because of a named external unblock condition
(data unavailable, sample size insufficient until time passes, prior
workstream must complete). Differs from promotion: the workstream will resume
when the unblock fires.

### Add / split / handoff

Evidence shows that an R&D uncertainty must be handled separately. Add a
dependent workstream, split the current workstream, or hand off a supported
finding to an R&D Workstream. Treat design,
evaluation, and engineering-support work as activities inside the selected
phenomenon workstream or R&D Workstream unless they expose a separate
research-state claim. Record the trigger, affected workstream IDs, ledger rows,
reused evidence scope, parent / child relationship, and next gate in
`decisions.md`.

Project-level pivot is reserved for a change in final intent or decision
audience, not for ordinary mixed research.

### Drift (anti-pattern)

Workstream simply stops being worked on without an explicit decision. When
returning to stale state, first decide whether to promote, park, add, split,
handoff, or resume; do not create review entries for the inactive period.

## Shared infrastructure governance

Same as the R&D Workstream rule (see
`references/rd/rd_workflow.md` § Shared infrastructure governance).
Phenomenon / Mechanism Research workstreams use the same
`shared/` folder and record the specific commits used in
`reproducibility/shared_pins.txt`.

A Phenomenon / Mechanism Research finding may itself become a `shared/`
artifact (e.g., a regime classifier proven in a phenomenon workstream that is
now used by multiple R&D Workstreams). The transition is a deliberate
move, not a copy: the artifact moves to `shared/` with documentation of its
origin workstream, and downstream consumers record the commit they used.

## Code reuse on workstream handoff

Same principle as the R&D Workstream: reuse the bricks (data
pipeline, helpers, verification-check scripts), not the house (problem
framing, decision logs, state documents). A new workstream gets its own state
document and cites the source via parent / child workstream IDs.

What can be reused from a phenomenon workstream:
- Data pipeline code, feature library, validation harness
- Sanity-check scripts
- Specific computational helpers

What cannot be reused as-is:
- The PR/FAQ as a R&D plan
- Pre-registrations as R&D decision criteria
- The explanation_ledger as an rd_plan
- Trial notebooks as R&D evidence without explicit role
  re-declaration

When the handoff direction is phenomenon -> R&D: an
`explanation_ledger` finding may be cited as a literature reference in the
R&D plan. The phenomenon workstream's
`decisions.md` link is preserved as a parent workstream reference.

For a Research-to-Technology Handoff, the R&D Workstream may consume
the phenomenon finding as an assumption, requirement, dependency, scope
condition, benchmark, or maintenance trigger. It must not copy the supported
claim into the R&D plan as though R&D work re-proved it;
cite the phenomenon `explanation_ledger.md` row and support decision instead.

## Communication conventions during a session

Agent should:

- State the **current Q + E pair being discriminated** when starting
  trial design (e.g., "Designing trial to discriminate Q1/E1 vs Q1/E2")
- Cite the **pre-registration file** when running preregistered work
- After any preregistered trial, state **Transparent Changes (none / material)**
  and **analysis tier reached** as the first lines of the trial summary

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Day 1 confirmation run | Code computed claim-bearing metrics before pre-registration was ready | Block confirmatory use; label the work exploratory / diagnostic and pre-register a confirmation if the claim still matters |
| Skipping Transparent Changes | Trial completes, no comparison to the written pre-registration | Block claim-bearing report use until changes are disclosed |
| Treating a plan-breaking change as harmless | "Period shift, but the methodology is the same" | Apply the matrix strictly; period shift > 1y is plan-breaking |
| New trial before pushing depth | Run a 2nd trial when 1st is at A2 | Force depth push first |
| Adding E mid-confirmation | Discovered alternative not in pre-reg and uses it to reinterpret the confirmatory result | Label as exploratory; pre-register a future confirmation if it becomes load-bearing |
| Drift | Stale ledger | Decide Promotion / Park / Add/split/handoff / Resume before new claim-bearing work |
| `supported` with sibling E still active | Promotion premature | All siblings must be at terminal status first |

## Relationship to other references

- Entry guardrails appear in summarized form in `SKILL.md` § Guardrails; this
  file is the elaboration
- PR/FAQ entry: `references/pure_research/prfaq.md`
- Pre-registration: `references/pure_research/preregistration.md`
  (the material-change matrix in this file informs Transparent Changes handling for
  claim-cited confirmatory work)
- State object: `references/pure_research/explanation_ledger_schema.md`
- IMRAD deliverable: `references/pure_research/imrad_draft.md`
- Promotion gate: `references/pure_research/pr_promotion_gate.md`
- Multiple testing discipline: project-specific multiple-testing plan
- Analysis depth: `references/shared/analysis_depth.md`
- R&D Workstream side rules for shared infra and handoff:
  `references/rd/rd_workflow.md`
