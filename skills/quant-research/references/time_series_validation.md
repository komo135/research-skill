# time_series_validation.md

Time-series-specific data splitting and validation methods.

## When to read

- Designing the data split for an experiment
- Setting up cross-validation for ML research
- Running walk-forward in the robustness phase

## Core principle

**No random shuffle on time-series data.** It causes information leakage.

## Splitting hierarchy

### 1. Time-ordered split (baseline)

```
[ train ]── embargo ──[ val ]── embargo ──[ test ]
```

- train < val < test in time order
- val: hyperparameter and threshold selection
- test: final evaluation, **once** — do not touch again

### 2. Embargo (prevent forward-looking leakage)

When features or labels depend on H bars in the future, leave a gap of at least H bars at
the boundary between train end and val start (and val end and test start).

Example: target = `close[t+12] / close[t] - 1` → embargo = 12 bars.

### 3. Purged k-fold (López de Prado)

For ML hyperparameter search and CV inside the train period:

- Split train into k folds in time order
- **Purge**: drop train samples whose label horizon overlaps the validation fold
- Insert **embargo** before and after each validation fold

`scripts/purged_kfold.py` provides a reference implementation.

### 4. CPCV (Combinatorial Purged Cross Validation)

López de Prado, AFML chapter 7. Combine many purged k-folds to generate multiple OOS paths.
Used to estimate backtest overfitting probability.

## Walk-forward

Before declaring completion, examine time stability with rolling windows:

```python
windows = pd.date_range(start, end, freq="3MS")  # 3-month rolling
for w_start, w_end in zip(windows, windows[1:]):
    pf = backtest(strategy, data[w_start:w_end])
    sharpe_dist.append(pf.sharpe)

mean_sharpe = sharpe_dist.mean()
pct_positive = (sharpe_dist > 0).mean()
```

Acceptance:

- mean Sharpe > 0
- pct_positive ≥ 60 %
- worst window ≥ −2 (no catastrophic loss)

## Test-set discipline

- The test set is touched **once**, for the final evaluation.
- Until val determines the model, hyperparameters, and thresholds, do not touch test.
- A bad test result is not a reason to rewrite the model on test — that is selection bias.

If test has been touched more than once, downgrade it to "partial OOS" in the writeup.

## Extra care for ML

### Data leakage

Make sure feature `X` does not contain future information about target `Y`.
`scripts/leakage_check.py` provides automated checks. Common cases:

| Leak | Example | Remedy |
|---|---|---|
| Direct | Target included in features | Code review |
| Aggregation contamination | Normalized using whole-period mean/std | Rolling normalization |
| Target encoding | Target encoding fit on all samples | Fit only inside the fold |
| Imputation | Missing values filled by whole-period median | Rolling median |
| Feature scaling | StandardScaler fit on all data | Fit on train only, transform val / test |

### Class imbalance

"Up vs. down" labels can be skewed enough that accuracy looks good. Use:

- Balanced accuracy / F1 / PR curve
- Class weights in the loss
- Choose the decision threshold on val (different from a default 0.5 cutoff)

### Feature-importance stability

If important features change a lot over time, model decay or overfit is happening. Compute
SHAP / permutation importance over rolling windows.

## Acceptance conditions to write at the top

In the experiment notebook's "Design" section:

```
- Data ranges: train [d1,d2] / val [d2+H,d3] / test [d3+H,d4], embargo H bars
- Cross-validation: purged 5-fold inside train, embargo H bars
- Robustness gates:
  - Walk-forward (3-month) mean Sharpe > 0 and pct_positive ≥ 60 %
  - Bootstrap 95 % CI lower bound > 0
  - Test set touched only once
```
