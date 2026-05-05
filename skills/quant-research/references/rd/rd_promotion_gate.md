# rd_promotion_gate.md

The R&D promotion checklist. Run this before declaring an R&D target
**promoted** (i.e., the project as a whole is complete or completed-v1).
Promotion is the highest bar in the skill: every load-bearing item below must
pass with concrete evidence cited. Non-load-bearing process notes may be
summarized, but not used to support the promotion claim.

## When to read

- About to mark an R&D project as promoted
- Reviewing another agent's promotion claim
- Before the closing entry in `decisions.md`

## Pre-conditions

The promotion gate may not start unless:

- Charter is frozen and on file (`charter.md` + `prereg/charter.lock`)
- `capability_map.md` Section 1 (Layer 1) is closed-for-work per
  `references/rd/core_technologies.md`
- Process review has run (`references/review/process_review.md`)
- Conclusion review has run (`references/review/conclusion_review.md`)

If any pre-condition is missing, the gate cannot start. State which
pre-condition is missing and stop.

## Checklist (every item required, evidence cited)

Format: `[ ] item — required evidence — citation`

### A. Charter integrity

- [ ] Charter exists, frozen, hash matches `prereg/charter.lock`
  - Evidence: `prereg/charter.lock` SHA-256 == sha256sum of `charter.md`
- [ ] No undocumented load-bearing charter amendments (scope, kill criteria,
  H7, H8, consumer, or promotion language)
  - Evidence: charter lock / git history reviewed against deviation entries;
    formatting-only changes do not count as amendments
- [ ] Charter H8 final exam criteria are met (cite the actual
  observation against the H8 criteria)
  - Evidence: per-criterion observation in this gate's review notes

### B. Layer 1 (core technologies) all `established`

- [ ] Every K row in Section 1 has status `established` (not active,
  blocked, parked, etc.) OR is `merged` / `stale` / `killed` with
  documented rationale
  - Evidence: list each K row with its terminal status and rationale
- [ ] Every `established` K satisfies its definition: all child
  capabilities matured, kill criteria un-fired, A4+ analysis
  - Evidence: per-K cross-reference to capabilities and kill log

### C. Layer 2 (capabilities) — per-capability conditions

For each capability on the critical path (i.e., not killed / merged /
stale), all of the following:

- [ ] `current_TRL == target_TRL` (typically 6)
  - Evidence: `capability_map.md` Section 2 row
- [ ] Status is `matured`
  - Evidence: same row
- [ ] Stage 5 (Integrate) exit conditions met (operational test on
  representative workload, cost within charter H7 budget)
  - Evidence: trial notebook ID + headline metric + cost measurement
- [ ] Kill criterion explicitly checked and un-fired (cite kill criterion
  ID + observation that confirmed un-fired)
  - Evidence: capability row's `kill_criteria` field + the observation
    proving it didn't fire
- [ ] Analysis depth at A4 minimum (A5 strongly preferred)
  - Evidence: trial notebook's Analysis section, with the 5 required
    sub-fields (Observation, Decomposition, Evidence weighing, Tier
    rating, Gap to next tier) all filled
- [ ] No generic terminal labels in the capability's success or failure
  explanation ("model is good" / "regime suited" / "data was clean"
  patterns are blocked per `references/shared/result_analysis.md`)
  - Evidence: explicit decomposition of any explanatory phrase
- [ ] Reproducibility 3-tuple recorded: data hash, git commit hash,
  uv.lock hash
  - Evidence: `scripts/reproducibility_stamp.py` output for the trial

### D. Integration test ordering

- [ ] Integration test (the capability with `core_tech_id == integration`)
  ran AFTER all upstream capability `matured` timestamps
  - Evidence: timestamp comparison from `decisions.md` session entries
    or trial timestamps
- [ ] No upstream capability re-opened during integration (no
  `matured → active` transitions in the integration window)
  - Evidence: `capability_map.md` git history during integration period

### E. Cross-project dependencies

- [ ] Every capability with `dependent_on_research` set has the named
  Pure Research project's claim at the required tier or higher
  - Evidence: cross-reference to the named project's
    `explanation_ledger.md` claim status

### F. Charter-level kill criteria

- [ ] Every charter H6 kill criterion explicitly checked and un-fired
  - Evidence: per-criterion observation against threshold

### G. Maintenance plan (conditional)

If any K is `継続改善型`, the closing `decisions.md` entry must include a
right-sized maintenance plan. If all K's are `永続型`, this section is N/A.
Production, external, or deployment-adjacent claims require all fields below.
Internal prototypes may record cadence or trigger, owner role, baseline
snapshot, and next review point.

- [ ] **Per-K plan**: For each `継続改善型` K, a separate maintenance
  plan block
- [ ] **Cadence**: Re-evaluation frequency (e.g., monthly, quarterly,
  on-demand-with-trigger)
- [ ] **Trigger condition**: Specific observable that prompts re-tuning
  (e.g., "rolling 3-month IC < baseline IC × 0.5 for ≥ 2 consecutive
  periods", or "foundation model new release in HuggingFace")
- [ ] **Owner**: Named person or role responsible for the
  re-evaluation
- [ ] **Baseline metric snapshot**: Headline metrics at promotion time,
  so drift is measurable (e.g., "Sharpe 1.2, ECE 0.07, IC 0.05 on
  2024-Q4 OOS evaluation")
- [ ] **Re-investment scope**: What fraction of the original work would
  be re-done if the trigger fires (re-tune only / re-fine-tune /
  re-architect)

#### Maintenance plan template

```markdown
## YYYY-MM-DD project promotion — maintenance plan

For each `継続改善型` core technology:

### K<id>: <core tech name>

- **Cadence**: <frequency>
- **Trigger**: <specific observable + threshold>
- **Owner**: <person or role>
- **Baseline metrics (at promotion)**:
  - <metric 1>: <value>
  - <metric 2>: <value>
- **Re-investment scope**: <what gets redone on trigger fire>
- **Next scheduled check**: <date>
```

### H. Reproducibility (project-wide)

- [ ] `reproducibility/data_hashes.txt` lists every data source used in
  trials, with hash
- [ ] `reproducibility/uv.lock` exists and is the env used at promotion
- [ ] `reproducibility/seed.txt` lists random seeds; if multiple seeds
  used, all are recorded
- [ ] All shared infrastructure pins are recorded in
  `reproducibility/shared_pins.txt` per `references/rd/rd_workflow.md`

### I. Documentation

- [ ] Final `README.md` updated with current status, links to charter,
  Layer 1 / Layer 2 final state, and (if applicable) maintenance plan
  link
- [ ] All trial notebooks have completed Analysis sections (5 sub-fields
  each)
- [ ] `decisions.md` has chronological coverage from project start
  through promotion (no gaps > 4 weeks without an explicit "no
  progress" entry)

## Promotion language

When a project promotes, the closing entry uses one of two templates
depending on lifecycle composition:

### All `永続型` — fully completed

```markdown
## YYYY-MM-DD project promoted (fully completed)

Target: <H1 from charter>
Charter hash: <sha256 from prereg/charter.lock>
Final TRL: every critical-path capability at TRL-6 matured
Lifecycle composition: all <N> core technologies are 永続型

Promotion claim: <H1> has been established as a TRL-6 operational
prototype, demonstrated under <H8 final exam conditions>, with kill
criteria un-fired (evidence cited in promotion review notes).

Project is frozen. No ongoing maintenance. Future use of the
established capability does not require this project to be active.
```

### Any `継続改善型` — v1 + maintenance scheduled

```markdown
## YYYY-MM-DD project promoted v1 (maintenance scheduled)

Target: <H1 from charter>
Charter hash: <sha256 from prereg/charter.lock>
Final TRL: every critical-path capability at TRL-6 matured
Lifecycle composition: <X> 永続型 + <Y> 継続改善型

Promotion claim: <H1> has been established as a TRL-6 operational
prototype v1, demonstrated under <H8 final exam conditions>, with kill
criteria un-fired (evidence cited in promotion review notes).

Maintenance plan filed below for the <Y> 継続改善型 core technologies.
Project status transitions to "maintenance mode": next scheduled check
is <date>; trigger conditions documented per K.

Maintenance plan: <inline or link>
```

## Failure modes blocked by this gate

| Failure mode | Where caught |
|---|---|
| Promote on integration test alone, upstream caps still TRL-3 | Section C: per-capability TRL check |
| Promote with kill criterion not explicitly checked | Section C: kill un-fired evidence required |
| Promote with A1 or A2 analysis | Section C: A4 minimum |
| Promote with generic "model is good" explanation | Section C: no terminal labels |
| Promote without integration test ordering verified | Section D: timestamp check |
| Promote 継続改善型 project without maintenance plan | Section G: required if any 継続改善型 |
| Promote with stale Pure Research dependency | Section E: cross-project dep check |
| Promote with un-reproducible setup | Section H: 3-tuple recorded |
| Charter rewritten mid-project to fit results | Section A: deviation entry count check |

## Common failure modes during the gate

| Failure | Symptom | Fix |
|---|---|---|
| Skipping load-bearing items | "Mostly satisfies" or "obvious from context" | Each promotion-supporting item requires explicit citation; no aggregations |
| Citing other people's work as evidence | "We ran a similar test before" | Citation must be from this project's trials |
| Vague "Sharpe is good" without target H8 comparison | Lazy success claim | Compare against H8 final exam criteria explicitly |
| Skipping maintenance plan because "we'll get to it" | Promotion premature | Block; require plan first |
| Using narrative language as evidence ("clearly works") | Per `GUARDRAILS.md` G16 | Replace with numerical / structural / null-result evidence |

## Relationship to other references

- `references/rd/rd_charter.md` (charter integrity, H6, H7, H8)
- `references/rd/core_technologies.md` (Layer 1 closure, lifecycle,
  `established` definition)
- `references/rd/capability_map_schema.md` (kill criteria, dependent_on_research,
  `matured` definition)
- `references/rd/trl_scale.md` (TRL-6 evidence requirements)
- `references/shared/analysis_depth.md` (A4 requirements)
- `references/shared/result_analysis.md` (terminal label prohibition)
- `references/review/process_review.md` (process audit, must run before
  this gate)
- `references/review/conclusion_review.md` (conclusion audit, must run
  before this gate)
- `references/shared/reproducibility.md` (3-tuple specification)
