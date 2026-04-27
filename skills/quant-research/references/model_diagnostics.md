# model_diagnostics.md

Assumption verification for math models, and overfit checks for ML models.

## When to read

- The conclusion depends on the validity of model assumptions
- An ML model has just finished training and overfit is a concern

## Math-model assumption verification

### Stochastic-process models (OU, jump-diffusion, GARCH, etc.)

| Assumption | Check |
|---|---|
| Stationarity | ADF test, KPSS test |
| Mean-reversion-speed significance | t-test on OU κ, confidence interval |
| Residual normality | Jarque-Bera, Q-Q plot |
| Residual independence | Ljung-Box, ACF / PACF |
| Homoscedasticity | ARCH test |

Example: Avellaneda & Lee (2010) drop instruments where the mean-reversion speed κ falls
below a threshold (κ < 8.4 / year). Always implement an analogous filter for instruments
that violate the assumption.

### Factor models (PCA, factor regression)

| Check | Detail |
|---|---|
| Eigenvalue spectrum | Confirm top-k eigenvalues are detached from the bulk |
| Explained-variance over time | Plot rolling and watch for regime shifts |
| Factor interpretability | Top and bottom loadings should show coherence with sector or style |
| Factor stability | Track factor reordering across rolling windows |

### State-space models (Kalman, HMM)

| Check | Detail |
|---|---|
| Innovation residuals | Mean ~ 0, uncorrelated, normal |
| State estimate confidence intervals | Report estimation uncertainty |
| Forward / backward smoothing agreement | Disagreement signals model mis-specification |
| Likelihood convergence | EM log-likelihood should be monotone non-decreasing |

## ML overfit checks

### Learning curves

Plot train loss and val loss against epoch:

| Shape | Interpretation |
|---|---|
| train ↓, val ↓ together | Healthy |
| train ↓, val starts to ↑ at some epoch | Overfit |
| train ↓, val flat | Underfit or data leakage suspected |
| train and val both low | Healthy (verify val is meaningful) |

### Feature-importance stability

If important features change a lot across time, decay or overfit is happening:

```python
for window in rolling_windows:
    model.fit(train_in_window)
    importances.append(permutation_importance(model, val_in_window))
```

Plot the importance time-series.

### Prediction distribution

| Sign | Interpretation |
|---|---|
| Predictions concentrated near 0 | Underfit / weak signal |
| Predictions saturated at 0 or 1 | Overfit / poor calibration |
| Prediction rank uncorrelated with target rank | Training failed |

### Probability calibration

For classification, check that predicted probabilities match observed frequencies:

- Reliability diagram
- Brier score
- Expected calibration error (ECE)

If predictions feed directly into position sizing, calibration is required.

### Residual analysis

For regression problems, examine prediction residuals:

- Residual vs. prediction (heteroscedasticity)
- Residual time series (autocorrelation)
- Residual distribution (heavy tails)

## What to do when assumptions fail

Either drop the offending instruments / periods / regimes as **model-not-applicable**, or
change the model. Record the decision in `decisions.md`.

Example:

```
exp_004 OU parameter estimation: 30% of instruments have κ < 1/0.5 (mean-reversion time
> 6 months). Decision: classify those instruments as OU-not-applicable and proceed with
the remaining 70%. Logged in decisions.md.
```

Without this, noise from mis-fit instruments contaminates the result.

## Where to place the checks

Run them at the end of feature-construction notebooks (`exp_NNN_features_*.py`) and at
the end of prediction-model notebooks.
