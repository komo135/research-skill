---
name: quant-research
description: Use proactively when the user runs any quantitative-finance or algorithmic-trading research, alpha-factor research, strategy backtest, return prediction, regime detection, optimal execution, or any data → model → evaluation loop in Jupyter or marimo notebooks. Covers both mathematical-model research (OU process, PCA, state-space, factor models) and machine-learning research (classical ML, deep learning, reinforcement learning, foundation models). Establishes a falsifiable hypothesis BEFORE implementation, enforces a one-Purpose-per-notebook structure (one open-ended investigation per notebook with one or more falsifiable hypotheses tested under it; derived hypotheses serving the same Purpose stay inside the same notebook) with multi-instrument universe, exit-strategy parallel-comparison (NOT time-stop alone), time-series validation with embargo / purged k-fold / walk-forward, multi-agent bug review (parallel specialists plus an adversarial cold-eye reviewer, triggered per-Hypothesis when results look too good or before declaring a verdict on any individual hypothesis), a mandatory co-gate via the separate `experiment-review` skill before verdict='supported' on any hypothesis (both `bug_review` and `experiment-review` must pass), robustness battery (bootstrap / fee sensitivity / Probabilistic Sharpe Ratio / regime conditional), iterative hypothesis cycles inside a single notebook when the Purpose is unchanged, and notebooks that are self-contained communication artifacts so a reader of the .py file alone can understand what was investigated, why, how, and what was concluded. Use even when the user does not say "research" — any backtest, factor screening, or ML-on-financial-time-series task is in scope.
---

# Quant Research

A protocol skill for quantitative-finance and algorithmic-trading research that uses either
mathematical models or machine learning.

## Purpose

Keep the research at publication-grade quality. Writing a paper is not the goal, but the
research itself should reach a level at which a paper could be written.

Concretely:

- Fix a falsifiable hypothesis before writing any implementation
- One **Purpose** (an open-ended investigation about the world) per notebook;
  one or more **Hypotheses** tested inside it. Derived hypotheses that emerge
  from running an earlier hypothesis stay inside the same notebook as long as
  the Purpose is unchanged. A new Purpose ⇒ a new notebook. (See the next
  section for the operational distinction.)
- Enforce time-series validation
- Verify robustness before declaring completion (per Hypothesis)
- Iterate hypothesis cycles instead of stopping after one — usually inside the
  same notebook
- Make differentiation against prior work explicit so the research is not a degraded
  reimplementation

## Purpose vs. Hypothesis (read this before deciding to start a new notebook)

These are two different layers and must not be confused. The user-facing
mistake this skill is built to prevent is letting a hypothesis quietly become
the goal of an investigation — which happens whenever a researcher splits a
notebook for every new H without asking whether the *Purpose* changed.

| | **Purpose** | **Hypothesis** |
|---|---|---|
| What it is | An open-ended question about the world | A specific, falsifiable comparison statement |
| Form | "Does X work on Y?" | "Method A beats baseline B on test Sharpe by ≥ N" |
| Count | One per notebook | One or more per notebook |
| Where it lives | Notebook header (the `## Purpose` cell) | Each round inside the notebook (the `## H<id>` block) |
| Examples | "Does mean-reversion work on EUR/USD intraday?" / "Can PCA factors predict next-day returns?" / "Does Chronos add value over a frozen-embedding baseline?" | "RSI≤30 entry × signal-flip exit beats B&H test Sharpe ≥ 0.5 with fee 1 bp/side" |

A hypothesis serves a Purpose. The notebook is the unit of one Purpose. The
hypothesis log inside the notebook is where individual H's are tested.

### When a derived hypothesis stays in the same notebook

Default: **same notebook**. A derived hypothesis stays in the current
notebook whenever the Purpose is unchanged. This includes (but is not limited
to):

- A sensitivity / parameter-sweep variant of an earlier H
- A failure-diagnosis variant ("H1 was rejected — was it the threshold or
  the data?")
- A specialization / refinement ("H1 worked overall — does it work in
  trending regime only?")
- An alternative formulation of the same investigation ("H1 used RSI; try
  Bollinger as a different lens on the same mean-reversion question")
- A follow-on layer on top of an earlier H ("H1's signal × vol-targeted
  sizing")

In all these cases the *open-ended investigation* the notebook is conducting
is the same. The next H is the next round inside the same hypothesis log,
not a new notebook.

### When to open a new notebook

Open a new notebook **only** when the Purpose itself changes. Concrete
triggers:

- Different phenomenon under investigation (mean-reversion → momentum,
  return prediction → volatility prediction)
- Different cross-section / asset class (FX → equity, single-name → index)
- Different prediction target where the target change reflects a new
  question (not just a different metric on the same target)
- Different model class **only when** that change reflects a different
  question (e.g. "is mean-reversion in this market?" vs. "do
  foundation-model embeddings add information here?")

### Anti-rationalizations to resist

| Excuse | Reality |
|---|---|
| "H2 is a different central hypothesis, so it goes in a new notebook." | The notebook is per-Purpose, not per-Hypothesis. "Different central hypothesis" is no longer a split criterion. Ask: did the Purpose change? |
| "exp_001 is already verdict='supported' and finalized; opening it again is dirty." | A finalized H1 inside a notebook does not seal the notebook. The notebook stays open for further H's serving the same Purpose. Each H has its own verdict; the notebook itself does not have a single verdict. |
| "I need clean re-runnability per hypothesis, so each H needs its own notebook." | Re-runnability is a marimo cell-graph property, not a file property. Use H-suffixed variable names (`signal_h1`, `signal_h2`) and per-H sub-sections inside one notebook. See `references/marimo_cell_granularity.md`. |
| "The derived H needs to read intermediate files from the earlier H — that's a dependency, so it's a different experiment." | If H2 builds on H1's signal, the natural place for H2 is the same notebook where H1's signal already lives. Intermediate-file passing across notebooks is the correct pattern only when the Purpose differs. |
| "If I keep adding H's the notebook will grow unmanageable." | Multi-Hypothesis notebooks legitimately exceed the old "10-30 cells / 200-500 lines" guidance. That guidance no longer applies. Physical splits (one Purpose, two `.py` files) are not a planned case. |
| "Run-now derived hypothesis means start the next notebook (the old `hypothesis_cycles.md` rule said so)." | The old rule was wrong and has been replaced. Run-now derived H's serving the same Purpose continue in the same notebook. See the updated `hypothesis_cycles.md`. |

## Notebook is a communication artifact from the start (not after-the-fact)

The notebook serves two readers (the `.py` source reader and the marimo reader)
and must communicate to both. Communication design — *what figure tells the
story, what observation each figure raises, what the reader takes away* — is
a **pre-implementation** concern, not an end-of-pipeline cleanup. If the
headline figure and the reader's takeaway are not designed before any code
runs, the notebook ends up as a calculation log retrofitted with charts.

Concretely:

- Step 2 (research design) requires the **headline figure plan** alongside
  Purpose / H1 / Universe / Data ranges — written before implementation.
- Each `## H<id>` block names its **per-H headline figure** in the per-H
  design header before any code in that round runs.
- The full figure / observation / interpretation discipline lives in
  `references/notebook_narrative.md`. Read it **before** writing the first H,
  not after. Treating it as an end-of-notebook polish step is the failure
  mode this skill is built to prevent.

The figure-plan-up-front rule is what differentiates a research notebook
from a script that happened to produce numbers.

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
  Hypothesis portfolio (hypotheses.md) — first H per Purpose
       ↓
[Open a notebook for one Purpose]
       ↓
  Create the notebook (experiments/exp_NNN_<purpose-slug>.py) with a
  Purpose header
       ↓
  Test H1 → bug_review (if triggered) → robustness → experiment-review →
    H1 verdict → append one row to results.parquet
       ↓
  Did a derived H emerge that serves the SAME Purpose?
       ↓ yes                                 ↓ no (new Purpose)
  Test H2 inside the same notebook        Close this notebook;
       ↓                                   open exp_<NNN+1>_*.py
  Continue until the Purpose is exhausted
       ↓
  Purpose-level conclusion (synthesis across H1…HN) +
    derived Purposes (= candidates for new notebooks)
       ↓
[Completion]
       ↓
  Per-Hypothesis robustness battery → research-quality checklist (per project)
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

### 2. Write the research design first in Markdown — including the figure plan

See `references/research_design.md`. At the top of each notebook, write:

- **Purpose** — the open-ended question the notebook investigates
- **First Hypothesis (H1)** — a specific falsifiable comparison statement
  serving the Purpose, with numeric acceptance / rejection thresholds
- Universe (list at least three instruments, or describe the cross-section)
- Data range (train / val / test, embargo size)
- **Headline figure plan** — what the one-and-only figure that conveys the
  answer to the Purpose will *show* (axes, comparison, observation the
  reader is supposed to draw). Written before any code runs; only the
  numeric values come from the data.
- **Reader takeaway** — one sentence: what the reader (`.py` or marimo)
  walks away knowing after reading this notebook end-to-end.

When a derived H emerges serving the same Purpose, add a new `## H<id>`
block inside the same notebook with its own falsifiable statement,
acceptance / rejection thresholds, **per-H headline figure plan**, and per-H
result row.

The figure plan and reader takeaway are required pre-implementation items.
"I'll figure out the figure when I have the data" is the failure mode that
produces calculation-log notebooks. Sketch the figure's *shape* (axes,
overlays, comparison) up front; the data fills in the values, not the
design.

See `references/notebook_narrative.md` for the full communication-artifact
spec. Read it before writing H1's first code cell, not at the end.

### 3. One Purpose = one notebook

See `references/experiment_protocol.md`. The unit of one notebook is one
**Purpose** (an open-ended investigation), not one Hypothesis. Multiple
hypotheses serving the same Purpose are tested as successive rounds inside
the same notebook.

Reasons one notebook still maps to one Purpose:

- The Purpose is the durable intent of the investigation; tying it to the
  notebook is what prevents derived hypotheses from quietly becoming the
  goal
- All H's under one Purpose share the same upstream data, splits, and
  baselines — duplicating those across notebooks per H is wasteful and
  invites silent divergence
- The Purpose-level synthesis (which H worked, which didn't, what the
  collective answer is) needs all the H's in one place to be readable

Reasons one notebook does **not** map to one Hypothesis (anti-rule, was
true under the previous protocol and is no longer):

- "Different central hypothesis = different notebook" — discarded
- "Run-now derived hypothesis = next notebook" — discarded
- "Sensitivity / refinement / failure-diagnosis = stays in the same
  notebook only as a sub-cell of the original H" — replaced by "is its own
  H<id> block in the same notebook"

The cell-graph constraints (marimo's no-redefinition rule, independent
re-runnability) are now handled by H-suffixed variable naming
(`signal_h1`, `signal_h2`) and per-H sub-sections, not by file splitting.
See `references/marimo_cell_granularity.md`.

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
Both are required before `verdict = "supported"` **on any individual hypothesis**.
The gate fires per Hypothesis, not per notebook: a notebook with H1, H2, H3 inside
runs the two review layers up to three times — once per H whose verdict is being
declared `supported`. Multiple H's completing in the same session can be batched
into one inline review summary, but every H named in the summary must be covered
by every dimension. The most common confusion is between the two `validation`
scopes — one in each layer.

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

### 11. Multi-agent bug review (per Hypothesis, runs *before* that H's robustness battery)

See `references/bug_review.md` and `references/sanity_checks.md`. A passing robustness
battery is necessary but not sufficient — leaks, misalignments, and accounting bugs
contaminate every robustness gate uniformly and turn the green ticks into false
confidence. This step fires **per Hypothesis** when any *trigger condition* is met
for that H:

- Numeric red flag (e.g. test Sharpe > 3, walk-forward mean Sharpe > 2, ML AUC > 0.65 on
  return-sign, headline metric outside bootstrap 95 % CI, headline ≥ 2 × walk-forward
  mean — full table in `bug_review.md`)
- State-change trigger: before `verdict = "supported"` is set for this H; before the
  test set is touched for this H; after any change to data ingestion, target, embargo,
  fold, feature scaling, signal alignment, or fee model that affects this H

If multiple H's in the same notebook are about to receive `verdict = "supported"` in
the same session, the bug-review pass may be batched (one inline summary covering
all of them) provided every H is named explicitly under every reviewer dimension.

When fired, dispatch six sub-agents *in parallel*: five specialist reviewers — one
each for leakage, PnL accounting, validation-correctness, statistics / metric
correctness, and generic code correctness — plus one adversarial cold-eye reviewer
with a deliberately minimum context bundle (code + reported numbers only; no other
reviewers' findings, no `decisions.md`, no `hypotheses.md`). The asymmetry of the
adversarial bundle is the mechanism that breaks same-model anchoring — see
`bug_review.md` for the exact bundle and instruction.

Each returns severity-tagged findings; `high` and `medium` findings block re-running
the battery and block any verdict change until resolved. Findings are aggregated
**inline in the assistant's reply** — the skill does not write to `decisions.md`
or create any file. The session transcript is the audit surface; if the user
wants a durable record they can copy the inline summary themselves.

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

### 13. Multi-agent experiment review (per Hypothesis, research quality) — invokes the `experiment-review` skill

The `experiment-review` skill is a **separate skill**. Invoke it via the Skill tool at
this step. **MANDATORY co-gate with step 11.** Both must pass before
`verdict = "supported"` is set for any individual hypothesis. This step is not
optional or advisory; it is a required gate.

The reviewer reads the entire notebook (Purpose header, all H<id> blocks up to and
including this H, the per-H result row schema), but the verdict gate it controls is
per-H. Multiple H's may share one experiment-review pass when they enter the gate
in the same session, provided every H is named explicitly in the dimension findings.

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
context. Returns severity-tagged findings aggregated **inline in the assistant's
reply** — the skill does not write a review report file or modify any project
artifact. See the `experiment-review` skill's own SKILL.md and references for
the dimension scopes and dispatch protocol.

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

### 14. Result aggregation (per Hypothesis)

See `references/results_db_schema.md`. **Each Hypothesis in the notebook produces
its own row** in `results/results.parquet`. The schema already carries
`experiment_id` (= the notebook = the Purpose) and `hypothesis_id` (= the
individual H within the Purpose) as separate columns; a notebook with three
H's emits three rows. The append happens at the end of each H's round inside
the notebook, not once at the end of the file. Without per-H rows, cross-H and
cross-experiment comparison is impossible.

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
not select numbers that flow into `results.parquet`). Every figure is either intuitive
at a glance or carries an embedded read-out (title naming the comparison, annotation
stating how to read the encoding, or a one-line conclusion in the figure); sweep
figures mark the adopted configuration when one exists. Every helper function defined
in the notebook has a docstring stating intent, the responsibility split, args / returns
with producing / consuming cells, and side effects. Each H block opens with a config
cell naming sweep grids and chosen-configuration constants; downstream cells reference
the names, not raw literals.

### 17. Iterate hypothesis cycles

See `references/hypothesis_cycles.md`. Do not stop after one cycle. After each H
inside the notebook, classify derived hypotheses as "run now / next session / drop"
and log them in `hypotheses.md` and `decisions.md`.

- A run-now derived H **serving the same Purpose** is the next round inside the
  same notebook (a new `## H<id>` block, not a new file).
- A run-now derived H whose investigation reflects a **new Purpose** opens the
  next notebook (`exp_<NNN+1>_*.py`).
- "Run-now derived hypothesis = next notebook" is the **old** rule and has been
  discarded. The new rule routes by Purpose continuity, not by run-readiness.

## Completion gate (per Hypothesis)

Before declaring `verdict = "supported"` on **any individual hypothesis**, all
**three** gates must pass for that H — *in this order*:

1. **Step 11 — `bug_review` (in this skill)**: 5 specialist reviewers + 1 adversarial
   cold-eye reviewer, no unresolved `high` or `medium` findings for this H.
2. **Step 13 — `experiment-review` (separate skill, invoke via Skill tool)**: 7
   specialist reviewers + 1 adversarial cold-eye reviewer, no unresolved `high` or
   `medium` findings for this H.
3. **`references/research_quality_checklist.md`**: passes as final self-check for
   the H (and at project level, the Purpose-level synthesis the notebook produces
   from the H's it contains).

Setting `verdict = "supported"` on any H without all three is a protocol violation
that downgrades that H's result to *preliminary screening*. Each gate's pass/fail
must be visible in the assistant's reply (trigger, reviewer roster, findings,
resolution) — the skills do not write to `decisions.md`. If the user wants a
durable record they can copy the inline summaries themselves.

The notebook itself does **not** carry a single verdict. Different H's inside the
same notebook can land at different verdicts (e.g. H1 = supported, H2 = rejected,
H3 = parked); the Purpose-level conclusion is a synthesis across those H verdicts,
not a separate gate.

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
