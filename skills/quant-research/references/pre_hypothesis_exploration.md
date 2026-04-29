# pre_hypothesis_exploration.md

Stage-0 protocol for the **data-without-phenomenon** start state. Run
when a researcher has data and a topic interest but no candidate
phenomenon to test yet. The stage's job is to produce a protocol-eligible
H1 candidate without contaminating the data that the rest of the
lifecycle will use to test it.

## When to read

- Starting a new project with **data but no candidate phenomenon yet**.
  Examples: new dataset, new exchange, new asset class, ambient
  curiosity ("there must be something in funding rates").
- Returning to an old dataset with no inherited Purpose.
- Conditional skip: if you arrive with a candidate phenomenon already
  in mind (from prior intuition, a paper you want to extend, or a
  derived Purpose handed off from a previous notebook), skip Stage 0
  and go directly to the literature review (`literature_review.md`).
  Document the source of the candidate in `decisions.md` so the
  provenance is recorded — an H with no traceable origin is a
  Stage-0-required H regardless of how confident the researcher feels.

## Goal

Take a researcher from "I have data and a topic interest" to "I have at
least one candidate H1, written falsifiably, with a documented origin
in either an EDA observation or prior work, and with no in-sample
selection bias from EDA on the testing data."

The non-goal: the comprehensive characterization of the dataset. EDA in
the sense of "look at everything" is unbounded and not a research
output. Stage 0 ends when a candidate H1 is locked, not when the
dataset is fully understood.

## The four protocol inventions

These are what make Stage 0 a protocol step, not a generic EDA pass.
Skipping any of them silently invalidates the rest of the research
lifecycle for the H's produced from this stage.

### 1. Exploration set (mandatory)

Reserve a fraction of the data for EDA. This fraction is **never** used
in train / val / test of any H produced by this Stage 0. It is the
data the researcher is "allowed to spend" on looking around.

Default sizing:

| Data shape | Exploration set | Rationale |
|---|---|---|
| Single long time series (BTC tick, FX 1-min) | First 20 % chronologically | Newest data is most valuable for test; oldest is least costly to spend |
| Cross-sectional panel (US equities, multi-name FX) | A held-out 20 % of names, full period | Preserves time structure for the train / val / test split that follows |
| Cross-sectional × time | 20 % of names × full period, OR full names × oldest 20 % of period | Researcher chooses; document the choice in the Stage-0 notebook header |
| Event-driven (earnings, FOMC) | First 20 % of events chronologically | Same logic as the time-series case |

Commit the exploration set definition (date range, instrument list, or
both) to `reproducibility/exploration_set.txt` and reference its hash
from the project's `INDEX.md`. Once committed, never touch it from any
H's training, validation, or test loops.

If the dataset is too small for 20 % to be meaningful (e.g. 50 monthly
observations), Stage 0 is not the right approach for this project —
move to a literature-driven start (Step 1) and accept the constraint
that the H must come from a paper or strong prior.

### 2. Structural-only observations (mandatory)

EDA records the *existence* of a phenomenon, not its *parameter
values*. Recording the values turns Stage 0 into in-sample fit on the
exploration set, and the H's parameters then carry that fit into the
test set without any guard catching it.

| Allowed (structural) | Disallowed (parametric) |
|---|---|
| "Funding rate has a heavy left tail" | "Funding rate's 5th percentile is -0.014" |
| "Returns show vol clustering at intraday horizons" | "Vol-clustering half-life is 12 minutes" |
| "Cross-sectional correlation drops in March 2020" | "Mean correlation falls from 0.6 to 0.2 around 2020-03-15" |
| "Funding-rate extremes precede price reversals" | "Z-score > 2 funding events have 53 % next-day reversal hit-rate" |
| "Some lag k between feature and target shows non-zero IC" | "IC at lag 3 is 0.04, at lag 5 is 0.06" |

The right column is the answer the H is supposed to test. Recording it
in Stage 0 means H1's acceptance threshold (or its parameter setting)
is selected with knowledge of what value will pass on the rest of the
data — the textbook in-sample selection bias.

The check: if the Stage-0 findings file were destroyed and the
researcher had only the candidate-phenomenon list (without the
parameter values), could they recover the H1 they would actually run?
If yes, Stage 0 was structural-only. If no, parameter values leaked
and the H is contaminated.

When the researcher genuinely needs a value to make the H well-formed
(e.g. "what threshold do I sweep around?"), the value is set from the
*train* split during Step 2 (Research design), not from the
exploration set. Stage 0 records "a threshold is needed" as part of
the candidate H's structure; the threshold itself is a Step-2 design
choice.

### 3. EDA → H provenance (mandatory)

Every candidate H produced by Stage 0 cites the EDA observation that
motivated it. Provenance turns the EDA → H step into an audit-able
artifact and surfaces double-dipping (the same observation motivating
both H1 and the threshold sweep that "tests" it).

Provenance entry format, in `eda/findings.md` (or `## Phenomenon`
sections in the Stage-0 notebook):

```markdown
## Phenomenon P<id>

### What was seen
[One paragraph, structural observation only. No specific parameter
values.]

### Where in the data
[Which slice of the exploration set. Date range, instrument(s),
frequency.]

### Why it might be worth testing
[One sentence on the mechanism: economic, microstructural, or
behavioural intuition for why this could be a real phenomenon and not
noise. If you cannot articulate a mechanism, the candidate is
probably noise pattern-matching.]

### Candidate H this maps to
[Falsifiable comparison statement in structural form. Specific
thresholds and parameters are intentionally blank — they will be set
in Step 2 from the train split, not from the exploration set.]

### Literature differentiation tier (filled in Step 1)
[Strong / Medium / Weak — see literature_review.md. Empty until
Step 1 has been run for this candidate.]

### Status
[live / parked / dropped, with a one-line reason on transitions]
```

Each candidate H that survives Stage 0 becomes an entry in
`hypotheses.md` with the phenomenon-id attached, so anyone reading
`hypotheses.md` can trace the H back to the EDA observation that
sourced it.

### 4. Stop rule (mandatory)

Stage 0 ends when one of these holds:

- A candidate H reaches **Strong / Medium tier** in the literature
  differentiation step (Step 1 run for this candidate) AND has the
  highest expected information gain among the live candidates →
  lock as H1, exit Stage 0.
- **N (default 5)** candidate phenomena have been recorded and none
  clear Strong/Medium tier → the project does not have a clear
  protocol-eligible angle under the researcher's current literature
  search. Pause; either widen the literature (the candidate may be
  novel under a different sub-field's prior work) or re-scope the
  project. Do not proceed to Step 2 with a Weak-tier candidate.
- A pre-set **time-box** (default 1-2 days of EDA effort, scaled to
  project intensity) is reached → if no candidate has cleared
  differentiation, treat as the second case above.

The stop rule's job is to prevent the EDA from becoming the project.
"We explored a lot" is not a research deliverable. A locked H1 with
provenance and a Step-1 differentiation tier is.

## EDA checklist

The checklist is domain-aware. Every item is run *on the exploration
set only*. The point is to surface candidate phenomena, not to compute
final metrics.

### Universal layer (run for any time-series financial dataset)

- **Distribution shape**: histogram, QQ-plot, kurtosis, skewness.
  Heavy tails / asymmetry are candidate phenomena.
- **Autocorrelation**: ACF / PACF on returns, on absolute returns, on
  squared returns. Non-zero structure is a candidate phenomenon.
- **Vol clustering**: rolling-window standard deviation, GARCH-style
  shape. Visible clustering is a candidate phenomenon.
- **Stationarity**: ADF test, KPSS test on the level and on returns.
  Non-stationarity is a constraint to plan around (not a phenomenon).
- **Regime hints**: rolling correlations, rolling volatility, structural
  breaks. Visible regime structure is a candidate phenomenon.

### Cross-sectional layer (when the dataset has multiple instruments)

- **Correlation matrix**: pairwise return correlations, time-averaged.
- **Principal components**: PCA on returns, what fraction of variance
  the first 1-3 components explain.
- **Cross-sectional dispersion**: cross-sectional standard deviation
  over time. Compression / expansion patterns.
- **Lead-lag structure**: cross-correlation of one instrument's return
  with another's lagged return.

### Time-varying layer

- **Rolling moments**: mean / variance / skew on rolling windows.
- **Rolling correlations**: how stable is the cross-sectional
  structure?
- **Calendar effects**: day-of-week, time-of-day, end-of-month.
- **Event windows**: behaviour around scheduled events (earnings,
  FOMC, futures roll, etc.) when applicable.

### Domain-specific layer

| Domain | Items to add |
|---|---|
| Rates / FX carry | Term structure of forwards / futures, basis curve dynamics, carry vs. realized return |
| Equity factors | Loadings on Fama-French / Carhart factors, residual return autocorrelation |
| Crypto perpetuals | Funding-rate distribution, basis between perp and spot, liquidation cluster timing |
| Order book / microstructure | Depth profile, queue dynamics, signed-volume imbalance, quote update frequency |
| Options / vol surface | Skew shape, term-structure of IV, IV vs. RV |

For each item: visualize, note the structural observation, evaluate
"is this a candidate phenomenon?" — and if yes, write a P<id> entry.

## Common loopholes and counters

| Loophole | Counter |
|---|---|
| "EDA is just exploration, I'll use the full dataset" | Stage 0 explicitly sets the exploration set aside *because* every observation made on the rest of the data biases H selection. The full-data EDA is the failure mode this stage exists to prevent. |
| "I found a strong correlation at lag 3 with IC 0.06; let me record that" | The IC value is a parameter; recording it in Stage 0 makes the H's "validate IC at lag 3 ≥ 0.05" threshold an in-sample fit. Allowed: "Some lag k shows non-zero IC, mechanism is X". The actual lag and threshold are Step-2 train-split choices. |
| "I have 10 candidate phenomena, let me list them all and decide later" | Stop rule N=5. Run Step 1 differentiation per candidate as you go; drop the ones that fall into Weak tier. The point is not to maximize the candidate count but to find one Strong/Medium-tier H worth running. |
| "The phenomenon is so obvious I don't need to write a provenance entry" | Without provenance, future readers (including the researcher 3 months later) cannot tell whether H came from EDA, from a paper, or from intuition. Provenance is what lets the literature differentiation tier be assigned correctly — an H with no documented EDA origin is treated as a Stage-0-required H. |
| "I'll skip Stage 0; I have a hunch" | Hunches are legal entry paths via the conditional skip — but the hunch must be cited in `decisions.md` as the H's origin (prior intuition, paper X, derived Purpose Y). An H with no traceable origin defaults back into Stage 0. |
| "I'll run Stage 0 on the full data and just *promise* not to use the values for H selection" | The contract is enforced by data isolation, not by self-discipline. The exploration set is committed to a file; the rest of the lifecycle reads from a different file. Self-policing the boundary fails the same way self-policing test-set leakage fails. |

## Output to Step 1 and Step 2

When Stage 0 completes (a candidate is locked as H1):

- The exploration-set definition (`reproducibility/exploration_set.txt`)
  is committed.
- The provenance file (`eda/findings.md` or the Stage-0 notebook)
  contains all candidate phenomena with status and (for the locked
  candidate) Strong/Medium-tier differentiation.
- `hypotheses.md` carries H1 with phenomenon-id attached, plus parked
  candidates as H2…HN.
- `decisions.md` records the Stage-0 closing entry: which candidate
  was locked, why, and which were parked or dropped.

The researcher then:

- Has already run Step 1 (literature review) for the locked candidate
  during the stop-rule check, so Step 1 is complete for H1.
- Proceeds to Step 2 (research design) on H1, where train-split
  parameters and acceptance thresholds are set.

The rest of the lifecycle (Steps 3 onwards) is unchanged.

## Anti-patterns specific to Stage 0

- **Stage 0 becomes the project.** Stop rule prevents this; if it fires
  twice on the same project, the project's data does not have a
  protocol-eligible angle and should be re-scoped, not re-explored.
- **Stage 0 produces a paper-ready figure.** Stage 0's figures are
  diagnostic; they are not the headline figure of any future
  notebook. Re-running EDA on the full dataset later, in a properly
  scoped notebook for the locked H, produces the artifacts that go
  into reports.
- **Stage 0 candidate is published.** A Stage-0 candidate that has
  not been tested on train / val / test is not a result; it is a
  hypothesis with provenance. Reporting a Stage-0 finding as a
  finding is a category error.
