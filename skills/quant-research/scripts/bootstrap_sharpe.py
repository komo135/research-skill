"""bootstrap_sharpe.py — Block-bootstrap confidence interval for per-trade Sharpe.

Block bootstrap preserves time-series dependence during resampling. Default block size
is sqrt(n) (a common choice; see Politis & Romano 1994).

Usage:
    from bootstrap_sharpe import bootstrap_sharpe_ci

    stats = bootstrap_sharpe_ci(
        returns=trade_returns,        # 1D numpy array of per-trade returns
        n_resample=10000,
        block=None,                   # auto = sqrt(n)
        seed=42,
    )
    print(stats)  # actual, mean, ci_low, ci_high, p_value
"""

from __future__ import annotations

import numpy as np


def bootstrap_sharpe_ci(
    returns: np.ndarray,
    n_resample: int = 10000,
    block: int | None = None,
    seed: int = 42,
    ci: float = 0.95,
) -> dict[str, float]:
    """Block-bootstrap CI for per-trade Sharpe (= mean / std).

    Args:
        returns: 1D array of per-trade returns.
        n_resample: number of bootstrap resamples.
        block: block size (default sqrt(n)).
        seed: RNG seed.
        ci: confidence level (e.g. 0.95).

    Returns:
        dict with actual, boot_mean, ci_low, ci_high, p_value (P[SR <= 0]).
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)
    if n < 30:
        raise ValueError(f"Too few samples for bootstrap: n={n}")

    if block is None:
        block = max(1, int(np.sqrt(n)))

    rng = np.random.default_rng(seed)
    actual = float(returns.mean() / (returns.std() + 1e-12))

    n_blocks = int(np.ceil(n / block))
    boot_sharpes = np.empty(n_resample)
    for i in range(n_resample):
        starts = rng.integers(0, n - block + 1, size=n_blocks)
        sample = np.concatenate([returns[s:s + block] for s in starts])[:n]
        boot_sharpes[i] = sample.mean() / (sample.std() + 1e-12)

    alpha = (1 - ci) / 2
    ci_low = float(np.percentile(boot_sharpes, alpha * 100))
    ci_high = float(np.percentile(boot_sharpes, (1 - alpha) * 100))
    p_value = float((boot_sharpes <= 0).mean())

    return {
        "n_samples":  n,
        "block_size": block,
        "actual":     round(actual, 4),
        "boot_mean":  round(float(boot_sharpes.mean()), 4),
        "ci_low":     round(ci_low, 4),
        "ci_high":    round(ci_high, 4),
        "p_value":    round(p_value, 4),
    }


def annualized(per_trade_sr: float, n_trades_per_year: int) -> float:
    """Convert per-trade Sharpe to annualized."""
    return per_trade_sr * np.sqrt(n_trades_per_year)
