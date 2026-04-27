"""sensitivity_grid.py — 2D threshold sensitivity grid.

Sweep entry / exit thresholds (or any two hyperparameters) over a grid and produce a
metric (Sharpe, IC, etc.) surface.

Usage:
    from sensitivity_grid import sweep_2d, surface_summary, to_pivot

    grid = sweep_2d(
        run_backtest=lambda en, ex: backtest(entry=en, exit=ex).sharpe,
        entry_grid=[-30, -25, -20, -15, -10],
        exit_grid=[0, 5, 10],
    )
    print(grid)
    print(surface_summary(grid, threshold=0.0))
"""

from __future__ import annotations

from typing import Callable

import polars as pl


def sweep_2d(
    run_backtest: Callable[[float, float], float],
    entry_grid: list[float],
    exit_grid: list[float],
    valid_when: Callable[[float, float], bool] | None = None,
) -> pl.DataFrame:
    """Sweep a 2D grid and return a long-format DataFrame.

    Args:
        run_backtest: callable (entry_thr, exit_thr) -> metric.
        entry_grid, exit_grid: 1D lists of values.
        valid_when: predicate (entry, exit) -> bool. False cells are skipped.

    Returns:
        polars DataFrame with columns: entry, exit, metric.
    """
    rows = []
    for en in entry_grid:
        for ex in exit_grid:
            if valid_when is not None and not valid_when(en, ex):
                continue
            try:
                metric = float(run_backtest(en, ex))
            except Exception as exc:  # noqa: BLE001
                print(f"warning: ({en}, {ex}) failed: {exc}")
                continue
            rows.append({"entry": en, "exit": ex, "metric": round(metric, 4)})
    return pl.DataFrame(rows)


def surface_summary(grid: pl.DataFrame, threshold: float = 0.0) -> dict[str, float]:
    """Summarize the surface: pct_above_threshold, max, min, std."""
    if grid.is_empty():
        return {"n_cells": 0}
    arr = grid["metric"].to_numpy()
    return {
        "n_cells":          int(len(arr)),
        "max":              round(float(arr.max()), 4),
        "min":              round(float(arr.min()), 4),
        "mean":             round(float(arr.mean()), 4),
        "std":              round(float(arr.std(ddof=1)), 4) if len(arr) > 1 else 0.0,
        "pct_above_thresh": round(float((arr > threshold).mean()), 3),
    }


def to_pivot(grid: pl.DataFrame) -> pl.DataFrame:
    """Convert long-format grid to a pivot table (rows=entry, cols=exit)."""
    return grid.pivot(values="metric", index="entry", on="exit", aggregate_function="first")
