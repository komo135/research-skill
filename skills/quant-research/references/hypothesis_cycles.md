# hypothesis_cycles.md

Protocol for iterating hypothesis cycles. Do not stop after one.

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
