"""aggregate_results.py — Append evidence rows to results/results.parquet.

Schema documented in `references/shared/results_db_schema.md`.

Common required fields (both modes):
    project, trial_id, mode, run_timestamp, primary_metric,
    verdict, notebook_path, analysis_tier (A0-A5)

Reproducibility notes (both modes, recommended for promotion-eligible):
    data_version_note, git_commit, env_lock_ref

Usage in Python:
    from aggregate_results import append_result
    append_result("results/results.parquet", {
        "project": "measurement_reliability",
        "trial_id": "trial_007",
        "mode": "rd",
        "run_timestamp": "2026-05-03T11:00:00Z",
        "primary_metric": 0.82,
        "primary_metric_name": "replication_accuracy",
        "analysis_tier": "A4",
        "verdict": "supported_candidate",
        "notebook_path": "purposes/trial_007_*.py",
        "data_version_note": "reproducibility/data_versions.txt#2026-05-03",
        "git_commit": "...",
        "env_lock_ref": "reproducibility/env_lock_ref.txt#trial_007",
    })

Usage from CLI (query):
    python aggregate_results.py --db results/results.parquet --where "mode = 'rd' AND analysis_tier = 'A4'"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import polars as pl  # noqa: F401
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


COMMON_REQUIRED = {
    "project",
    "trial_id",
    "mode",
    "run_timestamp",
    "verdict",
    "notebook_path",
    "analysis_tier",
}

VALID_MODES = {"rd", "pure-research"}
VALID_TIERS = {"A0", "A1", "A2", "A3", "A4", "A5"}


def validate_row(row: dict[str, Any]) -> list[str]:
    """Return a list of validation error messages (empty if valid)."""
    errors: list[str] = []

    missing_common = COMMON_REQUIRED - row.keys()
    if missing_common:
        errors.append(f"missing common required fields: {sorted(missing_common)}")

    mode = row.get("mode")
    if mode not in VALID_MODES:
        errors.append(f"mode must be one of {VALID_MODES}, got {mode!r}")
    tier = row.get("analysis_tier")
    if tier and tier not in VALID_TIERS:
        errors.append(f"analysis_tier must be one of {VALID_TIERS}, got {tier!r}")

    for field in ("data_version_note", "env_lock_ref"):
        if field in row and not str(row[field]).strip():
            errors.append(f"{field} must be a non-empty string when provided")

    return errors


def append_result(db_path: str | Path, row: dict[str, Any]) -> None:
    """Append one row to the results.parquet.

    Validates per the mode-aware schema. Raises ValueError on validation
    failure. Falls back from polars to pandas if polars is not available.
    """
    errors = validate_row(row)
    if errors:
        raise ValueError("Row validation failed:\n  - " + "\n  - ".join(errors))

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if HAS_POLARS:
        import polars as pl
        new_df = pl.DataFrame([row])
        if db_path.exists():
            existing = pl.read_parquet(db_path)
            merged = pl.concat([existing, new_df], how="diagonal_relaxed")
        else:
            merged = new_df
        merged.write_parquet(db_path)
    elif HAS_PANDAS:
        new_df = pd.DataFrame([row])
        if db_path.exists():
            existing = pd.read_parquet(db_path)
            merged = pd.concat([existing, new_df], ignore_index=True, sort=False)
        else:
            merged = new_df
        merged.to_parquet(db_path, index=False)
    else:
        raise RuntimeError("Neither polars nor pandas is installed; install one to use aggregate_results")


def query(db_path: str | Path, where: str | None = None, limit: int = 50) -> Any:
    """Read and optionally filter results.parquet.

    Returns a polars DataFrame if polars is installed, else a pandas DataFrame.
    `where` is a SQL WHERE clause (works only with polars; ignored on pandas).
    """
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"results.parquet not found: {db_path}")

    if HAS_POLARS:
        import polars as pl
        db = pl.read_parquet(db_path)
        if where:
            ctx = pl.SQLContext(results=db.lazy())
            return ctx.execute(f"select * from results where {where} limit {limit}").collect()
        return db.head(limit)
    if HAS_PANDAS:
        df = pd.read_parquet(db_path)
        if where:
            print(f"WARN: --where not supported without polars; showing head({limit})", file=sys.stderr)
        return df.head(limit)
    raise RuntimeError("Neither polars nor pandas is installed")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--db", default="results/results.parquet")
    p.add_argument("--where", default=None,
                   help="SQL WHERE clause (e.g., \"mode = 'rd'\"; polars-only)")
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()

    try:
        df = query(args.db, args.where, args.limit)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Try to print as a table
    try:
        if HAS_POLARS:
            import polars as pl
            pl.Config.set_tbl_rows(args.limit)
            print(df)
        else:
            print(df.to_string())
    except Exception:
        print(df)


if __name__ == "__main__":
    main()
