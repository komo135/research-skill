# multiple_testing.md

Multiple-testing correction reference for quant research. Covers the
discipline of honest trial-count, the methods (Bonferroni, Romano-Wolf,
DSR, Harvey-Liu-Zhu hurdle, FDR, PBO), and how each is selected based
on the testing scenario.

## When to read

- Designing a pre-registration that involves > 1 hypothesis or
  parameter combination
- Reviewing whether a `supported` / `matured` claim has honest
  multiple-testing correction
- Computing DSR or PSR (`scripts/psr_dsr.py`)
- Running `references/review/conclusion_review.md` Section "Statistical
  sufficiency"

## The principle

Selecting the best of N tested strategies as if it were a single test
inflates the apparent significance. The correction adjusts the
significance threshold to control either:

- **Family-wise error rate (FWER)**: probability of ≥1 false positive
  across all tests
- **False discovery rate (FDR)**: expected fraction of false positives
  among declared discoveries

Both are valid; the choice depends on the cost of false positives.

## Empirical context (why this matters in quant finance)

- Hou, Xue, Zhang (2020): 65% of 452 published anomalies fail to
  replicate at t > 1.96; 82% fail at t > 2.78. Single-test thresholds
  are insufficient given the testing density of the field.
- Harvey, Liu, Zhu (2016): with the trial count published in the
  literature, new financial factors should clear t > 3.0 to
  approximately match the historical false-discovery rate.
- López de Prado: with 7 strategy configurations, the expected best
  2-year backtest Sharpe under the null is > 1. After 100
  configurations, > 2.

The takeaway: in this field, **single-test significance is a starting
point, not a finding**. The skill enforces multiple-testing correction
as a hard requirement for promotion in `pr_promotion_gate.md` and
`rd_promotion_gate.md`.

## Honest trial count

The most common failure is under-reporting the trial count. A trial
count is honest when it includes:

- Every distinct hypothesis tested in **this trial**
- Every distinct hypothesis tested in **prior trials** of this
  project
- Every distinct **parameter combination** tried during model selection
  / hyperparameter sweep
- Every **alternative metric** considered before settling on the primary

It does NOT include:

- Sanity checks (these are validation, not hypothesis tests)
- Reproducibility checks (re-runs of the same test)
- Robustness sweeps that are pre-registered as part of the trial design

When in doubt, include it. Under-counting inflates apparent significance.

## Methods

### Bonferroni correction

Simplest. Divide alpha by the trial count: corrected α = α / N.

- **Use when**: small N (< 10), tests are roughly independent, FWER
  control desired
- **Strength**: simple, conservative, easy to verify
- **Weakness**: very conservative when tests are correlated

### Holm step-down

Refines Bonferroni by ordering p-values and applying decreasing
correction: smallest p compared to α/N, next to α/(N-1), etc.

- **Use when**: small-to-medium N, FWER desired, want more power than
  Bonferroni
- **Strength**: uniformly more powerful than Bonferroni, still controls
  FWER
- **Weakness**: assumes independence

### Romano-Wolf step-down (recommended for trading strategies)

Step-down procedure that controls FWER while accounting for the
**dependence structure** of test statistics via resampling.

- **Use when**: testing N strategies against a benchmark, dependent
  test statistics expected (correlated returns), FWER desired
- **Strength**: more powerful than Bonferroni / Holm under correlation,
  asymptotically controls FWER
- **Weakness**: requires bootstrap implementation; more complex to verify
- **Reference**: Romano & Wolf (2005), implementation in
  `scripts/multiple_testing.py`

### Hansen Superior Predictive Ability (SPA) test

Studentized version of White's Reality Check; less conservative than
RC because it avoids the least-favorable null configuration.

- **Use when**: comparing a benchmark against many alternative
  strategies; main question is "does any strategy beat the benchmark"
- **Strength**: more power than reality check; widely used in
  forecasting / backtest comparison
- **Weakness**: focuses on the best alternative, not all of them

### Probabilistic Sharpe Ratio (PSR)

Probability that the true Sharpe exceeds a threshold, accounting for
non-normality of returns (skewness + kurtosis).

```
PSR(SR*) = Φ((SR_obs - SR*) × √(T-1) / √(1 - γ_3 × SR_obs + ((γ_4-1)/4) × SR_obs²))
```

- **Use when**: claiming a single strategy's Sharpe is significantly
  > some threshold; returns are non-normal
- **Strength**: corrects for skewness / kurtosis; well-defined for a
  single test
- **Weakness**: per-period SR (not annualized) must be used in the
  formula; common to confuse this
- **Implementation**: `scripts/psr_dsr.py::psr` (per-period API)
- **Pass condition**: PSR(0) ≥ 0.95 ⇒ ≥ 95% probability that the true
  Sharpe is positive

### Deflated Sharpe Ratio (DSR)

PSR applied with the threshold set to the expected maximum Sharpe
across N independent trials. Multi-comparison correction in the SR
domain.

```
SR_max_expected = √(var(SR)) × ((1 - γ) × Φ⁻¹(1 - 1/N) + γ × Φ⁻¹(1 - 1/(N×e)))
```

where γ ≈ 0.5772 (Euler-Mascheroni).

- **Use when**: many strategies / parameter combinations have been
  tried (e.g., hyperparameter sweep) and the best one is being
  reported as the headline
- **Strength**: handles selection bias from large N elegantly
- **Weakness**: requires honest N (under-reporting inflates DSR);
  variance of SR across trials must be estimable
- **Implementation**: `scripts/psr_dsr.py::dsr`
- **Pass condition**: DSR ≥ 0.95

### Probability of Backtest Overfitting (PBO)

Bailey, Borwein, López de Prado, Zhu (2017). Estimates the probability
that the strategy selected as best on in-sample data will under-perform
the median on out-of-sample data, using combinatorially symmetric
cross-validation (CSCV).

- **Use when**: a backtest selection process is performed across many
  configurations; want to estimate selection-induced overfitting
- **Strength**: model-free, non-parametric
- **Weakness**: requires sufficient data to construct CSCV partitions
- **Implementation**: `scripts/pbo.py`
- **Pass condition**: PBO ≤ 0.5 (a strategy that selects randomly
  would have PBO ≈ 0.5; useful claim requires PBO substantially below)

### Harvey-Liu-Zhu single-test t-hurdle

For a new factor / strategy not part of a formal multi-test framework:
require t-statistic > 3.0 instead of the conventional > 2.0 (or > 1.96
for two-sided alpha=0.05).

- **Use when**: the testing framework is informal but the field's
  publication bias and prior testing inflate single-test significance
- **Strength**: simple rule of thumb; reflects the empirical field
  evidence
- **Weakness**: heuristic, not formally derived from the project's
  test count

### False Discovery Rate (FDR) — Benjamini-Hochberg

Controls the expected fraction of false discoveries among rejected
nulls. Less conservative than FWER methods.

- **Use when**: large N, willing to accept some false discoveries in
  exchange for power
- **Strength**: more discoveries than FWER methods
- **Weakness**: doesn't bound the worst-case (may have many false
  discoveries in some experiments)

## Selecting the right method

| Scenario | Recommended method |
|---|---|
| Single new factor / strategy claim | PSR + Harvey-Liu-Zhu t > 3.0 |
| Hyperparameter sweep, headline = best | DSR |
| Comparing many strategies vs benchmark | Romano-Wolf step-down |
| Forecasting model comparison | Hansen SPA |
| Backtest selection robustness | PBO |
| Many independent hypotheses, want power over FWER | FDR (Benjamini-Hochberg) |
| Few independent hypotheses, FWER critical | Bonferroni or Holm |

Most projects need **at least two** of these (e.g., DSR for hyperparameter
sweep + Romano-Wolf for cross-strategy comparison + PSR for the final
Sharpe claim). The promotion gate enumerates each based on the project's
trial structure.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Under-reporting trial count | Headline DSR computed with N=5 when actually 50 configurations were tried | Force honest N; recompute |
| Annualized SR in PSR formula | `psr(sr_obs=1.45, T=252, ...)` interpreted as annualized | Use per-period SR; see `scripts/psr_dsr.py` API |
| Confusing FWER and FDR | Project claims FWER control but uses BH-FDR (less conservative) | Document method and what's controlled |
| Skipping correction entirely | "p-value 0.04, significant" with no correction | Promotion gate blocks; require correction |
| Cherry-picking the favorable correction | Try Bonferroni, get rejected; try BH-FDR, get accepted; report BH-FDR | Pre-register the correction method in the `Analysis Plan` and bind pass/fail use in `Inference / Decision Criteria` |
| Pre-reg states 1 hypothesis but trial tests 5 | Major deviation per `pr_workflow.md` | Treat the trial as exploratory; create a new pre-reg with honest count |

## Implementations bundled in this skill

- `scripts/psr_dsr.py` — PSR and DSR (per-period API)
- `scripts/multiple_testing.py` — Romano-Wolf step-down
- `scripts/pbo.py` — Probability of Backtest Overfitting (CSCV)
- `scripts/bootstrap_sharpe.py` — Stationary block bootstrap for SR CI

## Relationship to other references

- `references/shared/psr_dsr_formulas.md` — formula details for PSR/DSR
- `references/pure_research/preregistration.md` — the `Analysis Plan`
  and `Inference / Decision Criteria` sections pre-register the
  multiple-testing correction method and bind how it will be used
- `references/pure_research/pr_promotion_gate.md` § D — checks honest
  trial count and correction method applied
- `references/rd/rd_promotion_gate.md` § C / D — same for R&D
- `references/review/conclusion_review.md` — statistical sufficiency
  axis verifies correction
- `references/shared/analysis_depth.md` — A4 requires alternatives
  excluded; multi-test correction is a key way to defend against
  selection-bias alternatives

## References

- Hou, Xue, Zhang (2020) "Replicating Anomalies", *Review of Financial
  Studies*
- Harvey, Liu, Zhu (2016) "...and the Cross-Section of Expected
  Returns", *Review of Financial Studies*
- Romano & Wolf (2005) "Stepwise Multiple Testing as Formalized Data
  Snooping", *Econometrica*
- Hansen (2005) "A Test for Superior Predictive Ability"
- Bailey & López de Prado (2012) "The Sharpe Ratio Efficient Frontier"
  (PSR)
- Bailey & López de Prado (2014) "The Deflated Sharpe Ratio"
- Bailey, Borwein, López de Prado, Zhu (2017) "The Probability of
  Backtest Overfitting", *Journal of Computational Finance*
- Benjamini & Hochberg (1995) "Controlling the False Discovery Rate"
