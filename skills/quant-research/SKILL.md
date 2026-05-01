---
name: quant-research
description: Use proactively when the user runs any quantitative-finance or algorithmic-trading research, alpha-factor research, strategy backtest, return prediction, regime detection, optimal execution, or any data → model → evaluation loop in Jupyter or marimo notebooks. Covers both mathematical-model research (OU process, PCA, state-space, factor models) and machine-learning research (classical ML, deep learning, reinforcement learning, foundation models). Establishes a falsifiable hypothesis BEFORE implementation, enforces a one-Purpose-per-notebook structure (one **research thesis** = parent claim about the world per notebook, tested by one or more falsifiable child hypotheses; derived hypotheses serving the same Purpose stay inside the same notebook AND must declare own falsifiable claim, own stated purpose distinct from parent, and a meaningful research unit — sensitivity sweeps and parameter-only follow-ons belong in the robustness battery, not the hypothesis log) with multi-instrument universe, exit-strategy parallel-comparison (NOT time-stop alone), time-series validation with embargo / purged k-fold / walk-forward, multi-agent bug review (parallel specialists plus an adversarial cold-eye reviewer, triggered per-Hypothesis when results look too good or before declaring a verdict on any individual hypothesis), a mandatory co-gate via the separate `experiment-review` skill before verdict='supported' on any hypothesis (both `bug_review` and `experiment-review` must pass), robustness battery (bootstrap / fee sensitivity / Probabilistic Sharpe Ratio / regime conditional), iterative hypothesis cycles inside a single notebook when the Purpose is unchanged, a Purpose-level verdict at notebook closure declaring the parent thesis supported / refuted / partial (NOT just per-H verdicts; the parent claim does not get to escape rejection by spawning a derived Purpose that re-asserts it), schema using `purpose_id` (NOT `experiment_id`) as the notebook's primary identifier so that `experiment` is reserved for "the apparatus that tests one hypothesis" (each `## H<id>` block is one experiment), and notebooks that are self-contained communication artifacts so a reader of the .py file alone can understand what was investigated, why, how, and what was concluded. Use even when the user does not say "research" — any backtest, factor screening, or ML-on-financial-time-series task is in scope.
---

# Quant Research

A protocol skill for quantitative-finance and algorithmic-trading research that uses either
mathematical models or machine learning.

## Purpose

Keep the research at publication-grade quality. Writing a paper is not the goal, but the
research itself should reach a level at which a paper could be written.

Concretely:

- Fix a falsifiable hypothesis before writing any implementation
- One **Purpose** (a research thesis: the parent claim about the world that
  the notebook is built to test) per notebook; one or more **Hypotheses**
  tested inside it as the falsifiable child claims that decompose the parent.
  Each H block is **one experiment** (= the apparatus that tests one
  hypothesis); the notebook is the cluster of experiments under one Purpose.
  Derived hypotheses that emerge from running an earlier hypothesis stay
  inside the same notebook as long as the Purpose is unchanged AND each
  derived H declares own falsifiable claim, own stated purpose distinct
  from parent, and a meaningful research unit (see "Derived hypothesis
  admissibility" below). A new Purpose ⇒ a new notebook. (See the next
  section for the operational distinction.)
- The notebook closes with a **Purpose-level verdict** declaring the
  parent thesis supported / refuted / partial — alongside (not replacing)
  the per-H verdicts. The parent claim is itself falsifiable; it does not
  get to escape rejection by spawning a derived Purpose that re-asserts it.
- Set the **cycle goal** before any code: name the downstream Consumer, the
  Decision they are blocked on, the Decision rule (YES / NO with binding axis
  / KICK-UP, committed before the cycle runs), and the Knowledge output. The
  H portfolio is *derived from* the decision rule, not improvised. See
  `references/cycle_purpose_and_goal.md`.
- Enforce time-series validation
- Verify robustness before declaring completion (per Hypothesis)
- Iterate hypothesis cycles instead of stopping after one — usually inside the
  same notebook. The cycle ends when the consumer can apply the decision rule
  (Primary YES / Fallback NO with binding axis / KICK-UP — all three are
  equivalent research outputs); N=5 / N=8 are emergency stops, not the
  intended termination.
- Make differentiation against prior work explicit so the research is not a degraded
  reimplementation

## Purpose vs. Hypothesis (read this before deciding to start a new notebook)

These are two different layers and must not be confused. The user-facing
mistake this skill is built to prevent is letting a hypothesis quietly become
the goal of an investigation — which happens whenever a researcher splits a
notebook for every new H without asking whether the *Purpose* changed.

| | **Purpose** (= research thesis = parent claim) | **Hypothesis** (= child claim, tested by one experiment) |
|---|---|---|
| What it is | A parent claim about the world the notebook is built to test (= the thesis) | A specific, falsifiable comparison statement that decomposes the parent claim |
| Form | "X works on Y under conditions C" (declarative, falsifiable at the notebook level) | "Method A beats baseline B on test Sharpe by ≥ N" |
| Count | One per notebook | One or more per notebook (each one tested by one experiment) |
| Where it lives | Notebook header (the `## Purpose` cell) — verdicted at notebook closure | Each round inside the notebook (the `## H<id>` block) — verdicted via the per-H 4-gate flow |
| Examples | "Mean-reversion at H1 frequency on EUR/USD generates risk-adjusted edge net of cost" / "PCA factors carry next-day return information beyond a market-cap factor" / "Chronos embeddings add information beyond a frozen-embedding baseline" | "RSI≤30 entry × signal-flip exit beats B&H test Sharpe ≥ 0.5 with fee 1 bp/side" |

A hypothesis serves a Purpose by partly decomposing the parent claim. The
notebook is the unit of one Purpose; the hypothesis log inside is where the
parent claim is tested by individual experiments. The Purpose itself is
verdicted at notebook closure (supported / refuted / partial); per-H
verdicts feed that Purpose-level verdict but do not replace it.

### Derived hypothesis admissibility (= what may legally become an H<id>)

A derived hypothesis is admitted to the hypothesis log only when **all
three** of the following hold:

1. **Own falsifiable claim** distinct from the parent H's claim — the
   derived H's acceptance / rejection threshold is on a different decision
   axis (not just a tighter / looser threshold on the parent's axis).
2. **Own stated purpose** — one sentence answering "what new question
   does this H answer that the parent H did not?". The answer is written
   in the per-H design header, not retrofitted at interpretation time.
3. **Meaningful research unit** — the H is at the granularity of an
   independent finding, not a 1-axis parameter sweep over the parent's
   pipeline. A sweep over sizing / threshold / regime / lookback is
   robustness analysis (Step 12), not a new H.

Admissible derived-H types (each must still pass the three conditions
above):

- A **failure-diagnosis** H ("H1 was rejected; H2 tests whether the
  rejection is driven by the threshold or by a regime composition
  change") — admissible when the diagnosis is itself a falsifiable claim
  with an axis distinct from H1's headline metric.
- A **specialization / refinement** H ("H1 supported overall; H2 tests
  whether the edge is conditional on a *named, pre-committed* regime
  signal external to the strategy") — admissible when the regime
  conditioning is a research question on its own (e.g. "does the signal
  encode regime-specific information?"), not a fitting attempt to
  recover headline performance after rejection.
- An **alternative formulation** H ("H1 used RSI; H2 tests whether
  Bollinger as a different operationalization of the same mechanism
  yields the same conclusion") — admissible when H2's purpose is to test
  whether the *conclusion* is robust to operationalization, not to find
  a sibling parameterization that rescues a rejected H1.

Inadmissible (= these belong elsewhere, NOT in the hypothesis log):

- **Sensitivity / parameter-sweep** variant of an earlier H — belongs in
  Step 12 robustness battery (`references/robustness_battery.md`),
  reported as 2D / 3D grids inside the parent H's section, not as a
  separate H<id>. Adding `signal × vol-targeted sizing` and registering
  it as `H2` is a sweep escalated to a hypothesis; the sizing axis is
  robustness, not a new finding.
- **Follow-on layer** on top of an earlier H ("H1's signal × X") where X
  is a sizing / cost / portfolio-construction layer that does not change
  the underlying claim about the world — belongs in Step 10 portfolio
  construction or Step 12 robustness, not as a new H.
- **Threshold-variation** rerun of an earlier H ("H1 with acceptance
  threshold lowered to recover marginal cases") — explicit
  anti-rationalization, never admissible.

In all admissible cases the *Purpose* the notebook is testing is the same.
The next H is the next round inside the same hypothesis log, not a new
notebook. In inadmissible cases, the work is real and may still be
necessary, but it is not an H — it is a robustness or engineering pass
inside the parent H's section.

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
| "pur_001 is already verdict='supported' and finalized; opening it again is dirty." | A finalized H1 inside a notebook does not seal the notebook. The notebook stays open for further admissible H's serving the same Purpose. Each H has its own verdict, and the notebook itself carries a Purpose-level verdict at closure (the parent thesis is verdicted supported / refuted / partial). The notebook is sealed only at Purpose-level closure, not at the first H reaching `supported`. |
| "H2 is a vol-targeted sizing variant of H1's signal — that's a follow-on layer, so it goes in the hypothesis log." | A sizing-layer / threshold-sweep / regime-conditioning variant whose only difference from the parent is one robustness axis is a sensitivity sweep escalated to a hypothesis. It belongs in Step 12 robustness battery, not in the hypothesis log. See "Derived hypothesis admissibility". |
| "H1 was rejected; let me run H2 with a tighter threshold / different period to see if it survives." | This is fishing for survival on the parent's axis. Inadmissible as a new H. Either (a) close H1 rejected and run a *failure-diagnosis* H with a different axis (Step 1.5 Pathway 4), or (b) record the threshold-sensitivity as robustness inside H1 and accept its rejection. |
| "Without a Purpose-level verdict the notebook is fine — H verdicts cover everything." | They do not. Per-H verdicts cover individual decompositions; the parent thesis (= Purpose) is itself a falsifiable claim and must receive its own verdict at notebook closure. Without it, the parent claim escapes rejection by spawning a derived Purpose that re-asserts it. |
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
  (Stage 0: Pre-hypothesis exploration) — IF the start state is
    data-without-candidate-phenomenon. Skipped when the researcher
    arrives with a candidate from prior intuition, a paper to
    extend, or a derived Purpose handed off from a previous notebook.
       ↓
  Literature review (literature/)
       ↓
  (Hypothesis generation: declare pathway 1-6 OR ad-hoc-with-provenance)
       ↓
  Hypothesis portfolio (hypotheses.md) — first H per Purpose
       ↓
[Open a notebook for one Purpose]
       ↓
  Set the cycle goal (cycle_purpose_and_goal.md) — name the Consumer,
  the Decision they are blocked on, the Decision rule (YES / NO with
  binding axis / KICK-UP, committed BEFORE the cycle runs), and the
  Knowledge output. The H portfolio below is derived from the
  decision rule.
       ↓
  Create the notebook (purposes/pur_NNN_<purpose-slug>.py) with a
  Purpose header AND the four cycle-goal items
       ↓
  Test H1 (= one or more sub-claims of the decision rule) →
    bug_review (if triggered) → robustness → experiment-review →
    H1 verdict → append one row to results.parquet
       ↓
  Can the consumer apply the decision rule yet? (Primary YES /
    Fallback NO with binding axis / KICK-UP — see hypothesis_cycles.md)
       ↓ no                                   ↓ yes
  Did a derived H emerge that serves         Close the cycle on the
    the SAME Purpose AND a sub-claim of      primary stop that fired.
    the same decision rule?
       ↓ yes              ↓ no (new Purpose)
  Test H2 inside           Close this notebook;
    the same notebook      open pur_<NNN+1>_*.py
       ↓
  Continue until consumer can decide (primary stop), OR the
    emergency stop fires (N=5 advisory / N=8 hard cap — emergency
    stops indicate frame mismatch, force cross-H synthesis)
       ↓
  Purpose-level conclusion = primary-stop outcome + synthesis across
    H1…HN + derived Purposes (= candidates for new notebooks)
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
├── README.md                 # Research goal + sub-claim list (G1.1, G1.2, ...) with status
├── literature/
│   ├── papers.md             # Related papers with one-paragraph summaries
│   └── differentiation.md    # Differentiation matrix vs. prior work
├── hypotheses.md             # H rows with target_sub_claim_id / pathway / Status (planned-runnow / ... / supported / rejected)
├── purposes/                # One file per Purpose (= one research thesis); each H block inside is one experiment
│   ├── INDEX.md              # List of Purpose notebooks with one-line Purpose-level verdicts
│   ├── pur_001_<slug>.py
│   ├── pur_002_<slug>.py
│   └── ...
├── decisions.md              # Per-Purpose entries with design hypothesis (open/close) + sub-claim progress update
├── results/
│   ├── results.parquet       # Aggregated numeric results across all experiments
│   └── figures/              # Figures intended for a report or paper
└── reproducibility/
    ├── env.lock              # Dependency lock file
    ├── data_hashes.txt       # SHA-256 of input data files
    └── seed.txt
```

The four-layer model (Research goal → Design hypothesis → Purpose →
Hypothesis) ties these files together. See
`references/research_goal_layer.md`. Briefly:

| Layer | Lives in | Question it answers |
|---|---|---|
| Research goal | `README.md` (sub-claim list with stable IDs `G1.1`, `G1.2`, …) | What is this project trying to find out? |
| Design hypothesis | `decisions.md` Purpose entries (at-open prediction, at-close verification) | Why this Purpose, in what order, given the research goal? |
| Purpose | Notebook header (Cycle goal 5th item: `target_sub_claim_id`); verdicted at notebook closure | What parent claim does this notebook test (= the research thesis)? |
| Hypothesis | Notebook `## H<id>` blocks; `hypotheses.md` rows with `target_sub_claim_id` | What falsifiable claim does this round test? |

Each derived hypothesis carries an explicit `target_sub_claim_id`
(inherited from parent or overridden with reason in `hypotheses.md`).
This is what prevents derived H's from drifting into "the natural next
test" status without an anchor in the project's research goal — the
failure mode the four-layer model exists to prevent.

## Mandatory order before touching code

### 0. Pre-hypothesis exploration (conditional — only when no candidate phenomenon yet)

See `references/pre_hypothesis_exploration.md`. Run this stage **only**
when the start state is *data without a candidate phenomenon* (new
dataset, new exchange, new asset class, ambient curiosity). Skip when
the researcher arrives with a candidate from prior intuition, a paper
to extend, or a derived Purpose handed off from a previous notebook —
in which case the H's origin is recorded in `decisions.md` and the
researcher proceeds directly to Step 1.

The stage's job is to produce a candidate H1 from data without
contaminating the data that the rest of the lifecycle will use to test
that H1. Four protocol inventions (all mandatory when the stage runs):

- **Exploration set**: a held-out fraction (default 20 %) of the data
  reserved for EDA. Never used in train / val / test of any H produced
  from this stage. Committed to `reproducibility/exploration_set.txt`.
- **Structural-only observations**: EDA records the *existence* of a
  phenomenon, not its *parameter values*. Recording the values turns
  Stage 0 into in-sample fit on the exploration set.
- **EDA → H provenance**: every candidate H cites the EDA observation
  that motivated it. Captured in `eda/findings.md` per phenomenon.
- **Stop rule**: N ≤ 5 candidates, time-boxed; lock H1 when a candidate
  clears Strong/Medium tier in literature differentiation.

An H produced without Stage 0 (or its conditional-skip equivalent) and
without any traceable origin in either an EDA finding or a literature
paper is treated as Stage-0-required — i.e. the researcher loops back
into Stage 0 before Step 1 proceeds.

### 1. Literature review (avoid producing a degraded reimplementation)

See `references/literature_review.md`. Collect 5-10 prior papers and write the
differentiation against them in `literature/differentiation.md`. Skipping this makes the
research likely to reinvent or weaken known results.

### 1.5. Hypothesis generation — declare the pathway

See `references/hypothesis_generation.md`. Every H declares **exactly one
primary pathway** chosen from a taxonomy of six legal generation
pathways, plus an ad-hoc escape hatch that pays a higher
differentiation hurdle. The pathway determines which provenance files
the H must point to and what differentiation tier is forecasted.

Pathways:

1. **Data-driven** — EDA finding from Stage 0 (provenance:
   `eda/findings.md` Phenomenon entry).
2. **Literature-extension** — re-test a paper's claim in a new
   universe / period / frequency / asset class (provenance: paper +
   section/page + differentiation matrix row).
3. **Literature-refutation** — test a paper's claim under stricter,
   adversarial conditions argued *a priori* to be where it fails
   (provenance: paper + a-priori argument).
4. **Failure-derived** — H_n's named failure axis → H_{n+1} that
   targets that one axis (provenance: parent H row + failure-mode
   analysis entry in `decisions.md`). Routing of H_{n+1} (same
   notebook vs. new) is owned by `hypothesis_cycles.md`; this pathway
   owns *content*.
5. **Cross-asset / cross-regime extension** — known phenomenon in
   market A → test in market B or regime R (provenance: source-market
   evidence + transfer-mechanism argument).
6. **Mechanism-driven** — causal mechanism (economic /
   microstructural / behavioural) implies an observable, H tests the
   observable (provenance: mechanism description, *not* retrofit to
   data).

An H with no declared pathway and no documented ad-hoc origin defaults
to Stage 0. An ad-hoc H (legal escape hatch) is allowed when origin is
documented in `decisions.md`, the differentiation matrix is filled,
and the H clears at least Medium tier in differentiation.

The pathway taxonomy makes generation provenance explicit *before*
Step 2 (research design) tries to formalize the H. Without it, content
is filled silently from the researcher's background and the protocol's
review layers cannot tell where the H came from.

### 2. Write the research design first in Markdown — including cycle goal and figure plan

See `references/research_design.md` and `references/cycle_purpose_and_goal.md`.
At the top of each notebook, write:

- **Purpose** — the parent claim the notebook tests, written as a
  declarative falsifiable statement (= the research thesis). The
  notebook's closure verdict will be on this exact statement. Avoid
  "Does X work on Y?" question form — that hides the parent claim
  inside an interrogative; the form makes Purpose-level verdict
  ambiguous
- **Cycle goal — five items, see `cycle_purpose_and_goal.md`** (mandatory,
  pre-implementation):
  - **Consumer** — concretely named (next derived Purpose, production
    strategy build, paper section, portfolio-sizing decision). "The
    research community", "future researchers", "myself someday" are not
    consumers; if the only consumer is that vague, return to Stage 0.
    "My own next Purpose, named as <slug>" is a legal escape hatch when
    the next Purpose is *nameable in one phrase*.
  - **Decision the consumer is blocked on** — the yes/no/pivot the
    consumer cannot make without this cycle's output, in one sentence.
  - **Decision rule** — the predicate the consumer applies to the
    knowledge output to land their decision. Three branches required:
    YES (numeric / structural threshold for going forward), NO (numeric
    / structural threshold for not going forward, with the binding axis
    that would justify it), KICK-UP (structural condition indicating the
    cycle's frame is the wrong layer). Committed *before* the cycle
    runs; without pre-commitment the rule becomes post-hoc
    rationalization.
  - **Knowledge output** — the artifact (per-H rows in results.parquet
    + Purpose-level synthesis paragraph + headline figure) onto which
    the decision rule is applied.
  - **Target sub-claim id** — the project README's research-goal
    sub-claim ID(s) this Purpose is expected to advance. Primary: 1
    sub-claim; secondary: 0-2. The link from this notebook to the
    project's running question. See `references/research_goal_layer.md`
    for the four-layer model (Research goal / Design hypothesis /
    Purpose / Hypothesis) — without `target_sub_claim_id`, the
    Purpose's relationship to the project's research goal is implicit
    and the next Purpose's selection becomes invisible.
- **First Hypothesis (H1)** — a specific falsifiable comparison statement
  serving the Purpose, with numeric acceptance / rejection thresholds.
  H1 is *derived from* the decision rule above: it tests one or more
  conjuncts of the YES / NO / KICK-UP branches. An H without a
  sub-claim mapping is not in the portfolio under this frame.
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
acceptance / rejection thresholds, **sub-claim mapping** to the decision
rule, **per-H headline figure plan**, and per-H result row. The
sub-claim mapping is enforced at carry-forward time by
`hypothesis_cycles.md` routing rule sub-step 1.5 (= conjunct
contribution gate): a derived H that closes only conjuncts the parent H
already landed is rejected at routing as redundant, even when Pathway
provenance is otherwise legitimate.

The cycle-goal items, the figure plan, and the reader takeaway are
required pre-implementation items. The cycle-goal items in particular
are what the H portfolio is *derived from* — without them, H's are
improvised per Purpose and downstream judgment becomes inconsistent.
"I'll figure out the figure when I have the data" / "I'll know the
consumer's decision when I see H1's result" are the failure modes this
step is built to prevent.

See `references/cycle_purpose_and_goal.md` for the derivation of why
the cycle goal exists and how to fill the five items, and
`references/research_goal_layer.md` for the four-layer model that the
5th item (`target_sub_claim_id`) ties the notebook into, and
`references/notebook_narrative.md` for the full communication-artifact
spec. Read all three before writing H1's first code cell.

#### 2.5. Data availability gate (verified before instantiating the cycle)

If the real data required to apply the Decision rule is **unavailable**
in the execution environment AND the cycle's research subject is
real-world behavior (markets, instruments, regimes, mechanisms), the
cycle is **BLOCKED**. Synthetic substitution within an instantiated
cycle is forbidden; synthetic-data scaffolding outside the protocol
(no Cycle goal, no verdict cell, no `results.parquet` row) is
engineering work, tracked separately. Synthetic data IS the research
subject only when the Decision rule is about an estimator / algorithm /
mathematical property whose ground truth lives in the DGP itself
(parameter recovery, convergence rate, estimator bias on a known DGP).

A BLOCKED cycle is itself a research output — it surfaces a
data-acquisition dependency the project must address before the
cycle's sub-claim can be attacked. File the unavailability in
`decisions.md` as a structural finding, mark the cycle suspended, and
pivot to a data-available cycle (or return to project portfolio
re-prioritization). See `references/experiment_protocol.md`
"Data availability gate" for the full rule, the diagnostic test
distinguishing real-world subjects from estimator-recovery subjects,
the forward path when BLOCKED, and the anti-rationalization table.

### 3. One Purpose = one notebook

See `references/experiment_protocol.md`. The unit of one notebook is one
**Purpose** (= one research thesis = one parent claim about the world),
not one Hypothesis. Multiple admissible hypotheses serving the same
Purpose are tested as successive rounds inside the same notebook; each
H block is one experiment that tests the parent thesis on a particular
falsifiable axis. The notebook closes with a Purpose-level verdict on
the parent thesis (in addition to the per-H verdicts).

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

#### 11b. Post-review reconciliation pass (mandatory before step 12)

After the inline review summary, before re-running the robustness battery, run the
reconciliation pass — see `references/post_review_reconciliation.md`. The reconciliation
pass enforces three things:

1. **A 4-pattern placement decision per finding** — every reflected change is one of
   P1 (in-place rewrite), P2 (same-section re-compute / sanity cell at the end of the
   existing `§N`), P3 (a single `## Post-review addenda` block placed immediately before
   the verdict cell), or P4 (a new `## H<id>` block). New chapters with lowercase /
   decimal suffixes (`§6a`, `§7b`) and figures that violate the up-front figure plan
   (`Fig 2b`) are forbidden.
2. **Definition of Done** — re-execute every dependent cell, align all abstract /
   per-H abstract / interpretation numbers with the post-fix pipeline output,
   regenerate every figure, rewrite every observation cell to describe the regenerated
   figure, and check that *past-round* findings are still reflected in the new numbers.
3. **A final verification pass** — read the notebook from top to bottom once and
   confirm that no reviewer vocabulary (`leakage-reviewer`, `claim-reviewer`,
   `(literature dimension)`), edit-history language ("after bug_review fix",
   "~~2.4~~ → 0.93"), or planning notes (`parked`, `follow-up`, `next-session`) has
   leaked into the notebook body. The notebook body is the **research artifact**;
   the inline review summary (chat transcript) is the **audit trail**;
   `decisions.md` / `hypotheses.md` is the **planning state**. The three are kept
   separate.

Without the reconciliation pass, "fixed" in the inline summary is premature — the
finding is at most "addressed in code." Step 12 (robustness battery) does not start
until reconciliation is complete.

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

1. Step 11 (`bug_review`) clean — every `high` and `medium` resolved **and step 11b
   reconciliation pass complete**
2. Step 12 (robustness battery) green
3. **Invoke `experiment-review` skill via the Skill tool** ← this step
4. Address every `high` and `medium` finding from `experiment-review`
5. **Step 13b reconciliation pass** — re-run `references/post_review_reconciliation.md`
   on the changes from step 4. `experiment-review` findings frequently touch the
   abstract, per-H abstract, claim wording, and the literature section, so the
   verification pass is what keeps reviewer dimension names (`validation-sufficiency`,
   `literature`, `claim`, `narrative`) and edit history out of the notebook body
6. Step 14 (result aggregation), then completion gate

Do NOT proceed to step 14 (result aggregation) until both `bug_review` and
`experiment-review` findings are addressed **and both reconciliation passes are
complete**. Setting `verdict = "supported"` before both layers pass is a protocol
violation that downgrades the result to *preliminary screening*. Skipping
reconciliation is the same violation in a quieter form: the inline summary will
read "fixed" while the notebook body still carries pre-fix figures, edit history,
and reviewer vocabulary.

Common rationalization to resist: "`bug_review` already ran, that is the review layer."
Different question (correctness vs. claim-warrant); both required.

### 14. Result aggregation (per Hypothesis) and Purpose-level synthesis

See `references/results_db_schema.md`. **Each Hypothesis in the notebook produces
its own row** in `results/results.parquet`. The schema carries `purpose_id`
(= the notebook = the Purpose; the prior name `experiment_id` was a vocabulary
inversion that conflated the notebook with an experiment, retired here),
`hypothesis_id` (= the individual H within the Purpose; each H block is itself
**one experiment**, the apparatus that tests that H), the H's `pathway`
declaration (from Step 1.5), `forecasted_tier`, and — filled post-review —
`verdict`, `failure_mode` (controlled vocabulary when verdict=rejected),
`parent_hypothesis_id` (when pathway=4), and `achieved_tier` (from the
experiment-review literature dimension's novelty check). A notebook with three
H's emits three rows, all sharing the same `purpose_id`. The append happens at
the end of each H's round inside the notebook; `verdict` and `achieved_tier`
are *updated* after Steps 11 and 13 finalize them.

When the Purpose closes (or when N ≥ 3 H have been tested under it), the
notebook also writes a **Purpose-level conclusion** following
`references/cross_h_synthesis.md`. The conclusion reads H1…HN's rows together
and extracts the *meta-finding* — what the cluster says about the world that
no single H said (e.g. Pattern A: "all H's failed on the same `fee_model`
axis → fees are the binding constraint here"). Without this synthesis,
`results.parquet` accumulates per-H rows but the project carries no durable
cross-H knowledge forward to derived Purposes. The synthesis itself is prose
in the notebook plus an entry in `decisions.md`; the cross-H query surface
the synthesis runs on is provided by the schema's pathway / verdict /
failure_mode / tier fields.

At Purpose closure, `decisions.md`'s Purpose entry also carries the
**research-goal layer's bookkeeping** (see `references/research_goal_layer.md`):

- **Research-goal sub-claim progress update** — for each sub-claim this
  Purpose touched, the transition (e.g., G1.1: in progress → confirmed).
  Sub-claims not touched are listed unchanged so the project's running
  state is fully visible at every cycle.
- **Design hypothesis at close** — verification of the prediction
  recorded at Purpose open (CONFIRMED / FALSIFIED / PARTIAL with a
  one-phrase reason). Falsified is a legitimate research output, not a
  process failure.

These two items are what the next Purpose's selection reads. Without
them, the next Purpose is chosen from per-H numeric observations alone
and the project's relationship to its research goal collapses into
implicit reasoning. Per-H planning state (run-now / next-session / drop)
lives in `hypotheses.md`'s `Status` column (`planned-runnow` /
`planned-nextsession` / `planned-drop`), single source of truth.

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

**Per-H abstract leads with the falsifiable claim's answer** in the H's own terms
(mechanism / market / regime / instrument). Implementation, library, and numerical
correctness statements (computation reconciliation, leak-check residuals, library
version match) belong in a clearly-bounded *Reproducibility note* at the end of the
abstract — never as the lead. The first sentence is the answer to the world the H
asked about; if that sentence is "the implementation is correct" or "the decomposition
matches sklearn", the cycle's de facto deliverable has inverted from research to
engineering. See `references/notebook_narrative.md` 1b "Format rule — first sentence
is the market claim, not the implementation".

### 17. Iterate hypothesis cycles — and stop on the synthesis trigger

See `references/hypothesis_cycles.md`. Do not stop after one cycle. After each H
inside the notebook, classify derived hypotheses as "run now / next session / drop"
and log them in `hypotheses.md` and `decisions.md`.

- A run-now derived H **serving the same Purpose** is the next round inside the
  same notebook (a new `## H<id>` block, not a new file).
- A run-now derived H whose investigation reflects a **new Purpose** opens the
  next notebook (`pur_<NNN+1>_*.py`).
- "Run-now derived hypothesis = next notebook" is the **old** rule and has been
  discarded. The new rule routes by Purpose continuity, not by run-readiness.

But cycles are not unbounded. The exhaustion-trigger rule (in
`hypothesis_cycles.md`) fires **before any H6 can be appended** when a Purpose
has 5 H tested without a four-gate-clean `verdict='supported'`. At the trigger,
cross-H synthesis (per `references/cross_h_synthesis.md`) is mandatory — its
Pattern match (A-E) determines whether the next move is close, derive, split,
or narrow. The hard cap at N=8 closes the Purpose mechanically; further work
opens a new Purpose with the previous Purpose's synthesis as documented prior.
Without the trigger, sunk-cost continuation is the modal failure of long
Purposes.

## Completion gate (per Hypothesis)

Before declaring `verdict = "supported"` on **any individual hypothesis**, all
**four** gates must pass for that H — *in this order*:

1. **Step 11 — `bug_review` (in this skill)**: 5 specialist reviewers + 1 adversarial
   cold-eye reviewer, no unresolved `high` or `medium` findings for this H.
2. **Step 13 — `experiment-review` (separate skill, invoke via Skill tool)**: 7
   specialist reviewers + 1 adversarial cold-eye reviewer, no unresolved `high` or
   `medium` findings for this H.
3. **`references/research_quality_checklist.md`**: passes as final self-check for
   the H (and at project level, the Purpose-level synthesis the notebook produces
   from the H's it contains).
4. **Achieved differentiation tier ≥ Medium, matching or exceeding the H's
   pathway-forecasted tier (declared in Step 1.5 via
   `references/hypothesis_generation.md`)**. A Weak-tier achievement is a
   degraded reimplementation, not a research advance, regardless of how clean
   the bug_review and experiment-review passes look. A tier downgrade (e.g.
   Pathway 6 forecasted Strong but the differentiation matrix shows Medium) is
   not a moral failure — the right next move is usually to narrow the abstract
   to match the achieved tier and re-run the relevant gates, not to relitigate
   the pathway choice. This gate is mechanically subsumed by gate 2 (the
   `literature` dimension's novelty check fires `high` on a sub-Medium tier),
   but is listed explicitly here so the load-bearing rule is visible to the
   researcher *before* the review fires.

Setting `verdict = "supported"` on any H without all four is a protocol violation
that downgrades that H's result to *preliminary screening*. Each gate's pass/fail
must be visible in the assistant's reply (trigger, reviewer roster, findings,
resolution) — the skills do not write to `decisions.md`. If the user wants a
durable record they can copy the inline summaries themselves.

Different H's inside the same notebook can land at different per-H verdicts
(e.g. H1 = supported, H2 = rejected, H3 = parked). The notebook **also**
carries a Purpose-level verdict on the parent thesis (see
"Purpose-level closure gate" below); this is in addition to, not in place
of, the per-H verdicts.

The two review gates intentionally remain *separate skills* and are *not* merged: they
answer different questions (correctness vs. claim-warrant) and their adversarial
reviewers receive different minimum bundles tuned to different failure modes
(`bug_review` adversary sees code + numbers; `experiment-review` adversary sees the
`.py` file alone). Merging them would dilute both.

## Purpose-level closure gate (per Notebook)

Before declaring the notebook closed and opening a derived Purpose (or
declaring the project Purpose-level finding), the **parent thesis** stated
in the Purpose header must itself receive a verdict. Per-H verdicts are
sub-claims; the parent thesis is its own falsifiable claim and must close.

The gate fires when **any** of the following becomes true for the notebook:

- All planned H's have reached per-H verdicts (supported / rejected /
  parked) AND the cycle goal's Decision rule (YES / NO / KICK-UP) is
  applicable
- The exhaustion-trigger rule has fired (N=5 advisory) and the cross-H
  synthesis has matched a Pattern (A-E) in `cross_h_synthesis.md`
- The hard cap (N=8) has fired

When fired, the notebook records a **Purpose-level verdict** with one of
the following values:

- **supported**: the parent thesis is supported by the cluster of H
  results, with the qualifying conditions named explicitly
- **refuted**: the parent thesis is rejected by the cluster of H
  results; the binding axis is named explicitly
- **partial**: the parent thesis is supported on a named subset of
  conditions and refuted on another named subset; the partition is made
  explicit (regime / instrument / horizon / cost regime / etc.)

A `partial` verdict is a legitimate research output, *not* a placeholder
for "I'll figure it out later". A notebook that closes with a
Purpose-level verdict naming an unresolved direction is closed as
`partial` with that direction as a derived-Purpose candidate; this is
distinct from leaving the parent thesis unverdicted.

Carrying the parent thesis forward into a derived Purpose (per
`cross_h_synthesis.md` Pattern A / B) requires the parent thesis to be
*verdicted* first. The derived Purpose tests a *different* parent thesis
(typically a refinement, restriction, or alternative scope of the
original), not the same parent thesis under a slightly modified label.
Rephrasing "Mean-reversion works on EUR/USD intraday" as "Mean-reversion
works on EUR/USD at lower frequencies" without first verdicting the
former as `refuted` (binding axis: H1 frequency does not survive cost)
is the explicit anti-pattern this gate exists to prevent.

## Bundled helper scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_purpose.py` | Generate a numbered Purpose notebook (one parent thesis per file) from the template |
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
| `purpose.py.template` | marimo notebook template for one Purpose (one parent thesis, multiple H experiments inside) |
| `INDEX.md.template` | Index of Purpose notebooks |
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
