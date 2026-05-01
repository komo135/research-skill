# prediction_to_decision.md

Layer separation between ML prediction accuracy and trading performance.

## When to read

- Converting an ML prediction into a trading rule
- A puzzling situation: AUC is good but the backtest loses money

## Principle

Prediction accuracy (AUC, RMSE, accuracy) and trading performance (Sharpe, drawdown) are
**different**. Mixing them causes:

- A model with AUC 0.6 producing a negative Sharpe
- "Accuracy 70 %" that still loses to fees
- "Predictions are correct but no money is made"

## Three-layer separation

```
Layer 1: Prediction
  Input:  features
  Output: probability / predicted value / signal score
  Eval:   AUC, RMSE, IC, ECE

Layer 2: Decision
  Input:  Layer 1 output
  Output: trading action (+1 / -1 / 0) or target position
  Eval:   hit rate, signal turnover, transaction count

Layer 3: Sizing
  Input:  Layer 2 action + Layer 1 confidence
  Output: position size (USD or shares)
  Eval:   Sharpe, drawdown, risk parity
```

Validate each layer in its own notebook so weaknesses can be localized.

## Per-layer metrics

### Layer 1 (prediction)

| Problem | Primary metric |
|---|---|
| Binary classification | AUC, PR-AUC, Brier score, ECE |
| Multi-class | log-loss, top-k accuracy |
| Regression | RMSE, MAE, R² |
| Ranking | IC (Spearman), IR, NDCG |

Do not stop at Layer 1. Always combine with Layers 2 and 3 to evaluate trading performance.

### Layer 2 (decision)

Rules to convert predictions to actions:

| Rule | Description |
|---|---|
| Threshold cutoff | predict_proba > 0.6 → long, < 0.4 → short |
| Top-k | Sort all instruments by prediction; long top-k, short bottom-k |
| Signal flip | Reverse position when the prediction sign flips |
| Asymmetric | Different thresholds for long and short |

Evaluate:

- Hit rate (fraction of actions that turn out right H bars later)
- Signal turnover (frequency of action change)
- Sensitivity to transaction cost

### Layer 3 (sizing)

| Approach | Description |
|---|---|
| Equal weight | Same size for every action |
| Confidence-proportional | size ∝ predict_proba − 0.5 |
| Kelly | size ∝ edge / variance |
| Vol-targeted | size ∝ 1 / ATR (constant volatility per position) |
| Risk parity | Equal volatility contribution per instrument |

Evaluate:

- Sharpe, Sortino, max drawdown, max DD duration
- Realized vs. target volatility

## Common failures

### Stopping at Layer 1

"AUC 0.65 obtained" and declaring done. Without Layers 2 and 3 the trading performance is
unknown. **A backtest that combines all three layers is the minimum bar for completion.**

### Mixing Layer 1 and Layer 3

Putting trading cost or Sharpe directly into the prediction loss. It is possible but makes
debugging extremely hard. **Start with separation; integrate only after limits are
understood.**

### Accuracy-vs-fee mismatch

60 % accuracy can still lose money if the average per-trade PnL is below 2 bp/side in
fees. **Always report per-trade PnL with fees included.**

## Example notebook structure

```
pur_005_predict_returns.py    (Layer 1)
  Input:  features
  Output: predicted values saved to parquet
  Eval:   AUC / IC / ECE

pur_006_decision_rules.py     (Layer 2)
  Input:  pur_005 predictions
  Output: actions (+1/-1/0) saved to parquet
  Eval:   hit rate, turnover, threshold sensitivity

pur_007_sizing.py             (Layer 3)
  Input:  pur_006 actions + pur_005 confidence
  Output: position sizes
  Eval:   vectorbt Sharpe / drawdown / fee sensitivity
```

## Propagating upstream changes

Changing the Layer 1 model invalidates Layers 2 and 3. Make upstream dependencies explicit
in each notebook and re-run downstream when upstream changes.

In `hypotheses.md`, record upstream and downstream hypotheses as separate entries.
