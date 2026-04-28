# research_design.md

Template for the research-design Markdown that goes at the top of every notebook,
and rules for writing falsifiable comparison statements.

## When to read

- Starting a new notebook (before any implementation)
- Adding a new H block to an existing notebook
- Adding a new hypothesis to `hypotheses.md`

## What to write at the top of each notebook (Purpose header — once)

Each notebook (`experiments/exp_NNN_<purpose-slug>.py`) starts with a Markdown
cell containing the **Purpose** of the investigation. The Purpose is open-ended
(it admits multiple H's); individual H's get their own per-H block lower in
the notebook.

```markdown
## exp_NNN: <one-line purpose-slug>

### Parent project
notebooks/<project-name>/

### Purpose (the open-ended investigation this notebook conducts)
[An open-ended question about the world. Examples:
"Does mean-reversion work on EUR/USD intraday?"
"Can PCA factors predict next-day stock returns?"
"Does Chronos add value over a frozen-embedding baseline?"
Multiple Hypotheses serving this Purpose live as `## H<id>` blocks below.]

### Universe (shared across all H's in this notebook)
- Instruments: [list at least three, or describe the cross-section]
- Period: [start, end]
- Frequency: [primary timeframe + auxiliary]

### Data ranges (shared across all H's in this notebook)
train [d1,d2] / val [d2,d3] / test [d3,d4], embargo H bars

### Upstream dependencies (shared across all H's in this notebook)
- Data: [paths and hashes]
- Pre-processing: [intermediate files produced by upstream notebooks]
- Upstream Purposes: [if their conclusions change, this notebook becomes invalid]

### Headline figure plan (written BEFORE any code runs)
- **What it shows**: [the one figure that conveys the answer to the Purpose
  — typically a multi-method comparison: cumulative PnL of every H against
  both baselines on the test set, or per-H Sharpe distribution, etc.]
- **Axes**: [x-axis = ?, y-axis = ?]
- **Comparisons / overlays**: [which series, which highlights, what
  shading for splits]
- **Observation the reader is supposed to draw from this figure alone**:
  [one sentence — what the reader sees when they look at this figure
  before reading any prose]
- Library / size: plotly or altair, full width, height ≥ 500 px
  (per `notebook_narrative.md`)

### Reader takeaway (one sentence, written BEFORE any code runs)
[After reading this notebook end-to-end, the reader walks away knowing:
 …]
```

The headline figure plan and reader takeaway are not stylistic — they are
the **goal-shape** of the notebook. Sketching them up-front prevents the
calculation-log failure mode where figures are added at the end as
decoration. The data fills in the numeric values; the figure's *shape* and
the takeaway sentence are research-design choices made before any data is
fitted.

## What to write per Hypothesis (one `## H<id>` block per H, repeated as new H's emerge)

Each Hypothesis block inside the notebook contains:

```markdown
## H<id> — <one-line statement>

### Linked hypothesis-portfolio entry
H<id>: [quote the entry from hypotheses.md; under the same `experiment_id`
as the notebook's Purpose]

### Question for this H
[Falsifiable comparison statement — see the table below.]

### Hypothesis
[Why it might or might not hold — from prior knowledge, or from earlier H's
in this notebook.]

### Why this H follows the previous one (only for derived H's)
[One sentence: which earlier H's result motivated this H, and what the
expected information gain is.]

### Design (this H only)
- Comparison: [method A / method B / baseline]
- Metrics: [Sharpe, IC, AUC, calibration, ...]
- Acceptance condition: [test-period numeric threshold that supports H]
- Rejection condition: [observation that would falsify H]
- Robustness gates: walk-forward mean Sharpe > 0, fee break-even fee reported,
  2D threshold surface majority-positive

### Per-H headline figure plan (written BEFORE this H's code runs)
- **What it shows**: [the figure that visualises this H's answer — usually
  cumulative PnL of this H vs. baselines on val/test, or this H's
  walk-forward Sharpe distribution]
- **Axes / overlays**: [...]
- **Observation the reader is supposed to draw from this figure alone**:
  [one sentence]

### Per-H observation the reader should leave with
[One sentence: what the reader knows about this H after reading just its
block.]
```

The universe / data ranges / upstream dependencies are inherited from the
notebook header (do not repeat them per H). Only what is genuinely H-specific
(comparison, metrics, thresholds, derived-from rationale) is repeated per H.

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
