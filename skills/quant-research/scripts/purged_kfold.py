"""purged_kfold.py — Purged k-fold cross-validation (López de Prado, AFML chapter 7).

When time-series data has overlapping labels, train samples whose label horizon overlaps
the validation fold are purged, and an embargo is inserted around each validation fold.

Usage:
    from purged_kfold import PurgedKFold

    cv = PurgedKFold(n_splits=5, embargo=12, label_horizon=12)
    for train_idx, val_idx in cv.split(X, target_times=target_end_times):
        model.fit(X[train_idx], y[train_idx])
        score = model.score(X[val_idx], y[val_idx])
"""

from __future__ import annotations

from typing import Iterator

import numpy as np
import pandas as pd


class PurgedKFold:
    """Purged k-fold CV for time-series with overlapping labels.

    Args:
        n_splits: number of folds.
        embargo: number of samples to drop on each side of the validation fold.
        label_horizon: horizon (in samples) of the target. Used to identify which train
            samples overlap with each validation fold and must be purged.
    """

    def __init__(self, n_splits: int = 5, embargo: int = 0, label_horizon: int = 0):
        if n_splits < 2:
            raise ValueError("n_splits must be >= 2")
        self.n_splits = n_splits
        self.embargo = max(0, int(embargo))
        self.label_horizon = max(0, int(label_horizon))

    def split(
        self,
        X: pd.DataFrame | np.ndarray,
        target_times: pd.Series | None = None,
    ) -> Iterator[tuple[np.ndarray, np.ndarray]]:
        """Yield (train_idx, val_idx) tuples.

        Args:
            X: features (DataFrame or ndarray), time-ordered.
            target_times: optional pd.Series mapping each row to the time at which its
                target ends. If provided, train samples whose target window overlaps the
                val window are purged. If None, only embargo + label_horizon-based purging
                is applied.
        """
        n = len(X)
        indices = np.arange(n)
        fold_size = n // self.n_splits

        for k in range(self.n_splits):
            v_start = k * fold_size
            v_end = (k + 1) * fold_size if k < self.n_splits - 1 else n
            val_idx = indices[v_start:v_end]

            # Train candidates: all samples not in val
            train_mask = np.ones(n, dtype=bool)
            train_mask[v_start:v_end] = False

            # Embargo: drop samples within `embargo` of the val boundaries
            emb_lo = max(0, v_start - self.embargo)
            emb_hi = min(n, v_end + self.embargo)
            train_mask[emb_lo:v_start] = False
            train_mask[v_end:emb_hi] = False

            # label_horizon: drop train samples whose target reaches into val
            if self.label_horizon > 0:
                hz_lo = max(0, v_start - self.label_horizon)
                train_mask[hz_lo:v_start] = False

            # Purge by target_times if provided
            if target_times is not None:
                target_times = pd.Series(target_times).reset_index(drop=True)
                val_time_min = (
                    target_times.iloc[v_start] if v_start < len(target_times) else None
                )
                val_time_max = (
                    target_times.iloc[v_end - 1] if v_end - 1 < len(target_times) else None
                )
                if val_time_min is not None and val_time_max is not None:
                    overlap = (target_times >= val_time_min) & (target_times <= val_time_max)
                    train_mask &= ~overlap.values

            yield indices[train_mask], val_idx
