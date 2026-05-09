# pr_workflow.md

Operating rules for a Pure Research project across sessions: initial-day
prohibitions, discriminating trial loop, deviation severity matrix,
state-change logging, stop conditions, shared infrastructure governance,
code reuse on pivot.

## When to read

- First session of a new Pure Research project
- After any trial result, before deciding whether to update the ledger
  or run the next trial
- When a deviation from pre-registration is being considered
- Setting up shared infrastructure
- Pivoting from Pure Research to R&D

## Initial-day prohibitions

Pure Research first day permits **only** the following:

- PR/FAQ (`references/pure_research/prfaq.md`)
- Targeted literature review (`references/shared/literature_review.md`)
  scoped by the PR/FAQ
- Pre-registration of the first trial (`references/pure_research/preregistration.md`)
- Empty `explanation_ledger.md` skeleton with Mode declared
- Data infrastructure setup, environment pinning (`uv.lock`), data hash
  recording, raw data sourcing, scaffold file creation

Pure Research first day **prohibits**:

- Any trial execution (no model fits, no trial run, no metric computed
  on real data)
- Any analysis section produced (no observation logging, no
  interpretation, no decomposition)
- Any explanation row marked anything other than `active`

Why: a trial run before the pre-registration is locked is a shopping
trip. Once you have seen the data, "pre-registration" written
afterwards is theater. The 30-60 minutes of PR/FAQ + 1 hour of
pre-registration prevent months of post-hoc rationalization on weak
findings.

## The discriminating trial loop

After the initial-day setup, work proceeds in trials. Each trial is one
unit of evidence and follows this loop:

```
1. Identify the question to advance (which Q-row in explanation_ledger)
2. Identify which E pair to discriminate (or test against null)
3. Pre-register the trial (preregistration.md, hash-locked)
4. Run the trial (data fetch, computation, verification checks)
5. prereg_diff against frozen pre-reg
6. Analysis section: observation, decomposition, evidence weighing,
   tier rating, gap to next tier (per rd_trial.py.template § 5)
7. If the result is claim-cited or changes support, scope, or status, update
   explanation_ledger row(s): which E weakened / strengthened / rejected /
   unchanged
8. Record durable state transitions in decisions.md when the result changes a
   claim, promotion path, scope, park/pivot decision, or other commitment
9. Decide next: push analysis depth on this trial, design next
   discriminating trial, or escalate to promotion gate
```

The loop runs until a stop condition (below) or a question is
`answered`.

## Result-to-Question Loop

After every claim-cited or promotion-relevant interpreted result, Pure Research
returns to Q/E state in `explanation_ledger.md`. The result may strengthen,
weaken, reject, split, merge, park, or leave unchanged one or more explanation
rows. Ordinary exploratory observations may stay in run notes, tracker runs,
notebook notes, or result rows until they become load-bearing.

Use the existing discriminating trial loop; this section names the return path
so results do not become orphan observations:

1. State the observed pattern and analysis tier.
2. Compare the result to the frozen pre-registration and record deviation
   severity.
3. Identify which Q row and E rows the result touches.
4. Update `explanation_ledger.md` only as far as the evidence warrants when
   the result changes support, scope, status, or next discriminating step.
5. Record durable transitions in `decisions.md`; do not record ordinary
   exploratory runs there.
6. Decide whether the next move is deeper analysis on the current result,
   another discriminating trial, promotion review, park, or pivot.

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

After a trial runs, `prereg_diff.py` compares actual analysis vs frozen
pre-registration. Deviations are classified per the matrix below:

| Deviation | Severity | Action |
|---|---|---|
| Parameter within ±10% of pre-reg (e.g., bandwidth slightly different) | minor | Record in `decisions.md` + continue trial |
| Sample size differs by < 5% (e.g., a few rows dropped due to data quality) | minor | Record in `decisions.md` + continue trial |
| Imputation method specified differently (e.g., median vs mean) but methodologically equivalent | minor | Record + continue |
| Test statistic logic adjusted within the same family (e.g., Pearson → robust Pearson under same hypothesis) | minor | Record + continue |
| **Population period shifted by > 1 year** (e.g., 2015-2024 → 2018-2024) | **major** | **Freeze trial. Required: new pre-registration with new period.** |
| **Sample size differs by > 10%** | **major** | Freeze + new pre-reg |
| **Test statistic changed across families** (e.g., Pearson → Spearman, t-test → bootstrap) | **major** | Freeze + new pre-reg |
| **Competing explanation added post-hoc** | **major** | Freeze + new pre-reg |
| **Threshold changed after seeing data** (e.g., kill threshold relaxed) | **major** | Freeze + new pre-reg |
| **Multiple-testing trial count under-reported** | **major** | Re-compute correction with honest count; if claim no longer holds, mark E `weakened` |
| **Imputation method changed in a way that affects test power** (e.g., dropping vs imputing missing) | **major** | Freeze + new pre-reg |
| **Hypothesis threshold near-miss**: primary metric within 10% of pre-reg threshold band (e.g., pre-reg said r > 0.6, observed r = 0.58) | **minor** | Document in `decisions.md` as "near-miss"; the explanation does not get the predicted support, treat as `weakened` rather than `supported`/`rejected` |
| **Hypothesis threshold large miss**: primary metric > 10% from pre-reg threshold (e.g., pre-reg said r > 0.6, observed r = 0.30) | **major** | Freeze + new pre-reg if you want to test the boundary behavior; otherwise treat the explanation as `rejected` cleanly |

**Major deviations invalidate the trial**. The trial is recorded in
`decisions.md` as "trial frozen due to major deviation; new
pre-registration filed as PR_<id+1>". The original pre-reg is
preserved (hash on file). The new trial under the new pre-reg
proceeds. The original trial result cannot be cited as evidence.

This is non-negotiable. The matrix exists because "minor" vs "major" is
ambiguous in practice; without an explicit rubric, agents and humans
both default to "this is minor" and the discipline collapses.

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

## Stop conditions — when does a Pure Research project end?

A project terminates when one of:

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
Reproducibility: data hash, git commit, env lock recorded for each cited trial
```

### Promotion (negative / null finding)

All explanations under a Q reach `rejected`. The Q is `answered` with
"none of the candidate explanations holds." This is a real finding.
The IMRAD draft documents the elimination.

### Park

The Q cannot progress because of a named external unblock condition
(data unavailable, sample size insufficient until time passes, prior
project must complete). Differs from promotion: the project will
resume when the unblock fires.

### Pivot

User realizes mid-project that the goal is actually R&D (build a
capability) rather than Pure Research (understand a phenomenon). Use
the Pivot protocol per `SKILL.md` § First Decision. Same options
(suspend + restart vs add secondary project) apply.

### Drift (anti-pattern)

Project simply stops being worked on without an explicit decision. When
returning to a stale project, first decide whether to promote, park, pivot, or
resume; do not create audit entries for the inactive period.

## Shared infrastructure governance

Same as R&D's rule (see `references/rd/rd_workflow.md` § Shared
infrastructure governance). Pure Research projects use the same
`shared/` folder and pin to specific commit hashes recorded in
`reproducibility/shared_pins.txt`.

A Pure Research finding may itself become a `shared/` artifact (e.g.,
a regime classifier proven via Pure Research that is now used by
multiple R&D projects). The transition is a deliberate move, not a
copy: the artifact moves to `shared/` with documentation of its origin
project, and downstream consumers pin to its commit hash.

## Code reuse on pivot

Same principle as R&D: reuse the bricks (data pipeline, helpers,
verification-check scripts), not the house (problem framing, decision logs,
ledgers / charters). The new project gets a fresh `decisions.md`
referencing the source via `parent_project_id`.

What can be reused from a pivoted Pure Research project:
- Data pipeline code, feature library, validation harness
- Sanity-check scripts
- Specific computational helpers

What cannot be reused as-is:
- The PR/FAQ (the new R&D charter is a different document)
- Pre-registrations (R&D doesn't use these)
- The explanation_ledger (R&D uses capability_map)
- Trial notebooks (re-purposed only with explicit role re-declaration)

When the pivot direction is Pure Research → R&D: an `explanation_ledger`
finding may be cited as a literature reference in the new R&D charter
(H3 novelty justification). The Pure Research project's
`decisions.md` link is preserved as `parent_project_id`.

For a Research-to-Technology Handoff, the R&D project may consume the Pure
Research finding as an assumption, requirement, dependency, scope condition,
benchmark, or maintenance trigger. It must not copy the supported claim into
the R&D ledger as though R&D re-proved it; cite the Pure Research
`explanation_ledger.md` row and promotion decision instead.

## Communication conventions during a session

Agent should:

- State the **current Q + E pair being discriminated** when starting
  trial design (e.g., "Designing trial to discriminate Q1/E1 vs Q1/E2")
- Cite the **frozen pre-reg hash** when running a trial
- After any trial, state **deviation severity (none / minor / major)**
  and **analysis tier reached** as the first lines of the trial summary

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Day 1 trial run | Code computed metrics on real data before pre-reg lock | Block; require pre-reg freeze first; original work is invalidated |
| Skipping prereg_diff | Trial completes, no diff run | Block promotion-eligibility until diff is recorded |
| Treating major deviation as minor | "Period shift, but the methodology is the same" | Apply the matrix strictly; period shift > 1y is major |
| New trial before pushing depth | Run a 2nd trial when 1st is at A2 | Force depth push first |
| Adding E mid-trial | Discovered alternative not in pre-reg | Counts as major deviation; new pre-reg required |
| Drift | Stale ledger | Decide Promotion / Park / Pivot / Resume before new claim-bearing work |
| `supported` with sibling E still active | Promotion premature | All siblings must be at terminal status first |

## Relationship to other references

- Initial-day prohibitions appear in summarized form in
  `SKILL.md` § Guardrails; this file is the elaboration
- PR/FAQ entry: `references/pure_research/prfaq.md`
- Pre-registration: `references/pure_research/preregistration.md`
  (deviation matrix in this file is consumed by `prereg_diff.py`)
- State object: `references/pure_research/explanation_ledger_schema.md`
- IMRAD deliverable: `references/pure_research/imrad_draft.md`
- Promotion gate: `references/pure_research/pr_promotion_gate.md`
- Multiple testing discipline: project-specific multiple-testing plan
- Analysis depth: `references/shared/analysis_depth.md`
- R&D side rules for shared infra and pivot: `references/rd/rd_workflow.md`
