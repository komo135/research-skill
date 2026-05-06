# results_db_schema.md

Common schema for appending queryable evidence records to
`results/results.parquet`, or for exporting an equivalent compact index from
an external tracker such as MLflow, Weights & Biases, Neptune, Trackio,
TensorBoard, Sacred, DVC, or an organizational experiment store.

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

If the project uses an external tracker, read this file as the minimum
interchange schema reviewers need. The tracker may store richer params,
metrics, artifacts, and lineage; the project still needs a durable way to map
`trial_id` to the tracker run record and to enumerate every load-bearing run
that counts for multiple-testing review.

## Principle

One row is one interpreted evidence artifact. It points back to the notebook,
run output, tracker record, and optional metrics. It does not replace the
project ledger and does not encode capability maturity, explanation status,
promotion, kill, park, or pivot decisions.

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
    "tracker": str,           # mlflow | wandb | neptune | trackio | dvc | local | other
    "tracking_uri": str,
    "run_id": str,
    "artifact_uri": str,
    "data_hash_sha256": str,
    "git_commit": str,
    "env_lock_hash": str,
}
```

These fields are optional only for exploratory rows and for local rows where
the information is stored in the local stamp files. They become required under
the conditions below.

## Conditional required fields

When an external tracker is the canonical run store, every load-bearing,
promotion-eligible, or claim-cited row must include:

```python
{
    "tracker": str,
    "tracking_uri": str,
    "run_id": str,
    "artifact_uri": str,
    "data_hash_sha256": str,
    "git_commit": str,
    "env_lock_hash": str,
    "seed": str,
}
```

When local stamp/parquet is the canonical run store, the same anchors may live
in `reproducibility/data_hashes.txt`, `results/results.parquet`,
`reproducibility/env_lock_hash.txt`, and `reproducibility/seed.txt`, but the
row or ledger citation must tell reviewers where to find them.

## Complete run inventory / export

For promotion review and multiple-testing correction, the project needs a
complete inventory of all load-bearing and promotion-eligible attempts, not
only the cited successful runs. The inventory may be:

- `results/results.parquet` when it is the canonical complete record.
- An exported tracker table from MLflow, W&B, Neptune, Trackio, TensorBoard,
  Sacred, DVC, or an organizational tracker.
- A durable file under `tracking/` that maps local run notes to the fields
  above.

The inventory must include failed runs, abandoned parameter combinations,
model-selection attempts, and robustness variants whenever they informed the
research decision or count toward trial-count / DSR / Bonferroni / Romano-Wolf
correction. A compact local index may point to external artifacts, but it must
not hide uncited or failed attempts.

Mode-specific protocol identifiers, if needed, belong in the ledger
assessment that cites the row. They are not required columns in the evidence
record.

## Tracking backend selection

Choose the backend with the user before the first load-bearing trial. Record
the choice in `decisions.md`:

```markdown
## YYYY-MM-DD tracking backend selected

Backend: <MLflow / W&B / Neptune / Trackio / DVC / local parquet / other>
Storage: <local path, tracking URI, remote project, or registry>
Reason: <why this fits this research and collaboration model>
Review retrieval: <how a reviewer resolves trial_id -> run record>
Minimum persisted fields: trial_id, run_id, artifact_uri, data hash,
git commit, env lock hash, seed, params, headline metrics
Run inventory/export: <path or tracker query covering all load-bearing,
promotion-eligible, failed, parameter-sweep, and model-selection attempts>
```

Do not write a custom tracker just because this skill includes helper scripts.
Use a mature tracker when it reduces operational risk or improves
collaboration. The local parquet schema remains useful as a portable export,
cache, or review index even when the canonical run record is external.

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
        "tracker": "mlflow",
        "tracking_uri": "file:./mlruns",
        "run_id": "7e4d2c...",
        "artifact_uri": "file:./mlruns/0/7e4d2c.../artifacts",
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
- If an external tracker is canonical, keep enough local index information for
  offline review: tracker name, run ID, artifact URI, and exported metrics
  needed by promotion review.
