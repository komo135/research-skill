"""walk_forward.py — Compute Sharpe (or any metric) distribution over rolling windows.

Usage:
    from walk_forward import walk_forward_sharpe

    stats, per_window = walk_forward_sharpe(
        run_backtest=lambda df: vbt.Portfolio.from_signals(
            df["close"], df["entry"], df["exit"]
        ).sharpe_ratio(),
        data=panel_pd,
        window="3MS",
        min_rows=1000,
    )
    print(stats)        # mean, std, p05, p50, p95, pct_positive
    print(per_window)   # per-window values
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def walk_forward_sharpe(
    run_backtest: Callable[[pd.DataFrame], float],
    data: pd.DataFrame,
    window: str = "3MS",
    min_rows: int = 1000,
) -> tuple[dict[str, float], pd.DataFrame]:
    """Apply run_backtest to each rolling window of `data` and aggregate.

    Args:
        run_backtest: callable returning a scalar metric per window.
        data: pandas DataFrame indexed by time.
        window: pandas frequency string (e.g. "3MS" = 3-month start).
        min_rows: skip windows shorter than this.

    Returns:
        stats: dict with mean / std / p05 / p50 / p95 / pct_positive / n_windows / worst.
        per_window: DataFrame with one row per window.
    """
    assert isinstance(data.index, pd.DatetimeIndex), "data must be time-indexed"
    starts = pd.date_range(
        start=data.index.min().normalize(),
        end=data.index.max().normalize(),
        freq=window,
        tz=data.index.tz,
    )

    rows = []
    for s, e in zip(starts[:-1], starts[1:]):
        sub = data[(data.index >= s) & (data.index < e)]
        if len(sub) < min_rows:
            continue
        try:
            metric = float(run_backtest(sub))
        except Exception as exc:  # noqa: BLE001
            metric = float("nan")
            print(f"warning: window {s.date()} failed: {exc}")
        rows.append({"window_start": s.date(), "n_rows": len(sub), "metric": metric})

    per_window = pd.DataFrame(rows)
    if per_window.empty or per_window["metric"].isna().all():
        return {"n_windows": 0}, per_window

    arr = per_window["metric"].dropna().to_numpy()
    stats = {
        "n_windows":    int(len(arr)),
        "mean":         round(float(arr.mean()), 3),
        "std":          round(float(arr.std(ddof=1)) if len(arr) > 1 else 0.0, 3),
        "p05":          round(float(np.percentile(arr, 5)), 3),
        "p50":          round(float(np.percentile(arr, 50)), 3),
        "p95":          round(float(np.percentile(arr, 95)), 3),
        "pct_positive": round(float((arr > 0).mean()), 3),
        "worst":        round(float(arr.min()), 3),
    }
    return stats, per_window
