"""vol_targeted_size.py — Position sizing using volatility targeting.

Per `references/shared/portfolio_construction.md` § Sizing options.

ATR / std relationship: ATR is essentially the average absolute true range,
which is a Mean-Absolute-Deviation-style estimator. Under approximately
normal returns, std ≈ MAD × √(π/2) ≈ MAD × 1.2533. The function
`atr_to_std` performs this conversion (with an `assume` parameter so the
caller declares whether they're providing ATR-as-MAD or ATR-as-std).

Per the review: silently treating ATR as std under-estimates true volatility
by ~25%, causing the vol-targeting routine to assign positions ~25% larger
than the target_vol implies. The conversion is mandatory for honest sizing.

Signed positions: `vol_targeted_size` returns a positive scalar size; for
directional strategies, the caller multiplies by the signal direction (±1).
The previous version's `clip(upper=1.0)` floor at 0 has been removed —
sizing is direction-agnostic; the caller composes sign × magnitude.
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np
import pandas as pd

# Std / MAD conversion under normality (E[|X|] / σ for X ~ N(0,1))
# = sqrt(2/π); inverse for std-from-MAD is sqrt(π/2)
STD_OVER_MAD_NORMAL = math.sqrt(math.pi / 2)  # ≈ 1.2533


def atr_to_std(
    atr: pd.Series | float,
    *,
    assume: Literal["mad", "std"] = "mad",
) -> pd.Series | float:
    """Convert an ATR-style measure to a standard-deviation-equivalent.

    Args:
        atr: ATR series or scalar (in price units).
        assume: "mad" if ATR is mean absolute deviation (the typical case
            for Wilder ATR / ATR-as-average-true-range); "std" if the user
            has already passed a standard-deviation estimator and wants
            no conversion.

    Returns:
        A series / scalar in std units (price units).
    """
    if assume == "std":
        return atr
    return atr * STD_OVER_MAD_NORMAL


def vol_targeted_size(
    atr: pd.Series,
    close: pd.Series,
    *,
    target_vol_annual: float = 0.10,
    bars_per_year: int = 252,
    atr_assume: Literal["mad", "std"] = "mad",
    cap: float | None = 1.0,
) -> pd.Series:
    """Compute position size (fraction of equity) inversely proportional to vol.

    Args:
        atr: ATR (price units), time-indexed. Per Wilder, this is a MAD-style
            measure; pass `atr_assume="mad"` (default) to apply √(π/2)
            conversion.
        close: close price aligned with atr.
        target_vol_annual: desired portfolio annualized volatility (decimal).
        bars_per_year: bars per year (e.g., 252 for daily, 252*78 for 5-min).
        atr_assume: "mad" or "std" — what kind of estimator the input ATR is.
        cap: maximum size (default 1.0 = fully invested no leverage). Set
            None to allow unbounded sizing (caller manages leverage budget).

    Returns:
        Series of POSITIVE position sizes (fraction of equity). The caller
        multiplies by signal direction (±1) for long/short.
    """
    sigma_per_bar_price = atr_to_std(atr, assume=atr_assume)
    bar_vol_pct = sigma_per_bar_price / close
    target_vol_per_bar = target_vol_annual / np.sqrt(bars_per_year)
    sizes = target_vol_per_bar / (bar_vol_pct + 1e-12)
    sizes = sizes.replace([np.inf, -np.inf], np.nan)
    if cap is not None:
        sizes = sizes.clip(upper=cap)
    return sizes


def equal_weight_size(n_positions: int, leverage: float = 1.0) -> float:
    """Equal weight across n positions."""
    if n_positions == 0:
        return 0.0
    return leverage / n_positions


def kelly_size(
    edge_per_trade: float,
    variance_per_trade: float,
    *,
    fraction: float = 0.5,
    allow_negative: bool = True,
) -> float:
    """Kelly fraction (defaults to half-Kelly).

    Args:
        edge_per_trade: expected return per trade (decimal). Sign-bearing.
        variance_per_trade: variance of per-trade return (must be positive).
        fraction: 0.5 for half-Kelly (recommended; full-Kelly is fragile).
        allow_negative: if True, negative edge → negative Kelly (short or
            reduce). If False (legacy behavior), negative edge → 0 (no trade).

    Returns:
        Kelly position size (signed if allow_negative).
    """
    if variance_per_trade <= 0:
        return 0.0
    kelly = edge_per_trade / variance_per_trade
    sized = fraction * kelly
    if not allow_negative:
        sized = max(0.0, sized)
    return sized
