# results_db_schema.md

Common schema for appending each Hypothesis result to
`results/results.parquet`.

## When to read

- Closing a Hypothesis round inside an experiment notebook
- Aggregating or comparing results across Hypotheses or across notebooks

## Principle

**One row per Hypothesis tested** (not one row per notebook). A notebook
conducts one Purpose containing one or more H's; each H produces its own row
in `results/results.parquet`. The append happens at the end of each H's
round inside the notebook, not once at the bottom of the file.

The schema below already carries `experiment_id` (= the notebook = the
Purpose) and `hypothesis_id` (= the individual H within the Purpose) as
separate columns; a notebook with three H's emits three rows that share
`experiment_id` and differ in `hypothesis_id`. Cross-H aggregation queries
group by `hypothesis_id`; cross-Purpose aggregation queries group by
`experiment_id`.

Without per-H rows, no cross-H comparison or per-H verdict tracking is
possible.

## Common schema

```python
{
    # Identification ----------
    "project":          str,    # project folder name
    "experiment_id":    str,    # exp_001, exp_002, ...
    "hypothesis_id":    str,    # H1, H2, ...
    "run_timestamp":    datetime,  # UTC

    # Universe / data ----------
    "instrument":       str,    # instrument identifier
    "timeframe":        str,    # M5, H1, D1, ...
    "data_start":       date,
    "data_end":         date,
    "split":            str,    # train / val / test / full

    # Method ----------
    "method":           str,    # free-text identifier
    "model_type":       str,    # math / classical_ml / dl / rl / foundation / hybrid
    "entry_rule":       str,
    "exit_rule":        str,
    "sizing":           str,    # equal / vol_target / kelly / ...

    # Cost ----------
    "fee_bp_per_side":  float,
    "slippage_model":   str,    # none / scalar / realistic

    # Primary metrics ----------
    "n_trades":         int,
    "win_rate":         float,
    "total_return":     float,
    "sharpe":           float,  # annualized
    "max_drawdown":     float,
    "ret_per_trade_bp": float,

    # Prediction-model metrics (ML research) ----------
    "auc":              float | None,
    "ic_spearman":      float | None,
    "ir":               float | None,
    "calibration_ece":  float | None,

    # Robustness ----------
    "wf_mean_sharpe":   float | None,
    "wf_pct_positive":  float | None,
    "bootstrap_ci_low": float | None,
    "bootstrap_ci_high":float | None,
    "bootstrap_p":      float | None,
    "psr":              float | None,
    "dsr":              float | None,

    # Generation pathway (from `hypothesis_generation.md`, Step 1.5) ----------
    "pathway":          str,    # 1-data-driven / 2-literature-extension /
                                # 3-literature-refutation / 4-failure-derived /
                                # 5-cross-asset-extension / 6-mechanism-driven /
                                # ad-hoc
    "parent_hypothesis_id": str | None,  # required when pathway=4 (the H_n
                                         # whose named failure axis sourced
                                         # this H_{n+1}); otherwise None

    # Verdict and tier (verdict and achieved_tier are filled post-review) ----
    "verdict":          str,    # supported / rejected / parked / preliminary
                                # provisional at append-time, finalized after
                                # bug_review + experiment-review pass
    "failure_mode":     str | None,  # required when verdict=rejected;
                                     # controlled vocabulary (see below);
                                     # None for verdict in {supported, parked}
    "forecasted_tier":  str,    # strong / medium / weak / variable — from
                                # the H's pathway forecast (B's table). Known
                                # at append-time.
    "achieved_tier":    str | None,  # strong / medium / weak — filled by
                                     # the experiment-review literature
                                     # dimension's novelty check (E). Null at
                                     # append-time, updated after Step 13.

    # Meta ----------
    "n_hyperparams_tried": int,    # used for DSR
    "notebook_path":    str,
    "notes":            str,
}
```

### `failure_mode` controlled vocabulary

Required when `verdict == "rejected"`. One value per row; the *primary*
failure axis (the one that, if fixed, would most plausibly change the
verdict). Free-text elaboration goes in `notes`.

| Value | Meaning | Typical fix |
|---|---|---|
| `leakage` | Look-ahead, target leak, or feature-scaling leak detected by `bug_review` or sanity checks | Fix the data flow; re-run |
| `regime_mismatch` | Held only in one regime; failed under regime-conditional sweep | Either narrow the H's claim to that regime or redesign |
| `fee_model` | Gross alpha exists but realistic fees consume it; break-even fee below realistic | Either change horizon / sizing to reduce trading frequency or close the H |
| `wrong_horizon` | Position held too long / too short for the signal's information half-life | Re-derive H4 (Pathway 4) targeting horizon as the named axis |
| `wrong_universe` | Signal exists in a narrow subset; failed on the declared universe | Either narrow the H or test universe-specific |
| `wrong_baseline` | Beat lower-bound but failed against hand-crafted upper-bound | Strengthen method beyond linear / GBT baseline |
| `threshold_brittleness` | Single peak in 2D sensitivity surface; failed outside the optimum | Likely overfit; reject or redesign with plateau-finding |
| `capacity_constraint` | Sharpe degrades sharply with notional | Either shrink the deployment claim or close |
| `signal_weakness` | No bug, no leak, just no alpha | Close the H; meta-knowledge that this direction does not work |
| `mechanism_misspecification` | Pathway 6 H: the declared cause-mechanism-observable chain did not predict the data | Re-examine the mechanism; do not silently switch pathways |
| `power_insufficient` | Test sample too small to distinguish from noise; not a true rejection | Re-collect data or close as inconclusive (verdict=parked rather than rejected) |
| `other` | None of the above | **Requires** a free-text paragraph in `notes` naming the axis explicitly. `other` without a `notes` paragraph is a schema-protocol violation. |

The vocabulary is extensible per the existing `extra_*` rule for
project-specific axes; the listed values are the protocol's defaults
and should be preferred when they fit.

### Post-review update pattern for `verdict` and `achieved_tier`

`verdict` and `achieved_tier` carry provisional values at append-time
(end of H round in the notebook) and are **updated** after both review
layers pass:

```python
import polars as pl

db_path = "results/results.parquet"
db = pl.read_parquet(db_path)

# After bug_review + experiment-review for H3 in exp_007 complete and
# the literature dimension reports achieved_tier=medium (forecast was
# strong for a Pathway-6 H — tier downgrade)
mask = (pl.col("experiment_id") == "exp_007") & (pl.col("hypothesis_id") == "H3")
db = db.with_columns([
    pl.when(mask).then(pl.lit("rejected")).otherwise(pl.col("verdict")).alias("verdict"),
    pl.when(mask).then(pl.lit("medium")).otherwise(pl.col("achieved_tier")).alias("achieved_tier"),
    pl.when(mask).then(pl.lit("mechanism_misspecification")).otherwise(pl.col("failure_mode")).alias("failure_mode"),
])
db.write_parquet(db_path)
```

A row whose `verdict` was set to `supported` at append-time but whose
final review verdict is `partial` or `preliminary` (per the
experiment-review verdict tiers) has the schema field `verdict`
*updated to match the review's final verdict*. The append-time value
is provisional precisely because the protocol's verdict gates fire
after the H's primary metrics are computed.

## Append pattern at the end of each H round (NOT at the end of the notebook)

```python
import polars as pl
from datetime import datetime, timezone

result_row = {
    "project": "<project-name>",
    "experiment_id": "exp_005_signal_flip",
    "hypothesis_id": "H3",
    "run_timestamp": datetime.now(timezone.utc),
    "instrument": "<instrument>",
    "timeframe": "M5",
    "data_start": ...,
    "data_end": ...,
    "split": "test",
    "method": "h8_filter+signal_flip",
    "model_type": "math",
    "entry_rule": "rsi_14<=-13 AND atr_p>=median",
    "exit_rule": "rsi_14>=0",
    "sizing": "equal",
    "fee_bp_per_side": 1.0,
    "slippage_model": "none",
    "n_trades": 223,
    "win_rate": 0.623,
    "total_return": -0.0241,
    "sharpe": -1.74,
    "max_drawdown": -0.031,
    "ret_per_trade_bp": -1.08,
    "auc": None,
    "ic_spearman": None,
    "ir": None,
    "calibration_ece": None,
    "wf_mean_sharpe": -0.10,
    "wf_pct_positive": 0.474,
    "bootstrap_ci_low": 0.009,
    "bootstrap_ci_high": 0.202,
    "bootstrap_p": 0.014,
    "psr": None,
    "dsr": None,
    "n_hyperparams_tried": 20,
    "notebook_path": "experiments/exp_005_signal_flip.py",
    "notes": "...",
}

import os
db_path = "results/results.parquet"
if os.path.exists(db_path):
    existing = pl.read_parquet(db_path)
    new = pl.concat([existing, pl.DataFrame([result_row])], how="diagonal_relaxed")
else:
    new = pl.DataFrame([result_row])
new.write_parquet(db_path)
```

`scripts/aggregate_results.py` wraps this into a function with required-field validation.

## Aggregation queries

Comparing across the full project:

```python
import polars as pl
db = pl.read_parquet("results/results.parquet")

# Conclusions per hypothesis
db.group_by("hypothesis_id").agg(
    pl.col("sharpe").mean().alias("avg_sharpe"),
    pl.col("split").n_unique().alias("n_splits"),
    pl.col("experiment_id").unique().alias("experiments"),
)

# Fee sensitivity for a specific hypothesis
(
    db
    .filter(pl.col("hypothesis_id") == "H3")
    .sort("fee_bp_per_side")
    .select(["fee_bp_per_side", "split", "sharpe"])
)
```

### Cross-H meta-knowledge queries (using the new fields)

These queries are the queryable surface that the cross-H synthesis
(see `cross_h_synthesis.md`) consumes:

```python
# Distribution of failure modes within one Purpose
(
    db
    .filter(pl.col("experiment_id") == "exp_007")
    .filter(pl.col("verdict") == "rejected")
    .group_by("failure_mode")
    .agg(pl.col("hypothesis_id").alias("rejected_H_ids"))
)

# All H's that lost on fee_model across the whole project — candidates
# for "lower-frequency" pivot
(
    db
    .filter(pl.col("failure_mode") == "fee_model")
    .select(["experiment_id", "hypothesis_id", "fee_bp_per_side", "sharpe"])
)

# H's that achieved Weak tier despite forecasting Medium or Strong —
# tier-downgrade audit
(
    db
    .filter(pl.col("achieved_tier") == "weak")
    .filter(pl.col("forecasted_tier").is_in(["medium", "strong"]))
    .select(["experiment_id", "hypothesis_id", "pathway",
             "forecasted_tier", "achieved_tier"])
)

# Derivation chain for a Pathway-4 H — what failure axis was the
# parent's, and did the derived H actually address it
(
    db
    .filter(pl.col("pathway") == "4-failure-derived")
    .join(
        db.select([
            pl.col("hypothesis_id").alias("parent_hypothesis_id"),
            pl.col("failure_mode").alias("parent_failure_mode"),
            pl.col("verdict").alias("parent_verdict"),
        ]),
        on="parent_hypothesis_id",
        how="left",
    )
    .select(["experiment_id", "hypothesis_id", "parent_hypothesis_id",
             "parent_failure_mode", "verdict", "failure_mode"])
)
```

The first three queries are the primary cross-H meta-learning surface;
the fourth verifies the Pathway-4 derivation chain is well-formed
(every Pathway-4 H names a parent that exists and has a recorded
failure mode).

## Extension

Topic-specific metrics may be added, with rules:

- Use the prefix `extra_<name>` for added columns
- Do not change the type of common-schema columns
- Older rows fill new columns with null

## Warning signs

- Forgot to append a row for some H → that H is invisible to aggregation; force
  the append at the end of every H round
- Same `(experiment_id, hypothesis_id)` pair appended multiple times → decide
  whether overwriting or duplicating is intended, and document
- A notebook emits only one row when its hypothesis log clearly shows multiple
  H's tested → likely a stale "one row per notebook" mental model; emit one
  row per H
- Schema changes per H → cross-H queries break; keep the common part fixed
  (extra metrics use the `extra_<name>` prefix per the Extension section)
