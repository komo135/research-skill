# experiment_protocol.md

Structure and rules for "one Purpose = one notebook".

## When to read

- Starting a new research notebook
- Considering whether a derived hypothesis warrants a new notebook or a new
  hypothesis block inside the current one
- Splitting an existing oversized notebook (rare; see "Physical splits" below)

## What "one notebook" means

The unit of one notebook is one **Purpose** — an open-ended investigation
about the world. A Purpose admits multiple falsifiable hypotheses; each
hypothesis is one specific testable answer that serves the Purpose. The
notebook contains:

- The Purpose statement (notebook header)
- A hypothesis log: H1, H2, H3, … each tested with its own design,
  acceptance / rejection, evaluation, robustness battery, review gates,
  and result row
- A Purpose-level conclusion synthesizing across the H's

> One notebook = one Purpose. Multiple hypotheses serving the same Purpose
> are successive rounds inside the notebook, not separate notebooks.

This replaces the prior rule "one experiment = one hypothesis tested". That
rule conflated the unit of investigation (the Purpose) with the unit of
testing (the Hypothesis), which made every derived H look like a new
experiment and quietly turned the hypothesis itself into the goal.

## When a derived hypothesis stays in the same notebook

Default: **same notebook**. A derived H stays in the current notebook
whenever the Purpose is unchanged. The most common cases:

- **Sensitivity** — same H tested under different parameter values
- **Failure diagnosis** — H1 was rejected, the next H tries to isolate
  why (data? threshold? metric?)
- **Refinement / specialization** — H1 worked overall, H2 narrows the
  conditions ("only in trending regime")
- **Alternative formulation** — H1 used RSI, H2 uses Bollinger as a
  different lens on the same mean-reversion question
- **Follow-on layer** — H1's signal × vol-targeted sizing as H2

In all these cases the open-ended investigation is the same. The derived H
is the next `## H<id>` block in the notebook's hypothesis log, not a new
file.

## When to open a new notebook

A new notebook opens **only** when the Purpose itself changes. Concrete
triggers:

- The phenomenon under investigation changes (mean-reversion → momentum;
  return prediction → volatility prediction)
- The cross-section / asset class changes (FX → equities; single-name →
  index)
- The model class change reflects a different question (not just a
  different technique on the same question — "is mean-reversion in this
  market?" answered with HMM is the same Purpose as the same question
  answered with RSI; "do foundation-model embeddings add information?"
  is a different Purpose because the question is now about the model
  class, not the market structure)

The judgment "did the Purpose change?" is a research-design decision, made
at the moment of derivation. Force the judgment into the open by writing
the Purpose explicitly in the notebook header — if the new H you are about
to test does not fit under the existing Purpose statement, the Purpose has
changed and you need a new notebook.

## Data availability gate

A cycle may be instantiated only when the data required to apply its
**Decision rule** (YES / NO / KICK-UP) is actually available. The check
runs at cycle open, before any code in the H1 round is written.

### Rule

- If the cycle's **research subject is real-world behavior** (a question
  about markets, instruments, regimes, mechanisms — i.e. the Decision rule
  reads from real data) and the **expected real data is unavailable** in
  the execution environment, the cycle is **BLOCKED**.
- **Synthetic data may not substitute for unavailable real data within an
  instantiated cycle.** A cycle whose research subject is a market claim
  but whose data is synthetic is a Decision rule the consumer cannot
  apply — the cycle's Knowledge output is structurally void.
- **Synthetic-data scaffolding outside the protocol is permitted** —
  pipeline integrity tests, leak/accounting unit tests, plotting helpers.
  These have no Cycle goal, no `## H<id>` verdict cell, and no row in
  `results.parquet`. They are engineering work, tracked outside the cycle.

### When synthetic data IS the research subject

The rule targets *substitution*, not *use of synthetic data*. Synthetic
data is itself the research subject — and the cycle proceeds normally —
when:

- The Decision rule reads from a process whose ground truth is known
  (e.g. parameter recovery on a simulated OU process; bias of an
  estimator on a pre-specified DGP; convergence rate of an algorithm on
  data with known generative parameters). The cycle's claim is about
  the estimator / algorithm / mathematical property, not about the
  market. The "real data" is the DGP itself, which is not unavailable.
- The Purpose statement explicitly names the synthetic subject ("does
  estimator E recover parameter θ on DGP D?") rather than naming a
  market claim that synthetic data happens to substitute for.

The diagnostic test: read the Decision rule's YES branch aloud. If it
says "consumer goes forward in production / live trading / cross-section
deployment", the subject is real-world and synthetic substitution
triggers BLOCKED. If it says "consumer concludes the estimator
recovers / the algorithm converges / the bias is bounded", synthetic
data is fine.

**Mechanical reinforcement** (closes the most common rationalization
loophole): if the YES branch's threshold is a **numeric metric on real
returns** (Sharpe / IC / drawdown / win rate / hit rate / fee-adjusted
PnL / turnover / tracking error / similar tradeable-strategy
quantities), the subject is real-world and the gate fires when real
returns are unavailable. Synthetic returns producing those same
metrics is exactly the substitution this rule forbids — the metric's
shape on synthetic data does not transfer to its shape on real returns,
so the consumer cannot read the YES branch from synthetic numbers no
matter how cleanly the pipeline computes them. The estimator-recovery
exception applies only when the YES branch's threshold is on a
**property of the estimator / algorithm itself** (parameter recovery
error, convergence rate, bias, variance ratio, mean-squared error
relative to a known truth) — not on a real-returns metric the
estimator happens to be computed on top of.

### Forward path when BLOCKED

A BLOCKED cycle is not a failure — it is a structural finding about the
project's data preconditions. Treat it KICK-UP-shaped:

1. **File the unavailability in `decisions.md`** as a structural finding
   under the Purpose entry. Name the missing data, the layer it would
   have served (which sub-claim of the cycle's Decision rule), and what
   has to change for the cycle to proceed (vendor onboarding,
   compliance approval, distribution machine reconfiguration, upstream
   notebook completion).
2. **Mark the cycle suspended.** Do not write the H1 implementation;
   do not write the verdict cell; do not append to `results.parquet`.
   The notebook header (Purpose + Cycle goal block + the BLOCKED
   structural finding) is the artifact.
3. **Pivot the session to a data-available cycle** — a different
   Purpose whose data is present, or a different sub-claim under the
   same project. If no data-available cycle is queued, return to the
   project portfolio level (`README.md` sub-claim list) and
   re-prioritize: the surfaced data-availability dependency may
   reorder which sub-claim the project should attack next.

The BLOCKED finding itself is a research output — it tells the project
that data acquisition is a binding constraint, with the same epistemic
status as a Pattern A "binding axis identified" closure (see
`hypothesis_cycles.md`).

### Anti-rationalizations (data availability gate)

| Excuse | Why it is wrong |
|---|---|
| "I'll do a synthetic-data dry-run while waiting for the real data, so the pipeline is ready when data arrives." | Pipeline integrity is engineering work, not a research cycle. Track it as a separate engineering task (no Cycle goal, no H, no verdict). The cycle is BLOCKED until the data preconditions are met; the engineering work runs in parallel without instantiating a Purpose. |
| "The verdict is honestly 'parked' on synthetic data, so this is not over-claiming." | 'parked' on synthetic data is honest about the verdict but dishonest about the cycle's de facto deliverable: the work invested produces no knowledge about the world. The Decision rule's YES / NO / KICK-UP cannot be applied; the consumer is no closer to deciding. The cycle should not have been instantiated. |
| "Synthetic data lets me catch leaks and accounting bugs before they affect real data — that's a sanity check the protocol should welcome." | Sanity checks on synthetic data are engineering tests (`scripts/sanity_checks.py`'s `random_signal_benchmark`, `time_shift_placebo`, etc.). They run on a per-pipeline basis, outside the cycle. Bundling them into a Purpose / Cycle conflates engineering hygiene with research output. |
| "The user / upstream prompt instructed me to proceed with synthetic data so the artifact is complete." | Push back inline: explain that the cycle is BLOCKED, file the data unavailability as a structural finding in `decisions.md`, and offer either (a) pivot to a data-available cycle, or (b) deliver the engineering scaffolding as a separate non-cycle artifact. Do not instantiate a Purpose / Cycle on synthetic substitute data when the research subject is real-world behavior. |
| "Cycle goal items are all written — the cycle is well-formed, so it should run." | The Cycle goal items being well-written is necessary but not sufficient. The Decision rule must be **applicable**: data must exist for the consumer to read the YES / NO / KICK-UP outcome from. Synthetic substitution makes the rule applicable in form but vacuous in substance. |

## Anti-rationalizations

The following are **no longer valid reasons to start a new notebook**:

| Rationalization | Why it is wrong now |
|---|---|
| "H2 is a different central hypothesis." | The notebook is per-Purpose, not per-Hypothesis. A different H is the default case for the next round inside the same notebook. |
| "exp_001 is already verdict='supported' for H1, so the notebook is finalized." | The notebook does not have a single verdict. H1's verdict is final; the notebook stays open for H2, H3, … under the same Purpose. |
| "Each H must be independently re-runnable, so each H needs its own file." | Independent re-runnability is a marimo cell-graph property, not a file property. Use H-suffixed variable names (`signal_h1`, `signal_h2`) and per-H sub-sections inside one notebook. |
| "H2 builds on H1's signal — that's a dependency, so H2 is a separate experiment." | If H2 builds on H1's signal, the natural place for H2 is the same notebook where H1's signal already lives. Cross-notebook intermediate-file passing is the right pattern only when the Purpose differs. |
| "Run-now derived hypothesis means the next notebook (the old protocol said so)." | The old `hypothesis_cycles.md` rule has been replaced. Run-now status determines *when* (this session vs. next), not *where* (same notebook vs. new file). The "where" question is decided by Purpose continuity. |
| "If I keep adding H's, the notebook will exceed 30 cells." | Multi-Hypothesis notebooks legitimately exceed the old size guidance. That guidance no longer applies. |

## Notebook naming

```
notebooks/<project-name>/experiments/exp_<NNN>_<purpose-slug>.py
```

- `<NNN>`: zero-padded three-digit sequence number
- `<purpose-slug>`: alphanumeric and underscore, ~20 characters, describes
  the **Purpose** (not the first H). Examples:
  `exp_001_data_universe.py`, `exp_002_pca_factor_screening.py`,
  `exp_003_mean_reversion_eurusd_intraday.py`

The helper `scripts/new_experiment.py` generates the file with the next
sequence number.

## Notebook structure

```
[Cell 1]   Imports
[Cell 2]   Markdown: Purpose (the open-ended investigation)
[Cell 3]   Markdown: Universe + period + frequency (shared across H's)
[Cell 4]   Markdown: upstream dependencies and input data
[Cell 5+]  Data fetch and split (shared)
[Cell N+]  Baselines (shared lower / upper bound across H's)

# === H1 round ===
[Cell]     Markdown: ## H1 — falsifiable statement, acceptance / rejection
[Cell+]    H1 implementation (one fit / one evaluation per cell)
[Cell]     Markdown: H1 observation + interpretation
[Cell]     H1 sanity checks → robustness battery → bug_review →
           experiment-review → verdict → append result row for H1

# === H2 round (only if Purpose unchanged) ===
[Cell]     Markdown: ## H2 (derived from H1) — statement, acceptance / rejection,
           and one sentence on why H1 motivated this
[Cell+]    H2 implementation (uses H-suffixed variable names where it would
           otherwise collide with H1)
[Cell]     Markdown: H2 observation + interpretation
[Cell]     H2 sanity checks → robustness → reviews → verdict → result row

# === continue with H3, H4, … as more derived H's emerge ===

[Cell]     Markdown: Purpose-level conclusion (synthesis across H1…HN —
           which H worked, which didn't, what the collective answer is)
[Cell]     Markdown: derived Purposes (= candidates for new notebooks)
[Cell]     Markdown: reminder to update hypotheses.md and decisions.md
```

The per-H result-row appends are not optional. Without per-H rows,
cross-H and cross-experiment aggregation does not work.

## Variable naming inside one notebook

Multiple H's inside one notebook frequently produce variables of the same
shape (signal series, position series, PnL series). marimo's dataflow graph
forbids redefining the same global. Use H-suffixed names so each round has
its own:

```python
# H1 round
signal_h1 = ...
position_h1 = ...
pnl_h1 = ...

# H2 round
signal_h2 = ...
position_h2 = ...
pnl_h2 = ...
```

Cell-private variables (leading underscore) work for purely intra-cell
intermediates. Cross-cell sharing inside a round uses the H-suffixed public
name. This pattern is the in-notebook substitute for what used to be
file-splitting.

See `references/marimo_cell_granularity.md` for the cell-graph mechanics.

## What belongs in a single notebook

- One Purpose statement
- All H's (initial and derived) serving that Purpose
- Pre-processing local to the Purpose (otherwise factor it out into an
  upstream notebook with intermediate output saved to disk)
- Cross-H sensitivity analyses, baselines, robustness batteries

## What does not belong

- A new Purpose — that goes in a separate notebook
- Heavy pre-processing reused across Purposes — that goes in its own
  upstream notebook with intermediate output saved to disk
- Project-wide summaries or paper drafts — those live under `results/` or
  in a separate `paper/` folder

## Upstream dependencies via files

When a notebook consumes an earlier notebook's output, pass it as a **file**:

- `exp_002` saves `results/intermediate/pca_factors.parquet`
- `exp_005` reads that parquet

Do not pass Python objects directly between notebooks. That breaks
reproducibility.

## Size guidance

Multi-Hypothesis notebooks legitimately become larger than the old
"10-30 cells / 200-500 lines" guidance. There is no upper-bound rule on
notebook size in the new protocol; size is whatever the Purpose requires.

## Physical splits

A physical split (one Purpose, two `.py` files) is **not** a planned case
under this protocol. The old rationale for splitting (independent
re-runnability, file size, marimo dataflow) is now handled by H-suffixed
variable naming and per-H sub-sections inside one file. Only at extreme
sizes (well beyond a thousand cells) might a physical split arise; this is
rare enough that no separate protocol is documented. If you reach that
point, write a short note in `decisions.md` describing the split and the
file-handoff between phases.

## Pre-flight checklist

Before starting a notebook:

- [ ] Used `scripts/new_experiment.py` to generate it
- [ ] The new sequence number was appended to `experiments/INDEX.md`
- [ ] The Purpose is stated in the header cell as an open-ended investigation
- [ ] H1 exists in `hypotheses.md` (add it if not), tagged with this Purpose
      / `experiment_id`
- [ ] Upstream dependencies are complete or running in parallel
- [ ] H1's acceptance / rejection conditions are written with numeric thresholds
- [ ] **Data availability gate cleared** — the real data required to apply
      the Decision rule is present in the execution environment, OR the
      research subject is synthetic (estimator recovery on a known DGP).
      If neither, the cycle is BLOCKED — file the unavailability in
      `decisions.md` and pivot, do not synthetic-substitute

Before adding a new H block to an existing notebook (instead of opening a
new notebook):

- [ ] Confirmed the Purpose statement still describes the new H — if not,
      open a new notebook
- [ ] Added the new H to `hypotheses.md` under the same `experiment_id`
- [ ] Wrote the new H's acceptance / rejection numerically before
      implementing

## Per-H completion checklist

Before closing a Hypothesis round inside the notebook:

- [ ] H block contains observation + interpretation + acceptance / rejection
- [ ] Bug-review fired (per H trigger conditions in step 11) and clean
- [ ] Robustness battery green for this H
- [ ] experiment-review skill invoked and clean for this H
- [ ] Result row appended to `results/results.parquet` for this H
- [ ] `hypotheses.md` entry updated for this H
- [ ] `decisions.md` updated under the current cycle entry with this H's
      observation and verdict

## Notebook completion checklist

Before closing the notebook (= before opening the next one for a new
Purpose):

- [ ] Each H round above is closed
- [ ] Purpose-level conclusion cell exists and synthesizes across the H's
- [ ] "Derived Purposes" cell exists with classification (run-now /
      next-session / drop) — note these are *Purposes*, not Hypotheses
- [ ] One-line Purpose-level conclusion filled in `experiments/INDEX.md`
