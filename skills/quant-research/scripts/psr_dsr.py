"""psr_dsr.py — Probabilistic and Deflated Sharpe Ratio.

Bailey & López de Prado (2012, 2014). See references/psr_dsr_formulas.md.

Usage:
    from psr_dsr import psr, dsr, expected_max_sr

    psr_value = psr(sr_obs=1.45, sr_threshold=0.0, T=252, skew=-0.2, kurt=4.5)
    print(f"PSR(0): {psr_value:.4f}")

    dsr_value = dsr(
        sr_obs=1.45, T=252, skew=-0.2, kurt=4.5,
        n_trials=20, var_sr=0.5,
    )
    print(f"DSR: {dsr_value:.4f}")
"""

from __future__ import annotations

import numpy as np
from scipy import stats

EULER_MASCHERONI = 0.5772156649


def psr(sr_obs: float, sr_threshold: float, T: int, skew: float, kurt: float) -> float:
    """Probabilistic Sharpe Ratio.

    Args:
        sr_obs: observed Sharpe (annualized or per-trade; keep T consistent).
        sr_threshold: comparison Sharpe (e.g. 0).
        T: number of return observations.
        skew: skewness of observed returns.
        kurt: raw kurtosis of observed returns.

    Returns:
        Probability in [0, 1] that the true Sharpe exceeds the threshold.
    """
    numerator = (sr_obs - sr_threshold) * np.sqrt(T - 1)
    denominator = np.sqrt(1 - skew * sr_obs + (kurt - 1) / 4 * sr_obs**2)
    return float(stats.norm.cdf(numerator / denominator))


def expected_max_sr(n_trials: int, var_sr: float) -> float:
    """E[max SR over N trials] under the null (Bailey & López de Prado 2014)."""
    if n_trials < 2:
        return 0.0
    a = (1 - EULER_MASCHERONI) * stats.norm.ppf(1 - 1 / n_trials)
    b = EULER_MASCHERONI * stats.norm.ppf(1 - 1 / (n_trials * np.e))
    return float(np.sqrt(var_sr) * (a + b))


def dsr(
    sr_obs: float,
    T: int,
    skew: float,
    kurt: float,
    n_trials: int,
    var_sr: float,
) -> float:
    """Deflated Sharpe Ratio: PSR with threshold = E[max SR over trials].

    Args:
        sr_obs: observed Sharpe.
        T: number of return observations.
        skew, kurt: observed-return skewness and raw kurtosis.
        n_trials: number of hyperparameter / model settings tried.
        var_sr: variance of Sharpe across trials.

    Returns:
        Probability in [0, 1] that the observed Sharpe is non-spurious after
        multi-comparison correction.
    """
    sr_threshold = expected_max_sr(n_trials, var_sr)
    return psr(sr_obs, sr_threshold, T, skew, kurt)


def from_returns(
    returns: np.ndarray,
    sr_threshold: float = 0.0,
    n_trials: int = 1,
    var_sr: float | None = None,
) -> dict[str, float]:
    """Compute PSR and (if n_trials > 1) DSR directly from a return series.

    Args:
        returns: 1D array of returns (per-period, e.g. daily).
        sr_threshold: PSR threshold.
        n_trials: trial count used for DSR.
        var_sr: variance of SR across trials. None disables DSR.

    Returns:
        dict with sr, T, skew, kurt, psr, [dsr, expected_max_sr].
    """
    returns = np.asarray(returns, dtype=float)
    T = len(returns)
    sr = float(returns.mean() / (returns.std(ddof=1) + 1e-12))
    skew = float(stats.skew(returns))
    kurt = float(stats.kurtosis(returns, fisher=False))  # raw kurtosis

    out = {
        "T":     T,
        "sr":    round(sr, 4),
        "skew":  round(skew, 4),
        "kurt":  round(kurt, 4),
        "psr":   round(psr(sr, sr_threshold, T, skew, kurt), 4),
    }
    if n_trials > 1 and var_sr is not None:
        out["dsr"] = round(dsr(sr, T, skew, kurt, n_trials, var_sr), 4)
        out["expected_max_sr"] = round(expected_max_sr(n_trials, var_sr), 4)
    return out
