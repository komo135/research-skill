# exit_strategy_design.md

Exit-strategy design and parallel comparison for strategy backtests.

## When to read

- Designing a strategy backtest
- After choosing an entry signal, before deciding the exit

## Principle

**Time-stop alone is not a valid exit strategy.**

The time scale captured by an entry signal (e.g. mean-reversion onset) and the time scale
that an exit should capture (mean-reversion completion, stop-loss, trend reversal) are
different. Forcing them onto the same horizon via a time-stop averages out the exit edge.

## Exit categories

| Exit | Description | Suitable for |
|---|---|---|
| Signal flip | Exit when the entry signal reverses (e.g. RSI returns to mid-line) | Mean-reversion |
| TP-SL | TP = N × ATR, SL = M × ATR fixed at entry | Trend / breakout |
| Trailing stop | Trail by N × ATR from the running maximum (long) | Trend |
| Volatility-based | Exit when volatility falls / spikes | Regime-aware |
| Signal-strength | Exit when prediction confidence drops below threshold | ML-prediction-based |
| Time stop | Fixed H bars | **Safety net only** |

## Required protocol

In a strategy backtest experiment, compare **at least three exit types in parallel**:

```python
# Example: parallel evaluation in vectorbt
results = {}
for name, kwargs in [
    ("signal_flip", {"exits": signal_flip_exits}),
    ("atr_tp_sl",   {"sl_stop": sl_pct, "tp_stop": tp_pct}),
    ("atr_trail",   {"sl_stop": ts_pct, "sl_trail": True}),
]:
    pf = vbt.Portfolio.from_signals(close, entries, fees=fee, **kwargs)
    results[name] = summarize(pf)
```

Tabulate Sharpe, win rate, average hold, drawdown for each.

## Correct use of time-stop

Use it as a **safety net** combined with another exit:

```python
# Example: signal-flip exit with a 96-bar max-hold
exit_signal = (rsi >= 0)
exit_safety = entries.shift(96).fillna(False).astype(bool)
exits = exit_signal | exit_safety
```

The primary exit is signal-flip; only abnormally long positions are caught by the time
stop.

## Robustness across val and test

Compare each exit's val and test results. Large val→test degradation suggests overfit:

| Pattern | Interpretation |
|---|---|
| High val Sharpe, high test Sharpe | Adopt |
| High val, low test | Val cherry-picked, reject |
| Moderate on both | Stable, candidate |
| Low on both | Reject |

## Coupling with ML prediction

Exit can also be derived from an ML prediction:

- Exit when prediction confidence drops below threshold
- Exit when prediction sign reverses
- Adjust TP / SL dynamically based on predicted return

See `prediction_to_decision.md` Layer 2.

## Warning signs

- Exit implemented as `entries.shift(H)` only → time-stop alone, redesign
- Only one exit type tried → require at least three
- Exit hyperparameters (TP factor, SL factor, trail factor) tuned on test → redo on val
- "Fixed-H exit follows naturally because IC is defined on forward return" — that is
  post-hoc rationalization; review
