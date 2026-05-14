---
name: quant-research
description: >-
  Use for quantitative finance, financial machine learning, alpha-factor work,
  backtests, return prediction, regime detection, portfolio construction,
  execution research, PnL validation, transaction-cost analysis, transaction
  cost review, Sharpe / PSR / DSR review, leakage checks, walk-forward
  validation, CPCV, PBO, and financial time-series research. This is a finance
  adapter on top of the research skill: Use research first for the project
  workstream and state object, then apply quant-research for finance-specific
  evidence, validation, implementation, and failure-mode checks.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Quant Research

`quant-research` is a finance adapter for the generic `research` skill. Use
research first for the project workstream and state object: `R&D Workstream`
with `rd_plan.md`, phenomenon / mechanism workstreams with their selected
ledger, Result-to-Question, A0-A5 analysis depth, right-sized rigor, report
packages, park, kill, and pivot decisions.

Use this skill after or alongside `research` when the research object is a
financial model, trading signal, alpha factor, portfolio process, execution
method, backtest, PnL validation workflow, or financial time-series workflow.

## Finance-Specific Checks

Finance-specific checks are claim-bearing checks. They
are not mandatory gates for exploratory finance work. Exploratory finance work
may choose the next experiment, provisional go / no-go, park, deprioritize, or
reject-for-now before the full finance check battery. If leakage, cost,
multiple-testing, or validation checks are not yet run, label the numbers
`untrusted` / caveated and do not use them as supported evidence.

- Backtest and walk-forward design: read
  `references/shared/time_series_validation.md`. For runnable split helpers,
  use `scripts/walk_forward.py`, `scripts/purged_kfold.py`, and
  `scripts/cpcv.py`.
- Leakage, whole-period normalization, split hygiene, and PnL contamination:
  before treating numbers as claim-bearing, read
  `references/shared/time_series_validation.md` and
  `references/shared/sanity_checks.md`. For runnable checks, use
  `scripts/leakage_check.py` and `scripts/sanity_checks.py`.
- Multiple testing, PBO, PSR/DSR, and Sharpe inflation: read
  `references/shared/multiple_testing.md` and
  `references/shared/psr_dsr_formulas.md`. For runnable diagnostics, use
  `scripts/multiple_testing.py`, `scripts/pbo.py`, `scripts/psr_dsr.py`,
  `scripts/bootstrap_sharpe.py`, and `scripts/rolling_segment_sharpe.py`.
- Portfolio construction, turnover, transaction cost, capacity, and execution
  feasibility: read `references/shared/portfolio_construction.md`,
  `references/shared/prediction_to_decision.md`, and
  `references/shared/exit_strategy_design.md`. For runnable sensitivity and
  sizing checks, use `scripts/fee_sensitivity.py`,
  `scripts/vol_targeted_size.py`, and `scripts/exit_compare.py`.
- Model diagnostics, feature construction, regime effects, and robustness:
  read `references/shared/model_diagnostics.md`,
  `references/shared/feature_construction.md`,
  `references/shared/modeling_approach.md`,
  `references/shared/robustness_battery.md`, and
  `references/shared/sanity_checks.md`. For runnable diagnostics, use
  `scripts/regime_label.py`, `scripts/sensitivity_grid.py`, and
  `scripts/sanity_checks.py`.

## Operating Rule

Do not let finance metrics replace research state. Sharpe, PSR, DSR, PnL,
drawdown, turnover, hit rate, portfolio capacity, feature importance, or
backtest plots are evidence artifacts. The state transition still belongs to
`research` ledgers and review gates.

## Finance Reporting Addendum

Apply `research` User-Facing Outcome Reports to finance work with
domain-specific visuals or tables. It must include the applicable
finance-specific visuals or tables from the smallest useful set when the user
is asked to trust a model, signal, portfolio process, or execution method:

- equity curve and drawdown curve, with benchmark or baseline when available.
- fee-sensitivity table or heatmap showing where the result stops working.
- regime-segmented performance, rolling Sharpe / PnL stability, or
  train/test/walk-forward comparison.
- Turnover, capacity, exposure, hit-rate, and tail-loss tables when they affect
  deployability.
- Leakage, multiple-testing, PSR/DSR, or PBO diagnostics when the headline
  result depends on them.

The visual evidence must make the failure modes visible, not just the headline
return. Cite the artifact path, run ID, data period, and cost assumptions behind
each displayed figure or table.

## Claim-Bearing Precondition

Before finance evidence is used to support a durable state transition,
report-package conclusion, external claim, deployment recommendation, or
terminal kill, run the finance implementation checks above that bear on the
claim, then invoke `research` for the generic review gates:
`research/references/review/process_review.md` first, followed by
`research/references/review/conclusion_review.md`. Finance metrics can feed
those reviews as evidence, but they do not replace them.

This applies whenever finance evidence supports a claim-bearing report package,
external claim, deployment recommendation, or terminal kill decision.
