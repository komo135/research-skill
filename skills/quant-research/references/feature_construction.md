# feature_construction.md

Treat feature / factor construction as a research topic in its own right.

## When to read

- Designing a new feature or factor
- Implementing pre-processing or decomposition (PCA, sector ETF regression, residualization)
- Running leakage checks (look-ahead bias, target leakage)

## Principle

Feature construction is a research topic separate from the prediction model. In many
papers (Avellaneda & Lee 2010 is one example) the central contribution is *how* returns
are decomposed, not the OU process applied to the residuals. Many ML research projects are
similarly centered on feature design.

Therefore:

- Validate feature construction in its own experiment notebook
- Use a two-stage pipeline: "feature notebook → prediction notebook"
- Save intermediate results to disk (parquet) and have downstream notebooks read them

## Feature categories

| Category | Examples | Caveat |
|---|---|---|
| Price-based | Returns, log-returns, ATR%, Bollinger %B | Standardization (rolling z-score) within the bar |
| Technical indicators | RSI, MACD, Stochastic | Confirm window is backward-looking only |
| Factor decomposition | PCA eigenportfolios, ETF residuals, factor-model residuals | Specify rolling correlation-matrix window length |
| Volume-based | Volume z-score, VWAP deviation, OFI | Rolling aggregation windows |
| State-space | HMM regime, Kalman latent state | Distinguish smoothing vs. filtering |
| Language features | Embeddings, sentiment | Define context window and inference timestamp |
| High-frequency | Order-book imbalance, microstructure noise | Tick-level timestamp alignment |

## Leakage check (mandatory)

### Look-ahead bias

Does feature `X[t]` use information from after time `t`? Check by:

1. Standardize the feature function as `f(data[:t])`
2. Compare `X[t]` computed on the full dataset vs. computed on data truncated at `t`
3. If they differ, look-ahead is present

```python
X_full = compute_features(data)
X_step = pd.concat([compute_features(data[:t]).iloc[-1:] for t in indices])
assert (X_full.loc[indices] == X_step).all().all()
```

### Target leakage

Does information used to compute target `Y` slip into feature `X`, directly or indirectly?

| Leak | Example | Remedy |
|---|---|---|
| Direct | Target included in feature | Code review |
| Aggregation contamination | Normalized using whole-period mean/std | Rolling normalization |
| Target encoding | Encoded using all samples | Fit inside the fold only |
| Imputation | Filled with whole-period median | Rolling median |
| Feature scaling | StandardScaler fit on all data | Fit on train only |

`scripts/leakage_check.py` provides automated detection.

## Feature-quality checks before adoption

Before adding a feature to a model, run an independent notebook that reports:

| Metric | Description | Pass example |
|---|---|---|
| Rank IC | Spearman(feature[t], return[t→t+H]) | val and test both `|IC| ≥ 0.02` |
| IR | mean(IC) / std(IC) over rolling windows | ≥ 0.3 |
| Auto-correlation | feature[t] vs. feature[t-1] | predicts turnover |
| Quintile spread | Top-quintile mean − bottom-quintile mean | val and test agree in sign |
| Inter-feature correlation | Rank correlation across features | If > 0.9, collapse them |
| Stationarity | ADF test | If non-stationary, difference or rolling-z |

## Saving intermediates

Feature notebooks save outputs to `results/intermediate/`:

```
results/intermediate/
├── pca_factors_<window>.parquet
├── etf_residuals.parquet
├── hmm_regime_labels.parquet
└── ...
```

Downstream notebooks read parquet files. Do not pass Python objects between notebooks —
that breaks reproducibility.

## Typical feature-notebook structure

```
pur_001_features_pca.py
├── Data fetch
├── Rolling correlation matrix
├── Eigendecomposition + top-m eigenvectors
├── Eigenportfolio returns
├── Per-instrument beta estimation against eigenportfolios
├── Residual returns
├── Feature-quality checks (stationarity, IC, quintile)
├── Save intermediate parquet
└── Update hypotheses.md and decisions.md
```

## Warning signs

- Feature construction and model training in the same notebook → split
- Intermediate results passed via Python objects → switch to file-based handoff
- No look-ahead check → run it
- Whole-period normalization or target encoding → make it fold-aware
