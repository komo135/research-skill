# capability_map_schema.md

R&D Layer 2 — operational decomposition. Capabilities are the
testable units that mature through evidence packages. Each capability is
tied to a parent core technology (Layer 1).

## When to read

- Writing the first capability after Layer 1 (core technologies) is
  closed
- Adding a new capability mid-project (verify Layer 1 is closed first)
- Splitting / merging / killing a capability
- Reviewing a promotion claim for capability-level conditions

## Position in `capability_map.md`

`capability_map.md` has two sections:

- **Section 1**: Core Technologies (Layer 1) — see
  `references/rd/core_technologies.md`
- **Section 2**: Capabilities (Layer 2) — defined by this schema

Section 2 cannot be populated until Section 1 is **closed-for-work** (per
core_technologies.md § Layer 1 closure).

## Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `ID` | `C1`, `C2`, ... | yes | Sequential, never reused |
| `capability` | string (1 sentence) | yes | What this capability does, no jargon |
| `core_tech_id` | `K1`, `K2`, ... \| `integration` | yes | Parent core tech; `integration` reserved for cross-cutting work |
| `parent_id` | `Ck` \| empty | optional | If this capability is a child of a split capability, the original parent |
| `depends_on` | list of `Ck` IDs | optional | Other capabilities that must mature first |
| `dependent_on_research` | `<project>:<min_tier>` \| empty | optional | If this capability requires a Pure Research finding from another project (e.g., `pure_vol_decay:A4`), promotion is blocked until that project's claim reaches the named tier |
| `current_TRL` | 0–6 | yes | Current maturity (see `references/rd/trl_scale.md`) |
| `target_TRL` | 0–6 | yes | The TRL this capability needs to reach to be `matured` (typically 6) |
| `exit_criteria` | string | yes | Concrete observation that advances current_TRL by exactly 1 |
| `kill_criteria` | string | yes | Concrete observation that kills this capability — see § Kill criteria below |
| `blocking_uncertainty` | string \| empty | optional | The single biggest unknown about this capability right now |
| `Status` | enum | yes | active / matured / blocked / split / merged / stale / parked / killed |

## Status vocabulary

| Status | Meaning |
|---|---|
| `active` | Currently being worked on |
| `matured` | Reached `target_TRL`, kill criteria un-fired, analysis at A4+, ready to be consumed by upstream caps or count toward parent K's `established` status |
| `blocked` | Cannot progress until a named dependency (capability, K, or Pure Research project) changes |
| `split` | Decomposed into 2+ children; original row stays for traceability |
| `merged` | Absorbed into another capability (record absorbing ID) |
| `stale` | No longer relevant after scope change |
| `parked` | Deferred with a named unblock condition |
| `killed` | Kill criterion fired with A4+ evidence; this capability is terminal under the current scope |

Allowed transitions:

```
active → matured (when target_TRL hit + exits + analysis met)
active → blocked (when dependency named)
active → split (becomes parent of new C-rows)
active → merged (when duplicate found)
active → stale (when scope shifts)
active → parked (with named unblock)
active → killed (with A4+ evidence per § Kill criteria)
blocked → active (when blocker resolved)
parked → active (when unblock fires)
parked → stale (when no longer relevant)
```

Disallowed without a deviation: `matured → active`; `killed → active`.
Re-opening either state requires a deviation entry. If the prior terminal
state was invalidated by data defect, implementation bug, or wrong threshold,
create a corrected C-row or explicitly re-open the row with the reason and
new evidence boundary.

## Granularity rule

A capability is sized so that one evidence package can justify one coherent
TRL claim. Concretely:

- If one evidence package tries to justify unrelated jumps, the capability
  is too coarse — split it.
- If two unrelated tests are needed to move it TRL-2 → TRL-3, the
  capability is two capabilities — split it.
- If the capability cannot be tested at all (no observable advance
  evidence), it may not be a capability — it might be a task (move to
  `decisions.md`) or a sub-task of another capability.

## Kill criteria — must be A4-anchored

Every capability row carries a `kill_criteria` field. Two requirements:

### 1. Kill criteria are concrete and observable at write-time

Good: "If zero-shot IC < 0.02 across 3 instruments after 1 week of
fine-tuning sweep on this capability, kill."

Bad: "If it doesn't work."
Bad: "If we run out of ideas."
Bad: "If management says so."

### 2. A kill firing requires A4+ evidence to validate

When a kill criterion fires, the agent does **not** mark the capability
`killed` immediately. The firing opens terminal review. Instead:

1. Record the A0 observation (what the metric actually was)
2. Decompose: name the primary failure hypothesis (A1) and at least one
   alternative (A2)
3. Run a discriminating test if feasible (A3)
4. Reach mechanism-level explanation (A4): "the kill fired because
   mechanism M; alternatives X, Y were tested and ruled out by
   observations Z, W"
5. Only then mark the capability `killed` and append the A4 analysis to
   the kill-fire log. If the failure is repairable, record `Hold`,
   `Recycle`, or `Re-scope` instead.

This prevents a shallow kill — e.g., "loss didn't drop, kill" — when the
real cause was a learning-rate misconfiguration. See
`references/shared/analysis_depth.md` for the tier definitions.

The A4-anchoring requirement applies symmetrically to `matured`
promotion (per `references/rd/rd_promotion_gate.md`). Both transitions
are evidence-heavy by design.

## Cross-project dependencies

Setting `dependent_on_research: <project>:<min_tier>` (e.g.,
`pure_vol_decay:A4`) means this capability cannot be promoted to
`matured` until the named Pure Research project produces a claim at
the named analysis tier or higher.

The promotion gate (`references/rd/rd_promotion_gate.md`) checks all
`dependent_on_research` entries before allowing `matured`. Unmet
dependencies block promotion regardless of TRL or kill state.

Cross-project dependencies are unidirectional: R&D consumes Pure
Research findings, not vice versa. Two-way feedback creates
circularity; if the user needs feedback from R&D into Pure Research,
that requires a new Pure Research project (with its own pre-registration)
that consumes R&D outputs as data.

## Capability → core tech graduation

If during a Stage gate (especially Scoping or De-risk) a capability is
discovered to require its own multi-stage research arc, or to need a
distinct lifecycle from its parent K, **promote it to its own K**:

1. File a deviation entry in `decisions.md` naming the capability ID and
   the trigger evidence (which Stage observation prompted the
   reclassification).
2. Add a new K row in Section 1 with the lifted capability's research
   question (per `references/rd/core_technologies.md`).
3. Move the capability under the new K (update `core_tech_id`).
4. Re-evaluate the original parent K's status (it may need new
   sub-capabilities to fill the gap).
5. Re-run Layer 1 closure check before any new Stage gates can run on
   sibling capabilities.

This is the explicit handle for "we discovered a research question we
hadn't seen". Mid-project Layer 1 expansion is allowed if accompanied by
an explicit deviation entry.

## Schema validation

`scripts/validate_ledger.py` enforces:

- Every capability has `core_tech_id` set and the K exists in Section 1
- Every `core_tech_id = integration` capability has at least 2
  `depends_on` entries (otherwise it is not actually integration)
- Every `parent_id` references an existing capability that is in `split`
  status
- Every `current_TRL` and `target_TRL` is in [0, 6]
- Single-update transitions don't advance TRL by > 1 (TRL skip detection)
- `dependent_on_research` values match the syntax `<project>:<tier>`
  where tier is A2-A5
- `kill_criteria` is non-empty and not a generic phrase ("if it doesn't
  work" patterns are flagged)
- Status transitions follow the allowed set (e.g., no `matured → active`)

## Rendered example

For the intraday vol forecasting project from
`references/rd/core_technologies.md` § Worked example:

```markdown
## Section 2: Capabilities

| ID | capability | core_tech_id | parent_id | depends_on | dependent_on_research | current_TRL | target_TRL | exit_criteria | kill_criteria | blocking_uncertainty | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Zero-shot TimesFM forecast on 5-min ES vol, single instrument | K1 | | | | 1 | 6 | OOS IC ≥ 0.05 on a 1-month held-out period for 1 instrument | OOS IC < 0.02 on 1-month held-out across 3 instruments after sanity checks pass | Whether per-bar vs per-window inference framing matters | active |
| C2 | Sanity-check sweep for C1 (look-ahead, calibration, sign) | K1 | | | | 0 | 4 | All sanity checks in `references/shared/sanity_checks.md` § 1, 6, 7 pass | Random-signal benchmark passes (signal evaluator broken) | | active |
| C3 | Fine-tuning protocol sweep on 6 months of ES data | K2 | | C1 | | 0 | 6 | Best fine-tuned IC > zero-shot IC by ≥ 0.03 on held-out, with config recorded | All sweep configs ≤ zero-shot IC | Whether enough data exists for stable fine-tuning | blocked |
| C4 | Inference latency benchmark on production hardware | K3 | | | | 0 | 6 | Median latency ≤ 100ms across 1000 trial bars on production HW | Median latency > 500ms with no obvious optimization remaining | | active |
| C5 | Calibration metric vs hedging benefit on shadow data | K4 | | C1 | | 0 | 6 | One metric (ECE / IC / calibrated PnL) explains ≥ 70% of variance in hedge-error reduction in OOS shadow-trade simulation | All candidate metrics explain < 30% | Hedge-sizing logic is partially open at consumer side | active |
| C6 | Integration: drive hedge-sizing logic on 2-week shadow paper trade | integration | | C1, C3, C4, C5 | | 0 | 6 | 2-week shadow trade with all upstream caps matured AND IC ≥ 0.04, ECE ≤ 0.10, latency ≤ 100ms | Shadow trade hedge-error worse than baseline static-vol estimator | | blocked |
```

Notes from this example:

- C1 is at TRL-1 already (literature plus zero-shot is principled). Other
  capabilities are TRL-0.
- C2 is a sanity-check capability tied to the same K (K1) as C1. Its
  target TRL is 4, not 6, because it does not need operational
  prototype demonstration — it only needs to validate that C1's
  evaluation isn't broken.
- C3 is `blocked` on C1 because fine-tuning protocol depends on the
  zero-shot baseline.
- C6 is `integration`, with multi-cap dependency. It is `blocked` until
  C1, C3, C4, C5 all mature. The integration test cannot run earlier;
  the promotion gate will verify the timestamp.
- Each `kill_criteria` is concrete (numeric or behavioral) and would
  itself require A4 analysis to fire (e.g., low IC after fine-tuning
  sweep — but C3 might fail because of bad hyperparameter range, not
  because of the underlying technology, so the A4 decomposition matters).

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Capability list with no `core_tech_id` | Layer 1 was skipped | Block; require Layer 1 closure first |
| Vague `exit_criteria` | "When it works" | Force concrete observable; numeric or behavioral |
| Vague `kill_criteria` | "If it doesn't work" | Force concrete observable; A4-anchored |
| Capability too coarse | One row, target TRL 6, exit criteria has 4 sub-tests | Split into multiple capabilities, one test each |
| Capability is actually a task | "Implement the data loader" | Move to `decisions.md` as engineering work, not capability |
| `dependent_on_research` set without target project existing | Hallucinated dependency | Validate the named project actually exists |

## Relationship to other references

- `references/rd/core_technologies.md` § Layer 1 closure must hold before
  any capability is added.
- `references/rd/trl_scale.md` defines what each TRL level demands as
  exit evidence.
- `references/rd/rd_stages.md` defines how a capability progresses
  through TRL levels (Scoping → De-risk → Build → Validate → Integrate).
- `references/rd/rd_promotion_gate.md` defines the per-capability
  conditions for `matured` and the project-level conditions for
  promotion.
- `references/shared/analysis_depth.md` defines the A0-A5 tier system
  used by both kill criteria and matured promotion.
