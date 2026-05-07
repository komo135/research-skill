---
name: quant-research
description: >-
  Use for quantitative finance, financial machine learning, alpha-factor work,
  backtests, return prediction, regime detection, portfolio construction,
  execution research, PnL validation, transaction-cost analysis, transaction
  cost review, Sharpe / PSR / DSR review, leakage checks, walk-forward
  validation, CPCV, PBO, and financial time-series research. This is a finance
  adapter on top of the research skill: Use research first for the project
  discipline, then apply quant-research for finance-specific evidence,
  validation, implementation, and failure-mode checks.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Quant Research

`quant-research` is a finance adapter for the generic `research` skill. Use research first
for project discipline: Pure Research vs R&D, R&D Program,
Result-to-Question, Result-to-Capability, A0-A5 analysis depth, right-sized
rigor, promotion, park, kill, and pivot decisions.

Use this skill after or alongside `research` when the research object is a
financial model, trading signal, alpha factor, portfolio process, execution
method, backtest, PnL validation workflow, or financial time-series workflow.

## Finance-Specific Checks

- Backtest and walk-forward design: read
  `references/shared/time_series_validation.md`. For runnable split helpers,
  use `scripts/walk_forward.py`, `scripts/purged_kfold.py`, and
  `scripts/cpcv.py`.
- Leakage, whole-period normalization, split hygiene, and PnL contamination:
  read `references/shared/time_series_validation.md` and
  `references/shared/sanity_checks.md` before trusting numbers. For runnable
  checks, use `scripts/leakage_check.py` and `scripts/sanity_checks.py`.
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

## Promotion Precondition

Before any finance claim is treated as supported, run the finance
implementation checks above, then invoke `research` for the generic review
gates: `research/references/review/process_review.md` first, followed by
`research/references/review/conclusion_review.md`. Finance metrics can feed
those reviews as evidence, but they do not replace them.
