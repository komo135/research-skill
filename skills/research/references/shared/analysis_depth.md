# analysis_depth.md

The A0-A5 analysis depth tier system. Read before claim-bearing interpretation
in either Capability / Technology Research or Phenomenon / Mechanism Research
workstreams. The tier is the primary deliverable axis of this skill.

## When to read

- Before writing any Analysis section in a trial notebook
- Before promoting an R&D capability to `matured` or a Pure Research
  claim to `supported`
- Before reviewing another agent's promotion claim
- When stuck on whether the current analysis is "deep enough"

## The principle

**Fact collection is not enough for a strong research claim.** A0-A3 can be
valid exploratory or diagnostic progress. A4 (estimation) and A5 (assertion)
are reserved for load-bearing claims and promotion-grade decisions.

A `supported` / `matured` promotion requires the analysis to reach
**A4 minimum**. "It worked" and "it failed" are both A0, not results.
This applies symmetrically to success and failure.

## The tier scale

| Tier | Meaning | Typical artifact |
|---|---|---|
| **A0** | Observation only — facts collected, no interpretation | "primary metric was 1.2 on 2018-2022 data." |
| **A1** | Hypothesized explanation named, no evidence | "Momentum effect explains it." |
| **A2** | ≥1 competing explanation identified | "Could be momentum or institutional flow." |
| **A3** | Discriminating evidence between primary and ≥1 alternative (preliminary) | "Test X distinguishes momentum from flow; observation supports momentum but flow not fully ruled out." |
| **A4** | **Estimation level** — mechanism named, alternatives excluded, scope precise, multiple sources of supporting evidence | "Mechanism M operates; alternatives X, Y excluded by tests T1, T2; scope is universe U / period P; evidence from sources S1, S2." |
| **A5** | **Assertion level** — mechanism causal, alternatives systematically excluded, replicable across instruments and periods, external prediction holds | "Mechanism M; replicated on instruments I1, I2, I3 and periods P1, P2; out-of-sample prediction X tested and held; falsifying alternatives Y, Z each had specific predictions that failed." |

### Promotion thresholds

- `A0-A2`: observation stage; not sufficient for any promotion claim, but
  enough for many exploratory notes and next-test choices
- `A3`: **preliminary**; can mark explanation `weakened` or capability
  Stage 3 (Build) exit, choose provisional go / no-go, park, deprioritize, or
  reject-for-now, but not promotion
- `A4`: **estimation level**; minimum for `matured` (R&D) or
  `supported` (Pure Research) promotion
- `A5`: **assertion level**; ideal for `supported` promotion of
  high-stakes findings (deployment, paper publication, line-closing
  decisions)

## Symmetric application: success AND failure

The tier system applies equally to positive findings and negative
findings. **A success with A1 analysis is not a result; a failure with
A1 analysis is not a result either.**

Common failure mode: agents apply rigor to failure analysis ("why did
the test fail?") but skim over success analysis ("it worked, ship
it"). The skill enforces symmetry — see
`references/shared/result_analysis.md` for decomposition patterns on
both sides.

## How to advance one tier

### A0 → A1

State a hypothesized explanation. The explanation must be a specific
mechanism, not a vague label.

- Bad (still A0): "There's a positive primary metric."
- Good (A1): "primary metric is positive because the strategy exploits the
  end-of-month rebalancing flow into large-cap names, which creates
  predictable buying pressure on the last 2 operational days."

### A1 → A2

Identify **at least one competing explanation** that could also
account for the observation.

- Bad (still A1): "The mechanism is end-of-month rebalancing flow."
- Good (A2): "Two candidates: (a) end-of-month rebalancing flow, or
  (b) sample-period bias — the test window happens to overlap a
  period of high index inflows."

### A2 → A3

Run a **discriminating test** that distinguishes the primary from
≥1 alternative. The test's result must change the relative weight of
the candidates.

- Bad (still A2): "We considered both; we think (a) is more likely."
- Good (A3): "Test: compare primary metric on last-2-day windows in
  high-inflow periods vs low-inflow periods. If (b) sample-period
  bias drives it, primary metric should be near zero in low-inflow periods.
  Observed: primary metric positive (0.8) even in low-inflow periods,
  weakening (b)."

### A3 → A4

- **Mechanism named** with a specific causal chain
- **Alternatives excluded** with at least one strong test per
  alternative
- **Scope precise** (universe, period, market structure preconditions)
- **Multiple sources** of supporting evidence (≥2 independent
  observations or evidence types)

- Bad (still A3): "The discriminating test supports mechanism M; we
  now believe M is the explanation."
- Good (A4): "Mechanism M (end-of-month rebalancing flow): supported
  by (i) cross-sectional test in low-inflow periods (primary metric 0.8); (ii)
  intraday volume signature on last-2-day windows showing 30%
  above-baseline volume in eligible names; (iii) literature
  reference (Author Year). Alternatives: (b) sample-period bias —
  excluded by (i); (c) coincidence with earnings season — excluded
  by re-run after removing earnings windows (primary metric 0.7). Scope:
  US large-cap, 2010-2024, monthly rebalancing instruments."

### A4 → A5

- **Mechanism remains causal under additional sources** (replicated
  across instruments, periods, OOS data)
- **External prediction made and tested**: a prediction the mechanism
  implies, tested on data that did not enter the original analysis
- **Falsifying alternatives have each been given specific predictions
  that failed**

- Good (A5): "Mechanism M holds across (i) dataset A, (ii)
  dataset B, (iii) dataset C — primary metric within ±0.2 on each.
  Out-of-sample prediction: M implies that during 2025
  (data not in original analysis), primary metric on held-out cohort D
  should be > 0.5; observed 2025-H1 = 0.6, holds.
  Falsifying alternative: 'M decays after broad institutional
  awareness post-2024' implied 2025-H1 primary metric < 0.3; rejected by
  the 0.6 observation."

## Required Analysis section structure

Every trial notebook (R&D and Pure Research) has an Analysis section
with these 5 sub-fields. See `assets/rd/rd_trial.py.template` § 5 and
`assets/pure_research/pr_trial.py.template` § 6.

### 5.1 Observation

Facts only, past tense. No interpretation. Quote the actual numbers
with uncertainty bands.

### 5.2 Decomposition

≥3 candidate explanations for the observation. For Pure Research, the
pre-registered E's go here plus any post-hoc candidates (clearly
flagged as not-pre-registered).

### 5.3 Evidence weighing

For each candidate, list supporting and weakening evidence with
**evidence type**:

- `numerical`: a measured number with uncertainty
- `structural-argument`: a logical / mathematical argument from the
  setup
- `literature-reference`: a citation to prior work that supports the
  mechanism
- `null-result-of-X`: an alternative that was tested and failed

**Constraint**: structural-argument alone cannot support an A4 claim.
At least one numerical evidence is required. (Per GUARDRAILS G16:
narrative is not evidence.)

### 5.4 Tier rating

State the current tier (A0–A5) and **why this tier and not the next**.
The "why not next" forces honest assessment.

### 5.5 Gap to next tier

If A4 not yet reached: name the specific evidence or test that would
advance the tier. If A4 reached and goal is A5: name the
multi-instrument / multi-period / OOS / external-prediction work.

## Push depth before designing new trials

A core principle from `references/pure_research/pr_workflow.md` and
`references/rd/rd_stages.md`: **before a promotion, external claim, or terminal
decision, push the current trial's analysis depth as far as it can go**.

Often the current data supports A2 → A3 → A4 transitions via:
- Feature ablation
- Sub-period or sub-universe breakdown
- Regime-conditional split
- Alternative metric on the same data

These extensions stay within the current trial (no new pre-registration
needed for Pure Research). New trials are justified when the current trial has
hit its analysis ceiling, when the next discriminating question requires a
different test design, or when the work is still exploratory and A2-A3 evidence
is enough to choose the next useful probe.

This avoids the failure mode of accumulating shallow trials at A2 when
each could have reached A3 or A4 with more analysis on existing data.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Stop at A0 | "primary metric was 1.2." (no interpretation) | Force § 5.1 → 5.2 → ... transition; an Analysis section with only § 5.1 is incomplete |
| Stop at A1 | Single explanation, no alternatives | Force § 5.2 to list ≥3 candidates |
| Confuse A3 with A4 | "Discriminating test passed, so we have estimation-level analysis" | A3 = preliminary; A4 needs ≥2 evidence sources, scope precision, alternatives excluded, mechanism named |
| Confuse A4 with A5 | Strong A4 case for one universe is claimed as A5 | A5 needs replication across instruments/periods AND external prediction held |
| Generic terminal labels | "noise / regime / cost / model is good" | Per `references/shared/result_analysis.md`, decompose into mechanism-level claims |
| Skip evidence type | Evidence weighing without categorizing each as numerical / structural / literature / null | Force the type column; structural-only cannot support A4 |
| Promote with A2 | Promotion claim made when analysis is still A2 | Promotion gate (`rd_promotion_gate.md` / `pr_promotion_gate.md`) requires A4 minimum |

## Relationship to other references

- This file is referenced by virtually every Phase 2/3 reference and
  by the Phase 4 review files
- `references/shared/result_analysis.md` — decomposition patterns for
  failure AND success, generic terminal label prohibition
- `references/rd/rd_stages.md` — per-stage analysis depth requirements
  (Scoping=A0, De-risk=A2, Build=A3, Validate=A4, Integrate=A4+)
- `references/rd/rd_promotion_gate.md` § Section C — A4+ for `matured`
- `references/pure_research/pr_workflow.md` § Push analysis depth
  before designing a new trial
- `references/pure_research/pr_promotion_gate.md` § Section E — A4+
  for `supported`
- `references/pure_research/imrad_draft.md` § 4 Discussion — A4+
  required for the Discussion section
- `references/review/conclusion_review.md` — analysis depth is one of
  the 6 axes
- CHARTER C13 — "Analysis depth is the first-class research artifact"
