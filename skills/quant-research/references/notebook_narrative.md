# notebook_narrative.md

A quant-research notebook is a primary research artifact for one **Purpose**.
It contains one or more Hypothesis rounds; the narrative layers carry both
the Purpose-level story and per-H stories. The notebook must communicate to
**two readers** at the same time:

| Reader | Sees | Must get |
|---|---|---|
| `.py` source reader | markdown cells + code + comments | Story, decisions, interpretation, conclusion |
| marimo reader | Rendered notebook + figures + UI widgets | Same story + visual evidence + drill-down |

If only one reader gets the picture, the notebook is broken.

## When to read

- Drafting the markdown cells of an experiment notebook
- Writing the figure cells
- Writing the conclusion / interpretation cells

## Required prose anchors

These markdown cells are mandatory in *every* experiment notebook.

### 1. Abstract cell at the top (200-400 words) — Purpose level

Filled in **after** all the H rounds are done, but placed immediately after
the title. Must contain:

- **Purpose** — the open-ended investigation in one sentence
- **Hypotheses tested** — H1, H2, …, each with its falsifiable statement
  in one short line
- **Conclusion** — Purpose-level synthesis: which H's were supported, which
  rejected, what the collective answer to the Purpose is, with the
  headline numbers per H (test Sharpe, drawdown, PSR)
- **Why this matters or doesn't** — one sentence at the Purpose level
- **Pointer to the headline figure** — cell number or fig name (usually a
  multi-method comparison spanning the H's)

Without this, the next reader has to read every H block to know whether the
Purpose is answered.

### 1b. Per-H abstract block (one short paragraph per H, immediately above the H block)

Each `## H<id>` block opens with a 2-3 sentence summary mirroring the
Purpose-level abstract but at the H level: H statement, verdict, headline
metric, one-sentence interpretation. This is what a reader scrolling
through the notebook sees first about each H.

### 2. Per-section "what & why" cell

Before each numbered section, a markdown cell of 1-3 sentences:

- What this section computes
- Why it exists — which decision in the design it informs
- What the reader should look for in the figure / table that follows

### 3. Per-figure observation cell

After every figure cell, a markdown cell with the *observation*. Not the metric
value — that's already in the figure title — but **what we infer**.

Examples:

- "IC drifts negative across 2020-Q2; the regime sensitivity here motivates
  derived hypothesis H5."
- "Walk-forward Sharpe is positive in 14 / 16 windows; the two negative windows
  are 2018-Q4 and 2020-Q1, both high-vol regressions."

A figure with no observation cell is decoration. Either write the observation or
remove the figure.

### 4. Prose interpretation cell before each programmatic verdict (per H)

Three sub-questions, **per H**:

1. What did the numbers say (for this H)?
2. Why is this the answer mechanistically — what is the model picking up?
3. What is the next falsifiable question this H raises (next H block in this
   notebook if same Purpose, candidate for a new notebook if new Purpose)?

A `print("supported")` cell on its own is not a conclusion.

### 4b. Purpose-level synthesis cell (after all H rounds)

After the last H block, a synthesis cell ties the H verdicts together:

1. Which H's were supported, which rejected, which parked?
2. What does that collectively say about the Purpose?
3. What derived **Purposes** does this raise for future notebooks?

This is distinct from any individual H's interpretation — it is the answer
the reader takes away about the Purpose itself.

## Figure rules

### Figures are evidence, not decoration

For every figure, you must be able to answer:

- Which decision in the research design does this figure support?
- What would a reader conclude from this figure alone?
- What is the comparison? (a single line of one method is rarely a figure)

If a figure cannot answer all three, delete it.

### Required figures per experiment

| Figure | Purpose |
|---|---|
| Universe + train / val / test split overlay | Orientation; verifies no leak |
| Multi-method comparison (cum return / IC) | Ranking the candidates |
| Robustness 2D surface (heatmap) | Parameter stability |
| Walk-forward Sharpe distribution | Time stability |
| Bootstrap / PSR distribution | Statistical confidence |
| Test-set evaluation (touched once) | The final answer |

Add more as the project requires; never fewer.

### Size

- **Width**: full-width — `width="full"` in plotly / altair, or matplotlib
  `figsize=(14, ...)`
- **Height**: ≥ 450 px for single-panel, ≥ 600 px for multi-panel
- A figure the reader has to squint at is a figure they will skip

### Library default

- **Headline figures: plotly or altair**. Hover, zoom, and legend-toggle let one
  figure carry more information than its static counterpart, with no cost to
  reproducibility (the figure is reproduced from fixed code; only the rendering
  is interactive).
- **Diagnostics: matplotlib is fine**. Use it for paper-style static panels or
  PNG export to a report.
- **Always** display the figure as the last expression of the cell so marimo
  renders it inline.

```python
import plotly.express as px

fig = px.line(df, x="date", y="cum_pnl", color="method", height=500)
fig.update_layout(width=None, legend=dict(orientation="h"))
fig
```

## Interactive UI elements (mo.ui)

`mo.ui` widgets are part of the communication layer.
**They explore evidence; they do not pick reported parameters.**

| Use mo.ui for | Do not use mo.ui for |
|---|---|
| Switching instrument / sector to inspect | Picking the threshold the conclusion uses |
| Toggling regime overlay on the equity curve | Tuning a hyperparameter for the headline number |
| Date-window zoom on a time series | Choosing fees / horizons that flow into results.parquet |
| Drill-down on a heatmap cell | Anything that flows into the verdict cell |

The reported numbers still come from the fixed sweep cells (threshold surface,
fee sweep, walk-forward) — exactly as the robustness battery prescribes. The
interactive widgets sit *next to* those cells so the reader can poke at the same
evidence the sweep summarized.

Recommended widgets per experiment:

- `mo.ui.dropdown(instruments, ...)` to swap the instrument shown in a
  per-instrument PnL figure
- `mo.ui.range_slider` over the date range for an equity-curve zoom
- `mo.ui.dropdown(regime_labels, ...)` to filter a regime-conditional figure

Anti-rationalization: "sliders cause p-hacking" is correct only when the slider
chooses the reported number. A dropdown that swaps which instrument is plotted,
or a range slider that zooms a time axis, does not select any number that
appears in `results.parquet`.

## What lives where

| Source-readable (markdown / comments / docstrings) | Figure-only |
|---|---|
| The hypothesis | The shape of returns |
| Acceptance / rejection thresholds | Visual diagnostic of fit |
| Numeric results | Cumulative PnL trajectory |
| Interpretation prose | Hover detail per data point |
| Next derived hypothesis | UI drill-down |

Both layers are required. Strip either and one reader loses the story.

## Quick checklist

Before declaring an experiment notebook complete:

- [ ] Purpose-level abstract cell at the top, filled in (not stub text), with
      a per-H summary line for each H tested
- [ ] Each `## H<id>` block opens with its own short per-H abstract
- [ ] Every section has a what & why markdown cell
- [ ] Every figure has an observation cell directly after it
- [ ] At least one prose interpretation cell before each per-H programmatic
      verdict
- [ ] Purpose-level synthesis cell after the last H block
- [ ] Headline figures use plotly / altair (interactive)
- [ ] Headline figure height ≥ 450 px, width = full
- [ ] At least one `mo.ui` widget for evidence drill-down
- [ ] No `mo.ui` widget controls a number that lands in `results.parquet`
