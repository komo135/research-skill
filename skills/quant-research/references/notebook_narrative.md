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

### A figure must be self-explanatory at figure-time

The reader must understand *what is shown* and *how to read it* without
cross-referencing the surrounding prose. Two acceptable shapes:

1. **Intuitive figure** — axes, units, color encoding, and a baseline /
   reference make the answer obvious at a glance. Examples: cumulative-PnL
   line chart colored by method; calibration plot with a `y = x` reference;
   rolling Sharpe with a horizontal zero line. The visual idiom is standard,
   so no extra read-out instruction is needed.
2. **Annotated figure** — when the encoding is not standard (heatmap of a
   non-standard quantity, multi-panel diagnostic, projection of a high-dim
   space), the figure itself carries the read-out:
   - **Title** names both the quantity and the comparison — not "Heatmap" but
     "Sharpe by (threshold, hold) on val (2022-2023)"
   - **Subtitle / footnote / annotation** states the read-out rule —
     "blue = better; the white midline = zero", "diagonal = perfect
     calibration", "shaded = 95 % bootstrap band". A divergent color scale
     (`RdBu`, `RdYlGn`) is intuitive *only* if the rule is also stated in the
     legend or annotation.
   - **OR** a one-line conclusion baked into the figure (text annotation,
     callout, or `mo.md` cell *immediately above* the figure with the
     take-away in one sentence)

**Conditional rule — chosen-point marker.** When a sweep figure (heatmap,
fee curve, threshold surface) is paired with a specific configuration that
the notebook adopts elsewhere (e.g. H1 reports threshold=30 and the heatmap
sweeps over thresholds), mark that point on the figure (annotation, scatter
overlay, vertical line). A reader looking at the surface should be able to
locate "this is the configuration H1 used" without reading prose. If the
sweep is purely surface-level evidence with no adopted point, this rule does
not apply.

The observation cell that follows (mandated by *Per-figure observation cell*
above) carries the *observation* — what we infer. The read-out instruction
is different: it tells the reader how to *look* at the picture so they can
verify the observation against the visual instead of trusting the prose
blindly. Both are required when the figure is not intuitive.

If a figure cannot be made self-explanatory by either route, the figure is
trying to carry too much — split it into two simpler figures, each of which
can.

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

## Code-level conventions (for the `.py`-source reader)

The prose-anchor rules above target both readers. The rules in this section
target the `.py`-source reader: the code itself must explain its intent so a
colleague reading the file (in an editor, in a diff, in a code review) can
follow the H's pipeline without running the notebook.

### Function docstrings — intent and responsibility

Every helper function defined inside the notebook must carry a docstring
covering all four of these. A one-line docstring that paraphrases the body
(e.g. `"""RSI mean-reversion: long when RSI <= threshold, exit on cross-back."""`)
does not satisfy this rule — it restates *what* the code does, which the
code already says, and omits the *why* and the *contract*.

1. **Intent (the role)** — one sentence: what this function is responsible
   for in the pipeline. Not a paraphrase of the body — the *role* it plays
   relative to the rest of the H's cells.
2. **Why this responsibility lives in its own function** — one phrase: what
   would become unclear or break if this were inlined into the calling cell.
   This is what justifies the abstraction; without it, the function tends to
   accrete unrelated logic over time.
3. **Args / Returns** — names with type or shape if non-obvious; mention the
   producing/consuming cell or section number when the binding is non-local
   (e.g. "consumed by §6 robustness battery"). The reader should be able to
   trace the function's inputs and outputs through the notebook by reading
   only the docstring.
4. **Side effects** — file writes, `results.parquet` appends, plot displays,
   global RNG mutation. State `Side effects: none.` explicitly when there
   are none. marimo's reactive graph hides side-effect ordering; a function
   that writes a file *must* declare it so the reader knows the cell is not
   idempotent.

```python
def fit_rsi_meanrev(prices, rsi_threshold, fee_per_side):
    """Fit one (threshold, fee) configuration of the H1 RSI mean-reversion
    strategy and emit the per-bar net-PnL series.

    Lives in its own function so the H1 sweep cell stays at one fit per call
    (see references/marimo_cell_granularity.md); inlining would mix
    parameter setup with sweep-loop bookkeeping.

    Args:
        prices         — close-price series (cell §1 output: `eurusd_5m`)
        rsi_threshold  — RSI level for the long entry (configured in the
                         H1 config cell, swept in §6)
        fee_per_side   — round-trip half-fee (configured in the H1 config
                         cell, swept in §7)

    Returns:
        pl.Series of per-bar net returns, consumed by the §6 sweep table and
        the §7 fee-sensitivity cell.

    Side effects: none.
    """
    ...
```

Lambdas and one-line helpers are exempt only when the name is fully
self-describing AND the helper is local to one cell. Anything that crosses
cells gets a docstring.

### Magic numbers belong in a config cell at the top of the H block

Bare numeric literals (`14`, `0.0001`, `"5min"`, `30`) buried mid-pipeline
force the reader to hunt for the value's meaning. Concentrate them in a
**config cell at the top of the H block**, named with a short comment:

```python
# H1 config — sweep ranges and chosen point
RSI_WINDOW       = 14            # standard RSI lookback (Wilder)
RSI_TAU_GRID     = [25, 30, 35, 40]
RSI_TAU_CHOSEN   = 30            # H1's reported configuration
HOLD_HORIZONS    = [6, 12, 24, 48]   # max-hold caps in 5-min bars
FEE_GRID         = [1e-4, 2e-4, 5e-4, 1e-3]  # per-side
FEE_CHOSEN       = 1e-4
BAR_FREQ         = "5min"
```

Cell-private grid lists (`_thresholds = [25, 30, 35, 40]` defined inside
the sweep cell itself) are not a substitute — the chosen configuration
constants and their semantic names belong at the top of the H block where
the reader meets them first. Downstream cells reference the named
constants, never raw literals.

This is also a **no-new-external-dependency** notebook: stay expressive
within the project's existing imports (marimo / polars / numpy / plotly /
altair / matplotlib). Reaching for a new library to make one figure prettier
propagates that dependency to every future notebook in the project — a
wrong trade.

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
- [ ] Every figure is either intuitive at a glance OR carries an embedded
      read-out (title naming the quantity + comparison, annotation stating
      how to read the encoding, or a one-line conclusion in the figure)
- [ ] When a sweep figure is paired with an adopted configuration elsewhere
      in the notebook, that point is marked on the figure
- [ ] At least one `mo.ui` widget for evidence drill-down
- [ ] No `mo.ui` widget controls a number that lands in `results.parquet`
- [ ] Every helper function defined in the notebook has a docstring stating
      intent, the responsibility split, args/returns with their producing /
      consuming cells, and side effects (`Side effects: none.` when none)
- [ ] H block opens with a config cell naming all sweep grids and chosen
      configuration constants; downstream cells reference the names, not
      raw literals
- [ ] No new external library is required beyond the project's existing
      imports
