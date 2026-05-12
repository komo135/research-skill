# rd_workflow.md

Operating rules for a Capability / Technology Research workstream across
sessions. This is the R&D-compatible workflow for entry guardrails,
state-change logging, stop conditions, shared infrastructure governance, and
handoff to other workstreams.

## When to read

- First session of a new Capability / Technology Research workstream
  (entry guardrails)
- End of a session that changed durable research state
- When deciding whether the workstream should close (stop conditions)
- Setting up shared code / data pipelines that may serve capability and
  phenomenon workstreams
- Adding, splitting, or handing off to a Phenomenon / Mechanism Research
  workstream and deciding what artifacts to carry over

## Entry guardrails

Before a Capability / Technology Research workstream has a reviewed charter
and kill criteria, prioritize:

- Charter (`references/rd/rd_charter.md`) — Heilmeier 8 questions
- Layer 1 closure (`references/rd/core_technologies.md`) — core
  technology decomposition
- Capability map skeleton (`references/rd/capability_map_schema.md`) —
  Section 2 rows in TRL-0 status
- Data infrastructure setup, environment pinning (`uv.lock`), data version
  recording, raw data sourcing, scaffold file creation
- Non-load-bearing scaffold, interface probe, smoke test, or wiring check
  when it is labeled as enabling work and is not cited for TRL advancement,
  promotion, kill, or an external claim

Before the charter and kill criteria exist, do not run or cite:

- Promotion-relevant or claim-bearing implementation
- Model training, trial runs, or metric-producing checks intended to advance
  TRL, fire a kill criterion, promote a capability, or support an external
  claim
- Any Stage gate (Scoping is part of capability writing in the table; it
  is OK to scope, but no de-risk test)
- Any analysis whose conclusions enter the ledger

Why: kill criteria are ready at charter close. Code written before kill
criteria exist accumulates sunk cost that biases later kill decisions.
A workstream that treats early exploratory code as evidence before the charter
is ready will resist redefining the charter (sunk cost), or worse, redefine the
kill criteria to fit the code (goalpost shifting).

The 1-2 hours of charter writing prevent weeks of effort on a misframed
target.

## State-change logging

Only sessions that change durable research state need a `decisions.md` entry.
Orientation, environment setup, interrupted work, smoke tests, debugging, and
ordinary exploration may stay in run notes, tracker runs, notebook notes, or
result rows unless they change a claim, state transition, gate decision,
promotion evidence, kill decision, pivot, or scope.

### Outcome A — At least one ledger row moved

A row in `capability_map.md` (Section 1 K-row OR Section 2 C-row) or
`decisions.md` changed status, advanced TRL, gained an analysis section,
or transitioned (active → matured / blocked / split / merged / killed /
parked / stale).

Append a short summary to `decisions.md` when the move is durable:

```markdown
## YYYY-MM-DD HH:MM session summary
- <K-id or C-id>: <transition or movement>
- (next session) <next planned step>
```

### Outcome B — No row moved

Record `no progress` only when the session was explicitly attempting a durable
state transition and the blocker itself matters for future project state:

```markdown
## YYYY-MM-DD HH:MM no progress: <reason>
- <reason in one sentence: what was attempted, what blocked it>
- (next session) <what would unblock>
```

Acceptable reasons: blocked by external dependency, sanity check uncovered
upstream issue requiring re-scope, or a promotion/kill/pivot decision could not
be made because a named piece of evidence was missing.

State-change logging is **necessary but not sufficient** for the session-level
R&D sequencing guardrail (per `SKILL.md` § Guardrails); moving any row records
the transition, but the sequencing rule still applies.

## Stop conditions — when does a capability workstream end?

A workstream terminates when one of:

### Promotion (success path)

All critical-path capabilities are `matured`, all upstream exits fired
before integration test (ordering verified), all kill criteria un-fired
with A4 evidence, project meets charter H8 final exam criteria, and
(if any K is `継続改善型`) the maintenance plan is filed.

See `references/rd/rd_promotion_gate.md` for the full checklist.

### Kill (failure path)

Charter-level kill criterion (Heilmeier H6) fires with A4-decomposed
evidence. The capability workstream or target is killed, not just one
low-level task.

The closing entry in `decisions.md`:

```markdown
## YYYY-MM-DD project killed
- Charter H6 kill criterion <id>: <observation>
- A4 decomposition: <mechanism, alternatives ruled out, scope>
- Lessons learned: <what would have changed the outcome>
- Disposition of artifacts: <what gets kept, what gets archived>
```

### Park (deferred)

The workstream is not making progress because of a named external
unblock condition (e.g., "waiting for vendor data feed", "waiting for
prior workstream K to mature"). Differs from kill: the workstream will resume
when the unblock fires.

The closing entry must name the **specific unblock condition** and the
**check cadence**. A workstream parked for > 6 months without the unblock
firing should be re-evaluated for kill.

### Add / split / handoff

Evidence shows that a phenomenon or mechanism uncertainty must be handled
separately. Add a dependent workstream, split the current workstream, or hand
off an observation to a Phenomenon / Mechanism Research workstream. Treat
design, evaluation, and engineering-support work as activities inside the
selected capability or phenomenon workstream unless they expose a separate
research-state claim. Record the trigger, affected workstream IDs, ledger
rows, reused evidence scope, parent / child relationship, and next gate in
`decisions.md`.

Project-level pivot is reserved for a change in final intent or decision
audience, not for ordinary mixed research. See § Code reuse on workstream
handoff below.

### Drift (anti-pattern, not an acceptable termination)

The workstream stops being worked on without an explicit Promotion / Kill /
Park / Add / Split / Handoff decision. When returning to stale state, first ask
whether it should promote, kill, park, add, split, hand off, or resume; do not
manufacture review entries for the inactive period.

## Shared infrastructure governance

Many capability workstreams use the same data pipeline, the same feature
library, or the same trial harness as other workstreams. The workstream-ledger
rule in `SKILL.md` § First Decision applies to **decision tracking**, not to
infrastructure code.

### Layout

Shared infrastructure lives outside any single project's folder, in a
`shared/` subdirectory at the workspace root:

```
workspace/
├── shared/
│   ├── data_pipeline/
│   ├── feature_lib/
│   ├── trial run_harness/
│   └── ... (libraries, helpers, utilities)
├── projects/
│   ├── alpha/
│   │   ├── project_state.md
│   │   ├── decisions.md
│   │   ├── workstreams/
│   │   │   ├── WS001-capability/
│   │   │   │   ├── charter.md
│   │   │   │   └── capability_map.md
│   │   │   └── WS002-phenomenon/
│   │   │       ├── prfaq.md
│   │   │       ├── prereg/
│   │   │       └── explanation_ledger.md
│   │   ├── purposes/
│   │   ├── results/
│   │   └── reproducibility/
│   └── ...
```

### Pinning

Each project or workstream that consumes shared infrastructure pins to a
**specific git commit** of `shared/`, recorded in the project's
`reproducibility/data_versions.txt` (or a similar file `shared_pins.txt`).

When a workstream starts a new trial, the pin is part of the reproducibility
3-tuple recorded via the selected tracking backend or local run note.

### Updating shared infrastructure

A change to `shared/` is its own deliberate change, recorded in
`shared/decisions.md` (a small ledger inside `shared/`). Projects that
depend on `shared/` decide independently whether to update their pin.

Updating a pin while a workstream is mid-trial is a **deviation**: file an
entry in the project's or workstream's `decisions.md` naming the new pin and the
rationale.

### Anti-patterns

- Forking the data pipeline into the project's folder ("just for this
  workstream") → defeats reuse, creates drift across workstreams, makes
  reproducibility comparisons impossible.
- Sharing decision-tracking files across workstreams → undermines the
  separate-ledgers rule and makes review ambiguous.
- Modifying `shared/` from inside a workstream session without filing
  `shared/decisions.md` entry → silent change, breaks downstream
  reproducibility.

## Code reuse on workstream handoff

When a capability workstream adds, splits, or hands off to another workstream,
existing code, notebooks, and figures may be relevant. The default is to reuse
what is reusable, but reuse must be **explicit**.

### What can be reused

- Data pipeline code (already in `shared/`, just keep the pin)
- Feature definitions and computations
- Validation harnesses (split logic, embargo, CV folds)
- Plot helpers and reporting templates
- Sanity check scripts

### What cannot be reused as-is

- Trial notebooks (the trial was designed for the old workstream role; in the
  new workstream, the trial design must be re-stated)
- Decision log entries (the new workstream gets its own state rows and cites
  the parent workstream)
- Capability map ↔ explanation ledger (different schemas, not portable)
- Charter ↔ PR/FAQ (different documents, must be re-written for the new
  workstream role)

### Reuse procedure

1. In the new workstream's note or ledger header, declare the source
   workstream: `parent_workstream_id: <old workstream id>` (also recorded in
   `decisions.md`).
2. List reusable artifacts: a `decisions.md` entry naming each file or
   module to be reused and the **role it plays in the new workstream**
   (the role may differ from the old).
3. Move (do not copy) reusable artifacts to the new workstream folder, OR
   move shared-eligible items to `shared/` and pin from the new workstream.
4. Trial notebooks from the old workstream: archive or leave in place as
   prior evidence rather than carrying over silently. Reference them
   from the new workstream as `prior_work` in `literature/papers.md` if
   they produced findings worth citing.

The principle: reuse the bricks, not the house. Code and data
preparation transfer; problem framing and decision logs do not.

## Communication conventions during a session

Within a working session, the agent should:

- State the **current Stage** explicitly when starting work on a
  capability (e.g., "Working C3 Stage 2 De-risk").
- Cite the **research question** (from the parent K) being addressed
  before running any test.
- After any test, state **TRL transition (or none)** and **analysis tier
  reached** as the first line of the trial summary.

These conventions make claim-bearing session notes easier to review later or by
another agent without requiring every exploratory session to enter
`decisions.md`.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Premature evidence-producing implementation | Promotion-relevant code or metrics cited before charter readiness | Block citation; require reviewed charter first |
| Durable state change not recorded | Capability promoted or killed with no ledger / decision entry | File the missing transition with evidence |
| Workstream drifts | Stale `capability_map.md` | Decide Promotion / Kill / Park / Add/Split/Handoff / Resume before new claim-bearing work |
| Shared infra forked into project | Duplicate copies of data pipeline | Move back to `shared/`, pin from project |
| Reuse without role declaration | Old code shows up in new project with no decisions.md entry | File the entry; state the role |

## Relationship to other references

- Entry guardrails appear in summarized form in
  `SKILL.md` § Guardrails; this file is the elaboration.
- Stop conditions integrate with `references/rd/rd_promotion_gate.md`
  (Promotion path) and the kill / park / handoff patterns embedded in
  `SKILL.md` and `decisions.md` template.
- Shared infrastructure governance is parallel to the version pinning done by
  the selected tracking backend or local run note.
- Workstream operations are defined in `SKILL.md` § First Decision; this file
  covers the code-reuse follow-up for capability workstreams.
