# results_db_schema.md

Common schema for appending queryable evidence records to
`results/results.parquet`.

## When to read

- A trial artifact should be queryable across notebooks.
- A claim is being considered for promotion and needs an audit trail.
- Prior evidence is being compared by mode, method, market, metric, or
  failure mode.

Do not append rows just because a notebook ran. Append when an artifact has an
observation and enough interpretation to be useful later. The row does not
move research state by itself; a ledger assessment in `capability_map.md`,
`explanation_ledger.md`, or `decisions.md` decides whether the evidence
supports a transition.

## Principle

One row is one interpreted evidence artifact. It points back to the notebook,
run output, and optional metrics. It does not replace the project ledger and
does not encode capability maturity, explanation status, promotion, kill, park,
or pivot decisions.

## Required fields

```python
{
    "project": str,
    "trial_id": str,          # e.g. trial_005_signal_flip
    "mode": str,              # rd | pure-research
    "run_timestamp": datetime,
    "verdict": str,           # observed / ambiguous / supported_candidate / rejected / partial / parked
    "notebook_path": str,
    "analysis_tier": str,     # A0-A5
}
```

Projects may add optional evidence fields such as:

```python
{
    "instrument": str,
    "timeframe": str,
    "data_start": date,
    "data_end": date,
    "split": str,
    "method": str,
    "model_type": str,
    "n_trades": int,
    "sharpe": float,
    "max_drawdown": float,
    "auc": float,
    "ic_spearman": float,
    "failure_mode": str,
    "scope_condition": str,
    "notes": str,
    "data_hash_sha256": str,
    "git_commit": str,
    "env_lock_hash": str,
}
```

Mode-specific protocol identifiers, if needed, belong in the ledger
assessment that cites the row. They are not required columns in the evidence
record.

## Failure mode vocabulary

Use one primary value when `verdict` is `rejected`, `partial`, or `parked`:

| Value | Meaning |
|---|---|
| `leakage` | Look-ahead, target leak, scaling leak, or timestamp error |
| `regime_mismatch` | Works only in a regime narrower than the claim |
| `fee_model` | Gross edge exists but realistic costs consume it |
| `wrong_horizon` | Holding period does not match the signal information horizon |
| `wrong_universe` | Result is specific to a narrower universe than claimed |
| `wrong_baseline` | Beats a weak baseline but not the relevant baseline |
| `threshold_brittleness` | Result depends on a narrow parameter optimum |
| `capacity_constraint` | Degrades materially with plausible notional / turnover |
| `signal_weakness` | No interpretable edge after checks |
| `mechanism_misspecification` | Proposed mechanism does not explain the observation |
| `power_insufficient` | Test cannot distinguish the explanations yet |
| `implementation_bug` | Correctness review invalidated the result |
| `other` | Requires a concrete explanation in `notes` |

Generic labels such as `noise`, `bad data`, or `market regime` are not valid
terminal explanations unless decomposed in `notes`.

## Append example

```python
from datetime import datetime, timezone
from aggregate_results import append_result

append_result(
    "results/results.parquet",
    {
        "project": "pca_factor_screening",
        "trial_id": "trial_005_signal_flip",
        "run_timestamp": datetime.now(timezone.utc),
        "mode": "pure-research",
        "instrument": "SPY",
        "timeframe": "D1",
        "split": "test",
        "method": "pca_factor_screening",
        "model_type": "math",
        "n_trades": 223,
        "sharpe": -1.74,
        "verdict": "rejected",
        "analysis_tier": "A3",
        "failure_mode": "regime_mismatch",
        "scope_condition": "fails outside low-volatility regime",
        "notebook_path": "purposes/trial_005_signal_flip.py",
        "notes": "Ledger assessment decides whether this weakens an explanation.",
    },
)
```

## Query examples

```python
import polars as pl

db = pl.read_parquet("results/results.parquet")

db.filter(pl.col("mode") == "rd").select(
    ["trial_id", "verdict", "analysis_tier", "notebook_path"]
)

db.group_by(["mode", "failure_mode"]).len().sort(["mode", "len"])

db.filter(pl.col("verdict") == "supported_candidate").select(
    ["trial_id", "sharpe", "analysis_tier", "notebook_path"]
)
```

## Extension rules

- Add project-specific metrics with the prefix `extra_<name>`.
- Do not change the type or meaning of common-schema columns.
- Older rows may leave new optional columns null.
- Keep state transitions in the relevant ledger; this table only indexes
  evidence.
