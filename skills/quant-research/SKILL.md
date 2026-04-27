---
name: quant-research
description: Use proactively when the user runs any quantitative-finance or algorithmic-trading research, alpha-factor research, strategy backtest, return prediction, regime detection, optimal execution, or any data → model → evaluation loop in Jupyter or marimo notebooks. Covers both mathematical-model research (OU process, PCA, state-space, factor models) and machine-learning research (classical ML, deep learning, reinforcement learning, foundation models). Establishes a falsifiable hypothesis BEFORE implementation, enforces a one-experiment-per-notebook structure with multi-instrument universe, exit-strategy parallel-comparison (NOT time-stop alone), time-series validation with embargo / purged k-fold / walk-forward, multi-agent bug review (parallel specialists plus an adversarial cold-eye reviewer, triggered when results look too good or before declaring a verdict), a mandatory co-gate via the separate `experiment-review` skill before verdict='supported' (both `bug_review` and `experiment-review` must pass), robustness battery (bootstrap / fee sensitivity / Probabilistic Sharpe Ratio / regime conditional), iterative hypothesis cycles, and notebooks that are self-contained communication artifacts so a reader of the .py file alone can understand what was investigated, why, how, and what was concluded. Use even when the user does not say "research" — any backtest, factor screening, or ML-on-financial-time-series task is in scope.
---

# Quant Research

A protocol skill for quantitative-finance and algorithmic-trading research that uses either
mathematical models or machine learning.

## Purpose

Keep the research at publication-grade quality. Writing a paper is not the goal, but the
research itself should reach a level at which a paper could be written.

Concretely:

- Fix a falsifiable hypothesis before writing any implementation
- Run multiple experiments at the granularity of one notebook per experiment, then aggregate
- Enforce time-series validation
- Verify robustness before declaring completion
- Iterate hypothesis cycles instead of stopping after one
- Make differentiation against prior work explicit so the research is not a degraded
  reimplementation

## When to use

- Strategy backtests of any kind
- Alpha-factor research (mathematical or ML based)
- Return / price prediction with ML
- Reinforcement learning for execution or portfolio rebalancing
- State-space models or stochastic-process models of markets
- Foundation-model applications (e.g. Chronos, TimesFM, Moirai) to financial time series

Out of scope: pure implementation tasks (CRUD, bug fix, refactor).

## Research lifecycle

```
[New project]
       ↓
  Literature review (literature/)
       ↓
  Hypothesis portfolio (hypotheses.md)
       ↓
[Run experiments]
       ↓
  Create one notebook per experiment (experiments/exp_NNN_<slug>.py)
       ↓
  At the end of each cycle: append to results/, update hypotheses.md, decisions.md
       ↓
  If a derived hypothesis can be tested with current data, start the next notebook
       ↓
[Completion]
       ↓
  Robustness battery → research-quality checklist
```

## Project folder layout

When starting a new research project, create this layout (the helper script
`scripts/new_project.py` generates it):

```
notebooks/<project-name>/
├── README.md                 # Question, status summary, links to sub-files
├── literature/
│   ├── papers.md             # Related papers with one-paragraph summaries
│   └── differentiation.md    # Differentiation matrix vs. prior work
├── hypotheses.md             # H1, H2, ... with state (in-progress / supported / rejected / parked)
├── experiments/
│   ├── INDEX.md              # List of experiment notebooks with one-line conclusions
│   ├── exp_001_<slug>.py
│   ├── exp_002_<slug>.py
│   └── ...
├── decisions.md              # Time-ordered decision log
├── results/
│   ├── results.parquet       # Aggregated numeric results across all experiments
│   └── figures/              # Figures intended for a report or paper
└── reproducibility/
    ├── env.lock              # Dependency lock file
    ├── data_hashes.txt       # SHA-256 of input data files
    └── seed.txt
```

## Mandatory order before touching code

### 1. Literature review (avoid producing a degraded reimplementation)

See `references/literature_review.md`. Collect 5-10 prior papers and write the
differentiation against them in `literature/differentiation.md`. Skipping this makes the
research likely to reinvent or weaken known results.

### 2. Write the research design first in Markdown

See `references/research_design.md`. At the top of each experiment notebook, write:

- Question — as a falsifiable comparison statement
- Hypothesis
- Universe (list at least three instruments, or describe the cross-section)
- Acceptance / rejection conditions (with numeric thresholds)
- Data range (train / val / test, embargo size)

### 3. One experiment = one notebook

See `references/experiment_protocol.md`. Do not mix multiple experiments in one notebook.
Reasons:

- marimo's dataflow graph forbids redefining the same global variable across cells
- each experiment must be independently re-runnable for reproducibility
- file size and clarity stay manageable

### 4. Pick math vs. ML deliberately

See `references/modeling_approach.md`. Choose between mathematical models (OU, PCA,
AR(1), HMM), classical ML (regression, trees), deep learning, reinforcement learning, or
foundation models based on the structure of the hypothesis. "Default to ML" or "default to
math" is not allowed as a reason.

### 5. Treat feature / factor construction as its own experiment

See `references/feature_construction.md`. Building features or factors is research in its
own right — give it its own notebook. Run leak checks (look-ahead bias, target leakage) on
every feature.

### 6. Time-series validation

See `references/time_series_validation.md`. Required:

- Time-ordered split (train < val < test)
- Embargo when features depend on future-leaking horizons
- Walk-forward (rolling window) to assess time stability
- Purged k-fold or CPCV (López de Prado) for ML research
- Test set is touched only once for the final evaluation

### 7. Verify model assumptions

See `references/model_diagnostics.md`. For mathematical models, statistically test the
assumptions (stationarity, normality, mean-reversion speed). For ML models, run overfit
checks (learning curves, feature-importance stability, prediction distribution).

### 8. Separate prediction from decision (ML research)

See `references/prediction_to_decision.md`. Prediction accuracy (AUC, RMSE) and trading
performance (Sharpe, drawdown) are not the same thing. Keep the layers separate.

### 9. Make exits a first-class design choice

See `references/exit_strategy_design.md`. Time-stop alone is not a valid exit strategy.
Compare signal-flip / TP-SL / trailing-stop / volatility-based exits in parallel; if a
time-stop is used at all, use it as a max-hold safety net.

### 10. Portfolio construction (strategy research)

See `references/portfolio_construction.md`. Sizing, hedging, market-neutralization, and
leverage should all be deliberate choices.

## Two review layers — boundary at a glance (read before steps 11 and 13)

Steps 11 and 13 are two separate review layers. They are intentionally *not* merged.
Both are required before `verdict = "supported"`. The most common confusion is between
their two `validation` scopes — one in each layer.

| | **Step 11: `bug_review`** (in this skill) | **Step 13: `experiment-review`** (separate skill) |
|---|---|---|
| One-line | Are the code and numbers correct? | Is the claim warranted by the design? |
| Question | Is the implementation contaminated? | Is the claim oversold relative to evidence? |
| Looks at | Code, data, PnL series | Hypothesis, universe, baselines, claim, notebook artifact |
| Specialists | 5: leakage / pnl-accounting / **validation (correctness)** / statistics (metric arithmetic) / code-correctness | 7: question / scope / method / **validation (sufficiency)** / claim / literature / narrative |
| Adversarial reviewer (minimum bundle) | code + reported numbers | `.py` file alone |
| Order in this skill | Step 11 (precondition) | Step 13 (postcondition, after robustness battery) |
| Verdict gate | **Both must pass.** | **Both must pass.** |

`validation` boundary rule of thumb:

- Step 11's `validation` checks "is the embargo wired in correctly?" (correctness)
- Step 13's `validation` checks "is N=8 walk-forward windows enough power to
  distinguish Sharpe 0.4 from 1.1?" (sufficiency)
- A finding genuinely on both axes is flagged independently by both layers.

### 11. Multi-agent bug review (runs *before* the robustness battery)

See `references/bug_review.md` and `references/sanity_checks.md`. A passing robustness
battery is necessary but not sufficient — leaks, misalignments, and accounting bugs
contaminate every robustness gate uniformly and turn the green ticks into false
confidence. This step fires when any *trigger condition* is met:

- Numeric red flag (e.g. test Sharpe > 3, walk-forward mean Sharpe > 2, ML AUC > 0.65 on
  return-sign, headline metric outside bootstrap 95 % CI, headline ≥ 2 × walk-forward
  mean — full table in `bug_review.md`)
- State-change trigger: before `verdict = "supported"`; before the test set is touched;
  after any change to data ingestion, target, embargo, fold, feature scaling, signal
  alignment, or fee model

When fired, dispatch six sub-agents *in parallel*: five specialist reviewers — one
each for leakage, PnL accounting, validation-correctness, statistics / metric
correctness, and generic code correctness — plus one adversarial cold-eye reviewer
with a deliberately minimum context bundle (code + reported numbers only; no other
reviewers' findings, no `decisions.md`, no `hypotheses.md`). The asymmetry of the
adversarial bundle is the mechanism that breaks same-model anchoring — see
`bug_review.md` for the exact bundle and instruction.

Each returns severity-tagged findings; `high` and `medium` findings block re-running
the battery and block any verdict change until resolved. Findings are logged under
`### Bug review for exp_NNN at <timestamp>` in `decisions.md` as the audit trail.

The notebook also runs the programmatic subset (random-signal benchmark, shuffled-target
test, PnL reconciliation, cost monotonicity, sign-flip identity, NaN/Inf scan, time-
shift placebo) in a "Sanity checks" cell *before* section 12 below. See
`scripts/sanity_checks.py`.

If parallel sub-agent dispatch is unavailable, run the six scopes sequentially in six
distinct passes — do not collapse them into one. The adversarial pass is run with the
minimum bundle only even in the fallback.

### 12. Robustness battery before declaring completion

See `references/robustness_battery.md`. **Run only after step 11 has produced a clean
bill of health.** At minimum:

- Threshold sensitivity (2D grid)
- Fee sensitivity sweep
- Walk-forward Sharpe distribution
- Bootstrap CI (block bootstrap)
- Probabilistic / Deflated Sharpe Ratio
- Regime conditional (trending / ranging, high / low vol, session)

### 13. Multi-agent experiment review (research quality) — invokes the `experiment-review` skill

The `experiment-review` skill is a **separate skill**. Invoke it via the Skill tool at
this step. **MANDATORY co-gate with step 11.** Both must pass before
`verdict = "supported"`. This step is not optional or advisory; it is a required gate.

Why two layers: step 11 (`bug_review`) asks "is the implementation correct?" Step 13
(`experiment-review`) asks "is the claim warranted by the experimental design?" These
are distinct questions with distinct failure modes. A clean experiment-review on top of
a buggy implementation produces confidence in a contaminated PnL — `bug_review` is
the precondition. A clean bug_review on top of an unsupported claim (wrong baseline,
single instrument, missed prior work) produces a deployment-ready overstatement —
`experiment-review` is the postcondition.

What `experiment-review` does: dispatches 7 specialist sub-agents in parallel (question /
scope / method / validation-sufficiency / claim / literature / narrative) plus 1
adversarial cold-eye reviewer that reads the `.py` file alone with deliberately minimum
context. Returns severity-tagged findings aggregated into
`notebooks/<project>/reviews/exp_NNN_<ISO-date>.md`. See the `experiment-review` skill's
own SKILL.md and references for the dimension scopes and dispatch protocol.

Sequence inside this skill:

1. Step 11 (`bug_review`) clean — every `high` and `medium` resolved
2. Step 12 (robustness battery) green
3. **Invoke `experiment-review` skill via the Skill tool** ← this step
4. Address every `high` and `medium` finding from `experiment-review`
5. Step 14 (result aggregation), then completion gate

Do NOT proceed to step 14 (result aggregation) until both `bug_review` and
`experiment-review` findings are addressed. Setting `verdict = "supported"` before both
layers pass is a protocol violation that downgrades the result to *preliminary
screening*.

Common rationalization to resist: "`bug_review` already ran, that is the review layer."
Different question (correctness vs. claim-warrant); both required.

### 14. Result aggregation

See `references/results_db_schema.md`. The final cell of each experiment notebook appends
to `results/results.parquet` using a shared schema. Without this, no cross-experiment
comparison is possible.

### 15. marimo cell granularity

See `references/marimo_cell_granularity.md`. One cell = one fit / one evaluation. Do not
loop over models × features × targets in a single cell.

### 16. Notebook as a self-contained communication artifact

See `references/notebook_narrative.md`. A reader who opens *only* the `.py` file must be
able to follow what was investigated, why, how, and what was concluded — without running
the notebook, without chat context, without slides. A reader who runs the notebook in
marimo additionally gets large interactive figures and `mo.ui` widgets to drill into the
evidence. Both readers must reach the same conclusion. Required: an abstract cell at the
top, per-section *what & why* cells, per-figure *observation* cells, prose interpretation
before the programmatic verdict, headline figures in plotly / altair at full width and
≥ 450 px height, and at least one `mo.ui` widget for evidence drill-down (widgets must
not select numbers that flow into `results.parquet`).

### 17. Iterate hypothesis cycles

See `references/hypothesis_cycles.md`. Do not stop after one cycle. At the end of every
notebook, classify derived hypotheses as "run now / next session / drop" and log them in
`hypotheses.md` and `decisions.md`. If a derived hypothesis can be tested in the current
session, start the next notebook.

## Completion gate

Before declaring research "complete" (`verdict = "supported"`), all **three** gates
must pass — *in this order*:

1. **Step 11 — `bug_review` (in this skill)**: 5 specialist reviewers + 1 adversarial
   cold-eye reviewer, no unresolved `high` or `medium` findings.
2. **Step 13 — `experiment-review` (separate skill, invoke via Skill tool)**: 7
   specialist reviewers + 1 adversarial cold-eye reviewer, no unresolved `high` or
   `medium` findings.
3. **`references/research_quality_checklist.md`**: passes as final self-check.

Setting `verdict = "supported"` without all three is a protocol violation that
downgrades the result to *preliminary screening*. Each gate is logged in `decisions.md`
with timestamp and the reviewer agent IDs.

The two review gates intentionally remain *separate skills* and are *not* merged: they
answer different questions (correctness vs. claim-warrant) and their adversarial
reviewers receive different minimum bundles tuned to different failure modes
(`bug_review` adversary sees code + numbers; `experiment-review` adversary sees the
`.py` file alone). Merging them would dilute both.

## Bundled helper scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_experiment.py` | Generate a numbered experiment notebook from the template |
| `aggregate_results.py` | Append rows to `results/results.parquet` and query them |
| `walk_forward.py` | Compute Sharpe distribution over rolling windows |
| `bootstrap_sharpe.py` | Block-bootstrap CI for per-trade Sharpe |
| `psr_dsr.py` | Probabilistic / Deflated Sharpe Ratio |
| `fee_sensitivity.py` | Fee sweep with break-even fee extraction |
| `sensitivity_grid.py` | 2D threshold sensitivity grid |
| `vol_targeted_size.py` | Position sizing with size ∝ 1/volatility |
| `purged_kfold.py` | Purged k-fold CV (López de Prado) |
| `leakage_check.py` | Detect look-ahead bias and target leakage in features |
| `sanity_checks.py` | Programmatic bug-detection helpers used by the multi-agent review layer (random-signal benchmark, shuffled-target test, PnL reconciliation, cost monotonicity, sign-flip, NaN/Inf scan, time-shift placebo) |

## File templates

| asset | purpose |
|---|---|
| `README.md.template` | Project root README |
| `experiment.py.template` | marimo notebook template for one experiment |
| `INDEX.md.template` | Index of experiments |
| `hypotheses.md.template` | Hypothesis portfolio tracker |
| `decisions.md.template` | Decision history log |
| `papers.md.template` | Prior-work catalog |
| `differentiation.md.template` | Differentiation-against-prior-work matrix |

## Key references

- López de Prado, *Advances in Financial Machine Learning* (2018) — purged k-fold, embargo,
  CPCV, backtest overfitting
- Bailey & López de Prado, *The Probabilistic Sharpe Ratio* (2012) and *The Deflated Sharpe
  Ratio* (2014)
- Bailey, Borwein, López de Prado, Zhu, *Pseudo-Mathematics and Financial Charlatanism* (2014)
- Politis & Romano, *Block Bootstrap* (1994)
- Avellaneda & Lee, *Statistical Arbitrage in the U.S. Equities Market* (Quantitative
  Finance, 2010) — reference example for math-driven research
