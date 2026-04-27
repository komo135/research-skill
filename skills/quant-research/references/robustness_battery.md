# robustness_battery.md

Robustness checks to run before declaring a research project complete.

## Pre-condition

**Run the multi-agent bug review (`references/bug_review.md`) first.** Robustness checks
operate on the PnL series; if the PnL is contaminated by a leak, an alignment bug, or a
fee-accounting error, every robustness gate inherits the same contamination uniformly
and produces credible-looking false confidence. The bug-review layer is a gate on this
file, not a follow-up to it.

## When to read

- Main experiment finished, sanity checks (`references/sanity_checks.md`) all green, and
  the multi-agent bug review (`references/bug_review.md`) has produced a clean
  `decisions.md` entry
- Just before declaring completion

## Required checks

Run all seven. Their results also become triggers for the next hypothesis cycle.

### 1. Threshold sensitivity (2D grid)

Sweep entry / exit thresholds (or ML prediction cutoff and a sizing parameter) on a 2D
grid and compute the primary metric (Sharpe, IC, ...):

```python
grid = []
for entry_thr in entry_grid:
    for exit_thr in exit_grid:
        sharpe = backtest(strategy(entry_thr, exit_thr), val_data).sharpe
        grid.append((entry_thr, exit_thr, sharpe))
```

Pass condition: a **majority of cells** is positive on the surface. A lone peak (cherry-
picked optimum) is a sign of overfit.

### 2. Fee sensitivity sweep

Plot Sharpe across fee = [0, 0.2, 0.5, 1.0, 1.5, 2.0] bp/side.

```python
for fee in [0, 0.00002, 0.00005, 0.0001, 0.00015, 0.0002]:
    sharpe = backtest(strategy, data, fee=fee).sharpe
```

Pass condition: report the break-even fee. State whether the strategy is viable at retail
/ ECN / futures cost levels.

### 3. Walk-forward Sharpe distribution

Compute Sharpe over rolling windows (e.g. 3 months):

```python
for w_start, w_end in rolling_windows(start, end, "3MS"):
    sharpe_dist.append(backtest(strategy, data[w_start:w_end]).sharpe)

mean_sharpe = sharpe_dist.mean()
pct_positive = (sharpe_dist > 0).mean()
worst = sharpe_dist.min()
```

Pass condition: mean > 0, pct_positive ≥ 60 %, worst ≥ −2.

### 4. Bootstrap CI

Block bootstrap of the per-trade or daily-return Sharpe at 95 %:

```python
n_resample = 10000
block = int(np.sqrt(len(returns)))
sharpes = [bootstrap_sharpe(returns, block) for _ in range(n_resample)]
ci_low, ci_high = np.percentile(sharpes, [2.5, 97.5])
p_value = (np.array(sharpes) <= 0).mean()
```

Pass condition: 95 % CI lower bound > 0, p-value < 0.05.

### 5. Probabilistic / Deflated Sharpe Ratio

Deflate Sharpe by the number of trials (Bailey & López de Prado 2014):

`scripts/psr_dsr.py` provides the implementation. Pass condition: PSR ≥ 0.95, DSR ≥ 0.95.

### 6. Realistic cost

Replace the scalar fee approximation with a realistic cost model:

- Apply per-bar spread if available
- Add a slippage model that depends on order size

Pass condition: the strategy remains positive under realistic cost.

### 7. Regime-conditional Sharpe

Compute Sharpe per regime (trending / ranging, high / low vol, session):

```python
regimes = label_regimes(data)  # HMM, threshold, or exogenous (e.g. VIX)
for r in regimes.unique():
    sharpe_r = backtest(strategy, data[regimes == r]).sharpe
```

Pass condition: positive in three or more regimes — not dependent on a single regime.

## Example acceptance block

In the experiment notebook's "Design" section:

```
Robustness gates:
- 2D threshold surface: ≥ 50 % of cells with Sharpe > 0
- Fee sensitivity: break-even fee ≥ 0.5 bp/side
- Walk-forward: mean Sharpe > 0 and pct_positive ≥ 60 %
- Bootstrap CI: 95 % lower bound > 0
- DSR: ≥ 0.95
- Realistic cost: positive Sharpe under per-bar spread
- Regime: positive in 3+ regimes
```

If any gate fails, the conclusion is **preliminary screening**, not a completed result.

## When a check fails

Each failure suggests a new hypothesis:

| Failed check | Direction for the next hypothesis |
|---|---|
| 2D threshold has only a single peak | Strong parameter dependence — diversify the signal |
| Break-even fee < 0.3 bp | Not viable at retail; look at futures venue or spread reduction |
| Walk-forward unstable | Strong regime dependence — re-evaluate per regime |
| Bootstrap CI lower near zero | Sample size or effect size too small; diversify across instruments / strategies |
| DSR < 0.95 | Too many hyperparameter trials; redesign and reduce trials |
| Only one regime works | Adopt a conditional strategy |

Log the failure in `decisions.md` and add the next hypothesis to `hypotheses.md`.
