# Proposition-First Result Feedback

The old plan-local iteration loop is replaced by proposition and derived-hypothesis state updates.

After every interpreted result:

1. Record `research-result-analysis` in the hypothesis plan.
2. Update `hypothesis.md` status.
3. Append a hypothesis decision.
4. Update parent `proposition.md` if proposition status, expected consequence, live hypotheses, or key material changed.
5. Append a proposition decision when proposition status changes.
6. Open the next derived hypothesis only if the updated proposition state warrants it.

## Hypothesis decisions

Allowed labels:

- `COMMIT`
- `PARK`
- `KILL`
- `TESTED_SUPPORTED`
- `TESTED_CONTRADICTED`
- `TESTED_PARTIAL`
- `TESTED_INCONCLUSIVE`
- `REVISE`

Hypothesis status values:

- `candidate`
- `ready-for-plan`
- `tested-supported`
- `tested-contradicted`
- `tested-partial`
- `tested-inconclusive`
- `parked`
- `killed`

## Proposition decisions

Allowed labels:

- `SUPPORT`
- `CONTRADICT`
- `UNREALIZED_CONDITION`
- `UNDER_SPECIFY`
- `SPLIT_NEEDED`
- `SPLIT`
- `CLOSE`
- `REOPEN`

Proposition status values:

- `open`
- `supported`
- `contradicted`
- `unrealized-condition`
- `under-specified`
- `split-needed`
- `split`
- `closed`

## Decision entry shape

```markdown
## YYYY-MM-DD - <DECISION_LABEL>: <short title>

- Scope: project | proposition Pxxx | hypothesis Hxxx
- Previous status:
- New status:
- Evidence or analysis pointer:
- Rationale:
- Follow-up state change:
```

## Routing from evidence

| Evidence after Result analysis | Hypothesis update | Proposition update |
|---|---|---|
| Planned discriminator supports hypothesis against competitor | `tested-supported` | usually `supported`, unless broader proposition remains under-specified |
| Planned discriminator contradicts hypothesis | `tested-contradicted` | `contradicted`, `unrealized-condition`, `under-specified`, or `split-needed` depending on whether the result breaks the proposition or only the realization |
| Evidence supports part but leaves a material clause unresolved | `tested-partial` | usually `under-specified` or still `supported` with narrowed expected consequence |
| Comparator, measurement, artifact, or evidence quality prevents interpretation | `tested-inconclusive` | usually unchanged or `under-specified` |
| Result shows a required condition was not realized | `tested-partial` or `tested-inconclusive` | `unrealized-condition` |
| Result exposes multiple hidden propositions | `tested-partial` | `split-needed` then `split` after child propositions are opened |

Do not write `NEXT_STEP`, `REFINE`, `ADJACENT`, `PARK`, or `CLOSE` as global plan branches in the new lifecycle. Those were plan-first labels. Use proposition and hypothesis status transitions instead.
