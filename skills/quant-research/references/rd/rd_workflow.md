# rd_workflow.md

Operating rules for an R&D project across sessions: initial-day
prohibitions, session-end ritual, stop conditions, shared infrastructure
governance, and the rules for code reuse on a discipline pivot.

## When to read

- First session of a new R&D project (initial-day prohibitions)
- End of any session (session-end ritual)
- When deciding whether the project should close (stop conditions)
- Setting up shared code / data pipelines that may serve both R&D and
  Pure Research projects
- Pivoting from R&D to Pure Research (or vice versa) and deciding what
  artifacts to carry over

## Initial-day prohibitions

R&D first day permits **only** the following:

- Charter (`references/rd/rd_charter.md`) — Heilmeier 8 questions
- Layer 1 closure (`references/rd/core_technologies.md`) — core
  technology decomposition
- Capability map skeleton (`references/rd/capability_map_schema.md`) —
  Section 2 rows in TRL-0 status
- Data infrastructure setup, environment pinning (`uv.lock`), data hash
  recording, raw data sourcing, scaffold file creation

R&D first day **prohibits**:

- Any implementation that runs (no model training, no backtest, no trial
  that produces a metric)
- Any Stage gate (Scoping is part of capability writing in the table; it
  is OK to scope, but no de-risk test)
- Any analysis whose conclusions enter the ledger

Why: kill criteria are frozen at charter close. Code written before kill
criteria exist accumulates sunk cost that biases later kill decisions.
A project that writes code on day 1 and discovers the charter is wrong on
day 5 will resist redefining the charter (sunk cost), or worse, redefine
the kill criteria to fit the code (goalpost shifting).

The 1-2 hours of charter writing prevent weeks of effort on a misframed
target.

## Session-end ritual

Every session must end with one of two outcomes:

### Outcome A — At least one ledger row moved

A row in `capability_map.md` (Section 1 K-row OR Section 2 C-row) or
`decisions.md` changed status, advanced TRL, gained an analysis section,
or transitioned (active → matured / blocked / split / merged / killed /
parked / stale).

Append a 1-line summary to `decisions.md`:

```markdown
## YYYY-MM-DD HH:MM session summary
- <K-id or C-id>: <transition or movement>
- (next session) <next planned step>
```

### Outcome B — No row moved

If the session produced no state change, **explicitly record this** in
`decisions.md`:

```markdown
## YYYY-MM-DD HH:MM no progress: <reason>
- <reason in one sentence: what was attempted, what blocked it>
- (next session) <what would unblock>
```

Acceptable reasons: blocked by external dependency, exploration without
result, sanity check uncovered upstream issue requiring re-scope.

Unacceptable: "spent the session reviewing", "thinking about the
problem". Reviewing or thinking that produces no state change is a sign
the work was not focused on a specific blocker.

The session-end ritual is **necessary but not sufficient** for the
session-level R&D sequencing guardrail (per `SKILL.md` § Guardrails);
moving any row satisfies the ritual but the sequencing rule still
applies.

## Stop conditions — when does an R&D project end?

A project terminates when one of:

### Promotion (success path)

All critical-path capabilities are `matured`, all upstream exits fired
before integration test (timestamp verified), all kill criteria un-fired
with A4 evidence, project meets charter H8 final exam criteria, and
(if any K is `継続改善型`) the maintenance plan is filed.

See `references/rd/rd_promotion_gate.md` for the full checklist.

### Kill (failure path)

Charter-level kill criterion (Heilmeier H6) fires with A4-decomposed
evidence. The whole project is killed, not just one capability.

The closing entry in `decisions.md`:

```markdown
## YYYY-MM-DD project killed
- Charter H6 kill criterion <id>: <observation>
- A4 decomposition: <mechanism, alternatives ruled out, scope>
- Lessons learned: <what would have changed the outcome>
- Disposition of artifacts: <what gets kept, what gets archived>
```

### Park (deferred)

The project is not making progress because of a named external
unblock condition (e.g., "waiting for vendor data feed", "waiting for
prior project K to mature"). Differs from kill: the project will resume
when the unblock fires.

The closing entry must name the **specific unblock condition** and the
**check cadence**. A project parked for > 6 months without the unblock
firing should be re-evaluated for kill.

### Pivot (discipline shift)

The user realizes mid-project that the goal is actually Pure Research
(understand a phenomenon) rather than R&D (build a capability). Use the
Pivot protocol per `SKILL.md` § First Decision.

Two paths:

- **Suspend + restart** the project as Pure Research, link via
  `parent_project_id` in `decisions.md`
- **Add secondary** Pure Research project alongside the still-active R&D
  project, with declared cross-project dependencies

See § Code reuse on pivot below.

### Drift (anti-pattern, not an acceptable termination)

The project simply stops being worked on without an explicit Promotion /
Kill / Park / Pivot decision. If a project goes 4+ weeks without a
session, the agent (in the next session) should force a stop-condition
decision: the user must declare one of the four above. Drifting is
worse than killing because it leaves the artifact in an ambiguous
state.

## Shared infrastructure governance

Many R&D projects use the same data pipeline, the same feature library,
the same backtest harness as other projects (R&D or Pure Research). The
"separate ledgers" rule (`SKILL.md` § First Decision) applies to
**decision tracking**, not to infrastructure code.

### Layout

Shared infrastructure lives outside any single project's folder, in a
`shared/` subdirectory at the workspace root:

```
workspace/
├── shared/
│   ├── data_pipeline/
│   ├── feature_lib/
│   ├── backtest_harness/
│   └── ... (libraries, helpers, utilities)
├── projects/
│   ├── rd_intraday_vol_forecasting/
│   │   ├── charter.md
│   │   ├── capability_map.md
│   │   ├── decisions.md
│   │   ├── purposes/
│   │   ├── results/
│   │   └── reproducibility/
│   ├── pr_vol_decay/
│   │   ├── prfaq.md
│   │   ├── prereg/
│   │   ├── explanation_ledger.md
│   │   ├── decisions.md
│   │   └── ...
│   └── ...
```

### Pinning

Each project that consumes shared infrastructure pins to a **specific
git commit hash** of `shared/`, recorded in the project's
`reproducibility/data_hashes.txt` (or a similar file `shared_pins.txt`).

When a project starts a new trial, the pin is part of the reproducibility
3-tuple stamped via the selected tracking backend or
`scripts/reproducibility_stamp.py`.

### Updating shared infrastructure

A change to `shared/` is its own deliberate change, recorded in
`shared/decisions.md` (a small ledger inside `shared/`). Projects that
depend on `shared/` decide independently whether to update their pin.

Updating a pin while a project is mid-trial is a **deviation**: file an
entry in the project's `decisions.md` naming the new pin and the
rationale.

### Anti-patterns

- Forking the data pipeline into the project's folder ("just for this
  project") → defeats reuse, creates drift across projects, makes
  reproducibility comparisons impossible.
- Sharing decision-tracking files across projects → undermines the
  separate-ledgers rule, makes audit ambiguous.
- Modifying `shared/` from inside a project session without filing
  `shared/decisions.md` entry → silent change, breaks downstream
  reproducibility.

## Code reuse on pivot

When a project pivots discipline (R&D → Pure Research or vice versa),
existing code, notebooks, and figures may be relevant to the new
project. The default is to reuse what's reusable, but reuse must be
**explicit**.

### What can be reused

- Data pipeline code (already in `shared/`, just keep the pin)
- Feature definitions and computations
- Validation harnesses (split logic, embargo, CV folds)
- Plot helpers and reporting templates
- Sanity check scripts

### What cannot be reused as-is

- Trial notebooks (the trial was designed for the old discipline; in the
  new discipline, the trial design must be re-stated)
- Decision log entries (new project gets a fresh `decisions.md`, with
  the pivot's `parent_project_id` link to the old one)
- Capability map ↔ explanation ledger (different schemas, not portable)
- Charter ↔ PR/FAQ (different documents, must be re-written for the new
  discipline)

### Reuse procedure

1. In the new project's `README.md`, declare the source project:
   `parent_project_id: <old project name>` (also recorded in
   `decisions.md`).
2. List reusable artifacts: a `decisions.md` entry naming each file or
   module to be reused and the **role it plays in the new project**
   (the role may differ from the old).
3. Move (do not copy) reusable artifacts to the new project folder, OR
   move shared-eligible items to `shared/` and pin from the new project.
4. Trial notebooks from the old project: archive in
   `<old_project>/archive/` rather than carrying over. Reference them
   from the new project as `prior_work` in `literature/papers.md` if
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

These conventions make the session log auditable when reviewed later or
by another agent.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Day 1 implementation | Code committed before charter frozen | Block; require charter freeze first |
| Session ends with no state change recorded | "Worked on this for 2 hours" with no ledger update | Force a `no progress: <reason>` entry |
| Project drifts (4+ weeks no session) | Stale `capability_map.md` | Force Promotion / Kill / Park / Pivot decision |
| Shared infra forked into project | Duplicate copies of data pipeline | Move back to `shared/`, pin from project |
| Reuse without role declaration | Old code shows up in new project with no decisions.md entry | File the entry; state the role |

## Relationship to other references

- Initial-day prohibitions appear in summarized form in
  `SKILL.md` § Guardrails; this file is the elaboration.
- Stop conditions integrate with `references/rd/rd_promotion_gate.md`
  (Promotion path) and the kill / park / pivot patterns embedded in
  `SKILL.md` and `decisions.md` template.
- Shared infrastructure governance is parallel to the version pinning done by
  the selected tracking backend or `scripts/reproducibility_stamp.py`.
- Pivot protocol is defined in `SKILL.md` § First Decision; this file
  covers the code-reuse follow-up.
