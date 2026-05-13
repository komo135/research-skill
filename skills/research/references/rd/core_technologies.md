# core_technologies.md

R&D Layer 1 — intellectual decomposition. The minimal set of technologies
that require research investment to establish for the target capability.

## When to read

- Immediately after the charter is reviewed, before any capability is written
- Before adding a new candidate K-row to `capability_map.md`
- When a sibling K is split, merged, or marked stale

## Purpose

Capabilities (Layer 2) are operationally testable units. Core technologies
(Layer 1) are the **research questions** that justify why each capability
matters. Skipping Layer 1 produces capability lists that look organized but
have no anchor for kill decisions, no anchor for A4-tier analysis, and no
basis for promotion claims.

Layer 1 lives in `capability_map.md` as Section 1, above the capability
table.

## Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `ID` | `K1`, `K2`, ... | yes | Sequential, never reused |
| `core_technology` | string (1 phrase) | yes | Short name, no jargon if possible |
| `research_question` | string (1 sentence) | yes | The single research question this core tech needs answered |
| `target_contribution` | string | yes | Why this is needed for the target capability (cite charter H1) |
| `lifecycle` | `establish-once` \| `continuous-improvement` | yes | Lifecycle — see § Lifecycle below |
| `prior_research` | path / link | yes | Section reference into `literature/papers.md` (may be `(none, novel)`) |
| `Status` | enum | yes | See § Status transitions |

The 7-column table sits at the top of `capability_map.md`. See
`assets/rd/capability_map.md.template` for the rendered format.

## Operational filter

A candidate K is admitted only when **all four conditions** hold:

### Condition 0 — Merge test (catches sibling overlap)

Before listing a candidate, scan the existing K rows. If the candidate's
research question shares >50% conceptual overlap with an existing K's
question, do **not** create a new row. Either:

- Merge into the existing K (extend its question to cover both), or
- If the candidate is genuinely distinct, draft both questions side-by-side
  and confirm with Condition 2 that they are isolated.

This catches the failure mode where an agent lists "feature engineering",
"feature scaling", and "feature selection" as three separate K's when they
are facets of one research question ("how should features for THIS task be
constructed?").

### Condition 1 — Research investment required

The candidate requires research / establishment work specifically for
**this** target. If the technology can be obtained off-the-shelf (a
standard library, a published method applied without modification, a
standard validation technique), it is a **dependency**, not a core tech.

- A pre-existing purged k-fold implementation that just needs to be
  imported → dependency.
- Adapting purged k-fold to handle this target's specific
  overlapping-label structure (where existing implementations don't fit)
  → core tech.

### Condition 2 — Single isolated research question

The candidate must be expressible as **a single research question**, and
that question must be **isolated** — meaning, if you discovered tomorrow
that a sibling K's research question is unanswerable, would this K's
question still be meaningful and executable?

- If yes → isolated, candidate qualifies.
- If no → coupled, merge into the parent.

**Rejected exemplar (coupling)**: For an RL task agent project, a
candidate proposed "reward design" as one K and "action space design" as
another. But you cannot design a reward function until you know what
actions are available. They are coupled. Correct decomposition: one K
("RL architecture: state/action/reward co-design") with separate
capabilities for each sub-component.

### Condition 3 — Independent of other K questions

This is the strict version of Condition 2. Even if two questions can each
be stated standalone, they may share so much overlap in their evidence
sources or testing infrastructure that they should be merged.

If two K's can only be tested by the same single experiment (the same
test would advance both research questions), they are not independent —
merge them.

### What if a candidate fails the filter?

- Fails (1) → list it as a **dependency** (used as-is, no research, not
  in capability_map). Document in `decisions.md` if the dependency is
  non-obvious.
- Fails (2) — coupling → merge into the parent K.
- Fails (3) — overlap in evidence → merge with the overlapping K.
- Cannot write a research question for it → it is a **capability** (Layer
  2) or a **task**. Move it under an existing K in Section 2, or drop it
  if it is just a task.

## No count target

There is no "3-7 K's" target. Target difficulty determines the count
naturally.

If you find yourself with **only 1 candidate K**:

1. Re-read the charter (especially H1 and H3). Is the goal narrow?
   - Narrow: e.g., "prove algorithm X converges on problem Y for the first
     time" — 1 K may be sufficient.
   - Broad: e.g., "build an RL task agent" — 1 K means the filter is
     too loose, the candidate is too large.
2. If broad: enumerate sub-questions of the candidate and apply Conditions
   0-3 again. The single K likely splits into 2-4.
3. If still 1 after step 2: the goal may be Pure Research (answer a
   question) rather than R&D (build a capability). Confirm with the user
   before continuing under R&D.

If you find yourself with **20+ candidate K's**: the filter is too loose.
Most are dependencies (failing Condition 1) or capabilities (failing
"single research question"). Run the filter strictly.

## Lifecycle

Each K is classified by **lifecycle type**, which determines what
"established" means for this K and what the project owes the consumer
after promotion.

### establish-once

The core technology, once established at TRL-6, requires no further
investment. It can be used as-is indefinitely.

Examples:
- Embargo logic for purged k-fold (mathematical correctness, doesn't
  decay)
- A specific validation methodology proven on a representative dataset
- An optimization routine with proven convergence properties on the
  problem class
- A point-in-time data alignment library

Test for `establish-once`: would the technology still be valid 5 years from now
with no re-investment, assuming the surrounding environment doesn't
change in ways that change the underlying problem? If yes → `establish-once`.

### continuous-improvement

The core technology, once established at TRL-6, requires periodic
re-investment to maintain relevance, accuracy, or performance. The
re-investment is built into the project's expected lifecycle.

Examples:
- A regime classifier (market regimes shift; the classifier must be
  retrained on a schedule)
- A specific feature set or predictive signal (signal decays; signals need
  refresh)
- A foundation-model adaptation that must track new model releases
- Any model whose accuracy depends on current market structure

Test for `continuous-improvement`: would the technology degrade in usefulness
over time without active maintenance? If yes → `continuous-improvement`.

### Lifecycle decision tree (when in doubt)

When the binary classification is unclear, walk this tree:

```
Q1: Would the technology degrade in usefulness without active
    maintenance within 1 year?
    → YES: continuous-improvement
    → NO: continue to Q2

Q2: Does the technology depend on parameters that drift with market
    conditions, even if the underlying methodology is stable?
    → YES: continuous-improvement (the parameters are part of the technology;
       fitting once and shipping forever is wishful thinking when
       the world changes)
    → NO: continue to Q3

Q3: Look at charter H7. Is the recurring cost > 0 and does it involve
    re-tuning, re-training, re-validation of this specific tech?
    → YES: continuous-improvement (recurring cost is the operational signature
       of continuous improvement)
    → NO: establish-once

Q4 (sanity check): If you assigned `establish-once`, can you name the external
    conditions under which the technology remains valid without scheduled
    re-investment? If yes, record those assumptions and keep `establish-once`.
    If no, use `continuous-improvement`.
```

The parameter-vs-methodology distinction matters: an HMM regime
classifier's *methodology* (Viterbi decoding, EM training) is stable,
but its *fitted parameters* drift as market structure evolves. The
parameters are part of the deployed technology, so the K is
`continuous-improvement`.

In contrast, a numerical optimizer for solving a fixed-form mean-variance
problem has stable methodology AND stable parameters — `establish-once`.

### Project-level implications

The composition of lifecycles in a project's K's determines the project's
termination semantics:

- **All K's are `establish-once`** and all `established` → project is **fully
  completed**. Final entry in `decisions.md` notes the write down. No
  ongoing obligation.
- **Any K is `continuous-improvement`** → project completion = **"v1 established + maintenance plan scheduled"**. The closing entry in `decisions.md` must
  include a right-sized maintenance plan. For production or external claims,
  include cadence + trigger condition + owner + baseline metric snapshot (see
  `references/rd/rd_promotion_gate.md`). For internal prototypes, a trigger
  condition and next review point are sufficient.

## Status transitions

Each K row has one status at a time. Allowed values:

| Status | Meaning |
|---|---|
| `active` | Currently being worked on; child capabilities are in progress |
| `established` | Critical-path child capabilities matured to TRL-6; non-critical/helper child capabilities reached target_TRL or are explicitly non-critical; kill criteria un-fired; analysis at A4+ |
| `blocked` | Cannot progress until a named dependency changes |
| `split` | Decomposed into 2+ child K's (record children's IDs); the original row remains for traceability |
| `merged` | Absorbed into another K (record the absorbing K's ID) |
| `stale` | No longer relevant after a scope change or upstream decision |
| `parked` | Deferred with a named unblock condition |
| `killed` | Charter or K-level kill criterion fired with A4+ mechanism evidence, plus charter/decisions evidence showing terminal scope |

Allowed transitions:

```
active → established (when promotion conditions met)
active → blocked (when dependency named)
active → split (when too coarse, becomes parent of children)
active → merged (when duplicate found)
active → stale (when scope shifts)
active → parked (when deferred)
active → killed (when terminal kill is validated with A4+ evidence and recorded in charter/decisions evidence)
blocked → active (when blocker resolved)
parked → active (when unblock condition fires)
parked → stale (when no longer relevant)
```

Disallowed: `established → active` (promote-then-demote); `killed → active`
also requires a deviation entry plus a new K or explicit re-open rationale.

Core tech terminal kill requires A4+ mechanism-level analysis plus
charter/decisions evidence: cite the charter H6 or K-level kill criterion,
the observation that fired it, alternatives ruled out, scope of the kill, and
the dated `decisions.md` entry. If the failure is repairable, use `blocked`,
`parked`, `split`, or `merged` instead of `killed`.

## Layer 1 closure

Layer 1 is **closed-for-work** when:

1. Every K has all 7 fields filled (no `TBD`, no empty cells).
2. Every K passes Conditions 0-3 of the operational filter.
3. The lifecycle of every K is explicitly assigned (no defaults).
4. Every K has a literature link or explicit `(none, novel)`.
5. Cross-K dependencies (e.g., K3 depends on K1) are noted in a
   dependency column or sub-section.

After closure, capability writing (Layer 2) may begin. Adding a new K
after closure requires a deviation entry in `decisions.md`.

## When to split a capability into its own K

During Stage gates (especially Scoping and De-risk), you may discover
that what you wrote as a capability is actually research-worthy in its
own right. Promote a capability to a new K when:

- The capability has its own multi-stage research arc
  (Scoping → De-risk → Build → Validate → Integrate, where each stage is
  non-trivial), OR
- The capability would require a separate kill criterion or different
  lifecycle assignment from its current parent K.

Promotion: file a deviation entry in `decisions.md`, add the new K row,
move the capability to be a child of the new K. The original parent K's
status may need re-evaluation.

## Worked example

Target (from charter H1): "Automated measurement-reliability review for
public benchmark datasets, using reusable statistical checks."

Naive decomposition (rejected):
- K1: "data pipeline"  — fails (1), this is a dependency
- K2: "model fine-tuning" — fails (2), what's the question?
- K3: "validation harness" — fails (1), use existing
- K4: "integration" — fails (1), this is a task

Better decomposition (passes filter):

| ID | core_technology | research_question | target_contribution | lifecycle | prior_research | Status |
|---|---|---|---|---|---|---|
| K1 | Cross-dataset review transfer | Does the review protocol generalize across text, image, and tabular benchmark families with agreement delta ≥ 0.05? | Decides whether one reusable protocol is viable | continuous-improvement (benchmarks update) | papers.md §A | active |
| K2 | Scoring calibration protocol | Which calibration protocol maximizes agreement delta under a realistic review budget? | Adaptation strategy | continuous-improvement | papers.md §B | active |
| K3 | Latency-bounded inference architecture | Can the chosen checks run at < 100ms per item on production hardware? | Operational viability | establish-once (once chosen, stable) | papers.md §C | active |
| K4 | Decision-relevant reliability metric | Which metric (ECE / agreement delta / calibrated outcome metric) best predicts downstream review-routing benefit? | Connects review output to the consumer decision | establish-once | (none, novel) | active |

This project will require a maintenance plan at completion (K1 and K2 are
continuous-improvement). K3 and K4 become static once established.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Listing dependencies as core techs | "K = 'pandas DataFrame manipulation'" | Apply Condition 1 strictly |
| Listing capabilities as core techs | "K = 'write the data loader'" | If you can't write a research question, it's a capability or task |
| Coupled K's | "K1 = reward design, K2 = action design" | Apply Condition 2 isolation test, merge |
| One huge K | "K1 = 'the entire RL agent'" | Apply the "no count target" guidance: re-decompose |
| Default lifecycle | "all K's are establish-once" | Each lifecycle assignment must be justified; re-examine |
| No literature | All K's have "(none, novel)" | Probably wrong; even genuinely novel work has adjacent prior work |

## Relationship to other references

- Operational filter Condition 1 distinguishes K (core tech) from a
  dependency. Dependencies are noted in `decisions.md` if non-obvious,
  not in `capability_map.md`.
- Status `established` is the gate that unlocks capability promotion in
  `references/rd/rd_promotion_gate.md`.
- Lifecycle `continuous-improvement` triggers the maintenance plan requirement in
  `references/rd/rd_promotion_gate.md`.
- Layer 1 closure unlocks capability writing per
  `references/rd/capability_map_schema.md`.
- See `references/rd/rd_stages.md` for what to do if a Stage discovers a
  new K (Layer 1 rollback).
