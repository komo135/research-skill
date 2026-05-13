# trl_scale.md

Technology Readiness Level — capability maturity scale, NASA-derived,
adapted to agent-driven research. TRL-6 (operational prototype) is the
**promotion line** for this skill; TRL-7+ is engineering hand-off and
outside scope.

## When to read

- Assigning the current TRL to a capability in `capability_map.md`
- Deciding whether a Stage gate's exit conditions advance the TRL
- Reviewing whether a promotion claim is supported by the right TRL
- Resolving "is this TRL-N or TRL-N+1?" disputes

## Why TRL exists

A target capability is reached by maturing many smaller capabilities. TRL
gives a **shared yardstick** so:

- Different capabilities can be compared by maturity
- Promotion conditions can be stated as "all critical-path caps at TRL ≥ N"
- Premature claims of completeness ("we ran the integration test, ship it")
  are caught — integration alone does not move every upstream capability
  to TRL-6.

## The scale (TRL-0 to TRL-6)

For each level: **meaning** + **exit evidence required to advance** + the
**typical agent action** at that level.

### TRL-0 — Named only

**Meaning**: The capability has been listed in `capability_map.md` with a
parent `core_tech_id`, but boundary, dependencies, and tests are not yet
specified.

**Exit evidence (to TRL-1)**:
- Capability statement is one sentence
- `core_tech_id` is set
- `depends_on` list is filled (may be empty)
- `exit_criteria` and `kill_criteria` drafted

**Typical agent action**: Scoping work. No implementation yet.

### TRL-1 — Principle / rationale exists

**Meaning**: There is a first-principles argument or prior-work citation
that the capability is achievable in principle. No code, no demo.

**Exit evidence (to TRL-2)**:
- A literature reference (linked to `literature/papers.md`) OR a
  first-principles argument written in `decisions.md`
- An explicit claim about which sub-question of the parent core tech this
  capability advances

**Typical agent action**: Literature lookup or theoretical sketch.

### TRL-2 — Toy proof of concept

**Meaning**: The capability is demonstrated on **synthetic** or **toy**
data designed to exhibit the property the capability is supposed to have.
No real-data evaluation, no realistic environment.

**Exit evidence (to TRL-3)**:
- A runnable script / notebook / test that exercises the capability on
  synthetic input
- The synthetic test produces the expected behavior, with the
  observation logged
- Failure modes on the synthetic data are noted

**Typical agent action**: Smallest implementation that demonstrates the
isolated property.

### TRL-3 — Critical function demonstrated on real data

**Meaning**: The capability's critical function works on **at least one
real-data sample** (single instrument, short period, simplified
environment). Edge cases not yet handled.

**Exit evidence (to TRL-4)**:
- A real-data test that isolates the critical function (other concerns
  controlled or stubbed)
- Verification checks pass on this real-data test (relevant subset of
  generic verification or domain-adapter implementation checks)
- Analysis depth at least A2 (competing explanation considered)

**Typical agent action**: First real-data trial. This is often the
de-risk gate's deliverable in Stage-Gate.

### TRL-4 — Component validated with realistic inputs

**Meaning**: The capability works on representative real-data inputs and
known failure modes are understood. Sample size sufficient for variance
to be measurable.

**Exit evidence (to TRL-5)**:
- Multi-instrument or multi-period evaluation
- Documented failure modes (`references/shared/result_analysis.md`
  decomposition)
- Robustness checks relevant to this capability run
- Analysis depth at least A3 (discriminating evidence vs ≥1 alternative)

**Typical agent action**: Build out the capability to handle real-data
edge cases.

### TRL-5 — Integrated prototype

**Meaning**: The capability operates within the larger pipeline
(neighboring components present), without breaking shared assumptions.
Interfaces are stable.

**Exit evidence (to TRL-6)**:
- The capability has been called by at least one consumer (another
  capability or the integration harness) without bespoke shims
- Interface specification is documented and stable
- No regressions in upstream capabilities caused by this one

**Typical agent action**: Validate stage. Wire up to neighbors.

### TRL-6 — Operational prototype

**Meaning**: The capability is demonstrated under representative workload,
data, and cost constraints. This is the **promotion line**: from this
point, the capability is considered "matured" and ready for upstream
consumption (or, at the project level, ready for promotion review).

**Exit evidence (to be marked `matured`)**:
- Operational test on representative workload (not toy size, not picked
  best-case) — sample size adequate for sub-period or regime breakdown
- Cost (compute, latency, memory) measured and within charter H7 budget
- Analysis depth at A4 minimum (mechanism named, alternatives excluded,
  scope precise)
- Kill criteria explicitly checked and un-fired (cite the kill criterion
  ID and the evidence)
- Reproducibility 3-tuple (data version + git commit + environment pin) recorded
  via the selected tracking backend or local run note

**Typical agent action**: Final validation under realistic load. Trigger
the capability's row to transition `active → matured` in
`capability_map.md`.

## Why TRL stops at 6 in this skill

TRL-7 (system prototype demonstration in operational environment), TRL-8
(actual system completed), and TRL-9 (actual system proven through
operations) belong to engineering / production hand-off. Once a capability
is at TRL-6, the research question is answered. Whether to deploy it,
operate it, monitor it in production, etc., is outside this skill's scope.

If the user explicitly requests engineering hand-off, treat that as a
separate (non-research) project and do not expand this scale.

## TRL skip is forbidden

A capability advances **one TRL at a time**. Strong evidence that a
capability "would obviously" jump from TRL-1 to TRL-3 or from TRL-2 to
TRL-5 is a red flag —
either:

- The intermediate evidence is being skipped (which means the test was
  insufficient), or
- The capability was originally over-decomposed and the TRL-2 → TRL-5
  trajectory is actually a single-test capability (in which case file a
  deviation entry, merge or restructure).

The schema checker catches this: any single
transition that advances TRL by > 1 in one row update is flagged.

In Stage-Gate terms, De-risk establishes the synthetic proof needed for
TRL-2. Build starts with the real-data proof that advances TRL-2 to TRL-3,
then records representative-input evidence for TRL-3 to TRL-4 as a separate
update if the evidence exists.

## TRL is per-capability, not per-project

target_TRL is the per-capability row target. It controls when a row may be
marked `matured`, but it is not the same as the workstream promotion line.
target_TRL below 6 is for non-critical or helper capabilities.
target_TRL below 6 does not satisfy critical-path promotion.

The project does not have a single TRL. Promotion of the **target
capability** (i.e., the project) requires:

- Critical-path capabilities must reach TRL-6 for workstream promotion
- The declared integration pattern's pattern-aware ordering check passed
  (Pattern 1, Pattern 2, or Pattern 3)

A "TRL-6 integration test" alone does not promote upstream capabilities
that are still at TRL-3. A favorable integration test in such a state is
**preliminary screening**, not promotion.

## TRL vs analysis depth (Axx)

TRL and analysis depth (`A0`–`A5`) are **independent axes**:

| | TRL low | TRL high |
|---|---|---|
| **A low** | Toy demo, no understanding | Operational system, no understanding (BAD — hidden risk) |
| **A high** | Toy demo, deep understanding | Operational system + deep understanding (the goal) |

A critical-path capability at TRL-5 with A1 analysis is not ready for
workstream promotion: target_TRL is 6 on the critical path, and that exit
requires A4 minimum. A non-critical/helper capability reaches `matured` at its
declared target_TRL, still with A4+ analysis and kill criteria un-fired.
Conversely, A4 analysis on a TRL-2 capability does not move it to TRL-3 — TRL
requires demonstration evidence, not just analysis.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| TRL inflation | "We ran one real-data test, it's TRL-5" | Re-read TRL definitions; demonstrate one level at a time |
| Skipping TRL-3 | Going from synthetic toy (TRL-2) directly to multi-instrument (TRL-4) | The single-real-data test (TRL-3) is exactly where leak / sign / alignment bugs surface; do not skip |
| TRL of project as a whole | "The project is at TRL-4" | TRL is per-capability; a project has a distribution of TRLs |
| "We ran the integration test" = TRL-6 | One favorable integration result | Integration evidence is one piece of maturity evidence. Critical-path caps independently need TRL-6 demonstration; helper/non-critical caps need their declared target_TRL evidence and cannot satisfy the workstream promotion line. |
| TRL skip via rhetoric | "Obviously TRL-X follows from this" | Forbidden; every transition needs concrete exit evidence |

## Relationship to other references

- TRL transitions are the **exit conditions** of the Stages in
  `references/rd/rd_stages.md` (Scoping → TRL-0/1,
  De-risk → TRL-2, Build / real-data proof → TRL-3, representative
  Build evidence → TRL-4, Validate → TRL-5, Integrate → TRL-6).
- For critical-path capabilities, TRL-6 + analysis A4+ + kill un-fired is
  required by `references/rd/rd_promotion_gate.md`. For non-critical/helper
  rows, `current_TRL == target_TRL` + analysis A4+ + kill un-fired is enough
  for row maturity but not for workstream promotion.
- See `references/shared/analysis_depth.md` for the A-tier orthogonal
  axis.
