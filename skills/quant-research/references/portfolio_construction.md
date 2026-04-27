# portfolio_construction.md

Position sizing, hedging, market-neutralization, and leverage. Used in strategy research.

## When to read

- Running a backtest with multiple instruments
- Requiring market neutrality or sector neutrality
- Mapping ML prediction confidence into position size

## Sizing options

| Method | Description | Typical use |
|---|---|---|
| Equal weight | Same size per instrument | Simple, for early validation |
| Confidence-proportional | size ∝ predict_proba − 0.5 | ML-prediction-based |
| Kelly | size ∝ edge / variance | When edge and vol estimates are reliable |
| Vol-targeted | size ∝ 1 / instrument ATR | Common choice; flatten per-instrument vol |
| Risk parity | Equal vol contribution per instrument | Portfolio-level vol control |
| Min-variance | Optimization with covariance matrix | Mid- and large-portfolio |
| Black-Litterman | Market prior + view | Institutional |

`scripts/vol_targeted_size.py` provides a reference vol-targeted implementation.

## Hedging

### Market beta neutrality

Cancel the strategy portfolio's correlation with the market:

```
hedge_amount = − portfolio_beta × portfolio_value
```

Hedge instruments are typically a market ETF or index futures.

### Sector neutrality

Long and short cancel within each sector:

```
sum(long positions in sector S) = sum(short positions in sector S)
```

Sector ETFs are commonly used. (See e.g. Avellaneda & Lee 2010.)

### Factor neutrality

Constrain factor exposure (PCA factor, Fama-French factor, etc.) to zero:

```
sum(position[i] × β[i,j]) = 0  for each factor j
```

Solve via constrained linear programming.

## Leverage

| Notation | Meaning |
|---|---|
| 1×1 | $1 long + $1 short per $1 of equity |
| 2×2 | $2 long + $2 short |
| 4×4 | $4 long + $4 short |

Leverage does not change Sharpe but does change drawdown and margin-call risk. Set a target
volatility (e.g. 10 % annualized) and back out leverage from there.

## Mapping ML prediction to size

Confidence-driven sizing pattern:

```python
# Map predict_proba to [-1, +1]
signal_strength = (predict_proba - 0.5) * 2

# Combine with vol-targeted scaling
position = signal_strength * target_vol / atr
```

Using confidence directly requires probability **calibration** (see `model_diagnostics.md`).

## Portfolio metrics

| Metric | Description |
|---|---|
| Portfolio Sharpe | Sharpe after aggregating all positions |
| Portfolio max DD | Aggregate maximum drawdown |
| Beta vs. market | Should be near zero if claiming market neutrality |
| Sector exposure | Net exposure per sector |
| Concentration (HHI) | Top-name concentration |
| Turnover | Daily position change (predictor of cost) |

## Warning signs

- Single-instrument validation used to claim "the portfolio works" — multi-instrument
  validation is required
- Sharpe boosted via leverage — Sharpe is leverage-invariant; look elsewhere
- Market-neutral claimed without computing beta — compute it
- Confidence-driven sizing without calibration — verify with ECE / reliability diagram

## Reference implementations

- `scripts/vol_targeted_size.py` — vol-targeted reference
- vectorbt: `from_orders` accepts size directly
- nautilus-trader: `SizingComponent` for complex sizing logic
