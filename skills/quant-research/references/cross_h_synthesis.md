# cross_h_synthesis.md

Protocol for taking H1…HN's rows in `results.parquet` and producing the
**Purpose-level meta-knowledge** — what the *cluster* of H's tells us
that no single H told us. Read this when closing a Purpose with two or
more H tested (any verdict mix), before writing the Purpose-level
conclusion in the notebook and `decisions.md`.

## When to read

- Closing a Purpose: at least one H is `verdict='supported'` or all H's
  are decided (rejected / parked / preliminary).
- Routine end-of-H check inside an active Purpose with N ≥ 3 H tested:
  is the cluster pattern visible yet?
- Before declaring a Purpose "exhausted" (see `hypothesis_cycles.md`).

## Goal

Convert H1…HN's structured rows in `results.parquet` into a one-paragraph
*meta-finding* about the Purpose. The meta-finding is the durable output
the project carries forward to derived Purposes — without it, every new
Purpose starts from the same priors that were already updated by the
previous Purpose's H's.

## Inputs

- `results.parquet` filtered to the current `experiment_id` (= the
  Purpose / notebook).
- `decisions.md` entries for any rejected H's (for the prose context
  behind the `failure_mode` controlled-vocabulary value).
- `hypotheses.md` for the pathway and forecasted-tier each H committed
  to.

## The patterns

The synthesis is pattern-matching on the cluster's `(verdict,
failure_mode, achieved_tier, pathway)` distribution. The patterns
below are the recurring shapes; a Purpose's actual cluster usually
matches one (sometimes two) of them. Each pattern names what the
cluster *says* about the world, distinct from what any single H said.

### Pattern A — Same axis fails everything

**Shape**: `verdict='rejected'` on most/all H's, `failure_mode` is the
same value across them (e.g., `fee_model` on H1, H2, H3).

**Meta-finding**: That axis is the **binding constraint** for this
Purpose. The Purpose, as scoped, is not viable under that axis
without a redesign that targets it specifically.

**Action**:
- Either redesign as a derived Purpose that addresses the axis (e.g.,
  `fee_model` binding → derived Purpose "lower-frequency variants of
  the same signal"; `regime_mismatch` binding → derived Purpose
  "regime-conditional version" with the regime as part of the
  Purpose statement),
- Or close the Purpose with the axis as the durable finding ("under
  realistic fees the funding-rate signal does not survive on this
  universe / horizon — `fee_model` is the binding constraint").

### Pattern B — Different axes, no convergence

**Shape**: `verdict='rejected'` on most H's, `failure_mode` is
*different* across them (H1: `wrong_horizon`, H2: `regime_mismatch`,
H3: `wrong_baseline`, …).

**Meta-finding**: The Purpose is **too broad**. The H's are testing
different specific claims under one umbrella; their failures share no
common cause; no single redesign helps. This is usually the symptom
of a Purpose that conflates a general phenomenon with a specific
predictive claim.

**Action**:
- Split the Purpose into derived Purposes, each tightly scoped to one
  axis the H's surfaced. For example, "Does funding signal carry
  information?" → split into "Does it carry information about return
  direction at the next funding interval?" + "Does it carry
  information about realized volatility?" + "Does it carry capacity
  for sized deployment?". Each derived Purpose is investigated in a
  separate notebook.
- Avoid the failure mode of "let me try H_{N+1} hoping it fits" —
  with no shared failure mode there is no axis for H_{N+1} to fix.

### Pattern C — Pareto re-allocation, not progress

**Shape**: Successive H's improved metric M_a but worsened metric M_b
(e.g., H1: high Sharpe but high drawdown; H2: lower Sharpe but lower
drawdown; H3: even lower Sharpe again). All H's might be `rejected`
or some `parked`; the pattern is in the metric *shape*, not the
verdicts alone.

**Meta-finding**: The cluster is exploring a **trade-off frontier**,
not converging on a winner. The frontier itself is the finding (the
research result is "there is a trade-off between Sharpe and drawdown
in this Purpose, with the following shape"); continued iteration along
the same axis is sunk-cost iteration.

**Action**:
- Stop iterating along this axis. Write the trade-off frontier as the
  Purpose-level conclusion.
- If a downstream consumer needs a deployment point on the frontier,
  that consumer's risk preference selects it — the research itself
  does not select.

### Pattern D — Monotonic improvement (with a selection caveat)

**Shape**: Successive H's monotonically improved on the primary
metric, all with the same `pathway` (typically Pathway 4 derivations
of each other). Some `rejected` early, latest `supported`.

**Meta-finding**: The cycle is **working as designed**; the Pathway-4
derivation chain converged on a viable H. *But*: a monotonically
improving cycle is also evidence of `selection`, and the verdict
`supported` on the latest H must use a DSR trial count that includes
*every cycle*, not just the latest.

**Action**:
- Keep the supported H, but require the `dsr` field with the honest
  trial count covering every H tried (per `experiment-review`'s
  `validation` and `question` dimensions).
- Treat the "the latest H worked, so the earlier rejections are
  irrelevant" framing as a red flag — the earlier rejections are part
  of the trial count.

### Pattern E — One H supported, others rejected on the same axis

**Shape**: One H `verdict='supported'`, others `verdict='rejected'`
with the same `failure_mode` (e.g., H2 supported with regime filter
"vol < 60%"; H1, H3 rejected with `regime_mismatch`).

**Meta-finding**: The supported H is a **special case**, not a
general result. The Purpose-level conclusion must scope the abstract
to the special case, not to the Purpose as originally stated.

**Action**:
- Narrow the abstract: "Funding-rate signal carries information *in
  low-volatility regimes only*, with the following effect size; in
  other regimes, the signal does not survive — `regime_mismatch` was
  the binding axis there".
- Do not generalize from the supported H's specific scope to the
  Purpose's broader claim. The `experiment-review` `claim` dimension
  catches this independently, but the cross-H synthesis surfaces it
  earlier (during the Purpose-level conclusion, before the abstract
  is locked).

### When patterns combine

A Purpose's cluster can match two patterns (e.g., Pattern A on
`fee_model` for half the H's and Pattern E on the other half — "the
signal works on low-frequency configurations but not high-frequency,
and the high-frequency failures all share `fee_model`"). The synthesis
names both patterns; the Purpose-level conclusion describes the
combined finding ("the signal exists in the low-frequency regime; in
the high-frequency regime, fees are the binding constraint").

## Templates

### Notebook: Purpose-level conclusion cell

```markdown
## Purpose-level conclusion

### Cluster summary
- N H tested under this Purpose: {N}
- Verdicts: {supported: {n}, rejected: {n}, parked: {n}, preliminary: {n}}
- Pathways used: {1-data-driven: {n}, 4-failure-derived: {n}, ...}
- Failure-mode distribution (rejected H's): {fee_model: {n}, regime_mismatch: {n}, ...}

### Meta-finding (Pattern: A / B / C / D / E or combined)
[One paragraph: what the cluster says that no single H said. Cite
the pattern by name. If it's a combined pattern, name both.]

### What the project carries forward
[One paragraph: the durable finding the next Purpose inherits as
prior. Examples:
- "Fee model is the binding constraint on this universe at this
  frequency — derived Purposes should test lower frequencies."
- "The Purpose was too broad — split into derived Purposes A / B / C
  scoped to the specific axes the H's surfaced."
- "The trade-off frontier shape is the result; do not iterate further
  along this axis."]

### Derived Purposes proposed (= candidate next notebooks)
[List with one-sentence justification each, plus the
`target_sub_claim_id` each derived Purpose will attack (referencing
the project README's sub-claim list). Classified per
hypothesis_cycles.md as run-now / next-session / drop.]
```

### `decisions.md` entry

```markdown
## {date} — exp_NNN Purpose-level synthesis

- Pattern: {A / B / C / D / E or combined}
- Meta-finding: {one sentence}
- Cluster: N H tested, {supported}/{rejected}/{parked}/{preliminary}
- Binding axis (if Pattern A): {failure_mode value}
- Derived Purposes:
  - {one-sentence each, with target_sub_claim_id and run-now / next-session / drop}
```

## Handoff to the next notebook (when a derived Purpose opens)

When the synthesis produces a derived Purpose that will be opened as a
new notebook (`exp_<NNN+1>_*.py`), the handoff between old and new
notebook follows the four-layer model in
`references/research_goal_layer.md`:

1. **The new notebook's body does NOT carry the old Purpose's synthesis,
   Pattern label, binding axis, or any derivation prose.** That information
   lives in `decisions.md` (the old Purpose entry's Purpose-level synthesis
   + Derived Purposes section). The new notebook reads as if its Purpose
   were independent — because under the four-layer model it is anchored
   to a research-goal sub-claim, not to the old Purpose's narrative.
2. **The new notebook's `target_sub_claim_id`** (Cycle goal 5th item) is
   chosen from the project README's sub-claim list — not "inherited"
   from the old Purpose. The chosen sub-claim is whichever the synthesis
   identified as the next sub-claim to attack (e.g., Pattern A's binding
   axis often shifts the question to a different sub-claim).
3. **The new notebook's `## Purpose` statement** is written as an
   open-ended question about the world, in the form
   `cycle_purpose_and_goal.md` requires. Phrases like "派生した", "handoff",
   "Pattern A", "binding axis carried over from", "as decided in
   cross_h_synthesis", or "from exp_<NNN>" do not appear in the Purpose
   header, the docstring, or any markdown cell of the new notebook.
4. **The new notebook's `decisions.md` Purpose entry** carries the link
   in two places: the *Design hypothesis at open* line ("opening this
   Purpose will close G1.X to confirmed or falsified") implicitly carries
   the upstream provenance, and the project README's sub-claim status
   (which the previous Purpose moved to `confirmed` or `falsified`)
   provides the reading context. Together these are sufficient — no
   prose handoff in the new notebook is needed.
5. **Minimal cross-references** in the new notebook are allowed and
   encouraged when they convey research content: e.g., a Figure plan
   line like `Fig 4 — H_old / H_new comparison of cumulative PnL` names
   the comparison series. This is research content, not handoff prose.
   The line "as a follow-up to exp_<NNN>'s Pattern A finding" is
   handoff prose and is not allowed.

### Why this matters

Without the handoff rules above, the derived Purpose's notebook drifts
into being a continuation of the old notebook's narrative. The reader
who opens only the new notebook then sees a research artifact whose
Purpose is "exp_<NNN>'s Pattern A consequence" rather than an open-ended
investigation of a research-goal sub-claim. That reframes the unit of
research from sub-claim-anchored Purpose to handoff-chain Hypothesis,
which is the failure mode the four-layer model exists to prevent.

The information that *would* go into the handoff prose belongs in
`decisions.md` (cross-Purpose audit trail), `hypotheses.md` (per-H
provenance via `parent_id` in the Statement column), and the project
README sub-claim status (project-level distance update). The new
notebook stays as a research artifact about its own Purpose.

## Worked example (the funding-mean-reversion case from RED-4)

Hypothetical end state after H4:

| H | pathway | forecasted_tier | verdict | failure_mode | achieved_tier |
|---|---|---|---|---|---|
| H1 | 6-mechanism-driven | strong | rejected | fee_model | medium |
| H2 | 4-failure-derived (parent H1) | variable | rejected | fee_model | medium |
| H3 | 4-failure-derived (parent H2) | variable | rejected | fee_model | medium |
| H4 | 4-failure-derived (parent H3) | variable | rejected | fee_model | medium |

Synthesis:

- **Pattern**: A (same axis fails everything; `fee_model` on all four).
- **Meta-finding**: Fee model is the binding constraint for the
  funding-rate signal on BTC perpetuals at the daily horizon. Across
  four H's exploring different entry / exit / regime variants, the
  break-even fee remained below realistic execution fees. The signal
  exists in gross terms but does not survive net-of-fee.
- **What the project carries forward**: A derived Purpose
  ("Lower-frequency funding signal: does the same mean-reversion
  carry at multi-day or weekly horizons?") is run-now-eligible.
  Continued daily-horizon iteration along the H1 → H4 chain is sunk
  cost. The Purpose itself is closed.
- **Derived Purposes**:
  - "Funding-rate signal at multi-day / weekly horizons" — run-now.
  - "Funding-rate signal as input to a portfolio overlay rather than
    standalone strategy" — next-session.
  - "Funding-rate signal as a *risk* signal rather than a return
    signal" — drop (no compelling mechanism).

Note that **without the schema's `failure_mode` and `pathway` fields,
this synthesis would be ad-hoc prose dependent on the researcher's
memory of why each H failed.** With them, the synthesis is a query +
pattern match + paragraph; auditable and reproducible.

## Anti-patterns

- **"Try H5"**: when Pattern A or B is visible, a fifth H of the same
  shape adds noise, not information. Either redesign around the
  binding axis or split the Purpose. The stop rule in
  `hypothesis_cycles.md` should fire here.
- **"The supported H is the result; the rejected H's are noise"**:
  rejected H's are *part* of the meta-finding under Patterns A, B, E.
  Suppressing them in the Purpose-level conclusion is selection bias.
- **"Skip the synthesis; the abstract speaks for itself"**: the
  abstract is per-H. The synthesis is the Purpose's contribution.
  Without it, the project's accumulated knowledge stays in
  `results.parquet` rows that no narrative reads back together.
