# research_design.md

Template for the research-design Markdown that goes at the top of every notebook,
and rules for writing falsifiable comparison statements.

## When to read

- Starting a new notebook (before any implementation)
- Adding a new H block to an existing notebook
- Adding a new hypothesis to `hypotheses.md`

## What to write at the top of each notebook (Purpose header — once)

Each notebook (`experiments/exp_NNN_<purpose-slug>.py`) starts with a Markdown
cell containing the **Purpose** of the investigation plus the four
cycle-goal items defined in `cycle_purpose_and_goal.md`. The Purpose is
open-ended (it admits multiple H's); the cycle-goal items make explicit
*who consumes the cycle's knowledge output and what decision rule they will
apply to it*. Individual H's get their own per-H block lower in the
notebook.

The cycle-goal items (Consumer / Decision / Decision rule / Knowledge
output / target_sub_claim_id) are pre-implementation required. They are
what H1's design is derived from — without them, the H portfolio is
improvised per Purpose and downstream judgment becomes inconsistent. See
`cycle_purpose_and_goal.md` for the derivation of why these five items
exist and how to fill them, and `research_goal_layer.md` for the
four-layer model that the 5th item (`target_sub_claim_id`) ties this
notebook into.

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

### Cycle goal (five items — see cycle_purpose_and_goal.md)

#### Consumer
[Concretely named — the next derived Purpose, the production
strategy build, the paper section, the portfolio-sizing decision.
"The research community" / "future researchers" / "myself someday"
are NOT acceptable; if the only consumer is that vague, return to
Stage 0. "My own next Purpose, named as <slug>" is a legal
escape hatch when the next Purpose is *nameable in one phrase*.]

#### Decision the consumer is blocked on
[One sentence: the yes/no/pivot the consumer cannot make without
this cycle's output.]

#### Decision rule (committed BEFORE the cycle runs)
- YES (consumer goes forward): [numeric/structural threshold]
- NO  (consumer does not go forward, with binding axis): [numeric/
  structural threshold + which `failure_mode` would be the binding
  axis]
- KICK-UP (frame is wrong, return to upstream): [structural
  condition — e.g., bug_review surfaces unresolvable upstream
  data issue]

#### Knowledge output (artifact that lets consumer apply the rule)
[What the cycle produces — typically per-H rows in results.parquet
+ Purpose-level synthesis paragraph + headline figure. State it
explicitly so the H portfolio below can be checked against it.]

#### Target sub-claim id (research-goal anchor)
[The project README's research-goal sub-claim ID(s) this Purpose is
expected to advance. Primary: 1 sub-claim. Secondary: 0-2.
A Purpose targeting > 3 sub-claims is too broad; split before opening.
Example: "Primary G1.1 (`quality factor yields net edge in TOPIX500`).
Secondary: none."
See `cycle_purpose_and_goal.md` and `research_goal_layer.md`.]

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

### Sub-claim of the decision rule that this H tests
[Name the conjunct of the YES / NO / KICK-UP branches in the notebook's
decision rule that this H produces evidence for. Examples:
"YES branch's `walk-forward positive-rate ≥ 60%` conjunct"
"NO branch's `binding axis = fee_model` identification"
"YES branch's `no Pattern A binding axis` conjunct AND
NO branch's `regime_mismatch` identification — one well-designed
test covers both."
An H with no sub-claim mapping is not in the portfolio under
cycle_purpose_and_goal.md's frame; either map it to a conjunct of
the decision rule, expand the decision rule in decisions.md to
cover it (with justification), or drop the H.]

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
