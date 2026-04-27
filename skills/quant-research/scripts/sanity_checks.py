"""sanity_checks.py — Bug-detection helpers for quant-research notebooks.

Programmatic side of the multi-agent bug-review layer. See
`references/bug_review.md` and `references/sanity_checks.md`.

Helpers are deliberately small and pure so a reviewer can verify the helper itself
before trusting its output. Each helper takes a callable representing the user's
evaluation pipeline and returns a small dict / DataFrame.

Conventions:
    - run_pipeline(signal: pd.Series) -> dict with keys 'sharpe' and 'pnl' (pd.Series).
    - fit_score(target: pd.Series) -> float (a metric where chance level is 0.5 for
      AUC, 0.0 for IC).
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
import pandas as pd


def random_signal_benchmark(
    run_pipeline: Callable[[pd.Series], dict],
    index: pd.Index,
    n_trials: int = 100,
    seed: int = 42,
) -> dict:
    """Run run_pipeline with i.i.d. ±1 signals; return the Sharpe distribution.

    Pass condition: |median sharpe| < 0.5 across trials, and the real-signal Sharpe is
    outside the 95 % CI of this distribution (the caller compares).
    """
    rng = np.random.default_rng(seed)
    sharpes: list[float] = []
    for _ in range(n_trials):
        sig = pd.Series(rng.choice([-1, 1], size=len(index)), index=index)
        out = run_pipeline(sig)
        sharpes.append(float(out["sharpe"]))
    arr = np.asarray(sharpes)
    return {
        "n_trials":      n_trials,
        "sharpe_mean":   float(arr.mean()),
        "sharpe_median": float(np.median(arr)),
        "sharpe_p2_5":   float(np.percentile(arr, 2.5)),
        "sharpe_p97_5":  float(np.percentile(arr, 97.5)),
        "ok":            abs(np.median(arr)) < 0.5,
    }


def shuffled_target_test(
    fit_score: Callable[[pd.Series], float],
    target: pd.Series,
    n_shuffles: int = 20,
    block_size: int = 1,
    seed: int = 42,
) -> dict:
    """Permute target (block-wise if block_size > 1), refit, return metric distribution.

    Pass condition (caller checks): metric distribution is centered on the chance level
    (0.5 for AUC, 0.0 for IC) and the real-signal metric is outside the 95 % band.
    """
    rng = np.random.default_rng(seed)
    n = len(target)
    metrics: list[float] = []
    for _ in range(n_shuffles):
        if block_size <= 1:
            perm = rng.permutation(n)
        else:
            n_blocks = max(n // block_size, 1)
            block_perm = rng.permutation(n_blocks)
            perm = np.concatenate(
                [np.arange(b * block_size, (b + 1) * block_size) for b in block_perm]
            )
            perm = perm[:n]
        shuffled_values = target.to_numpy()[perm]
        shuffled = pd.Series(shuffled_values, index=target.index)
        metrics.append(float(fit_score(shuffled)))
    arr = np.asarray(metrics)
    return {
        "n_shuffles": n_shuffles,
        "mean":       float(arr.mean()),
        "std":        float(arr.std(ddof=1) if n_shuffles > 1 else 0.0),
        "p2_5":       float(np.percentile(arr, 2.5)),
        "p97_5":      float(np.percentile(arr, 97.5)),
        "samples":    arr.tolist(),
    }


def pnl_reconciliation(
    position: pd.Series,
    price:    pd.Series,
    fee:      float = 0.0,
    realized_pnl: pd.Series | None = None,
    rtol:     float = 1e-9,
) -> dict:
    """Recompute PnL using the documented identity and (optionally) compare against realized.

    The identity assumed:
        pnl[t] = position[t-1] * (price[t] - price[t-1]) - |Δposition[t]| * fee * price[t]

    This is the textbook lagged-position convention. If the notebook uses a different
    convention (e.g. signal[t] * fwd_ret[t]), pass the equivalent `position` series so
    the comparison is meaningful.
    """
    pos = position.astype(float)
    pr  = price.astype(float)
    cost = pos.diff().abs().fillna(0.0) * fee * pr
    pnl_recon = (pos.shift(1) * pr.diff()).fillna(0.0) - cost
    out: dict = {"cum_pnl_recon": float(pnl_recon.cumsum().iloc[-1])}
    if realized_pnl is not None:
        cum_reported = float(realized_pnl.cumsum().iloc[-1])
        diff = cum_reported - out["cum_pnl_recon"]
        scale = max(abs(cum_reported), 1.0)
        out.update({
            "cum_pnl_reported": cum_reported,
            "rel_diff":         float(diff / scale),
            "ok":               abs(diff / scale) < rtol,
        })
    return out


def cost_monotonicity(
    run_with_fee: Callable[[float], float],
    fee_grid:     Sequence[float],
) -> dict:
    """Sweep fee, return whether net PnL is monotonically non-increasing.

    run_with_fee(fee) -> scalar net PnL (e.g. cumulative or annualized).
    """
    pnls = [float(run_with_fee(f)) for f in fee_grid]
    monotone = all(pnls[i] >= pnls[i + 1] - 1e-12 for i in range(len(pnls) - 1))
    return {
        "fee_grid": list(fee_grid),
        "pnls":     pnls,
        "monotone": bool(monotone),
        "ok":       bool(monotone),
    }


def sign_flip_test(
    run_pipeline: Callable[[pd.Series], dict],
    signal:       pd.Series,
    cost_per_bar: float | None = None,
    rtol:         float = 0.1,
) -> dict:
    """Compare PnL of signal vs. -signal. With zero costs they should mirror.

    With non-zero `cost_per_bar` (a scalar floor for round-trip cost over the period),
    the expected asymmetry is 2 × cost_per_bar; the test passes if observed asymmetry
    is within `rtol` × |PnL_orig| of that target.
    """
    out_pos = run_pipeline(signal)
    out_neg = run_pipeline(-signal)
    pnl_pos = float(_total(out_pos["pnl"]))
    pnl_neg = float(_total(out_neg["pnl"]))
    expected_asym = 2.0 * (cost_per_bar or 0.0)
    observed_asym = abs(pnl_pos + pnl_neg)
    base = max(abs(pnl_pos), abs(pnl_neg), 1e-12)
    deviation = abs(observed_asym - expected_asym) / base
    return {
        "pnl_pos":       pnl_pos,
        "pnl_neg":       pnl_neg,
        "observed_asym": observed_asym,
        "expected_asym": expected_asym,
        "deviation":     deviation,
        "ok":            deviation < rtol,
    }


def nan_inf_scan(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-column counts of NaN and Inf, sorted by NaN count descending."""
    rows = []
    for col in df.columns:
        s = df[col]
        n_nan = int(s.isna().sum())
        if pd.api.types.is_numeric_dtype(s):
            n_inf = int(np.isinf(s.to_numpy(dtype=float, na_value=np.nan)).sum())
        else:
            n_inf = 0
        rows.append({
            "column":  col,
            "n_nan":   n_nan,
            "n_inf":   n_inf,
            "pct_nan": n_nan / max(len(s), 1),
        })
    return pd.DataFrame(rows).sort_values("n_nan", ascending=False).reset_index(drop=True)


def time_shift_placebo(
    run_pipeline: Callable[[pd.Series], dict],
    signal:       pd.Series,
    shifts:       Sequence[int] = (-3, -2, -1, 0, 1, 2, 3),
) -> pd.DataFrame:
    """Sweep shift k; report Sharpe at each.

    k > 0  -> signal moved into the future (delayed)        : should DEGRADE Sharpe.
    k = 0  -> baseline.
    k < 0  -> signal moved into the past   (peeking ahead)  : should IMPROVE Sharpe.

    Improvement at k > 0 is a smoking gun for an existing forward leak of size |k|.
    """
    rows = []
    for k in shifts:
        sig = signal.shift(k)
        out = run_pipeline(sig)
        rows.append({"shift_bars": int(k), "sharpe": float(out["sharpe"])})
    return pd.DataFrame(rows)


def _total(pnl) -> float:
    if hasattr(pnl, "sum"):
        return float(pnl.sum())
    return float(pnl)
