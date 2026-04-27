"""vol_targeted_size.py — Position sizing with size proportional to 1 / volatility.

Per-instrument and per-timestamp position sizes are inversely proportional to volatility
(ATR or rolling std), keeping the portfolio's volatility roughly constant.

Usage:
    from vol_targeted_size import vol_targeted_size

    sizes = vol_targeted_size(
        atr=atr_series,             # ATR in price units (NOT pct)
        close=close_series,
        target_vol_annual=0.10,     # 10% annualized target vol
        bars_per_year=252 * 288,    # example for 5-min bars
    )
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def vol_targeted_size(
    atr: pd.Series,
    close: pd.Series,
    target_vol_annual: float = 0.10,
    bars_per_year: int = 252,
) -> pd.Series:
    """Compute position size (as a fraction of equity) inversely proportional to ATR.

    Args:
        atr: rolling ATR in price units, time-indexed.
        close: close price aligned with atr.
        target_vol_annual: desired portfolio annualized volatility.
        bars_per_year: number of bars per year.

    Returns:
        Series of position sizes (decimal of equity, capped at 1.0).
    """
    bar_vol = atr / close
    target_vol_per_bar = target_vol_annual / np.sqrt(bars_per_year)
    sizes = target_vol_per_bar / bar_vol
    return sizes.replace([np.inf, -np.inf], np.nan).clip(upper=1.0)


def equal_weight_size(n_positions: int, leverage: float = 1.0) -> float:
    """Equal weight across n positions."""
    if n_positions == 0:
        return 0.0
    return leverage / n_positions


def kelly_size(
    edge_per_trade: float,
    variance_per_trade: float,
    fraction: float = 0.5,
) -> float:
    """Kelly fraction (defaults to half-Kelly).

    Args:
        edge_per_trade: expected return per trade (decimal).
        variance_per_trade: variance of per-trade return.
        fraction: 0.5 for half-Kelly (recommended).

    Returns:
        Position size as a fraction of equity.
    """
    if variance_per_trade <= 0:
        return 0.0
    kelly = edge_per_trade / variance_per_trade
    return max(0.0, fraction * kelly)
