# results_db_schema.md

Common schema for appending each experiment notebook's results to
`results/results.parquet`.

## When to read

- Writing the final cell of an experiment notebook
- Aggregating or comparing results across experiments

## Principle

The final cell of every experiment notebook appends a row to `results/results.parquet`
using a shared schema. Without this, cross-experiment comparison and synthesis are
impossible.

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

    # Meta ----------
    "n_hyperparams_tried": int,    # used for DSR
    "notebook_path":    str,
    "notes":            str,
}
```

## Append pattern at end of notebook

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

## Extension

Topic-specific metrics may be added, with rules:

- Use the prefix `extra_<name>` for added columns
- Do not change the type of common-schema columns
- Older rows fill new columns with null

## Warning signs

- Forgot to append the row → no aggregation possible; force the append in every cycle
- Same `experiment_id` appended multiple times → decide whether overwriting or duplicating
  is intended, and document
- Schema changes per experiment → cross-experiment queries break; keep the common part
  fixed
