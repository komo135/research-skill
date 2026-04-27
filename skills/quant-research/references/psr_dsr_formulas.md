# psr_dsr_formulas.md

Formulas and implementation for Probabilistic and Deflated Sharpe Ratio.

## When to read

- Claiming statistical significance for an observed Sharpe
- Correcting Sharpe after a hyperparameter search

## Notation

- Observed Sharpe (`SR_obs`): annualized Sharpe from the backtest
- Threshold Sharpe (`SR_*`): comparison value (e.g. baseline B&H, or 0)
- Number of trials (`N`): count of distinct hyperparameter / model settings tried

## Probabilistic Sharpe Ratio (PSR)

Bailey & López de Prado (2012). Probability that the observed Sharpe exceeds a threshold:

```
PSR(SR_*) = Φ( (SR_obs - SR_*) × √(T - 1) / √(1 - γ_3 × SR_obs + (γ_4 - 1)/4 × SR_obs²) )
```

- `Φ`: standard normal CDF
- `T`: number of return observations (e.g. trading days for daily Sharpe)
- `γ_3`: skewness of observed returns
- `γ_4`: raw kurtosis of observed returns (note: not excess kurtosis)

Pass condition: `PSR(0) ≥ 0.95` (≥ 95 % confident SR > 0).

## Deflated Sharpe Ratio (DSR)

Bailey & López de Prado (2014). Multi-comparison correction for `N` trials:

```
SR_max_expected = √(var(SR)) × ((1 - γ) × Φ⁻¹(1 - 1/N)
                              + γ × Φ⁻¹(1 - 1/(N×e)))
```

- `γ`: Euler-Mascheroni constant ≈ 0.5772
- `var(SR)`: variance of Sharpe across trials

DSR is then `PSR(SR_max_expected)`:

```
DSR = Φ( (SR_obs - SR_max_expected) × √(T - 1) / √(1 - γ_3 × SR_obs + (γ_4 - 1)/4 × SR_obs²) )
```

Pass condition: `DSR ≥ 0.95`.

## Reference Python implementation (psr_dsr.py)

```python
from scipy import stats
import numpy as np

def psr(sr_obs, sr_threshold, T, skew, kurt):
    numerator = (sr_obs - sr_threshold) * np.sqrt(T - 1)
    denominator = np.sqrt(1 - skew * sr_obs + (kurt - 1) / 4 * sr_obs**2)
    return stats.norm.cdf(numerator / denominator)

def expected_max_sr(N, var_sr):
    gamma_em = 0.5772156649
    return np.sqrt(var_sr) * (
        (1 - gamma_em) * stats.norm.ppf(1 - 1 / N)
        + gamma_em * stats.norm.ppf(1 - 1 / (N * np.e))
    )

def dsr(sr_obs, T, skew, kurt, N, var_sr):
    sr_threshold = expected_max_sr(N, var_sr)
    return psr(sr_obs, sr_threshold, T, skew, kurt)
```

## Counting `N` honestly

`N` is the number of distinct settings tried.

| Setting | N |
|---|---|
| One fixed hyperparameter set | 1 |
| 5 hyperparameter values × 4 patterns | 20 |
| 50-cell sweep grid | 50 |
| Multiple feature sets | Sum across feature sets |

Under-reporting `N` makes DSR optimistic (weakens the correction). Be honest.

## Estimating `var(SR)`

Variance of Sharpe across trials. Run backtests at each trial setting and collect Sharpes:

```python
trial_sharpes = [backtest(setting).sharpe for setting in settings]
var_sr = np.var(trial_sharpes, ddof=1)
```

If only one setting was tried, `var(SR)` cannot be estimated and DSR cannot be computed.
PSR remains usable.

## Caveats

- Use `T` = number of return observations, not "years" (daily would be 252 × years)
- Skewness and kurtosis are computed on the observed return series
- DSR is over-optimistic if the trial count is under-reported

## References

- Bailey, D. H. & López de Prado, M. (2012). The Sharpe Ratio Efficient Frontier. *Journal of Risk*.
- Bailey, D. H. & López de Prado, M. (2014). The Deflated Sharpe Ratio: Correcting for
  Selection Bias, Backtest Overfitting, and Non-Normality. *Journal of Portfolio Management*.
