# bug_review.md

Multi-agent bug-review layer. Run *before* the robustness battery and *before* setting any
`verdict = "supported"`.

## When to read

- Any one of the **trigger conditions** below has fired
- About to run the robustness battery (running the battery on a buggy PnL wastes compute
  and produces credible-looking false positives)
- About to declare `verdict = "supported"` for any experiment
- After any change to the data pipeline, target definition, signal alignment, feature
  scaling / normalization, fold definition, or fee model

## Why this layer exists

A passing robustness battery is *necessary but not sufficient*. Robustness checks measure
overfitting and regime stability — not implementation correctness. A look-ahead leak, a
misaligned `shift`, a whole-period normalization, or a wrong sign convention will pass
every robustness gate, because the leak is present in every walk-forward window and every
bootstrap resample. Robustness checks operate on the PnL series; if the PnL series itself
is contaminated, all gates inherit the contamination.

A single linear self-review is also insufficient at notebook length. Long notebooks
exceed reliable single-pass attention. Distinct specialist reviewers in parallel, each
with a narrow scope, catch substantively different things than one pass trying to cover
everything. Narrowness is the point.

## Trigger conditions (any one fires the layer)

### Numeric red flags ("too good to be true")

These thresholds are aggressive on purpose — they fire on results that, *if real*, would
already be world-class. The point is to pause and verify, not to decide.

| Flag | Threshold |
|---|---|
| Test Sharpe (after costs) | > 3 |
| Walk-forward mean Sharpe | > 2 |
| Information Coefficient (Spearman) on financial returns | > 0.10 |
| ML AUC on a return-sign target | > 0.65 |
| Per-trade win rate | > 65 % |
| Max drawdown / annualized vol | < 0.5 (suspiciously smooth equity) |
| Bootstrap 95 % CI lower bound | > 1.5 (unusually tight CI is also a flag) |
| Test metric outside the bootstrap 95 % CI | any direction |
| Headline Sharpe ≥ 2 × walk-forward mean Sharpe | any |

### State-change triggers (run regardless of metrics)

- Before `verdict = "supported"` is set
- Before the test set is touched the only time
- After any change to: data ingestion, target, embargo, fold definition, feature
  scaling / normalization, signal alignment, fee model
- After a feature notebook is rebuilt and downstream notebooks are re-run
- After collapsing or re-deriving a multi-instrument panel

### Recommended (not strict)

- At the end of every research cycle, even when no flag has fired

## Reviewer roster (5 specialists + 1 adversarial, dispatched in parallel)

Each reviewer is a sub-agent invoked via the assistant's sub-agent tool. The five
specialist scopes are deliberately narrow. Do not collapse them — narrowness is what
makes parallel review catch what single-pass review misses. The sixth reviewer
(`adversarial-reviewer`) intentionally runs with a *different* (minimum) context bundle —
that asymmetry is what makes it catch what same-context review of the same model misses.

The five specialists each receive:

- The path of the experiment notebook under review
- Paths of upstream feature notebook(s) listed in the design cell
- This file (`bug_review.md`)
- `references/sanity_checks.md`
- The reviewer-specific scope below
- The instruction "Return findings only. Do not modify files."

The sixth reviewer (`adversarial-reviewer`) receives a *different* bundle — see its
section below.

### 1. leakage-reviewer

Scope: look-ahead bias, target leakage, future-information contamination.

- Walk every feature definition. For each: does it use only data with `time ≤ t`?
- Whole-period normalization, target encoding, scaler-fit-on-all-data, whole-period
  imputation, whole-period quantile thresholds
- HMM / Kalman: smoothing (uses future) vs. filtering (causal) — which is used?
- `shift(-k)` on signals or features (target-only `shift(-k)` is OK)
- Cross-sectional ranks / standardizations: computed within each date only?
- PCA / factor decomposition: rolling vs. whole-period covariance
- Programmatic check: run `scripts/leakage_check.py::lookahead_check`

### 2. pnl-accounting-reviewer

Scope: position-to-return alignment, sign conventions, fee accounting, currency, turnover.

- Verify `pnl[t] = position[t-1] * ret[t]` (or the explicit alternative the notebook
  documents) — and verify the notebook documents the convention
- Same-bar `signal[t] * ret[t→t+1]` requires MOC fills; demand explicit justification or
  reject
- Cost: `position.diff().abs() * fee` is only valid when `position` is per-symbol; on a
  flattened multi-instrument frame it generates fake trades at ticker boundaries
- Fee monotonicity: increasing fee must monotonically reduce PnL
- Sign-flip identity: reversing all signals should mirror PnL minus 2× costs
- Programmatic checks: `scripts/sanity_checks.py::pnl_reconciliation`,
  `cost_monotonicity`, `sign_flip_test`

### 3. validation-reviewer

Scope: split correctness, embargo, test-set discipline, walk-forward purging.

- Train < val < test ordering by time, no overlap
- Embargo size ≥ target horizon
- Purged k-fold or CPCV used where overlap exists
- Test set touched exactly once — verify by counting code paths that read the test
  partition
- Walk-forward windows do not leak across boundaries (refit per window; no global
  statistic carried across windows)
- The robustness battery runs on val / CPCV, NOT on the test set (a common silent leak)

### 4. statistics-reviewer

Scope: metric correctness, trial counting, regime claims, internal consistency.

- DSR trial count: does it include every parameter combination tried across the project,
  not just this notebook? Recompute if unsure.
- Bootstrap CI must bracket the headline metric. Headline outside CI ⇒ bug.
- Walk-forward mean and test Sharpe must be roughly consistent. Test ≫ walk-forward mean
  ⇒ a single favorable test window or test-set leakage.
- AUC reported on a regression target ⇒ an undisclosed binarization step.
- Regime "positive in 5/5 regimes": how many bars per regime? A regime with 30 bars
  proves nothing.
- Sharpe annualization factor matches bar frequency.

### 5. code-correctness-reviewer

Scope: generic correctness, independent of domain.

- Off-by-one in indexing, slicing, `iloc` vs `loc`
- Sort order assumed but not enforced (`sort_values('date')`, `sort_values(['symbol','date'])`)
- NaN handling: does the model see NaNs? Does PnL silently treat NaN as zero?
- Dtype surprises (int division, datetime tz mismatch)
- Hidden global state (random seeds not set, mutable defaults)
- Multi-instrument operations missing `groupby('symbol')`
- Exception swallowing (`try / except: pass`)
- Hard-coded paths or magic constants that disagree with the design cell

### 6. adversarial-reviewer (cold-eye)

Scope: from code and reported numbers alone, identify at least one implementation bug
that could plausibly contaminate the result. This reviewer is structurally different
from the five specialists — same model, but a *deliberately different* (minimum)
context bundle. The asymmetry is the mechanism: same-context same-model review shares
priors, anchoring, and lost-in-middle effects. Stripping context forces the reviewer
to reason from the artifact alone, not from the author's narrative.

**Receives (minimum bundle)**:

- The notebook `.py` file body
- Upstream feature notebook `.py` files named in the design cell (only if named there)
- Reported headline numbers as listed in the abstract cell (Sharpe, DSR, win rate,
  max drawdown, etc.)

**Does NOT receive**:

- This file (`bug_review.md`) — including the trigger table
- The five specialist reviewers' findings
- `sanity_checks.py` output
- `decisions.md` / `hypotheses.md`
- Chat context / design-process discussion

**Instruction (give verbatim)**:

> "You are reading this code and the reported numbers cold, as an external reviewer.
> Identify at least one implementation bug that could plausibly explain the reported
> numbers. The five specialist reviewers' findings are intentionally withheld — the
> goal is to keep you from anchoring on the priors that the same model shares with
> them. Adopt the working hypothesis 'these numbers are the output of a bug' and try
> to falsify the result."

**Rationale**: Cross-Context Review (Song, arxiv 2603.12123) showed that
review with only the artifact (no production history, no intermediate reasoning, no
generation prompt) yielded the largest gains specifically on code review (+4.7 F1).
The mechanism: a fresh session has no anchor. Same-model perplexity preference is
not addressed by this — that is an accepted residual risk of single-model review —
but anchoring, sycophancy, and lost-in-middle are removed.

## Dispatch protocol

1. The assistant verifies that at least one trigger has fired. State the trigger
   explicitly to the user.
2. The assistant prepares **two** context bundles — the full bundle for the five
   specialists, and the minimum bundle for the adversarial reviewer — and dispatches
   all six reviewers **in parallel** in a single tool-call batch. Parallelism is
   required: it forces independent reads, which is the mechanism that makes
   specialist review work. Bundle asymmetry is required: it is the mechanism that
   makes the adversarial pass add value over a sixth specialist would add.
3. Each reviewer returns findings in this schema:

   ```
   - severity: high | medium | low
     where:    <file>:<cell-or-line>
     what:     <one-sentence description>
     why:      <which check / reference / convention is violated>
     fix:      <concrete remediation or a follow-up question>
   ```

4. The assistant aggregates findings into `decisions.md` under the heading
   `### Bug review for exp_NNN at <ISO timestamp>`.
5. The assistant addresses every `high` and every `medium` finding before re-running the
   battery or declaring a verdict. `low` findings are logged and may be parked, with a
   one-line reason in `decisions.md`.

## Single-agent fallback

If parallel sub-agent dispatch is unavailable (single-process platform, sub-agent quota,
etc.), the assistant runs the same six scopes sequentially in six distinct passes,
clearing context (or at least re-loading the notebook from scratch) between passes. Six
focused single-pass reviews still substantially outperform one mixed-scope pass. The
adversarial pass is run *with the minimum bundle only* even in the fallback — bundle
asymmetry is preserved.

Do not skip scopes. The temptation to merge "leakage" + "validation" into one pass is
exactly the failure mode this layer prevents. The temptation to give the adversarial
reviewer the full bundle "for fairness" is also a failure mode — that collapses the
asymmetry that makes the layer work.

## When findings disagree

Two reviewers can produce contradictory readings (e.g. the leakage-reviewer says "this is
filtering, OK" and the statistics-reviewer says "the in-sample fit is too tight"). Log
both. Do not silently pick the more convenient one. If unresolved after a code re-read,
raise it as a derived hypothesis and run a falsifying experiment (typically a randomized-
target test that the answer should fail).

## Failure mode this layer prevents

The most common failure: agent reads the robustness battery output (all green), declares
`verdict = "supported"`, appends to `results.parquet`, moves on. If the underlying PnL
had a leak, every robustness metric is corrupted in the same direction and the green
ticks are meaningless.

**Bug review precedes robustness battery, not the other way around.** A
`verdict = "supported"` entry in `decisions.md` without a preceding bug-review entry is a
protocol violation that downgrades the result to *preliminary screening*.

## Relationship to `experiment-review` skill

This layer (`bug_review`) and the separate `experiment-review` skill are **distinct,
complementary, and both required** before `verdict = "supported"`. They are intentionally
not merged; their adversarial reviewers in particular receive *different* minimum
bundles tuned to different failure modes.

| | `bug_review` (here) | `experiment-review` (separate skill) |
|---|---|---|
| Question | Is the implementation correct? | Is the claim warranted by the design? |
| Failure mode prevented | Contaminated PnL passing all robustness gates | Real numbers that don't support the abstract's claim |
| Specialists | 5 (leakage / pnl-accounting / validation-correctness / statistics / code-correctness) | 7 (question / scope / method / validation-sufficiency / claim / literature / narrative) |
| Adversarial bundle | code + reported numbers | `.py` file alone |
| Order | Precondition (run first) | Postcondition (run after robustness battery) |

A clean `experiment-review` on top of a buggy implementation produces confidence in a
contaminated PnL — `bug_review` is the precondition. A clean `bug_review` on top of an
unsupported claim produces a deployment-ready overstatement — `experiment-review` is
the postcondition. Neither layer alone is sufficient.

## Audit

`decisions.md` is the audit trail. Every triggered review must end with an entry that
names:

- The trigger that fired (numeric or state-change)
- The six reviewers that were run, with their agent IDs / timestamps
- The findings produced, severity-tagged
- What was done about each finding (fixed / parked-with-reason)

If any of these is missing, the layer was not actually run.
