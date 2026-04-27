# hypothesis_cycles.md

Protocol for iterating hypothesis cycles. Do not stop after one.

## When to read

- An experiment notebook has just been completed (conclusion cell is filled)
- Before declaring overall completion

## Principle

Research is fundamentally a loop of **hypothesis → test → derived hypothesis → re-test**.
Stopping after one cycle yields a single experiment, not research.

## What to write at the end of each notebook

```markdown
### Conclusion
- Observed values: [Sharpe X, win rate Y, IC Z, ...]
- Hypothesis H<id>: [supported / rejected / partially supported / parked]

### Cannot conclude
- [State which dimensions are not tested: instruments, regime, sizing, exit, factor]

### Derived hypotheses
| New hypothesis | Run-now / next-session / drop | Reason |
|---|---|---|
| H<new>: ... | run-now | testable with current data |
| H<new>: ... | next-session | needs multi-asset data |
| ... | drop | refuted in prior work (papers.md) |
```

## Updating hypotheses.md

At the end of every cycle, update `hypotheses.md`:

```markdown
| ID | Statement | Status | Linked experiments | Last update |
|---|---|---|---|---|
| H1 | ... | supported | exp_001, exp_003 | 2026-04-26 |
| H2 | ... | rejected | exp_004 | 2026-04-26 |
| H3 | ... | in-progress | exp_005 | 2026-04-26 |
| H4 | ... | planned | (none yet) | 2026-04-26 |
```

## Updating decisions.md

Append a time-ordered entry:

```markdown
## YYYY-MM-DD cycle <N> (exp_<NNN>_<slug>)

- Tested hypothesis: H<id> (one-line restatement)
- Observation: [observed values, anomalies]
- Verdict: [supported / rejected / partially supported / parked]
- Derived hypotheses:
  - H<new> (run-now): ...
  - H<new> (next-session): ...
- Direction rejected: [what was tried and did not work, with reason]
- Robustness battery status: [pass / fail per item]
```

## Run-now vs. next-session classification

| Run-now | Next-session |
|---|---|
| Testable with current data | Requires new data acquisition |
| Existing features suffice | Requires new feature construction |
| Runs in under ~30 minutes | Needs hours of compute |
| Upstream notebooks complete | Upstream is still in planning |

If multiple hypotheses qualify as "run-now", start the next notebook
(`exp_<NNN+1>_*.py`) directly.

## Completion criteria

A research project counts as complete when all of these hold:

- (a) The seven items in `robustness_battery.md` pass
- (b) Every candidate hypothesis is classified (executed / next-session / dropped)
- (c) `hypotheses.md` has no entries left in an "untriaged" state
- (d) `decisions.md` provides a traceable history across all cycles

If any is missing, the work is preliminary screening.

## Failure patterns

- "Next hypothesis" listed as TODO and the project closed → cycle stopped; if it can run
  now, run it
- Conclusion declared after one supporting result → reverse-test against contradictory
  scenarios
- "Diminishing returns" claimed without verification → check the robustness-battery status
  before stopping

## Cycle-count guidance

| Cycles | Assessment |
|---|---|
| 1 | Single experiment, not research |
| 2-3 | Initial screening |
| 5-8 | Standard research |
| 10+ | Substantial body of work, approaching publication grade |

Quality of derived-hypothesis generation matters more than raw count.
