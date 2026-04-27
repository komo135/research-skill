# research_design.md

Template for the research-design Markdown that goes at the top of every experiment notebook,
and rules for writing falsifiable comparison statements.

## When to read

- Starting a new experiment notebook (before any implementation)
- Adding a new hypothesis to `hypotheses.md`

## What to write at the top of each experiment notebook

Each experiment notebook (`experiments/exp_NNN_<slug>.py`) starts with a Markdown cell
containing:

```markdown
## exp_NNN: <one-line purpose>

### Parent project
notebooks/<project-name>/

### Linked hypothesis
H<id>: [quote the entry from hypotheses.md]

### Question
[Falsifiable comparison statement — see the table below.]

### Hypothesis
[Why it might or might not hold — from prior knowledge.]

### Universe
- Instruments: [list at least three, or describe the cross-section]
- Period: [start, end]
- Frequency: [primary timeframe + auxiliary]

### Design
- Comparison: [method A / method B / baseline]
- Metrics: [Sharpe, IC, AUC, calibration, ...]
- Acceptance condition: [test-period numeric threshold that supports H]
- Rejection condition: [observation that would falsify H]
- Data ranges: train [d1,d2] / val [d2,d3] / test [d3,d4], embargo H bars
- Robustness gates: walk-forward mean Sharpe > 0, fee break-even fee reported,
  2D threshold surface majority-positive

### Upstream dependencies
- Data: [paths and hashes]
- Pre-processing: [intermediate files produced by upstream notebooks]
- Upstream hypotheses: [if their conclusions change, this experiment becomes invalid]
```

## How to write a falsifiable statement

Existence claims ("Is there X in Y?") are not falsifiable. Restate as **comparisons,
conditions, or numeric thresholds**.

| Not falsifiable | Falsifiable |
|---|---|
| Is there signal in the embedding? | Method X beats baseline Y on test [d1,d2] avg PnL by ≥ N basis points |
| Does ML work? | GBM beats LR on val and test AUC by ≥ 0.02 |
| Is Chronos useful here? | Chronos-2 LoRA-fine-tuned forecaster beats frozen-embed + LR on test avg PnL |
| Does mean-reversion work? | RSI ≤ 30 entry × signal-flip exit beats B&H on test Sharpe AND achieves Sharpe ≥ 0.5 with fee 1 bp/side |
| Does factor selection matter? | Top-3 IC factor rank-average beats best single factor on val and test IR |

## Acceptance and rejection conditions must be numeric

Use "exceeds by at least N", not "exceeds". Set the threshold up front and do not move it
afterwards.

| Metric | Example acceptance threshold |
|---|---|
| Sharpe (annualized) | test ≥ 0.5 (with fee) and walk-forward mean ≥ 0 |
| IC (Spearman rank) | val and test both `|IC| ≥ 0.02` |
| AUC | val and test both ≥ baseline + 0.02 |
| Probabilistic Sharpe Ratio | PSR ≥ 0.95 |
| Bootstrap CI low | > 0 |
| Walk-forward positive rate | ≥ 60 % |

## Baselines

Each experiment must include a lower and upper baseline:

- **Lower bound**: do-nothing / B&H / random-signal avg PnL
- **Hand-crafted upper bound**: linear model with hand features, or a simple moving-average
  crossover

The proposed method (ML or complex math model) is meaningful only when it beats **both**
baselines. Beating only the lower bound is consistent with noise.

## Upstream dependencies must be made explicit

Some experiments depend on upstream experiments (e.g. exp_002 produces PCA factors that
exp_005 consumes). State the dependency and note "if the upstream conclusion changes, this
experiment is invalidated".

Without this, downstream experiments are silently invalidated when upstream changes.
