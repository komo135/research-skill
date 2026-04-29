# hypothesis_cycles.md

Protocol for iterating hypothesis cycles. Do not stop after one.

## Scope and ownership split

This file owns **routing of derived H's** — same Purpose / same notebook
(next `## H<id>` block) vs. new Purpose / new notebook; classification
as run-now / next-session / drop. It does **not** own *content
generation* of derived H's, and it does **not** own *cross-H synthesis*
of multiple H's into a Purpose-level meta-finding.

| Concern | Owned by |
|---|---|
| Routing (where the next H lives) | This file |
| Content generation of a derived H | `hypothesis_generation.md` Pathway 4 |
| Cross-H synthesis (Purpose-level meta-finding from H1…HN) | `cross_h_synthesis.md` |

The three files compose: `hypothesis_generation.md` writes the H's
substance; this file places it in the right notebook; `cross_h_synthesis.md`
reads N H's together at Purpose closure to extract what the cluster
says that no single H said. The Purpose-level conclusion section in
each notebook follows `cross_h_synthesis.md`'s pattern templates.

## When to read

- A Hypothesis round inside the current notebook has just been completed
  (its observation + verdict are filled)
- A whole notebook (one Purpose) has been wrapped up
- Before declaring overall completion

## Principle

Research is fundamentally a loop of **hypothesis → test → derived hypothesis
→ re-test**. Stopping after one cycle yields a single hypothesis, not
research.

The cycle plays out at two scales:

| Scale | Where the next round happens |
|---|---|
| **Within a Purpose** (most cycles) | Next H block inside the same notebook |
| **Across Purposes** | Next notebook (`exp_<NNN+1>_*.py`) |

Default to the within-a-Purpose scale. Crossing into a new notebook is
reserved for cases where the Purpose itself has shifted (see
`references/experiment_protocol.md` for the Purpose-change triggers).

## What to write at the end of each H round (inside the current notebook)

```markdown
### H<id> conclusion
- Observed values: [Sharpe X, win rate Y, IC Z, ...]
- Verdict for H<id>: [supported / rejected / partially supported / parked]

### Cannot conclude
- [State which dimensions are not tested by this H specifically]

### Derived hypotheses (next rounds inside THIS notebook, or candidates for
### new notebooks)
| New hypothesis | Where | Run-now / next-session / drop | Reason |
|---|---|---|---|
| H<new>: …                          | same notebook | run-now      | same Purpose, sensitivity / refinement / failure-diagnosis / follow-on |
| H<new>: …                          | same notebook | next-session | same Purpose but needs more compute |
| H<new>: …  (= candidate Purpose P) | new notebook  | run-now      | new Purpose: phenomenon / cross-section / question changed |
| …                                  | drop          | —            | refuted in prior work (papers.md) |
```

## Routing rule (the most important rule in this file)

When a derived H emerges, decide where it goes by the following test, in
order:

1. **Does the current notebook's Purpose statement still cover the new H?**
   - Yes → the new H is the next `## H<id>` block in the same notebook.
     Run-now / next-session / drop only determines *when* you do it.
   - No → the new H reflects a new Purpose; it goes in the next notebook.

2. (Subordinate to 1) Run-now / next-session / drop:
   - **Run-now**: testable in the current session with current data /
     features / compute
   - **Next-session**: requires data acquisition, new feature
     construction, or hours of compute
   - **Drop**: refuted in prior work, out of scope, or judged not worth
     the effort

The old rule "run-now derived hypothesis ⇒ start the next notebook" has
been **replaced**. Run-readiness no longer routes the H to a new file; only
Purpose change does.

## Updating hypotheses.md

At the end of every H round, update `hypotheses.md`:

```markdown
| ID | Statement | Status | experiment_id (= notebook = Purpose) | Last update |
|---|---|---|---|---|
| H1 | ... | supported | exp_001 (mean-reversion EUR/USD intraday) | 2026-04-28 |
| H2 | ... | supported | exp_001                                  | 2026-04-28 |
| H3 | ... | rejected  | exp_001                                  | 2026-04-28 |
| H4 | ... | planned   | exp_002 (momentum EUR/USD intraday)      | 2026-04-28 |
```

Each H row points to the `experiment_id` (= notebook = Purpose) it lives
under. Multiple H's per Purpose share the same `experiment_id`.

## Updating decisions.md

Append a time-ordered entry per Purpose / cycle. A Purpose with multiple H's
yields one entry with H sub-bullets:

```markdown
## YYYY-MM-DD cycle <N> (exp_<NNN>_<purpose-slug>) — Purpose: <one-line>

- Tested H1: [one-line restatement]
  - Observation: [observed values, anomalies]
  - Verdict: [supported / rejected / partially supported / parked]
- Tested H2 (derived from H1): [one-line restatement]
  - Observation: [observed values, anomalies]
  - Verdict: [supported / rejected / partially supported / parked]
- Tested H3 (derived from H2): …
- Purpose-level synthesis: [one or two sentences across H1…HN]
- Derived Purposes for the next notebook:
  - P<id> (run-now): …
  - P<id> (next-session): …
- Direction rejected: [what was tried inside this Purpose and did not work,
  with reason]
- Robustness battery status (per H): H1 — [pass/fail per item], H2 — …
```

## Run-now vs. next-session classification

| Run-now | Next-session |
|---|---|
| Testable with current data | Requires new data acquisition |
| Existing features suffice | Requires new feature construction |
| Runs in under ~30 minutes | Needs hours of compute |
| Upstream notebooks complete | Upstream is still in planning |

This classification is orthogonal to the same-notebook-vs-new-notebook
decision. A run-now H whose Purpose is unchanged is the next round inside
the current notebook *now*. A run-now H whose Purpose has changed opens
the next notebook *now*.

## Exhaustion criteria — the synthesis-trigger rule

Patterns A-E in `cross_h_synthesis.md` define the *action* for each
cluster shape. This section defines the *trigger* — when the
researcher must stop generating H's and look at the cluster.

Without a trigger, the patterns are advisory documentation that fires
only when the researcher remembers to consult them. The empirical
failure mode is that researchers mid-iteration on a Purpose do not
remember; they keep generating H's. The trigger fixes this.

### Hard trigger (mandatory)

A Purpose has accumulated **5 H tested without any
`verdict='supported'`** → the next action is **not** H6. The next
action is the cross-H synthesis per `cross_h_synthesis.md`. No new H
may be appended to this Purpose until the synthesis has produced a
Pattern match (A-E or combined) and the corresponding action has been
recorded in `decisions.md`.

The 5-H count is over the Purpose, not the project. It includes any
mix of `verdict ∈ {rejected, parked, preliminary}`. A single
truly-supported H (all four completion gates pass — see SKILL.md
"Completion gate per Hypothesis") resets the trigger; the Purpose has
produced a working result and further H's are exploring the result's
scope, not searching for one.

### Soft trigger (advisory)

The hard trigger fires at N=5. Earlier soft triggers are
advisory — the researcher can ignore them without violating the
protocol, but the protocol surfaces them so iteration is not blind:

- **N=3 advisory**: First synthesis check. If a pattern is already
  visible at N=3 (e.g., all three rejections share the same
  `failure_mode` → Pattern A), close or derive without waiting for
  N=5.
- **Pattern-C-shape advisory**: As soon as a Pareto trajectory is
  visible in the metric shape (one metric improving, another
  worsening, regardless of verdict count), trigger synthesis. Pattern
  C's mechanism is metric-shape-driven, not count-driven.

### Default-to-Pattern-B rule

If the synthesis at N=5 matches *no* clear pattern (mixed signals, no
shared `failure_mode`, no Pareto trajectory, no monotonic
improvement), the **default is Pattern B** (Purpose is too broad,
split into derived Purposes).

The reason: a Purpose that has produced 5 unconnected rejections is
empirically a Purpose whose H's are testing different things. The
researcher's intuition that a 6th H "might fit" is exactly the
sunk-cost rationalization the trigger exists to interrupt.

Default-to-B is overridable: the researcher can argue against the
default in `decisions.md` if they have a specific Pattern-A mechanism
that didn't surface in the cluster yet. But the *default* is split,
not continue.

### Hard cap (escape valve)

Beyond **N=8 H tested under one Purpose** without
`verdict='supported'`, no H_{N+1} is appendable to this Purpose. The
Purpose closes mechanically. If the researcher believes more work is
warranted, it is opened as a new Purpose (new notebook, new
`experiment_id`) carrying the previous Purpose's synthesis as
documented prior.

The hard cap is statistical, not punitive: beyond 8 H, the
multiple-testing inflation makes any subsequent `supported` verdict's
DSR honest-trial-count too punishing to clear cleanly. Continued
iteration is busywork.

### What resets the trigger

Only a **truly supported** H resets the trigger — i.e., one for which
all four completion gates pass (`bug_review`, `experiment-review`,
`research_quality_checklist`, achieved_tier ≥ Medium). A provisional
`verdict='supported'` written at append-time but downgraded to
`partial` or `preliminary` after review **does not** reset.

This robustness matters: the trigger cannot be escaped by writing
`verdict='supported'` on a shaky H. The reset is gated on the same
four-gate machinery that gates real publication-grade verdicts.

### Common rationalizations

| Excuse | Reality |
|---|---|
| "I'm at N=5 but I have a really good idea for H6" | The trigger doesn't ask whether your H6 idea is good. It asks you to look at H1-H5 first. Run synthesis; if Pattern A emerges and your H6 is a Pathway-4 derivation against the binding axis, H6 is legal. If Pattern B emerges, H6 belongs in a derived Purpose, not this one. |
| "The synthesis is overhead; let me just append H6 and synthesize later" | "Later" historically does not happen. The trigger fires *before* H6 specifically because the synthesis is what determines whether H6 is the right next step. |
| "I'll mark H4 as supported provisionally to reset the trigger" | Reset requires four-gate-clean. A provisional supported that hasn't passed both review layers does not count. |
| "N=5 is arbitrary; I'll override it" | Yes, 5 is arbitrary; any cutoff is. The override is legal but documented in `decisions.md` with a Pattern-A mechanism argument. Overriding without that argument is sunk-cost. |
| "I'm at N=8, the cap is unfair, let me do H9" | Cap is mechanical. Open a new Purpose; the work continues but with fresh DSR trial count and the previous synthesis as inheritance. |

## Completion criteria

A research project counts as complete when all of these hold:

- (a) The seven items in `robustness_battery.md` pass for every H whose
  verdict is `supported`
- (b) Every candidate H is classified (executed / next-session / dropped)
- (c) Every candidate Purpose is classified (executed-as-its-own-notebook /
  next-session / dropped)
- (d) `hypotheses.md` has no entries left in an "untriaged" state
- (e) `decisions.md` provides a traceable history across all cycles, with
  H sub-bullets under each Purpose

If any is missing, the work is preliminary screening.

## Failure patterns

- "Next hypothesis" listed as TODO with no further round → cycle stopped;
  if it can run now and the Purpose is unchanged, run it as the next H
  block in the same notebook
- "Next H needs a new notebook because the Purpose feels different" stated
  but the Purpose statement was never re-read → re-read the Purpose
  statement before splitting; many "feels different" cases are sensitivities
  or refinements
- Conclusion declared after one supporting H → reverse-test against
  contradictory variants in the same notebook
- "Diminishing returns" claimed without verification → check the
  robustness-battery status (per H) before stopping

## Cycle-count guidance

| Cycles (H rounds across all notebooks) | Assessment |
|---|---|
| 1 | Single hypothesis, not research |
| 2-3 | Initial screening |
| 5-8 | Standard research |
| 10+ | Substantial body of work, approaching publication grade |

A "cycle" here is one Hypothesis round. Multiple cycles inside one notebook
all count. Quality of derived-hypothesis generation matters more than raw
count.
