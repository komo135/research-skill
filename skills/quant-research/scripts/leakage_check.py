"""leakage_check.py — Look-ahead and target-leakage checks for features.

Usage:
    from leakage_check import lookahead_check, target_leakage_check

    # look-ahead bias: feature uses future information?
    ok = lookahead_check(
        compute_features=lambda df: my_feature_pipeline(df),
        full_data=panel_pd,
        time_col="time",
        feature_cols=["rsi_14", "atr_p"],
        sample_points=10,
    )

    # target leakage: feature correlated with target abnormally
    leakage = target_leakage_check(
        features=feature_df,
        target=target_series,
    )
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def lookahead_check(
    compute_features: Callable[[pd.DataFrame], pd.DataFrame],
    full_data: pd.DataFrame,
    time_col: str,
    feature_cols: list[str],
    sample_points: int = 10,
    rtol: float = 1e-6,
) -> dict[str, list]:
    """At each sampled time t, compare features computed on data[:t] vs. on the full data.

    A mismatch indicates look-ahead bias.

    Args:
        compute_features: callable taking a DataFrame -> DataFrame with feature columns.
        full_data: complete dataset (sorted by time).
        time_col: name of the time column.
        feature_cols: columns to validate.
        sample_points: how many random points to test.
        rtol: relative tolerance for comparison.

    Returns:
        dict with 'mismatches', 'n_tested', 'n_mismatch', 'ok'.
    """
    full = full_data.sort_values(time_col).reset_index(drop=True)
    full_features = compute_features(full)

    rng = np.random.default_rng(42)
    # Avoid the very first rows where features may be NaN due to window startup
    candidates = np.arange(max(100, len(full) // 10), len(full) - 1)
    sample_idx = rng.choice(candidates, size=min(sample_points, len(candidates)), replace=False)

    mismatches = []
    for idx in sample_idx:
        truncated = full.iloc[: idx + 1].copy()
        step_features = compute_features(truncated)
        for col in feature_cols:
            full_val = full_features[col].iloc[idx]
            step_val = step_features[col].iloc[-1]
            if pd.isna(full_val) and pd.isna(step_val):
                continue
            if pd.isna(full_val) or pd.isna(step_val):
                mismatches.append((idx, col, full_val, step_val))
                continue
            if not np.isclose(full_val, step_val, rtol=rtol):
                mismatches.append((idx, col, float(full_val), float(step_val)))

    return {
        "n_tested":   len(sample_idx) * len(feature_cols),
        "n_mismatch": len(mismatches),
        "mismatches": mismatches,
        "ok":         len(mismatches) == 0,
    }


def target_leakage_check(
    features: pd.DataFrame,
    target: pd.Series,
    horizon_lag: int = 0,
) -> pd.DataFrame:
    """Compute Pearson correlation between each feature and target to flag suspicious ones.

    Args:
        features: feature DataFrame.
        target: target series (aligned with features by index).
        horizon_lag: positive = shift target into the future before comparison
            (the typical forward-return setting). 0 = same time index.

    Returns:
        DataFrame with columns: feature, corr_with_target, n_obs.
        Absolute correlation above ~0.5 is suspicious.
    """
    if horizon_lag != 0:
        target = target.shift(-horizon_lag)

    rows = []
    for col in features.columns:
        merged = pd.concat([features[col], target], axis=1).dropna()
        if len(merged) < 30:
            continue
        corr = merged.iloc[:, 0].corr(merged.iloc[:, 1])
        rows.append({"feature": col, "corr_with_target": round(float(corr), 4), "n_obs": len(merged)})
    return pd.DataFrame(rows).sort_values("corr_with_target", key=abs, ascending=False)
