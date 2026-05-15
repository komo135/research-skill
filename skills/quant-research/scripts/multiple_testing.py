"""multiple_testing.py — Multiple-hypothesis correction utilities.

Implements:
  - Bonferroni / Holm step-down (FWER)
  - Benjamini-Hochberg FDR
  - Romano-Wolf step-down via bootstrap (FWER, accounts for dependence)
  - Harvey-Liu-Zhu single-test t-hurdle (recommended t > 3.0 for new factors)

References (per `references/shared/multiple_testing.md`):
- Romano & Wolf (2005). Stepwise Multiple Testing as Formalized Data
  Snooping. *Econometrica*.
- Harvey, Liu, Zhu (2016). ...and the Cross-Section of Expected Returns.
- Benjamini & Hochberg (1995). Controlling the False Discovery Rate.

Usage:
    from multiple_testing import romano_wolf, bonferroni, holm, benjamini_hochberg

    # N strategies vs benchmark, returns matrix of shape (T, N)
    rejected, adj_p = romano_wolf(returns_matrix, n_bootstrap=1000, alpha=0.05)
"""

from __future__ import annotations

import numpy as np

HARVEY_LIU_ZHU_T_HURDLE = 3.0


# ---------------------------------------------------------------------------
# Single-step methods
# ---------------------------------------------------------------------------


def bonferroni(pvalues: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """Bonferroni FWER correction.

    Returns:
        (rejected_mask, adjusted_pvalues)
    """
    pvalues = np.asarray(pvalues, dtype=float)
    n = len(pvalues)
    adj = np.minimum(pvalues * n, 1.0)
    rejected = adj <= alpha
    return rejected, adj


def holm(pvalues: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """Holm step-down (FWER, more powerful than Bonferroni).

    Returns:
        (rejected_mask, adjusted_pvalues)
    """
    pvalues = np.asarray(pvalues, dtype=float)
    n = len(pvalues)
    order = np.argsort(pvalues)
    sorted_p = pvalues[order]
    raw_adjusted = np.minimum(sorted_p * (n - np.arange(n)), 1.0)
    adj_sorted = np.maximum.accumulate(raw_adjusted)
    adj = np.empty(n)
    adj[order] = adj_sorted
    rejected = adj <= alpha
    return rejected, adj


def benjamini_hochberg(pvalues: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """Benjamini-Hochberg FDR (less conservative than FWER methods).

    Returns:
        (rejected_mask, adjusted_pvalues)
    """
    pvalues = np.asarray(pvalues, dtype=float)
    n = len(pvalues)
    order = np.argsort(pvalues)
    sorted_p = pvalues[order]
    ranks = np.arange(1, n + 1)
    bh = sorted_p * n / ranks
    # Enforce monotonicity (cumulative min from the right)
    bh_sorted = np.minimum.accumulate(bh[::-1])[::-1]
    bh_sorted = np.minimum(bh_sorted, 1.0)
    adj = np.empty(n)
    adj[order] = bh_sorted
    rejected = adj <= alpha
    return rejected, adj


# ---------------------------------------------------------------------------
# Romano-Wolf step-down (with stationary bootstrap for dependence)
# ---------------------------------------------------------------------------


def romano_wolf(
    returns_matrix: np.ndarray,
    *,
    n_bootstrap: int = 1000,
    alpha: float = 0.05,
    block_mean: float | None = None,
    seed: int = 42,
    null_mean: float = 0.0,
) -> dict[str, np.ndarray | float]:
    """Romano-Wolf step-down for testing N strategies' Sharpe vs a null.

    Tests the hypothesis: H0_n: E[returns_n] = null_mean (typically 0).

    Uses stationary bootstrap (Politis & Romano 1994) to preserve the
    cross-sectional dependence structure of the test statistics.

    Args:
        returns_matrix: shape (T, N). Per-period returns of N strategies.
        n_bootstrap: number of bootstrap replications.
        alpha: FWER level.
        block_mean: mean block length for stationary bootstrap (default:
            sqrt(T)).
        seed: RNG seed.
        null_mean: null hypothesis value (default 0).

    Returns:
        dict with:
            t_stats: observed t-statistics (mean - null_mean) / SE
            adj_pvalues: Romano-Wolf-adjusted p-values
            rejected: boolean mask of rejections at alpha
            n_rejected: count of rejected hypotheses
    """
    M = np.asarray(returns_matrix, dtype=float)
    if M.ndim != 2:
        raise ValueError(f"returns_matrix must be 2D, got shape {M.shape}")
    T, N = M.shape
    if T < 30:
        raise ValueError(f"T={T} too small for bootstrap (need ≥ 30)")

    if block_mean is None:
        block_mean = float(np.sqrt(T))

    rng = np.random.default_rng(seed)

    # Observed t-statistics
    means = M.mean(axis=0) - null_mean
    stds = M.std(axis=0, ddof=1)
    se = stds / np.sqrt(T)
    t_obs = means / (se + 1e-12)

    # Bootstrap distribution of t-statistics under H0 (centered means)
    centered = M - M.mean(axis=0)  # remove sample mean to simulate H0
    p = 1.0 / block_mean
    t_boot = np.empty((n_bootstrap, N))
    for b in range(n_bootstrap):
        # Stationary bootstrap indices
        idx = np.empty(T, dtype=np.int64)
        idx[0] = rng.integers(0, T)
        flips = rng.random(T - 1) < p
        fresh = rng.integers(0, T, size=T - 1)
        for i in range(1, T):
            if flips[i - 1]:
                idx[i] = fresh[i - 1]
            else:
                idx[i] = (idx[i - 1] + 1) % T
        sample = centered[idx]
        sample_means = sample.mean(axis=0)
        sample_stds = sample.std(axis=0, ddof=1)
        t_boot[b] = sample_means / (sample_stds / np.sqrt(T) + 1e-12)

    # Romano-Wolf step-down
    # Order hypotheses by |t_obs| descending
    order = np.argsort(-np.abs(t_obs))
    adj_pvalues = np.zeros(N)
    rejected = np.zeros(N, dtype=bool)
    remaining = list(order)
    while remaining:
        # For the remaining hypotheses, compute the bootstrap distribution
        # of max |t| over them
        sub_t_boot = t_boot[:, remaining]
        max_abs_t_boot = np.abs(sub_t_boot).max(axis=1)
        # Test the most extreme remaining hypothesis
        first = remaining[0]
        crit = np.quantile(max_abs_t_boot, 1 - alpha)
        p_value = float((max_abs_t_boot >= abs(t_obs[first])).mean())
        adj_pvalues[first] = p_value
        if abs(t_obs[first]) > crit:
            rejected[first] = True
            remaining.pop(0)
        else:
            # All remaining hypotheses are NOT rejected
            for r in remaining:
                if adj_pvalues[r] == 0:
                    adj_pvalues[r] = p_value  # at least this large
            break

    return {
        "t_stats":     t_obs,
        "adj_pvalues": adj_pvalues,
        "rejected":    rejected,
        "n_rejected":  int(rejected.sum()),
    }


# ---------------------------------------------------------------------------
# Harvey-Liu-Zhu hurdle
# ---------------------------------------------------------------------------


def harvey_liu_zhu_check(t_stat: float, t_hurdle: float = HARVEY_LIU_ZHU_T_HURDLE) -> dict[str, object]:
    """Single-test hurdle for new financial factors.

    Per Harvey, Liu, Zhu (2016): given the field's accumulated testing
    density, new factors should clear t > 3.0 to maintain a reasonable
    false-discovery rate.

    Args:
        t_stat: observed t-statistic of the factor / strategy claim.
        t_hurdle: threshold (default 3.0).

    Returns:
        dict with: t_stat, t_hurdle, passes, margin (t_stat - t_hurdle).
    """
    return {
        "t_stat":    float(t_stat),
        "t_hurdle":  float(t_hurdle),
        "passes":    abs(t_stat) >= t_hurdle,
        "margin":    round(abs(t_stat) - t_hurdle, 3),
    }
