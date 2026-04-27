# sanity_checks.md

Programmatic bug-detection checks. Each reviewer in `bug_review.md` references this
catalog and runs the checks relevant to its scope. Notebooks should also call the
relevant subset directly in a "Sanity checks" cell that runs *before* the robustness
battery.

## When to read

- The multi-agent bug-review layer (`bug_review.md`) has fired
- Adding a "Sanity checks" section to an experiment notebook
- An evaluation result looks too good or internally inconsistent

## Catalog

Each entry: name · what · when · pass condition · helper · failure interpretation.

### 1. Random-signal benchmark

**What.** Replace the strategy's signal with i.i.d. ±1 (or `N(0, 1)`) of matching length
and rerun the same evaluation pipeline. Repeat N times.

**When.** After every signal-pipeline change. Mandatory at first run.

**Pass condition.** |median Sharpe| < 0.5 across trials, and the real-signal Sharpe is
outside the 95 % CI of the random-signal distribution.

**Failure interpretation.** Random signals scoring well means the *evaluation* leaks
(test partition, fee model, sizing, PnL accounting), not the *signal*. Stop everything
and locate the leak before any further work — every existing metric is contaminated.

**Helper.** `scripts/sanity_checks.py::random_signal_benchmark`.

### 2. Shuffled-target test

**What.** Permute the target series (block-permute if seasonality matters) and retrain /
re-evaluate the model with the same hyperparameters and folds. Predictability should
disappear: AUC ≈ 0.5, IC ≈ 0.

**When.** Every ML experiment, before declaring a feature predictive.

**Pass condition.** Mean AUC across N ≥ 20 shuffles is in [0.48, 0.52], and the real AUC
is outside that band.

**Failure interpretation.** Predictability under shuffled targets ⇒ target leakage,
non-causal label construction, or a metric that responds to label distribution rather
than label content.

**Helper.** `scripts/sanity_checks.py::shuffled_target_test`.

### 3. PnL reconciliation

**What.** Verify the documented PnL identity holds:
`cum_pnl[T] − cum_pnl[0] ≈ Σ position[t-1] · (price[t] − price[t-1]) − Σ |Δposition[t]| · fee · price[t]`.

**When.** Whenever PnL accounting code is touched.

**Pass condition.** Relative reconciliation error < 1e-9.

**Failure interpretation.** A non-zero gap is *always* a bug — either the documented
convention is wrong, or the code does something the convention does not say.

**Helper.** `scripts/sanity_checks.py::pnl_reconciliation`.

### 4. Cost monotonicity

**What.** Sweep fee ∈ a grid (e.g. `[0, 0.5, 1, 2, 5, 10] bp/side`) and verify net PnL is
monotonically non-increasing.

**When.** Whenever cost code is touched.

**Pass condition.** Strict monotonicity (with floating-point tolerance).

**Failure interpretation.** Non-monotonicity ⇒ fee is being subtracted with the wrong
sign, applied to the wrong leg, or applied conditionally on something that correlates
with returns.

**Helper.** `scripts/sanity_checks.py::cost_monotonicity`.

### 5. Sign-flip identity

**What.** Replace `signal` with `-signal` and rerun. With zero costs, net PnL must be
≈ −PnL_orig. With costs, net PnL ≈ −PnL_orig − 2 × cost.

**When.** Whenever signal generation is touched.

**Pass condition.** Asymmetry < 10 % after the cost adjustment.

**Failure interpretation.** Asymmetric magnitudes hint at a sign or alignment bug, or a
cost model that depends on direction.

**Helper.** `scripts/sanity_checks.py::sign_flip_test`.

### 6. NaN / Inf scan

**What.** After every transformation, count NaNs and Infs in features, signals, returns,
and PnL.

**Pass condition.** NaNs concentrated only at series boundaries (rolling-window warm-up);
no Inf anywhere; no NaN in PnL.

**Failure interpretation.** NaN inside the time-series body of any feature implies the
model is being trained on partially-defined inputs. NaN in PnL means trades silently went
missing or something divided by zero.

**Helper.** `scripts/sanity_checks.py::nan_inf_scan`.

### 7. Time-shift placebo

**What.** Shift the signal `+k` bars into the past (should not help), and `−k` bars into
the future (must help spuriously, exactly by the amount the strategy already leaks if it
leaks).

**When.** Once per signal pipeline.

**Pass condition.** Forward-shifting (`+k`, "delayed") degrades Sharpe; backward-shifting
(`−k`, "look ahead") improves Sharpe by a magnitude that quantifies the upper bound on
true edge.

**Failure interpretation.** Forward-shift improving Sharpe ⇒ the original signal was
already future-leaking by `k` bars.

**Helper.** `scripts/sanity_checks.py::time_shift_placebo`.

### 8. Look-ahead via truncation

**What.** Recompute features at sample times `t` using only `data[:t+1]`; compare to the
same features computed on the full data. Equality everywhere ⇒ no look-ahead.

**Helper.** `scripts/leakage_check.py::lookahead_check` (existing).

### 9. Whole-period statistic scan

**What.** Static review of the feature notebook for whole-period statistics: `.mean()`,
`.std()`, `.median()`, `StandardScaler().fit(`, `fit_transform(` (without train/test
discipline), `df['x'].quantile(`, `df.corr()` without rolling, etc.

**Pass condition.** Every such call is fenced inside a per-fold or rolling construction.

**Helper.** None — this is a read-only review pass.

### 10. Trial-count audit for DSR

**What.** Enumerate every parameter combination tried across the entire project (not just
the current notebook), feed it to `scripts/psr_dsr.py`, recompute DSR.

**When.** Before declaring `verdict = "supported"`.

**Pass condition.** DSR ≥ 0.95 with the *honest* trial count.

**Failure interpretation.** DSR drops below 0.95 with the honest count ⇒ strategy is not
robust to selection bias; the headline metric is partly noise mining.

### 11. Cross-instrument / cross-time aggregation scan

**What.** Pattern-search for `pct_change`, `diff`, `rolling`, `cumsum` calls applied to a
DataFrame that is *not* grouped by symbol. On long-form panels these compute across
ticker boundaries and produce nonsense returns at every transition.

**Pass condition.** Every such call is either inside a `groupby('symbol')` (or
equivalent) or operates on a per-symbol Series.

**Helper.** None — read-only review pass.

### 12. Embargo-existence check

**What.** Verify `embargo_bars >= target_horizon_bars`. Verify the embargo is actually
applied at every train/val and val/test boundary, not only at one of them.

**Pass condition.** Both conditions hold; the design cell records `embargo_bars`.

## Reading the helpers

`scripts/sanity_checks.py` is small and pure on purpose. A reviewer can verify the helper
itself before trusting its output. Existing `scripts/leakage_check.py` and
`scripts/psr_dsr.py` cover items 8 and 10 respectively.

## How a notebook uses this catalog

Insert a "Sanity checks" section right after the proposed-method evaluation cell, before
the robustness battery section. That section calls the subset of helpers relevant to the
experiment shape (always: PnL reconciliation, cost monotonicity, NaN/Inf scan,
random-signal benchmark; for ML: shuffled-target test; for multi-instrument:
aggregation scan). The output of each helper is rendered in its own cell with an
*observation* markdown cell underneath. A failing helper blocks the rest of the notebook.

The multi-agent review (per `bug_review.md`) is *additional* to these programmatic checks
and reads code that the helpers cannot reach (sign conventions buried in custom
functions, interactions between feature notebook and model notebook, etc.).
