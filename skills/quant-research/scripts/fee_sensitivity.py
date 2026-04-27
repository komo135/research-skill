"""fee_sensitivity.py — Fee sensitivity sweep with break-even fee extraction.

Usage:
    from fee_sensitivity import fee_sweep, breakeven_fee

    rows = fee_sweep(
        run_backtest=lambda fee: vbt.Portfolio.from_signals(
            close, entries, exits, fees=fee, freq="5min"
        ).sharpe_ratio(),
        fees_bp=[0, 0.2, 0.5, 1.0, 1.5, 2.0],
    )
    print(rows)
    be = breakeven_fee(rows, target=0.0)
    print(f"breakeven fee: {be} bp/side")
"""

from __future__ import annotations

from typing import Callable

import polars as pl


def fee_sweep(
    run_backtest: Callable[[float], float],
    fees_bp: list[float] | None = None,
) -> pl.DataFrame:
    """Run backtest at multiple fee levels and tabulate the chosen metric.

    Args:
        run_backtest: callable taking fee (decimal, e.g. 0.0001 for 1 bp) and returning
            a metric.
        fees_bp: list of fees in bp/side. Default [0, 0.2, 0.5, 1.0, 1.5, 2.0].

    Returns:
        polars DataFrame with columns: fee_bp_per_side, metric.
    """
    if fees_bp is None:
        fees_bp = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0]

    rows = []
    for fee_bp in fees_bp:
        fee = fee_bp / 1e4
        metric = float(run_backtest(fee))
        rows.append({"fee_bp_per_side": fee_bp, "metric": round(metric, 4)})
    return pl.DataFrame(rows)


def breakeven_fee(sweep: pl.DataFrame, target: float = 0.0) -> float | None:
    """Linearly interpolate to find the fee at which metric crosses the target.

    Args:
        sweep: output of fee_sweep().
        target: target metric value (default 0 for Sharpe break-even).

    Returns:
        fee in bp/side at which metric == target, or None if metric never crosses.
    """
    rows = sweep.sort("fee_bp_per_side").to_dicts()
    for prev, curr in zip(rows, rows[1:]):
        if (prev["metric"] - target) * (curr["metric"] - target) <= 0:
            x0, y0 = prev["fee_bp_per_side"], prev["metric"]
            x1, y1 = curr["fee_bp_per_side"], curr["metric"]
            if y1 == y0:
                return x0
            t = (target - y0) / (y1 - y0)
            return round(x0 + t * (x1 - x0), 3)
    return None
