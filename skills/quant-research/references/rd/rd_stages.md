# rd_stages.md

Cooper-style 5-stage progression for each capability, with Go / Kill /
Hold / Recycle decisions between stages. Each gate is an evidence-based
investment decision: pass to the next stage, terminate with A4+ evidence,
hold for missing evidence, or recycle / re-scope the work when the design
is wrong.

## When to read

- About to start work on a specific capability
- About to advance a capability past a Stage gate
- A capability stalled mid-stage and needs evaluation
- A new core tech was discovered mid-stage (rollback)

## Pre-condition: integration pattern declared

Before applying the 5 stages, the project must have declared its
integration pattern in the charter (Heilmeier H8, see
`references/rd/integration_patterns.md`). The Stage-Gate ordering and
the meaning of Stage 5 (Integrate) differ per pattern:

- **Pattern 1 (vertical slice)**: framework + baselines built before any
  K Stage-Gate. Per K, Stage 5 (Integrate) = baseline replacement +
  A/B vs baseline. No final integration capability — integration is
  continuous.
- **Pattern 2 (bottom-up)**: K Stage-Gate runs in isolation per K.
  Stage 5 = integration with stub upstream/downstream. A separate
  `core_tech_id == integration` capability runs after all K's matured.
- **Pattern 3 (skeleton + spike, default)**: skeleton built before any
  K Stage-Gate. Per K, Stage 5 = skeleton component replacement +
  A/B vs skeleton. Optional final integration capability for end-to-end
  evaluation under realistic conditions.

See `references/rd/integration_patterns.md` for full detail. The 5 stages
themselves (below) are pattern-agnostic; only the integration step
(Stage 5) and the existence of a final integration capability differ.

## The 5 stages

For each capability, work flows through five stages. Each stage gathers
evidence for a TRL claim (see `references/rd/trl_scale.md`) AND requires a
minimum analysis depth (see `references/shared/analysis_depth.md`):

| Stage | TRL transition | Analysis depth required |
|---|---|---|
| 1. Scoping | 0 → 1 | A0 (observation only — no test yet) |
| 2. De-risk | 1 → 3 | **A2 minimum** (≥1 competing explanation) |
| 3. Build | 3 → 4 | **A3 minimum** (discriminating evidence vs alternative) |
| 4. Validate | 4 → 5 | **A4 minimum** (mechanism named, alternatives excluded, scope precise) |
| 5. Integrate | 5 → 6 | **A4 minimum** (A5 strongly preferred for `matured`) |

Both axes (TRL + analysis tier) must be justified by evidence. Promotion to
`matured` requires TRL-6 AND A4+. A capability at TRL-5 with A2 analysis is
not ready for the next gate, even if the operational test technically
succeeded.

```
Scoping  ──Gate 1──  De-risk  ──Gate 2──  Build  ──Gate 3──  Validate  ──Gate 4──  Integrate  ──Gate 5──  matured
TRL 0→1, A0           TRL 1→3, A2          TRL 3→4, A3        TRL 4→5, A4              TRL 5→6, A4+
```

### Stage 1 — Scoping

**Purpose**: Define the capability precisely and surface the hardest
sub-question.

**Entry condition**: Layer 1 (core technologies) is closed; the
capability's `core_tech_id` exists in Section 1.

**Work**:
- Write capability statement (1 sentence, no jargon)
- Identify dependencies (`depends_on`, `dependent_on_research`)
- Draft `exit_criteria` (1 concrete observable that advances TRL)
- Draft `kill_criteria` (1 concrete observable that kills, A4-anchored
  per `references/rd/capability_map_schema.md`)
- Identify `blocking_uncertainty` (the single biggest unknown)
- Identify the **hardest sub-question** of this capability (the
  sub-question whose failure would invalidate the whole capability)

**Exit (Gate 1)**:
- Capability row complete in `capability_map.md` Section 2
- Hardest sub-question written and is the focus of Stage 2 (De-risk)
- Exit and kill criteria both pass the "concrete observable" test
- TRL advances 0 → 1

**Recycle or re-scope at Gate 1 if**:
- The capability has no concrete exit criterion
- The hardest sub-question is "everything"
- The capability is actually a task (not a research-worthy unit)

These are scoping failures, not evidence that the underlying research target
is false. Move the row to a task, split it, or rewrite it before running
evidence-producing work.

### Stage 2 — De-risk (hardest part first)

**Purpose**: Run the smallest test that resolves the hardest sub-question
identified in Scoping. Designed to **kill the capability if the hardest
question fails**, not to confirm a hypothesis.

**Entry condition**: Gate 1 passed.

**Work**:
- Design the smallest test that distinguishes "hardest sub-question
  works" from "hardest sub-question fails"
- Build the minimum implementation to run that test
- Run the test on synthetic data (TRL-2) and then on a single real-data
  sample (TRL-3)
- Run sanity checks relevant to this test (`references/shared/sanity_checks.md`)
- Decompose the result with at least A2 analysis (≥1 competing
  explanation considered)

**Exit (Gate 2)**:
- Hardest-sub-question test passed: produces the expected behavior
- Sanity checks pass
- Analysis at A2 minimum, A3 for `matured` track
- Kill criterion not fired
- TRL advances 1 → 3

**Kill at Gate 2 if** (this is the most common kill point):
- Hardest-sub-question test fails AND the failure is mechanism-level
  (A4-decomposed: not a config bug, not a data issue, the technology
  itself doesn't work for this target)
- Sanity check fails in a way that invalidates the test design (e.g.,
  random-signal benchmark passes — meaning the evaluator is leaking and
  no result is meaningful)
- Kill criterion fires with A4 evidence

**Why de-risk first**: Stage-Gate's central principle. A capability that
fails its hardest test should be killed before Build investment. Building
out a capability and discovering at Validate stage that the core
sub-question never worked is the failure mode this stage prevents.

### Stage 3 — Build

**Purpose**: Build out the capability to handle real-data edge cases and
known failure modes.

**Entry condition**: Gate 2 passed (hardest sub-question is answered).

**Work**:
- Extend implementation to handle multi-instrument or multi-period data
- Document and handle known failure modes (`references/shared/result_analysis.md`
  decomposition pattern)
- Run robustness checks relevant to this capability
- Push analysis to A3 (discriminating evidence vs alternatives)

**Exit (Gate 3)**:
- Capability works on representative real-data inputs
- Failure modes documented (with mechanism, not generic labels)
- Sanity checks pass
- Analysis at A3 minimum
- Kill criterion not fired
- TRL advances 3 → 4

**Hold, re-scope, or kill at Gate 3 if**:
- Real-data edge cases reveal that the technology has a fundamental
  limitation that wasn't visible in the de-risk test
- Required robustness check (e.g., regime-conditional Sharpe) shows the
  capability works only in a degenerate regime
- Cost (compute / data / wall-clock) exceeds charter H7 budget by > 2x

Cost or robustness problems are terminal only when A4 analysis shows the
failure is intrinsic to the capability under the chartered scope. Otherwise
file `Hold` for missing evidence or `Recycle` for a narrower scope /
alternate implementation.

### Stage 4 — Validate

**Purpose**: Confirm the capability operates within the larger pipeline
without breaking shared assumptions.

**Entry condition**: Gate 3 passed.

**Work**:
- Wire the capability to its consumer (another capability or the
  integration harness)
- Verify upstream and downstream interfaces are stable
- Confirm no regressions in neighboring capabilities
- Push analysis to A4 (mechanism named, alternatives excluded, scope
  precise)

**Exit (Gate 4)**:
- The capability is consumed by at least one other component without
  bespoke shims
- Interface specification documented in `decisions.md`
- No regressions in upstream capabilities (re-run their sanity checks)
- Analysis at A4
- TRL advances 4 → 5

**Kill at Gate 4 if**:
- Integration with neighbors requires assumptions the capability cannot
  honor
- Validate stage exposes A4 analysis that contradicts earlier A3 claims

### Stage 5 — Integrate

**Purpose** (varies by integration pattern):

- **Pattern 1**: replace the K's baseline implementation in the framework
  with the K_real implementation; A/B vs baseline meets criteria
- **Pattern 2**: run the K under stub upstream/downstream environment
  representing realistic conditions; final integration capability is a
  separate Stage-Gate cycle later
- **Pattern 3**: replace the K's skeleton component with K_real
  implementation; A/B vs skeleton meets criteria

In all patterns: demonstrate the K under representative workload.

**Entry condition**: Gate 4 passed.

**Work** (pattern-specific portions noted):
- Run the capability on representative workload (not toy size, not
  cherry-picked)
- (Pattern 1 / 3) Replace baseline / skeleton component with K_real;
  measure A/B delta vs baseline / skeleton
- (Pattern 2) Wire K with stub upstream/downstream representing realistic
  data flow; measure under realistic conditions
- Measure cost (compute, latency, memory) against charter H7 budget
- Confirm kill criteria un-fired
- Record reproducibility 3-tuple via `scripts/reproducibility_stamp.py`
- Final A4+ analysis

**Exit (Gate 5)**:
- Operational test on representative workload completes
- Cost within charter H7 budget
- Kill criteria explicitly checked and un-fired (cite kill criterion ID
  + observation)
- Reproducibility 3-tuple recorded
- Analysis at A4 minimum (A5 strongly preferred for `matured`)
- TRL advances 5 → 6 → status `matured`

**Hold, re-scope, or kill at Gate 5 if**:
- Operational performance fails to meet charter H8 final exam criteria
- Cost exceeds charter H7 budget at scale
- A previously un-fired kill criterion now fires under realistic load

Kill requires A4+ evidence that the miss is not a repairable implementation,
configuration, data, or scope problem.

## Gate decision protocol

At each gate, the decision is one of three:

- **Go**: All exit conditions met; advance to next stage.
- **Kill**: Kill criterion fired (with A4 evidence) or this stage's exit
  conditions cannot be met for intrinsic, non-repairable reasons. Mark
  capability `killed` in `capability_map.md`. Append A4 analysis to the
  kill log in `decisions.md`.
- **Hold**: Need more information; do not advance, do not kill. Specify
  what new evidence is needed and why current evidence is insufficient.
  Logged in `decisions.md`.
- **Recycle / Re-scope**: The capability, test design, threshold, dependency
  path, or implementation frame is wrong. Rewrite the relevant row, split the
  capability, move it to a task, or narrow the scope before retrying.

The asymmetry: **Default to Hold or Recycle under uncertainty**. Kill is a
terminal decision, not a synonym for doubt. Holding is acceptable but must
name the specific blocker, not be a soft "let's wait and see"; recycling is
acceptable when the work should continue under a corrected design.

## Hardest-part-first principle

In Scoping (Stage 1), explicitly identify which sub-question of the
capability is hardest. The de-risk stage (Stage 2) is built around
that sub-question. The reason: **find the kill, don't avoid it**.

### Identifying the hardest sub-question (rubric)

For each candidate sub-question, score it on two axes:

1. **Kill probability**: If this sub-question fails, how likely is it
   to fire a charter H6 kill criterion or this capability's
   `kill_criteria`? (high / medium / low)
2. **Evidence cost**: How much infrastructure / data / time is needed
   to test this sub-question with reasonable A2-A3 analysis?
   (high / medium / low)

The **hardest** sub-question is the one with **highest kill probability**
(if it fails, the project is in serious trouble). Among candidates with
similar kill probability, prefer the one with **higher evidence cost**
(getting it out of the way earlier prevents expensive sunk cost).

If kill probability is low for all sub-questions, the capability may not
need a separate de-risk stage — it can proceed straight from Scoping to
Build. Document this decision in `decisions.md` if you skip de-risk.

If you build out the easy parts of a capability first (data loader,
visualization, etc.) and discover at Build stage that the hardest part
fails, you have built infrastructure with no consumer. That's the
investment-without-evidence pattern Stage-Gate prevents.

A common pattern: agents and humans both naturally tackle the easiest
part first because it produces visible progress. The skill explicitly
inverts this. The de-risk stage's success criterion is: **the hardest
sub-question now has an evidence-based answer, in either direction**.

## Rollback: new core tech discovered mid-stage

A Stage gate may surface a research question that was not in Layer 1.
For example, during Stage 2 (De-risk) of capability C3 under K2, the
agent realizes that the "best fine-tuning protocol" depends on a prior
question — "does the foundation model's pretraining distribution
generalize to financial time series?" — that is a separate research
question, not just a sub-task of K2.

When this happens:

1. **Suspend** the current Stage gate; do not declare Go/Kill/Hold yet.
2. **File a deviation entry in `decisions.md`** naming the discovered
   research question, the capability that surfaced it, and the Stage
   that was in progress.
3. **Add a new K row in Section 1** of `capability_map.md` per
   `references/rd/core_technologies.md` (re-run the operational filter).
4. **Re-close Layer 1** per `core_technologies.md` § Layer 1 closure.
5. **Re-evaluate the suspended capability** under the new Layer 1: it
   may need to be re-scoped, or split, or moved under the new K, or
   marked `blocked` until the new K's capabilities mature.
6. **Then resume the original Stage** under the updated state.

Rollback events are valuable, not failures: they catch under-decomposition.
A project with zero rollbacks across many stages may be over-confident
about its initial Layer 1; a project with rollback every other stage is
under-decomposing at the start. Some rollback is healthy.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Skip de-risk, build first | Stage 3 produces nice infrastructure, Stage 4 reveals the underlying technique doesn't work | Re-read § Hardest-part-first |
| Build before scoping | Capability row is `active` but has no `kill_criteria` | Block work; complete Stage 1 first |
| "Hold" with no specific blocker | Indecision | Specify blocker or convert to Kill |
| Stage gate run while Layer 1 incomplete | Sibling K not closed | Block per `SKILL.md` § Session-level R&D sequencing |
| TRL advances by > 1 in single gate | Skipping levels | Per `references/rd/trl_scale.md`: forbidden, re-evaluate evidence |
| Rollback ignored | Mid-stage discovery is suppressed because "we're committed" | Sunk cost bias; rollback is healthy, file the deviation |

## Relationship to other references

- Stages map to TRL transitions per `references/rd/trl_scale.md`
- Capability schema per `references/rd/capability_map_schema.md`
- Layer 1 closure check per `references/rd/core_technologies.md`
- Sanity checks per `references/shared/sanity_checks.md`
- Analysis depth A0-A5 per `references/shared/analysis_depth.md`
- Result decomposition per `references/shared/result_analysis.md`
- Kill > Promote asymmetry per `SKILL.md` § Guardrails
