# pr_workflow.md

Operating rules for a Phenomenon / Mechanism Research workstream across
sessions. This is the Pure Research-compatible workflow for exploratory
research loop, confirmatory research loop, pre-registration comparison,
deviation handling, state-change logging, stop conditions, shared
infrastructure governance, and handoff to capability workstreams.

## When to read

- First session of a new Phenomenon / Mechanism Research workstream
- After any trial result, before deciding whether to update the ledger
  or run the next trial
- When a deviation from pre-registration is being considered
- Setting up shared infrastructure
- Adding, splitting, or handing off to a Capability / Technology Research
  workstream

## Initial-day prohibitions

Phenomenon / Mechanism Research first day permits **only** the following:

- PR/FAQ (`references/pure_research/prfaq.md`)
- Targeted literature review (`references/shared/literature_review.md`)
  scoped by the PR/FAQ
- Exploratory research planning, current-state assessment, hypothesis or
  explanation candidates, and initial-approach search
- Pre-registration of a confirmatory trial
  (`references/pure_research/preregistration.md`) when a confirmation target
  is ready
- Empty `explanation_ledger.md` skeleton with workstream ID and label declared
- Data infrastructure setup, environment pinning (`uv.lock`), data version
  recording, raw data sourcing, scaffold file creation

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
   promotion-relevant.
4. Try the smallest useful analyses, plots, probes, or model checks.
5. Record observations, assumptions tested, and approach changes in run notes,
   tracker rows, notebook notes, or result rows.
6. Label conclusions explicitly as exploratory / diagnostic.
7. Decide next: continue exploring, park/stop, or move to confirmatory
   research if a
   specific finding needs higher reliability.
```

Exploratory research does not have to be followed by confirmatory research.
Exploration can end with a map, a negative diagnostic result, a parked
question, or a decision that no claim is worth confirming. If the result will
become a `supported / external claim / high reliability claim`, move to
confirmatory research.

## Confirmatory Research Loop

Use this loop when an exploratory result, literature-derived prediction, or
explicit research question is ready for a reliability-raising test. This is
where pre-registration belongs.

```
1. Identify the question to advance (which Q-row in explanation_ledger)
2. Identify which E pair to discriminate (or test against null)
3. Write or select the pre-registration (`prereg/PR_<id>.md`, `Status: READY`)
4. Before execution, compare `PR_<id>` against the current state: current
   question, exploratory result, data availability, assumptions,
   implementation constraints, and analyst/data exposure. The purpose of
   comparing the pre-reg against the current state is not only to follow the
   pre-reg, but also to verify that the current state has not broken the PR's
   assumptions.
5. If the PR no longer matches the current situation, do not force it. Return
   to exploratory research, write transparent changes, or create a new
   confirmatory PR.
6. Run the confirmatory trial (data fetch, computation, verification checks)
7. Deviation review against the pre-registration
8. Analysis section: observation, decomposition, evidence weighing,
   tier rating, gap to next tier (per pr_trial.py.template § 5)
9. If the result is claim-cited or changes support, scope, or status, update
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

After every claim-cited or promotion-relevant interpreted result, the
workstream returns to Q/E state in `explanation_ledger.md`. The result may
strengthen, weaken, reject, split, merge, park, or leave unchanged one or more
explanation rows. Ordinary exploratory observations may stay in run notes,
tracker runs, notebook notes, or result rows until they become load-bearing.

Use the existing discriminating trial loop; this section names the return path
so results do not become orphan observations:

1. State the observed pattern and analysis tier.
2. Compare the result to the pre-registration and record deviation
   severity.
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
**current trial's analysis depth as far as it can go**. This is the
core principle from CHARTER C13.

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

## Deviation severity matrix

After a trial runs, `deviation review` compares actual analysis vs the
pre-registration. Deviations are classified per the matrix below:

The review first separates **confirmation target** from **initial approach**.
The confirmation target is the thing being tested: question, competing
explanations, scope, primary metric, thresholds, and interpretation rules. The
initial approach is the planned way to answer it: analysis method, estimator,
period-fetch mechanics, data-acquisition route, implementation path, and
operational choices.
The initial approach is not the confirmation target itself.

An initial-approach change that preserves the confirmation target, threshold,
scope, and interpretation is not a major deviation. Record the rationale and
continue; a new PR is not required, and do not treat the change as hypothesis
failure. If the change alters the confirmation target, threshold, scope,
interpretation, or multiple-testing family, classify it with the
major-deviation rows below.

| Deviation | Severity | Action |
|---|---|---|
| Parameter within ±10% of pre-reg (e.g., bandwidth slightly different) | minor | Record in `decisions.md` + continue trial |
| Sample size differs by < 5% (e.g., a few rows dropped due to data quality) | minor | Record in `decisions.md` + continue trial |
| Imputation method specified differently (e.g., median vs mean) but methodologically equivalent | minor | Record + continue |
| Test statistic logic adjusted within the same family (e.g., Pearson → robust Pearson under same hypothesis) | minor | Record + continue |
| Initial approach changed while confirmation target, threshold, scope, interpretation, and multiple-testing family are unchanged | minor | Record rationale + continue under the same PR |
| **Population/scope period shifted by > 1 year** (e.g., confirmation target changes from 2015-2024 to 2018-2024) | **major** | **Treat the trial as exploratory. Required: new pre-registration with new scope period.** |
| **Sample size differs by > 10%** | **major** | Document + new pre-reg |
| **Test statistic or estimator changed across families in a way that changes the primary metric, threshold meaning, or interpretation** (e.g., Pearson threshold reinterpreted as Spearman threshold after seeing data) | **major** | Document + new pre-reg |
| **Competing explanation added post-hoc** | **major** | Document + new pre-reg |
| **Threshold changed after seeing data** (e.g., kill threshold relaxed) | **major** | Document + new pre-reg |
| **Multiple-testing trial count under-reported** | **major** | Re-compute correction with honest count; if claim no longer holds, mark E `weakened` |
| **Imputation method changed in a way that affects test power** (e.g., dropping vs imputing missing) | **major** | Document + new pre-reg |
| **Hypothesis threshold near-miss**: primary metric within 10% of pre-reg threshold band (e.g., pre-reg said r > 0.6, observed r = 0.58) | result interpretation | Threshold miss is result interpretation, not deviation. Document the observed miss; the explanation does not get the predicted support, treat as `weakened` rather than `supported`/`rejected`. New PR is not required unless a future trial changes threshold, scope, or interpretation. |
| **Hypothesis threshold large miss**: primary metric > 10% from pre-reg threshold (e.g., pre-reg said r > 0.6, observed r = 0.30) | result interpretation | Threshold miss is result interpretation, not deviation. Interpret under the pre-registered rule, usually `rejected` or strongly `weakened`; do not create a new PR merely because the threshold was missed. |

**Major deviations invalidate the trial for claim-cited use**. Record the
major deviation in `decisions.md`, create a new pre-registration for the
changed design, and run a new trial. The original trial result remains an
exploratory result and cannot be cited as support for the claim.

This is non-negotiable. The matrix exists because "minor" vs "major" is
ambiguous in practice; without an explicit rubric, agents and humans
both default to "this is minor" and the discipline collapses.

HARKing and goalpost shifting remain blocking: changing thresholds or scope
after seeing results, changing interpretation after seeing data, or adding a
favorable explanation post-hoc is still major. The allowed flexibility applies
only to initial-approach improvements that preserve what was being checked.

## State-change logging

Same as R&D's state-change logging rule (see `references/rd/rd_workflow.md` §
State-change logging). Use `decisions.md` only for:

- durable support/status/scope transitions in `explanation_ledger.md`
- promotion, rejection, park, pivot, or major-deviation decisions
- blockers that prevent an intended durable state transition

Ordinary exploration, smoke tests, debugging, interrupted work, and lightweight
run notes do not need `decisions.md` entries. The loop discipline above (push
analysis before new trial, deviation matrix applied) still applies when the
result is claim-cited.

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

Evidence shows that a capability uncertainty must be handled separately. Add a
dependent workstream, split the current workstream, or hand off a supported
finding to a Capability / Technology Research workstream. Treat design,
evaluation, and engineering-support work as activities inside the selected
phenomenon or capability workstream unless they expose a separate
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

Same as Capability / Technology Research's rule (see
`references/rd/rd_workflow.md` § Shared infrastructure governance).
Phenomenon / Mechanism Research workstreams use the same
`shared/` folder and record the specific commits used in
`reproducibility/shared_pins.txt`.

A Phenomenon / Mechanism Research finding may itself become a `shared/`
artifact (e.g., a regime classifier proven in a phenomenon workstream that is
now used by multiple capability workstreams). The transition is a deliberate
move, not a copy: the artifact moves to `shared/` with documentation of its
origin workstream, and downstream consumers record the commit they used.

## Code reuse on workstream handoff

Same principle as Capability / Technology Research: reuse the bricks (data
pipeline, helpers, verification-check scripts), not the house (problem
framing, decision logs, ledgers / charters). A new workstream gets its own
ledger and cites the source via parent / child workstream IDs.

What can be reused from a phenomenon workstream:
- Data pipeline code, feature library, validation harness
- Sanity-check scripts
- Specific computational helpers

What cannot be reused as-is:
- The PR/FAQ as a capability charter
- Pre-registrations as capability kill criteria
- The explanation_ledger as a capability_map
- Trial notebooks as capability evidence without explicit role
  re-declaration

When the handoff direction is phenomenon -> capability: an
`explanation_ledger` finding may be cited as a literature reference in the
capability charter (H3 novelty justification). The phenomenon workstream's
`decisions.md` link is preserved as a parent workstream reference.

For a Research-to-Technology Handoff, the capability workstream may consume
the phenomenon finding as an assumption, requirement, dependency, scope
condition, benchmark, or maintenance trigger. It must not copy the supported
claim into the capability ledger as though capability research re-proved it;
cite the phenomenon `explanation_ledger.md` row and support decision instead.

## Communication conventions during a session

Agent should:

- State the **current Q + E pair being discriminated** when starting
  trial design (e.g., "Designing trial to discriminate Q1/E1 vs Q1/E2")
- Cite the **pre-registration file** when running a trial
- After any trial, state **deviation severity (none / minor / major)**
  and **analysis tier reached** as the first lines of the trial summary

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Day 1 confirmation run | Code computed claim-bearing metrics before pre-registration was ready | Block confirmatory use; label the work exploratory / diagnostic and pre-register a confirmation if the claim still matters |
| Skipping deviation review | Trial completes, no comparison to the written pre-registration | Block promotion-eligibility until deviations are recorded |
| Treating major deviation as minor | "Period shift, but the methodology is the same" | Apply the matrix strictly; period shift > 1y is major |
| New trial before pushing depth | Run a 2nd trial when 1st is at A2 | Force depth push first |
| Adding E mid-confirmation | Discovered alternative not in pre-reg and uses it to reinterpret the confirmatory result | Label as exploratory; pre-register a future confirmation if it becomes load-bearing |
| Drift | Stale ledger | Decide Promotion / Park / Add/split/handoff / Resume before new claim-bearing work |
| `supported` with sibling E still active | Promotion premature | All siblings must be at terminal status first |

## Relationship to other references

- Initial-day prohibitions appear in summarized form in
  `SKILL.md` § Guardrails; this file is the elaboration
- PR/FAQ entry: `references/pure_research/prfaq.md`
- Pre-registration: `references/pure_research/preregistration.md`
  (deviation matrix in this file is consumed by `deviation review`)
- State object: `references/pure_research/explanation_ledger_schema.md`
- IMRAD deliverable: `references/pure_research/imrad_draft.md`
- Promotion gate: `references/pure_research/pr_promotion_gate.md`
- Multiple testing discipline: project-specific multiple-testing plan
- Analysis depth: `references/shared/analysis_depth.md`
- Capability / Technology Research side rules for shared infra and handoff:
  `references/rd/rd_workflow.md`
