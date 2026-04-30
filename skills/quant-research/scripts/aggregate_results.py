"""aggregate_results.py — Append result rows to results/results.parquet.

Called from the final cell of an experiment notebook. The schema is documented in
references/results_db_schema.md.

Usage in Python:
    from aggregate_results import append_result
    append_result(
        db_path="results/results.parquet",
        row={
            "project": "...",
            "experiment_id": "exp_005_signal_flip",
            ...
        },
    )

Usage from CLI:
    python aggregate_results.py --db results/results.parquet --query "hypothesis_id == 'H3'"
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import polars as pl

# Required keys per the common schema (keep aligned with results_db_schema.md).
# target_sub_claim_id and pathway are required per research_goal_layer.md
# (the four-layer model that anchors every H to a project research-goal
# sub-claim) and hypothesis_generation.md (the H's generation provenance).
# parent_hypothesis_id is conditionally required (only when pathway == "4-...")
# and therefore is NOT in REQUIRED_FIELDS — append_result accepts it as an
# optional column.
REQUIRED_FIELDS = {
    "project",
    "experiment_id",
    "hypothesis_id",
    "run_timestamp",
    "instrument",
    "timeframe",
    "method",
    "model_type",
    "fee_bp_per_side",
    "n_trades",
    "sharpe",
    "notebook_path",
    "pathway",
    "target_sub_claim_id",
}


def append_result(db_path: str | Path, row: dict[str, Any]) -> pl.DataFrame:
    """Append one result row, validating that required fields are present."""
    missing = REQUIRED_FIELDS - row.keys()
    if missing:
        raise ValueError(f"Missing required fields in result row: {missing}")

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    new_df = pl.DataFrame([row])
    if db_path.exists():
        existing = pl.read_parquet(db_path)
        merged = pl.concat([existing, new_df], how="diagonal_relaxed")
    else:
        merged = new_df
    merged.write_parquet(db_path)
    return merged


def query(db_path: str | Path, expr: str | None = None) -> pl.DataFrame:
    """Read and optionally filter results.parquet."""
    db = pl.read_parquet(db_path)
    if expr:
        ctx = pl.SQLContext(results=db.lazy())
        return ctx.execute(f"select * from results where {expr}").collect()
    return db


def main() -> None:
    p = argparse.ArgumentParser(
        description="Inspect or aggregate the results.parquet database.",
    )
    p.add_argument("--db", default="results/results.parquet")
    p.add_argument(
        "--query",
        default=None,
        help="SQL where clause (e.g., \"hypothesis_id = 'H3'\")",
    )
    p.add_argument("--limit", type=int, default=20)
    args = p.parse_args()

    df = query(args.db, args.query)
    pl.Config.set_tbl_rows(args.limit)
    print(df)


if __name__ == "__main__":
    main()
