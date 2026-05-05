# rd_charter.md

DARPA Heilmeier Catechism — the 8-question entry document for any R&D project.

## When to read

- The very first step of any R&D project, before decomposition or implementation
- When a sub-agent is asked to elicit a charter from the user
- Before any other R&D reference is consulted

## Purpose

The charter answers 8 questions in **one page**. Without a complete charter on
file, evidence-producing R&D work is forbidden: no Stage gate and no
promotion-cited trial. Setup, scaffolding, and exploratory design notes may
continue when clearly labeled as non-evidence-producing.

The charter is a **review anchor** — once committed, load-bearing amendments
require a dated deviation entry in `decisions.md`. Hash-lock via
`scripts/prereg_freeze.py` (the same mechanism used for Pure Research
pre-registration).

## The 8 questions

Answer each in 1-3 sentences. No jargon. If you cannot answer in plain
language, the project is not ready.

### H1. What capability should exist?

State the target as a single sentence describing what new capability the
project will produce. Use no internal jargon, no library names, no model
names. Imagine explaining it to a smart person from a different domain.

- **Bad**: "Implement TimesFM-based intraday volatility forecasting on
  Polygon ES futures data with marimo notebook integration."
- **Good**: "An automated system that, given the recent price history of an
  index futures contract, produces a probabilistic forecast of its
  volatility over the next hour, calibrated well enough that a desk can
  size positions from it."

### H2. How is this approximated today, and what are the limits?

Describe the current best practice that the team uses (or that the field
uses) and what specifically is unsatisfactory about it. Quantify the limit
where possible.

- **Bad**: "We don't have a good way to do this."
- **Good**: "Today the desk uses a 60-day rolling realized-volatility
  estimate. It tracks slow regime changes but lags fast ones by ~30
  minutes, costing approximately N bp per turn during volatility spikes.
  Existing GARCH variants tested in 2024 reduced lag but added 4× compute
  per bar, which the live engine cannot afford."

### H3. What is new in the proposed approach, and why do we believe it might work?

Name the specific novelty (algorithm class, data source, decomposition,
validation method, etc.) and the prior evidence or mechanism that makes
success plausible. **Novelty axis** (existing / extension / novel) is
captured here, not on individual core technologies.

- **Bad**: "Try a neural network."
- **Good**: "Foundation models for time series (Chronos, TimesFM, Moirai)
  are trained on billions of time series and ship with zero-shot
  forecasting heads. Reported zero-shot performance on generic financial
  series suggests comparable accuracy to specialized models without
  per-instrument training. If this transfers to intraday vol of a single
  futures contract, it would close the H2 gap without per-instrument
  training cost."

### H4. Who cares? Who is the consumer, and what decision does this capability serve?

Name a specific consumer (a person, a system, a workflow) and the decision
that consumer is currently blocked on. If you cannot name the consumer and
the blocked decision, the capability has no demand.

- **Bad**: "The whole desk would benefit."
- **Good**: "The intraday execution desk (3 traders + 1 systematic
  engineer) currently sizes index hedges using a static vol estimate
  refreshed at session open. The proposed forecast would feed the
  hedge-sizing logic at 5-minute intervals, replacing the static estimate.
  The decision being unblocked is 'how large should the hedge be in the
  next 5-minute window?'"

### H5. If we succeed, what changes downstream?

Describe the world after success in concrete terms. What workflows change?
What metrics improve? What gets retired? Quantify if possible.

- **Bad**: "Better hedging."
- **Good**: "Hedge resizing cadence drops from once-per-session to every
  5 minutes. Intraday hedge-error variance reduces by an estimated X% (per
  H2 baseline). The session-open sizing job is retired. Risk reporting
  switches from end-of-session realized to forecast-based intra-session."

### H6. What are the dominant risks, and what evidence would kill this project?

List the top 3-5 risks. For each, name **specific observable evidence**
that would cause the project to be killed. These evidence statements become
the project's binding kill criteria.

The kill criteria written here are **frozen as decision anchors** at charter
close. They are not a prison: discovering mid-project that a test, threshold,
or data source was wrong is a reason to file a deviation entry and either
re-scope the criterion for future evidence or start a new charter. It is not a
reason to silently reinterpret the original criterion after seeing results.

- **Bad**: "It might not work."
- **Good**:
  1. "Foundation model zero-shot accuracy is too low. KILL if zero-shot
     IC ≤ 0.02 on 3 representative instruments after 2 weeks of
     evaluation, AND fine-tuning does not lift IC ≥ 0.05 within an
     additional week."
  2. "Inference cost too high for live use. KILL if per-bar inference
     latency > 100ms on the production hardware after batch + cache
     optimization."
  3. "Forecast not actionable for sizing. KILL if calibration ECE > 0.10
     on out-of-sample evaluation period."
  4. "Maintenance burden too high. KILL if the foundation model release
     cadence requires re-fine-tuning more often than quarterly to keep
     drift ECE < 0.10."

### H7. Cost: budget for compute, data, and wall-clock

State the total cost in three dimensions. **Distinguish one-time setup cost
from recurring cost** (this distinction will inform the lifecycle
classification of core technologies in the next step).

- **One-time**: charter writing, decomposition, initial fine-tuning,
  infrastructure setup
- **Recurring**: re-fine-tuning cadence, monitoring, drift re-evaluation,
  data feed cost

Example:

> **One-time**:
> - Compute: ~200 GPU-hours for fine-tuning sweep
> - Data: $X for 5 years of 5-minute futures data
> - Wall-clock: 6 weeks of focused work (1 researcher)
>
> **Recurring (annual)**:
> - Compute: ~50 GPU-hours/year for quarterly re-tuning
> - Data: $Y/year ongoing data feed
> - Wall-clock: ~2 weeks/year of monitoring + re-tuning

### H8. Midterm exam, final exam, AND integration pattern

Define two checkpoints (midterm + final) plus the integration pattern.
**The "done" definition must be lifecycle-aware**: if any core technology
is expected to be `継続改善型` (continuous improvement), "done" means
"v1 + scheduled maintenance plan", not "permanently shipped and walked
away from".

#### Midterm exam

A concrete demonstration that the hardest sub-question has been answered.
Typically corresponds to TRL-3 demonstration of the highest-risk capability.

#### Final exam

TRL-6 operational prototype demonstration on representative workload, with
all core technologies `established`, plus (if applicable) maintenance plan
filed.

#### Integration pattern (REQUIRED)

Per `references/rd/integration_patterns.md`, declare which pattern this
project uses. Without an explicit declaration, the project implicitly
defaults to Pattern 2 (bottom-up), which produces no working version
until very late.

Pick one:

- **Pattern 1 (vertical slice / framework-first)**: framework + baselines
  built day 1, K's replace baselines iteratively. Use when architecture
  is well-understood, K's are well-defined slots, baselines are writable.
- **Pattern 2 (bottom-up / component-first)**: each K matured in isolation,
  integrated at the end. Use when K's are independent technologies,
  architecture is unknown.
- **Pattern 3 (skeleton + spike)** [recommended default]: throwaway
  skeleton built day 1-3, K's identified after skeleton, replace skeleton
  components iteratively.

State the pattern + the reason (architecture certainty + K interface
stability):

> Example: "Pattern 3 (skeleton + spike). Architecture broad shape is
> known (signal → sizing → execution → risk), but specific signal feature
> set and sizing model are research-worthy. Skeleton phase = 3 days,
> after which K identification distinguishes research from engineering."

Example for Midterm + Final + Integration pattern:

> **Midterm**: Foundation model fine-tuned on 6 months of 5-minute ES
> data; out-of-sample IC ≥ 0.05 on a 1-month held-out period; latency
> measurement establishes feasibility for live inference.
>
> **Final**: System runs for 2 weeks on paper-trading shadow data,
> producing 5-minute forecasts that the hedge-sizing logic consumes. Live
> measurement shows IC ≥ 0.04 (allowing for some out-of-sample
> degradation), ECE ≤ 0.10, latency ≤ 100ms. Maintenance plan filed
> covering re-tuning cadence and drift trigger.
>
> **Integration pattern**: Pattern 3 (skeleton + spike). Day 1-3:
> skeleton with naive linear forecast + static hedge sizing. Day 4: K
> identification (foundation model is K1, fine-tuning protocol is K2,
> sizing dynamics is K3 if needed). K's replace skeleton components
> iteratively, A/B vs skeleton each replacement.

Example:

> **Midterm**: Foundation model fine-tuned on 6 months of 5-minute ES
> data; out-of-sample IC ≥ 0.05 on a 1-month held-out period; latency
> measurement establishes feasibility for live inference.
>
> **Final**: System runs for 2 weeks on paper-trading shadow data,
> producing 5-minute forecasts that the hedge-sizing logic consumes. Live
> measurement shows IC ≥ 0.04 (allowing for some out-of-sample
> degradation), ECE ≤ 0.10, latency ≤ 100ms. Maintenance plan filed
> covering re-tuning cadence and drift trigger.

## Charter format

The charter lives at the project root as `charter.md`. It uses the template
at `assets/rd/charter.md.template`. Length: 1 page (~50-80 lines of content
including the answers).

Structure:

```markdown
# Charter — <project name>

Frozen: <YYYY-MM-DD HH:MM:SS UTC>
Hash: <SHA-256 from prereg_freeze.py>

## H1. What capability should exist?
[Answer.]

## H2. How is this approximated today, and what are the limits?
[Answer.]

... (H3-H8 in same format)

## Approval
- Drafted by: <agent / user>
- Reviewed by: <user>
- Frozen at: <timestamp>
```

## Freezing the charter

After H1-H8 are filled and reviewed:

```bash
python scripts/prereg_freeze.py --type charter --path charter.md
```

This:
1. Computes SHA-256 of the file content
2. Writes `prereg/charter.lock` with hash + UTC timestamp + path
3. Records the freeze in `decisions.md` as a state transition

After freezing, **do not edit `charter.md` in place for load-bearing changes**.
Minor typo or formatting fixes may be noted normally. Any change that affects
scope, kill criteria, cost, final exam, consumer, or promotion language
requires a dated deviation entry in `decisions.md` naming the H-number that
changed and the trigger evidence. Frequent load-bearing deviations mean the
charter was under-specified; next time, spend more time on this step.

## Why the charter blocks downstream work

Without a frozen charter:

- **Kill criteria do not exist**. Any "kill" decision later in the project
  would be based on shifting goalposts. Sunk cost will bias the agent
  toward "let's try one more thing" rather than killing.
- **Consumers cannot evaluate**. H4 (consumer + decision) is what makes the
  project a research project rather than an exploration. No consumer = no
  project.
- **TRL targets cannot be assigned**. H8 (midterm/final exam) sets what
  TRL-6 means for *this* project. Capabilities cannot be sized without it.
- **Decomposition has no basis**. Core technologies (next step) are
  identified relative to the target. Without H1-H3, decomposition is
  guessing.

If the user pushes to "skip charter and just start", the response is: you
are guessing about the first 4 weeks of work. The 1-2 hours of charter
writing pays for itself within the first week of decomposition.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Vague H1 | "Build a system that does X" with no consumer or success criterion | Force H4 first; H1 follows |
| Missing H6 kill criteria | "Risks: technical risk, schedule risk" without observable evidence | Each risk must name a numeric or behavioral threshold |
| H7 collapses one-time and recurring | Single number for total cost | Force the split; recurring cost determines lifecycle of core techs |
| H8 too vague | "Finish the project" | Both midterm and final must be demonstrable, not aspirational |
| Charter rewritten mid-project | Goalpost shifting | Refuse silent rewrite; require deviation entry per load-bearing amendment, file new charter if substantial |

## Relationship to other references

- After charter is frozen → read `references/rd/core_technologies.md` to
  define Layer 1 (intellectual decomposition).
- The novelty axis (`既存` / `発展的` / `新規`) lives in H3, not on
  individual core technologies.
- The lifecycle distinction (`永続型` / `継続改善型`) is determined per
  core technology in core_technologies.md, but the project-level
  composition of lifecycles affects H8 (the "final exam" definition) and
  the project's eventual termination semantics.
- Cost decomposition in H7 (one-time vs recurring) feeds into the
  maintenance plan template in `references/rd/rd_promotion_gate.md`.
